#!/usr/bin/env python3
"""vault-lint 掃描器：純 stdlib，跨平台（Windows/mac/Linux 行為一致）。

在 vault root（cwd 有 vault-map.md）執行：

    python3 .agents/skills/vault-lint/scripts/lint.py

輸出單一 JSON 物件到 stdout，欄位對應 SKILL.md 的掃描項表。
不修改任何檔案；判讀與互動確認由呼叫端 agent 依 SKILL.md 處理。
"""
import datetime
import json
import re
import sys
from pathlib import Path

# Windows console 預設 cp950，強制 UTF-8 才能正確輸出中文檔名 / JSON
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
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

# 敏感資料 token 前綴正典：CLAUDE.md「### 2. 敏感資料」的機器執行副本，正規化為比對用 stem
# （`xox[baprs]-`→`xox`、`-----BEGIN ... PRIVATE KEY-----`→`-----BEGIN`）。
# 與 WHITELIST 同理：格式與 CLAUDE.md 散文不可互通，靠 sensitive_drift() 校驗不漂移。
SENSITIVE_PREFIXES = [
    "sk-", "sk-ant-", "ghp_", "gho_", "AKIA", "AIza", "xox", "eyJ", "-----BEGIN",
]

# 各 skill 中「自包含複製」這份黑名單的 subagent reference（執行時不保證載入 CLAUDE.md，故各自列全）。
# 新增含敏感黑名單的 reference 時加入此清單，sensitive_drift() 會校驗它們涵蓋正典每個前綴。
SENSITIVE_REFERENCE_FILES = [
    ".agents/skills/ob-write/references/write.md",
    ".agents/skills/vault-youtube-sync/references/subagent-note-creator.md",
    ".agents/skills/vault-updates-daily/references/item-analyzer.md",
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


def strip_markdown_code(text: str) -> str:
    """移除 fenced code blocks 與 inline code，避免程式範例被當成 wikilink。"""
    text = re.sub(r"(?ms)^```.*?^```", "", text)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def claude_schema_order():
    """解析 CLAUDE.md frontmatter schema 表格第一欄，回傳欄位順序 list；解析不到回 None。

    識別表頭為含「欄位 / 用途 / 值格式」的那一列，其後逐列抽 `| `field` |` 第一欄，
    遇空行或非表格列即視為表格結束。
    """
    lines = read(ROOT / "CLAUDE.md").splitlines()
    fields, in_table = [], False
    for ln in lines:
        if not in_table:
            # 表頭須是 `|` 開頭的表格列，避免散文句同時含這三詞被誤判
            if ln.lstrip().startswith("|") and "欄位" in ln and "用途" in ln and "值格式" in ln:
                in_table = True
            continue
        s = ln.strip()
        if not s:
            break
        if set(s) <= set("|-: "):  # header 下的分隔列
            continue
        m = re.match(r"^\|\s*`([a-zA-Z_][a-zA-Z0-9_]*)`", ln)
        if m:
            fields.append(m.group(1))
        else:
            break
    return fields or None


def schema_drift():
    """校驗 lint.py 的 WHITELIST 是否與 CLAUDE.md schema 表格一字不差。

    WHITELIST 是 CLAUDE.md frontmatter schema 的機器執行副本（格式不可互通、無法消除）；
    此檢查讓兩者一旦漂移即被 lint 抓到，不靠人工同步。一致回 None。
    """
    declared = claude_schema_order()
    if declared is None:
        return {"error": "無法解析 CLAUDE.md frontmatter schema 表格"}
    if declared == WHITELIST:
        return None
    return {"claude_md": declared, "lint_whitelist": list(WHITELIST)}


def claude_sensitive_prefixes():
    """解析 CLAUDE.md「敏感資料」段落的 token 前綴，正規化為比對用 stem list；解析不到回 None。

    取該 `###` 段落內所有反引號 token，截斷到第一個 `[`（字元類）與空白之前，
    使 `xox[baprs]-`→`xox`、`-----BEGIN ... PRIVATE KEY-----`→`-----BEGIN`。
    """
    lines = read(ROOT / "CLAUDE.md").splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("#") and "敏感資料" in ln:
            start = i
            break
    if start is None:
        return None
    seg = []
    for ln in lines[start + 1:]:
        if ln.lstrip().startswith("#"):
            break
        seg.append(ln)
    stems = []
    for tok in re.findall(r"`([^`]+)`", "\n".join(seg)):
        stem = tok.split("[")[0].split()[0]
        if stem and stem not in stems:
            stems.append(stem)
    return stems or None


def sensitive_drift():
    """校驗敏感資料 token 黑名單未漂移，分兩層（一致回 None）：

    1. CLAUDE.md 正典 vs lint.py 的 SENSITIVE_PREFIXES（機器執行副本）。
    2. 各 subagent reference（自包含複製）是否涵蓋正典每個前綴。

    類比 schema_drift()，補上「高後果（公開發佈洩密）＋ 多處手抄 ＋ 原本零校驗」的盲點。
    """
    canon = claude_sensitive_prefixes()
    if canon is None:
        return {"error": "無法解析 CLAUDE.md 敏感資料段落"}
    result = {}
    if canon != SENSITIVE_PREFIXES:
        result["canon_vs_lint"] = {"claude_md": canon, "lint_const": list(SENSITIVE_PREFIXES)}
    refs = {}
    for relpath in SENSITIVE_REFERENCE_FILES:
        p = ROOT / relpath
        if not p.is_file():
            refs[relpath] = ["<檔案不存在>"]
            continue
        text = read(p)
        lack = [s for s in SENSITIVE_PREFIXES if s not in text]
        if lack:
            refs[relpath] = lack
    if refs:
        result["references"] = refs
    return result or None


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

    # 5. vault-map 未收錄的 Topics（含巢狀子目錄；子字串比對目錄名）
    #    遞迴到子目錄，否則 Topics/X/Y/ 這類第二層漏收 vault-map 抓不到
    vmap = read(ROOT / "vault-map.md")
    all_topic_dirs = (
        sorted(d for d in topics.rglob("*") if d.is_dir() and not _hidden(d))
        if topics.is_dir() else []
    )
    # 比對帶尾斜線的目錄名（樹狀條目皆為 `<name>/`），避免散文中同字串（如描述裡的「部署」）造成假陰性
    out["topics_not_in_vaultmap"] = [rel(d) for d in all_topic_dirs if (d.name + "/") not in vmap]

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
        body = strip_markdown_code(body)
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

    # 12. WHITELIST 與 CLAUDE.md schema 漂移校驗（None = 一致）
    out["schema_drift"] = schema_drift()

    # 13. 敏感資料 token 黑名單漂移校驗（None = 一致）
    out["sensitive_drift"] = sensitive_drift()

    return out


def main():
    if not (ROOT / "vault-map.md").is_file():
        print(json.dumps({"error": "cwd 不在 vault root（找不到 vault-map.md）"}, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps(scan(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
