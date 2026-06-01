#!/usr/bin/env python3
"""vault-lint 掃描器：純 stdlib，跨平台（Windows/mac/Linux 行為一致）。

在 vault root（cwd 有 vault-map.md）執行：

    python .agents/skills/vault-lint/scripts/lint.py

輸出單一 JSON 物件到 stdout，欄位對應 SKILL.md 的 11 個掃描項。
不修改任何檔案；判讀與互動確認由呼叫端 agent 依 SKILL.md 處理。
"""
import datetime
import json
import re
import sys
from pathlib import Path

# Windows console 預設 cp950，強制 UTF-8 才能正確輸出中文檔名 / JSON
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

ROOT = Path.cwd()

WHITELIST = [
    "title", "description", "created", "updated", "source",
    "published", "parent", "last_sync_id", "draft", "extracted_to", "tags",
]
WL_ORDER = {k: i for i, k in enumerate(WHITELIST)}

REQUIRED_DIRS = [
    "Inbox", "Inbox/Clippings", "Inbox/Updates", "Inbox/YouTube", "Cards", "Topics",
]


def rel(p: Path) -> str:
    """相對 vault root 的 posix 路徑（一律正斜線）。"""
    return p.relative_to(ROOT).as_posix()


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _hidden(p: Path) -> bool:
    """路徑含 `.` 開頭的元件（.agents/.claude/.git/.obsidian…），對齊 ripgrep 預設略過隱藏目錄。"""
    return any(part.startswith(".") for part in p.relative_to(ROOT).parts)


def md_files(*dirs: str):
    for d in dirs:
        base = ROOT / d
        if base.is_dir():
            yield from sorted(p for p in base.rglob("*.md") if not _hidden(p))


def has_line(text: str, prefix: str) -> bool:
    """任一行以 prefix 開頭（對應 rg '^prefix'）。"""
    return any(ln.startswith(prefix) for ln in text.splitlines())


def frontmatter_keys(text: str):
    """取第一段 frontmatter（首兩個 --- 之間）的頂層欄位名，依出現順序。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    keys = []
    for ln in lines[1:]:
        if ln.strip() == "---":
            break
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*):", ln)
        if m:
            keys.append(m.group(1))
    return keys


def scan():
    out = {"date": datetime.date.today().isoformat()}

    # 1. Inbox 積壓（排除 Inbox/Updates/）
    updates = (ROOT / "Inbox" / "Updates")
    backlog = [
        p for p in md_files("Inbox")
        if updates not in p.parents
    ]
    out["inbox_backlog"] = len(backlog)

    # 2. extracted_to 遺留（Inbox 內）
    out["extracted_to"] = [
        rel(p) for p in md_files("Inbox") if has_line(read(p), "extracted_to:")
    ]

    # 3. Frontmatter 缺欄位（Cards/Topics）
    missing_title, missing_tags, missing_updated = [], [], []
    for p in md_files("Cards", "Topics"):
        # 用 frontmatter 頂層欄位判定，避免正文行首 `title:` 等造成假陰性
        keys = frontmatter_keys(read(p))
        if "title" not in keys:
            missing_title.append(rel(p))
        if p.name != "index.md" and "tags" not in keys:
            missing_tags.append(rel(p))
        if "updated" not in keys:
            missing_updated.append(rel(p))
    out["missing_title"] = missing_title
    out["missing_tags"] = missing_tags
    out["missing_updated"] = missing_updated

    # 4. Topics 資料夾缺 index.md
    topics = ROOT / "Topics"
    topic_dirs = sorted(d for d in topics.iterdir() if d.is_dir()) if topics.is_dir() else []
    out["topics_missing_index"] = [
        rel(d) + "/" for d in topic_dirs if not (d / "index.md").is_file()
    ]

    # 5. vault-map 未收錄的 Topics（子字串比對，與既有行為一致）
    vmap = read(ROOT / "vault-map.md")
    out["topics_not_in_vaultmap"] = [d.name for d in topic_dirs if d.name not in vmap]

    # 6. Tag 同義異寫：統計純英數 YAML list 項，取 top 60
    tag_re = re.compile(r'^\s+-\s*"?([A-Za-z0-9_-]+)"?\s*$')
    counts = {}
    for p in md_files("."):
        for ln in read(p).splitlines():
            m = tag_re.match(ln)
            if m:
                counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:60]
    out["tag_counts"] = top

    # 7. 孤立頁面（Cards/Topics，排除 index.md，無入站 [[title）
    all_md = list(md_files("."))
    texts = {p: read(p) for p in all_md}
    orphans_cards, orphans_topics = [], []
    for p in md_files("Cards", "Topics"):
        if p.name == "index.md":
            continue
        title = p.stem
        needle = "[[" + title
        cited = any(needle in body for q, body in texts.items() if q != p)
        if not cited:
            r = rel(p)
            (orphans_cards if r.startswith("Cards/") else orphans_topics).append(r)
    out["orphans_cards"] = orphans_cards
    out["orphans_topics"] = orphans_topics

    # 8. 死連結（wikilink 目標不存在）
    link_re = re.compile(r"\[\[([^\]|#]+)")
    targets = set()
    for body in texts.values():
        for m in link_re.finditer(body):
            targets.add(m.group(1).strip())
    # 建立檔名索引（basename → 存在），同樣略過隱藏目錄
    names = {p.name for p in ROOT.rglob("*") if p.is_file() and not _hidden(p)}
    dead = []
    for t in sorted(targets):
        if not t or "<" in t:  # 跳過 schema 佔位符 [[<...>]]
            continue
        base = t.split("/")[-1]
        wanted = base if base.endswith(".base") else base + ".md"
        if wanted not in names:
            dead.append(f"[[{t}]]")
    out["dead_links"] = dead

    # 9. 規範資料夾實體存在
    out["missing_required_dirs"] = [
        d for d in REQUIRED_DIRS if not (ROOT / d).is_dir()
    ]

    # 10. description 缺失（三類規範必填）
    desc_targets = []
    desc_targets += [d / "index.md" for d in topic_dirs]
    clip = ROOT / "Inbox" / "Clippings"
    if clip.is_dir():
        desc_targets += sorted(clip.glob("*.md"))
    yt = ROOT / "Inbox" / "YouTube"
    if yt.is_dir():
        desc_targets += [p for p in sorted(yt.rglob("*.md")) if p.name != "01.index.md"]
    out["missing_description"] = [
        rel(p) for p in desc_targets
        if p.is_file() and "description" not in frontmatter_keys(read(p))
    ]

    # 11. Frontmatter 欄位順序錯亂 / 白名單外游離欄位
    rogue, order = [], []
    for p in md_files("Cards", "Topics", "Inbox"):
        keys = frontmatter_keys(read(p))
        if not keys:
            continue
        r = [k for k in keys if k not in WL_ORDER]
        if r:
            rogue.append([rel(p), r])
        inwl = [k for k in keys if k in WL_ORDER]
        if inwl != sorted(inwl, key=lambda k: WL_ORDER[k]):
            order.append(rel(p))
    out["frontmatter_rogue"] = rogue
    out["frontmatter_order"] = order

    return out


def main():
    if not (ROOT / "vault-map.md").is_file():
        print(json.dumps({"error": "cwd 不在 vault root（找不到 vault-map.md）"}), ensure_ascii=False)
        sys.exit(1)
    print(json.dumps(scan(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
