#!/usr/bin/env python3
"""vault-wiki-build cluster 偵測：掃 Inbox raw，依既有 tags 找 ≥N 篇共享主題的散落項。

在 vault root（cwd 有 vault-map.md）執行：

    python3 .agents/skills/vault-wiki-build/scripts/cluster.py --min 3

輸出單一 JSON 物件到 stdout；不修改任何檔案。判讀與提議由呼叫端 agent 依 SKILL.md 處理。
已被既有 wiki 頁 wikilink 指到的 raw 視為「已綜合」，整群皆已綜合的 cluster 不重複提議。
"""
import argparse
import json
import re
import sys
from pathlib import Path

# Windows console 預設 cp950，強制 UTF-8 才能正確輸出中文
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

ROOT = Path.cwd()

# 結構/格式標記，非主題訊號，排除出 clustering
STOP_TAGS = {"index", "channel", "youtube", "clippings", "archive", "updates"}


def read(p):
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def frontmatter(text):
    """回傳 (tags:list, title:str, description:str)。取首段 --- 之間的頂層欄位。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], "", ""
    tags, title, desc = [], "", ""
    in_tags = False
    for ln in lines[1:]:
        if ln.strip() == "---":
            break
        if in_tags:
            m = re.match(r"\s+-\s*\"?([^\"]+?)\"?\s*$", ln)
            if m:
                tags.append(m.group(1).strip())
                continue
            in_tags = False
        m = re.match(r"^([a-zA-Z_][\w]*):\s*(.*)$", ln)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if key == "tags":
            in_tags = True
            if val and val not in ("", "[]"):  # inline list fallback
                tags += [t.strip().strip('"') for t in val.strip("[]").split(",") if t.strip()]
                in_tags = False
        elif key == "title":
            title = val.strip('"')
        elif key == "description":
            desc = val.strip('"')
    return tags, title, desc


def covered_stems():
    """已被既有 wiki 頁 wikilink 指到的 raw basename（不含副檔名）。"""
    covered = set()
    wiki = ROOT / "wiki"
    if not wiki.is_dir():
        return covered
    link_re = re.compile(r"\[\[([^\]|#]+)")
    for p in wiki.glob("*.md"):
        for m in link_re.finditer(read(p)):
            base = m.group(1).strip().split("/")[-1]
            covered.add(base[:-3] if base.endswith(".md") else base)
    return covered


def scan(min_n):
    inbox = ROOT / "Inbox"
    notes = []
    if inbox.is_dir():
        for p in sorted(inbox.rglob("*.md")):
            if p.name == "01.index.md":
                continue
            tags, title, desc = frontmatter(read(p))
            notes.append({
                "path": p.relative_to(ROOT).as_posix(),
                "stem": p.stem,
                "title": title or p.stem,
                "description": desc,
                "tags": [t for t in tags if t not in STOP_TAGS],
            })
    covered = covered_stems()
    groups = {}
    for n in notes:
        for t in n["tags"]:
            groups.setdefault(t, []).append(n)
    clusters = []
    for tag, members in sorted(groups.items()):
        if len(members) < min_n:
            continue
        new_members = [m for m in members if m["stem"] not in covered]
        if not new_members:
            continue  # 整群已綜合過，不重複提議
        clusters.append({
            "tag": tag,
            "count": len(members),
            "new_count": len(new_members),
            "notes": [
                {"path": m["path"], "title": m["title"],
                 "description": m["description"], "covered": m["stem"] in covered}
                for m in members
            ],
        })
    clusters.sort(key=lambda c: (-c["new_count"], -c["count"], c["tag"]))
    return {"min": min_n, "cluster_count": len(clusters), "clusters": clusters}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=int, default=3, help="cluster 門檻（共享同主題的最少篇數）")
    args = ap.parse_args()
    if not (ROOT / "vault-map.md").is_file():
        print(json.dumps({"error": "cwd 不在 vault root（找不到 vault-map.md）"}, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps(scan(args.min), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
