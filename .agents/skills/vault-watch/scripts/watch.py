#!/usr/bin/env python3
"""vault-watch: 讀 watchlist、用 gh 抓 GitHub issue/PR 現況、與快照比對、吐機器可讀 deltas。

- 追蹤標的來源 = 看板檔（預設 feeds/watch/01.index.md）內出現的所有 owner/repo#num。
- 快照存 state.json（機器資料檔，非 vault 筆記）。
- 精選訊號：state 轉換（含 PR merged）、官方/maintainer 新回應、label 變動。
  一般路人留言與 reaction 數不當「變化」，只在需要時附現值。
- 本腳本不改看板、不寫 digest、不碰 git——那些由主 agent 依 runbook 用 harness 工具處理。
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

OFFICIAL = {"OWNER", "MEMBER", "COLLABORATOR"}
REF_RE = re.compile(r"\b([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)#(\d+)\b")
# 看板列尾標記：該項改採全部留言（含社群），不只 OFFICIAL。預設不標＝只認官方。
ALL_COMMENTS_TAG = "[全留言]"


def gh_api(path, paginate=False):
    """呼叫 gh api，回傳解析後的 JSON；失敗回 (None, err_msg)。"""
    cmd = ["gh", "api", path]
    if paginate:
        cmd.append("--paginate")
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
    except FileNotFoundError:
        return None, "找不到 gh CLI，請先安裝 GitHub CLI 並 gh auth login"
    if r.returncode != 0:
        return None, (r.stderr or r.stdout or "gh api 失敗").strip().splitlines()[-1]
    try:
        return json.loads(r.stdout), None
    except json.JSONDecodeError as e:
        return None, f"gh 回傳非 JSON：{e}"


def collapse(text, limit=140):
    s = re.sub(r"\s+", " ", (text or "").strip())
    return s[:limit] + ("…" if len(s) > limit else "")


def parse_refs(index_path):
    """從看板檔抽出所有 owner/repo#num，去重、保序；同列有 [全留言] 者 scope="all"。"""
    text = Path(index_path).read_text(encoding="utf-8")
    seen, refs = set(), []
    for line in text.splitlines():
        scope = "all" if ALL_COMMENTS_TAG in line else "official"
        for owner_repo, num in REF_RE.findall(line):
            ref = f"{owner_repo}#{num}"
            if ref not in seen:
                seen.add(ref)
                refs.append((owner_repo, num, ref, scope))
    return refs


def fetch_one(owner_repo, num, prev, scope="official"):
    """抓單一 issue/PR 現況 + 自 prev.checked_ts 起的新留言。回 (snapshot, deltas, error)。

    scope="official" 只認 OWNER/MEMBER/COLLABORATOR（預設，擋熱門 issue 洗版）；
    scope="all" 連社群留言一併採計，給留言量小、關鍵訊號常來自非 maintainer 的冷門項。
    """
    data, err = gh_api(f"repos/{owner_repo}/issues/{num}")
    if err:
        return None, [], err
    is_pr = data.get("pull_request") is not None
    state = data.get("state", "unknown")
    if is_pr and state == "closed":
        pr, perr = gh_api(f"repos/{owner_repo}/pulls/{num}")
        if not perr and pr.get("merged"):
            state = "merged"
        elif not perr:
            state = "closed-unmerged"
    labels = sorted(l["name"] for l in data.get("labels", []))
    title = data.get("title", "")

    snap = {
        "type": "pr" if is_pr else "issue",
        "state": state,
        "labels": labels,
        "title": title,
        "last_official_id": prev.get("last_official_id") if prev else None,
        "last_official_at": prev.get("last_official_at") if prev else None,
    }

    # 新回應：僅對已知項（prev 有 checked_ts）抓 since 之後的留言，避免首輪灌全串。
    # 標記由 official→all 時不回填舊留言（快照之前的留言不再回報），維持「跟上次比」的增量語意。
    new_official = None
    if prev and prev.get("checked_ts"):
        cpath = f"repos/{owner_repo}/issues/{num}/comments?since={prev['checked_ts']}&per_page=100"
        comments, cerr = gh_api(cpath, paginate=True)
        if not cerr and isinstance(comments, list):
            offs = [
                c
                for c in comments
                if scope == "all" or c.get("author_association") in OFFICIAL
            ]
            if offs:
                latest = max(offs, key=lambda c: c["id"])
                if latest["id"] != prev.get("last_official_id"):
                    new_official = latest
    if new_official:
        snap["last_official_id"] = new_official["id"]
        snap["last_official_at"] = new_official["created_at"]

    # 計算 deltas
    deltas = []
    if prev is None:
        deltas.append(("new", f"{snap['type']} {state}"))
    else:
        if prev.get("state") != state:
            deltas.append(("state", f"{prev.get('state')}->{state}"))
        prev_labels = set(prev.get("labels", []))
        cur_labels = set(labels)
        for added in sorted(cur_labels - prev_labels):
            deltas.append(("label+", added))
        for removed in sorted(prev_labels - cur_labels):
            deltas.append(("label-", removed))
        if new_official:
            deltas.append(
                (
                    "official",
                    f"{new_official['user']['login']}|{new_official.get('author_association', 'NONE')}"
                    f"|{new_official['created_at'][:10]}|{collapse(new_official.get('body'))}",
                )
            )
    return snap, deltas, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", default="feeds/watch/01.index.md")
    ap.add_argument(
        "--state",
        default=str(Path(__file__).resolve().parent.parent / "state.json"),
    )
    args = ap.parse_args()

    index_path = Path(args.index)
    if not index_path.exists():
        print(f"ERROR|index|找不到看板檔 {index_path}", flush=True)
        sys.exit(2)

    refs = parse_refs(index_path)
    if not refs:
        print("ERROR|index|看板內無任何 owner/repo#num", flush=True)
        sys.exit(0)

    state_path = Path(args.state)
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        state = {}

    now = datetime.now(timezone.utc)
    checked_ts = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    checked_date = now.strftime("%Y-%m-%d")

    changed = 0
    for owner_repo, num, ref, scope in refs:
        prev = state.get(ref)
        snap, deltas, err = fetch_one(owner_repo, num, prev, scope)
        if err:
            print(f"ERROR|{ref}|{err}", flush=True)
            continue
        # checked_ts 是抓新留言的 since 游標；無實質變化的一輪不推進它，也不寫任何純裝飾的
        # 日期欄，讓 state.json 在 quiet round 產出 byte-identical、不留要 commit 的 churn。
        # 有 CHANGE（含首見 new）才推進到現在，順帶收窄下輪的留言抓取窗。
        snap["checked_ts"] = checked_ts if deltas else (prev or {}).get("checked_ts", checked_ts)
        state[ref] = snap
        title = collapse(snap["title"], 80)
        print(f"ITEM|{ref}|{snap['type']}|{snap['state']}|{title}", flush=True)
        if deltas:
            changed += 1
            for kind, detail in deltas:
                print(f"CHANGE|{ref}|{kind}|{detail}", flush=True)
        else:
            print(f"NOCHANGE|{ref}", flush=True)

    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"SUMMARY|checked={len(refs)}|changed={changed}|date={checked_date}", flush=True)


if __name__ == "__main__":
    main()
