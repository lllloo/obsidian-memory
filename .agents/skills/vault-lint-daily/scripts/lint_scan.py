#!/usr/bin/env python3
"""vault-lint-daily 機械層掃描：死連結、孤立頁、frontmatter、tag 盤點、raw 消化缺口。

在 vault root 執行；輸出 machine-readable lines（一行一發現），由主 agent 組裝報告：

  DEADLINK:<file>:<target>   wikilink 指向不存在的檔案
  ORPHAN:<file>              wiki 頁無任何入連（01.index 除外）
  FM:<file>:<問題>           frontmatter 缺必要欄位 / tags 非 YAML list
  TAG:<tag>:<count>          tag 盤點（同義異寫漂移由主 agent 判讀）
  RAWGAP:<file>              raw 檔未被任何 wiki 頁引用（待消化原料）
  INDEXGAP:<dir>:<file>      raw 資料夾 literal index 漏登
  BASEIDX:<dir>              該 index 用 .base 動態清單，跳過漏登檢查
  CHANGED:<file>             近 N 天有 git 變動的 wiki 頁（語意層輸入）
  SUMMARY:<key>=<value>      各類計數

用法：python3 .agents/skills/vault-lint-daily/scripts/lint_scan.py [--days 7]
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# 掃描邊界：cards/topics 與消費性 feeds 不掃。
# feeds/youtube 只進連結解析 universe，讓 wiki 對已選用影片來源的 wikilink 仍可解析；
# 後續 DEADLINK/FM/TAG/RAWGAP/INDEXGAP 各層規則都不把 feeds 當掃描目標。
EXCLUDED_TOP = {
    "cards", "topics",
    ".obsidian", ".clipper", ".agents", ".claude", ".git",
    "node_modules", "public", "quartz",
}
EXCLUDED_FEED_CHILDREN = {"updates", "lint"}

REQUIRED_FIELDS = ("title", "created", "updated", "tags")

WIKILINK_RE = re.compile(r"\[\[([^\[\]]+?)\]\]")
FENCE_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def is_excluded(path: Path) -> bool:
    parts = path.parts
    if not parts:
        return False
    if parts[0] in EXCLUDED_TOP or parts[0].startswith("."):
        return True
    return len(parts) > 1 and parts[0] == "feeds" and parts[1] in EXCLUDED_FEED_CHILDREN


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> dict:
    """極簡 frontmatter 解析：只取 top-level key 與 tags 是否為 YAML list。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm: dict = {}
    current_key = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            current_key = m.group(1)
            fm[current_key] = m.group(2).strip()
            if current_key == "tags":
                fm.setdefault("_tag_items", [])
        elif current_key == "tags":
            item = re.match(r"^\s+-\s+(.+)$", line)
            if item:
                fm["_tag_items"].append(item.group(1).strip().strip('"'))
    return fm


def extract_links(text: str) -> list:
    """抽 wikilink 目標；先剝 code fence 與 inline code 避免範例誤判。"""
    body = FENCE_RE.sub("", text)
    body = INLINE_CODE_RE.sub("", body)
    targets = []
    for raw in WIKILINK_RE.findall(body):
        t = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if t:
            targets.append(t)
    return targets


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7, help="語意層取近 N 天變動的 wiki 頁")
    args = ap.parse_args()

    root = Path(".")
    if not (root / "schema" / "vault-map.md").is_file():
        print("ERROR:not-vault-root（找不到 schema/vault-map.md，請在 vault root 執行）")
        return 1

    # ---- 收集檔案宇宙（連結解析範圍：全 vault 減去排除區）----
    universe = [
        p for p in root.rglob("*")
        if p.suffix in (".md", ".base") and p.is_file() and not is_excluded(p.relative_to(root))
    ]
    rel = {p: p.relative_to(root).as_posix() for p in universe}

    # 解析鍵：md 用 stem 與去副檔名相對路徑；.base 連結必須帶副檔名，用完整檔名
    resolvable = set()
    for p in universe:
        if p.suffix == ".md":
            resolvable.add(p.stem)
            resolvable.add(rel[p][:-3])
        else:
            resolvable.add(p.name)
            resolvable.add(rel[p])

    # ---- 逐檔抽連結、frontmatter ----
    texts, fms, outlinks = {}, {}, {}
    for p in universe:
        if p.suffix != ".md":
            continue
        texts[p] = read_text(p)
        fms[p] = parse_frontmatter(texts[p])
        outlinks[p] = extract_links(texts[p])

    inbound: dict = {}
    for p, targets in outlinks.items():
        for t in targets:
            key = t[:-3] if t.endswith(".md") else t
            base = key.split("/")[-1]
            inbound.setdefault(base, set()).add(p)

    findings = {k: [] for k in ("DEADLINK", "ORPHAN", "FM", "RAWGAP", "INDEXGAP", "BASEIDX", "CHANGED")}

    def top_of(p: Path) -> str:
        return rel[p].split("/", 1)[0]

    # ---- DEADLINK：wiki/raw/schema 內指向不存在檔案的 wikilink ----
    for p in texts:
        if top_of(p) not in ("wiki", "raw", "schema"):
            continue
        for t in outlinks[p]:
            key = t[:-3] if t.endswith(".md") else t
            if key in resolvable or key.split("/")[-1] in resolvable:
                continue
            findings["DEADLINK"].append(f"DEADLINK:{rel[p]}:{t}")

    # ---- ORPHAN：wiki 頁（01.index 除外）無任何入連 ----
    for p in texts:
        if top_of(p) != "wiki" or p.name == "01.index.md":
            continue
        linkers = {
            q for q in inbound.get(p.stem, set()) - {p}
            if top_of(q) in ("wiki", "raw", "schema")
        }
        if not linkers:
            findings["ORPHAN"].append(f"ORPHAN:{rel[p]}")

    # ---- FM：缺必要欄位 / tags 非 list（draft 占位跳過）----
    for p in texts:
        if top_of(p) not in ("wiki", "raw"):
            continue
        fm = fms[p]
        if fm.get("draft") == "true":
            continue
        missing = [f for f in REQUIRED_FIELDS if f not in fm]
        if missing:
            findings["FM"].append(f"FM:{rel[p]}:missing={','.join(missing)}")
        if "tags" in fm and fm.get("tags") and not fm.get("_tag_items"):
            findings["FM"].append(f"FM:{rel[p]}:tags-not-list")

    # ---- TAG 盤點（wiki + raw）----
    tag_counts: dict = {}
    for p in texts:
        if top_of(p) in ("wiki", "raw"):
            for t in fms[p].get("_tag_items", []):
                tag_counts[t] = tag_counts.get(t, 0) + 1
    tag_lines = [f"TAG:{t}:{c}" for t, c in sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))]

    # ---- RAWGAP：raw 檔未被任何 wiki 頁引用 ----
    for p in texts:
        if top_of(p) != "raw" or p.name == "01.index.md" or fms[p].get("draft") == "true":
            continue
        linkers = inbound.get(p.stem, set())
        if not any(top_of(q) == "wiki" for q in linkers):
            findings["RAWGAP"].append(f"RAWGAP:{rel[p]}")

    # ---- INDEXGAP / BASEIDX：raw 各資料夾 index 漏登 ----
    for idx in sorted((root / "raw").rglob("01.index.md")):
        folder = idx.parent
        idx_text = texts.get(idx, "")
        drel = folder.relative_to(root).as_posix()
        if ".base" in idx_text:
            findings["BASEIDX"].append(f"BASEIDX:{drel}")
            continue
        for f in sorted(folder.glob("*.md")):
            if f.name == "01.index.md":
                continue
            if f.stem not in idx_text:
                findings["INDEXGAP"].append(f"INDEXGAP:{drel}:{f.name}")

    # ---- CHANGED：近 N 天 git 變動的 wiki 頁（語意層輸入）----
    try:
        r = subprocess.run(
            ["git", "log", f"--since={args.days} days ago", "--name-only", "--pretty=format:"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        changed = sorted({
            line.strip() for line in r.stdout.splitlines()
            if line.strip().startswith("wiki/") and line.strip().endswith(".md")
            and not line.strip().endswith("01.index.md") and (root / line.strip()).is_file()
        })
        findings["CHANGED"] = [f"CHANGED:{c}" for c in changed]
    except OSError:
        print("ERROR:git-unavailable（CHANGED 清單缺漏，語意層請自行判斷範圍）")

    # ---- 輸出 ----
    for key in ("DEADLINK", "ORPHAN", "FM", "RAWGAP", "INDEXGAP", "BASEIDX", "CHANGED"):
        for line in findings[key]:
            print(line)
    for line in tag_lines:
        print(line)
    for key in ("DEADLINK", "ORPHAN", "FM", "RAWGAP", "INDEXGAP", "CHANGED"):
        print(f"SUMMARY:{key.lower()}={len(findings[key])}")
    print(f"SUMMARY:tags={len(tag_counts)}")
    scanned_targets = sum(1 for p in texts if top_of(p) in ("wiki", "raw", "schema"))
    print(f"SUMMARY:scanned={scanned_targets}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
