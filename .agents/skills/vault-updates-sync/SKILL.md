---
name: vault-updates-sync
description: 同步高信任 developer tooling 更新到 Obsidian，來源以官方 changelog / release notes、GitHub releases、GitHub issues / discussions 為主。使用者提到「updates sync」、「changelog 同步」、「release notes 同步」、「GitHub issue 同步」、「Codex/Claude Code/Copilot/Cursor 更新」、「官方變更整理」、「agent tooling 變更」時使用。
---

# Vault Updates Sync

同步高信任 developer tooling 更新到 Obsidian。重點是可回查、可操作、可沉澱的來源：官方 changelog、release notes、GitHub releases、GitHub issues / discussions。

## 定位

優先來源：

1. **官方 changelog / release notes**：最高信任，適合建立正式來源筆記。
2. **GitHub releases**：版本、功能、breaking change、修復資訊。
3. **GitHub issues / discussions**：actionable bug、workaround、tooling change、maintainer confirmation。

不處理：

- GitHub issues（訊噪比太差，已移除）
- YouTube 頻道同步（用 `vault-youtube-sync`）
- 既有 vault 查詢或單篇筆記建檔（用 `ob`）
- 社群日報或輿情 briefing

## 產出

- 筆記：`content/Inbox/Updates/<YYYY-MM-DD>-weekly-updates.md`（每次 sync 一篇，按工具分 section）
- Index：`content/Inbox/Updates/01.index.md`
- 筆記代表「高信任待消化來源」，進 Inbox 不直接發佈；後續可由使用者整理到 `Cards/` 或 `Topics/`。

### Frontmatter

```yaml
---
title: "<YYYY-MM-DD> Weekly Updates"
created: <今日 YYYY-MM-DD>
updated: <今日 YYYY-MM-DD>
tags:
  - updates
  - <涵蓋的工具 tag，如 claude-code、codex、copilot、cursor>
---
```

常用 tags：`updates`、`claude-code`、`codex`、`copilot`、`cursor`、`mcp`。

### 筆記結構

```markdown
## <工具名>（版本範圍，日期）

**新功能**
- ...

**Bug Fixes**
- ...

**待注意**
- ...

---

## <工具名>
...
```

每個工具一個 section，按重要性排序（自用工具優先）。跳過無使用者可見變更的項目。

## Source index

若 `content/Inbox/Updates/01.index.md` 不存在，先建立下列預設 index，再繼續同步：

```markdown
---
title: Tool Updates
created: <今日 YYYY-MM-DD>
updated: <今日 YYYY-MM-DD>
tags:
  - updates
  - index
---

高信任 developer tooling 更新來源。

## Official changelogs

- OpenAI Codex|https://help.openai.com/en/articles/11428266-codex-changelog|codex
- Claude Code|https://code.claude.com/docs/en/changelog|claude-code
- GitHub Changelog|https://github.blog/changelog/feed/|copilot
- Cursor Changelog|https://www.cursor.com/changelog|cursor

## GitHub repositories

- openai/codex|codex
- anthropics/claude-code|claude-code

## GitHub starred

sync: releases
```

來源格式：

- Official changelogs：`- <name>|<url>|<tag>`
- GitHub repositories：`- <owner>/<repo>|<tag>`
- GitHub starred：`sync: releases` 代表啟用，從 authenticated user 的星星清單抓 releases（`gh` CLI 需已登入）

## 前置作業

### Cwd 契約

本 skill 是 repo-local，所有讀寫路徑均為 repo root 相對的 `content/...`。呼叫前先確認 cwd 為 repo root：

```bash
[ -f "content/master-index.md" ] || { echo "ERROR: cwd 不在 repo root"; exit 1; }
```

### 寫入前 Checklist

這是 `content/` 的寫入路徑。寫入前依 `content/CLAUDE.md` 自檢：

- 敏感資料零容忍：issue / discussion / release body 若含 token、private key、API key，移除該段；若核心內容依賴敏感內容則跳過。
- Frontmatter schema：欄位、順序、白名單以 `scripts/vault-schema.mjs` 為準。
- Tag 沿用既有：新增非固定 tag 前先 grep 既有 vault tags。
- 命名：檔名不含空格，不含 `?:;"'` 等特殊字元。

## 步驟 1：讀取來源

讀 `content/Inbox/Updates/01.index.md`：

- `## Official changelogs` 段：官方 changelog / release notes。
- `## GitHub repositories` 段：GitHub release / issue / discussion 來源。

若 index 不存在，用上方範本建立。若某段為空，略過該來源類型，不中止整體流程。

## 步驟 2：抓候選

預設同步最近 7 天；使用者指定日期時用該日期到今天。

從 index 解析：

- `## GitHub repositories` 段：逐行取 `<owner>/<repo>` 傳給 `--repo`
- `## GitHub starred` 段含 `sync: releases`：加上 `--starred` flag

```bash
SCRIPT=".claude/skills/vault-updates-sync/scripts/fetch_updates.py"
PY=$(command -v python3 || command -v python)

# 從 index 解析 repos（用 array 避免換行問題）
REPO_ARGS=()
while IFS= read -r repo; do
  [[ -n "$repo" ]] && REPO_ARGS+=("--repo" "$repo")
done < <(grep -A50 '## GitHub repositories' content/Inbox/Updates/01.index.md \
  | grep -E '^\- [A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+' \
  | sed 's/^- //' | cut -d'|' -f1)

# 檢查是否啟用 starred
STARRED=()
grep -A5 '## GitHub starred' content/Inbox/Updates/01.index.md \
  | grep -q 'sync: releases' && STARRED=("--starred")

$PY $SCRIPT --since <YYYY-MM-DD> "${REPO_ARGS[@]}" "${STARRED[@]}"
```

輸出格式：

- `META:since|||<YYYY-MM-DD>`
- `OFFICIAL:<name>|||<url>|||<tag>`
- `CHANGELOG:<source>|||<published>|||<title>|||<url>`
- `RELEASE:<repo>|||<published>|||<tag>|||<name>|||<url>`
- `DISCUSSION:<repo>|||<updated>|||<comments>|||<title>|||<url>`（explicit repos 才抓；starred repos 只抓 releases）
- `ERROR:<source>:<message>`（記錄後繼續）

官方 changelog 若沒有 RSS/API（例如單頁 changelog），由主流程或 subagent 直接讀 URL，抽取最近日期區段；不要把整頁全文寫入筆記。

## 步驟 3：高精度粗篩

保留候選：

- 官方 changelog entry 有 workflow / CLI / API / model / connector / billing-quota / deprecation / breaking change 影響。
- GitHub release 包含新功能、breaking change、security fix、workflow 變更、重要 bug fix。
- GitHub discussion 形成具體做法、官方回答、或重要設計決策。

跳過候選：

- release 只有內部依賴 bump、alpha/noise、或無使用者可見變更。
- changelog 與 developer tooling / coding agent / workflow 無關。
- starred repo 的 release 若與 coding agent / developer workflow 無關（例如純 UI library patch）。

若粗篩後候選仍過多，最多送 24 筆給分析階段，優先順序：

1. 官方 changelog / release notes
2. Stable GitHub releases 或明確 user-facing release
3. 有 `has repro`、workaround、maintainer confirmation、或 comments >= 5 的 issue
4. 有具體設計決策或官方回答的 discussion

## 步驟 4：分批分析與建檔

將通過粗篩的候選按每批 5-6 筆，使用 general-purpose subagent 平行分析。無 subagent 能力時由主 agent 直接讀 `references/item-analyzer.md` 執行同流程。

Subagent prompt：

```text
任務：分析 developer tooling update 的可操作價值，必要時建立 Obsidian 筆記。
詳細指示請依 `.claude/skills/vault-updates-sync/references/item-analyzer.md`。

NOTES_ROOT：content/Inbox/Updates/
今日日期：<YYYY-MM-DD>

候選清單：
1. <TYPE> <source/repo> <published/updated> <title>
   URL: <url>
   metadata: <labels/comments/tag/state 等>

回傳格式：每篇一行 `<url> save|skip <一行原因>`。
```

## 步驟 5：彙整

回覆固定包含：

- 各來源抓取數 / 粗篩通過數 / 存入數
- 已建立筆記路徑
- 跳過原因分布
- 需要人工追蹤但未建檔的候選（最多 5 筆）

不自動 commit。所有變更留給使用者審核。

## 去重

建立筆記前先用 `source:` URL 去重：

```bash
grep -rl "^source: <url>$" content/Inbox/Updates content/Cards content/Topics 2>/dev/null
```

若 changelog entry 沒有獨立 URL，使用該頁 URL 加 heading slug 作為 canonical URL（例如 `<url>#<entry-slug>`），避免整頁只能存一次。
