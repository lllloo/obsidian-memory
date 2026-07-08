#!/usr/bin/env python3
"""vault-lint 掃描器：純 stdlib，跨平台（Windows/mac/Linux 行為一致）。

在 vault root（cwd 有 vault-map.md）執行：

    python3 .agents/skills/vault-lint/scripts/lint.py

輸出單一 JSON 物件到 stdout，欄位對應 SKILL.md 的掃描項表。
不修改任何檔案；判讀與互動確認由呼叫端 agent 依 SKILL.md 處理。

掃描範圍：只有 `raw/`、`wiki/`，加上根層治理 .md（CLAUDE.md / SYSTEM-DESIGN.md /
vault-map.md / README.md / index.md，僅用於 dead_links 的連結來源與目標索引）。
`Cards/`、`Topics/` 是使用者私人區、Quartz 唯一公開層，agent 一律不讀、不寫、
不掃描、不索引——所有走訪目錄的邏輯都排除這兩個資料夾。
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

# CLAUDE.md「### 4. Frontmatter schema」表格第一欄的機器執行副本，順序即正典順序。
WHITELIST = [
    "title", "description", "created", "updated", "source",
    "published", "parent", "last_sync_id", "draft", "tags",
]
WL_ORDER = {k: i for i, k in enumerate(WHITELIST)}

REQUIRED_DIRS = ["raw", "raw/Clippings", "raw/Updates", "raw/YouTube", "wiki"]

# Cards/Topics 是使用者私人區，agent 不掃；所有目錄走訪一律排除。
EXCLUDED_TOP_DIRS = {"Cards", "Topics"}

# dead_links 的連結來源／目標索引額外納入的根層治理檔（raw/wiki 之外唯一可掃的內容）。
ROOT_GOVERNANCE_FILES = ["CLAUDE.md", "SYSTEM-DESIGN.md", "vault-map.md", "README.md", "index.md"]


def rel(p: Path) -> str:
    """相對 vault root 的 posix 路徑（一律正斜線）。"""
    return p.relative_to(ROOT).as_posix()


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _excluded(p: Path) -> bool:
    """隱藏路徑（.agents/.claude/.git/.obsidian…），或落在 Cards/Topics 底下（使用者私人區，agent 不掃）。"""
    parts = p.relative_to(ROOT).parts
    if not parts:
        return False
    if parts[0] in EXCLUDED_TOP_DIRS:
        return True
    return any(part.startswith(".") for part in parts)


def md_files(*dirs: str):
    for d in dirs:
        base = ROOT / d
        if base.is_dir():
            yield from sorted(p for p in base.rglob("*.md") if not _excluded(p))


def governance_files():
    return [ROOT / f for f in ROOT_GOVERNANCE_FILES if (ROOT / f).is_file()]


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


def scan():
    out = {"date": datetime.date.today().isoformat()}

    # 1. raw 散項：直接躺在 raw root、未歸進任何 raw 子夾的 md
    #    raw 層永久留存，各子夾（Clippings/Archive/Updates/YouTube）本就會長、不算積壓；
    #    只有還沒歸進任何子夾的散項才提醒歸檔。
    raw_dir = ROOT / "raw"
    out["inbox_backlog"] = sum(1 for p in md_files("raw") if p.parent == raw_dir)

    # 2. Frontmatter 缺欄位（raw + wiki，agent 唯一能寫的層）
    missing_title, missing_tags, missing_updated = [], [], []
    for p in md_files("raw", "wiki"):
        # 用 frontmatter 頂層欄位判定，避免正文行首 `title:` 等造成假陰性
        keys = frontmatter_keys(read(p))
        if "title" not in keys:
            missing_title.append(rel(p))
        if "tags" not in keys:
            missing_tags.append(rel(p))
        if "updated" not in keys:
            missing_updated.append(rel(p))
    out["missing_title"] = missing_title
    out["missing_tags"] = missing_tags
    out["missing_updated"] = missing_updated

    # 3. description 缺失（規範必填三類：wiki 頁、raw/Clippings、raw/YouTube 影片筆記；
    #    各自的 01.index.md 是目錄/導覽頁，不算內容頁，排除）
    desc_targets = [p for p in md_files("wiki") if p.name != "01.index.md"]
    clip = ROOT / "raw" / "Clippings"
    if clip.is_dir():
        desc_targets += [p for p in sorted(clip.glob("*.md")) if p.name != "01.index.md"]
    yt = ROOT / "raw" / "YouTube"
    if yt.is_dir():
        desc_targets += [p for p in sorted(yt.rglob("*.md")) if p.name != "01.index.md"]
    out["missing_description"] = [
        rel(p) for p in desc_targets
        if p.is_file() and "description" not in frontmatter_keys(read(p))
    ]

    # 4. Tag 同義異寫：統計純英數 YAML list 項（raw + wiki），取 top 60
    tag_re = re.compile(r'^\s+-\s*"?([A-Za-z0-9_-]+)"?\s*$')
    counts = {}
    for p in md_files("raw", "wiki"):
        for ln in read(p).splitlines():
            m = tag_re.match(ln)
            if m:
                counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:60]
    out["tag_counts"] = top

    # 5. dead_links 的連結來源／目標索引：raw + wiki + 根層治理檔（唯一可掃的內容範圍）
    scanned = list(md_files("raw", "wiki")) + governance_files()
    texts = {p: read(p) for p in scanned}

    # 5a. wiki 孤立頁（排除 01.index.md，無任何入站 [[title 連結）
    #     只在掃描範圍內找入站連結——wiki 單向連回 raw，交叉引用只會出現在 raw/wiki/根層治理檔裡，
    #     Cards/Topics 一律不讀，即便它們私下連了 wiki 頁也不算數。
    orphans_wiki = []
    for p in md_files("wiki"):
        if p.name == "01.index.md":
            continue
        title = p.stem
        needle = "[[" + title
        cited = any(needle in body for q, body in texts.items() if q != p)
        if not cited:
            orphans_wiki.append(rel(p))
    out["orphans_wiki"] = orphans_wiki

    # 5b. 死連結（wikilink 目標不存在）
    link_re = re.compile(r"\[\[([^\]|#]+)")
    targets = set()
    for body in texts.values():
        body = strip_markdown_code(body)
        for m in link_re.finditer(body):
            targets.add(m.group(1).strip())
    # 建立檔名索引（basename → 存在），同樣排除隱藏目錄與 Cards/Topics
    names = {p.name for p in ROOT.rglob("*") if p.is_file() and not _excluded(p)}
    dead = []
    for t in sorted(targets):
        if not t or "<" in t:  # 跳過 schema 佔位符 [[<...>]]
            continue
        base = t.split("/")[-1]
        wanted = base if base.endswith(".base") else base + ".md"
        if wanted not in names:
            dead.append(f"[[{t}]]")
    out["dead_links"] = dead

    # 6. 規範資料夾實體存在（僅 agent 管的 raw/wiki 子夾；git 不追蹤空目錄）
    out["missing_required_dirs"] = [
        d for d in REQUIRED_DIRS if not (ROOT / d).is_dir()
    ]

    # 7. Frontmatter 欄位順序錯亂 / 白名單外游離欄位（raw + wiki）
    rogue, order = [], []
    for p in md_files("raw", "wiki"):
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

    # 8. WHITELIST 與 CLAUDE.md schema 漂移校驗（None = 一致）
    out["schema_drift"] = schema_drift()

    return out


def main():
    if not (ROOT / "vault-map.md").is_file():
        print(json.dumps({"error": "cwd 不在 vault root（找不到 vault-map.md）"}, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps(scan(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
