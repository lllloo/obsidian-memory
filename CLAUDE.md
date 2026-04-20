# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概覽

Obsidian 個人知識庫，以 [Quartz 4](https://quartz.jzhao.xyz/) 發佈至 `ob.bugloop.com`。Vault 內容放在 `content/`，Quartz 框架程式碼在 `quartz/`。

## 常用指令

需要 Node.js 22+、npm 10.9.2+（`package.json` engines）。

```bash
npx quartz build --serve         # 本地預覽（localhost:8080）
npm run check                    # TypeScript 型別檢查 + Prettier 格式驗證
npm run format                   # 自動格式化
npm test                         # tsx --test（Quartz 測試套件；修改 quartz/ 才會用到）
```

## 架構

- `content/` — Obsidian vault（筆記、模板），Quartz 從此目錄讀取 Markdown 建站
- `content/master-index.md` — Vault 入口索引，查詢知識時先讀這份確認資料夾與 tag 分布
- `quartz/` — Quartz 框架原始碼（不需修改）
- `quartz.config.ts` — 站台設定（外觀、plugins、ignorePatterns）
- `quartz.layout.ts` — 版面配置
- `AGENTS.md` — `CLAUDE.md` 的 symlink，給非 Claude Code 的 agent 工具讀（改 CLAUDE.md 自動同步）
- `.github/workflows/deploy.yml` — push 到 `main` 自動建置並部署至 GitHub Pages

## Quartz 重要行為

- `ignorePatterns` 包含 `private`、`.obsidian`、`CLAUDE.md`、`YouTube`、`Clippings`，這些不會發佈至網站
- frontmatter 加 `draft: true` 的筆記會被 `RemoveDrafts` plugin 過濾，不發佈
- 日期優先順序：frontmatter → git → filesystem（`CreatedModifiedDate` plugin）
- Plugin pipeline：transformers（解析 Markdown）→ filters（篩選頁面）→ emitters（產生 HTML/靜態資源）
- Wikilink 以 `shortest` 解析（`CrawlLinks`），連結目標需在 `content/` 下存在對應檔案

## Obsidian Vault 規則

筆記結構、命名規則、tag 格式、安全規範等詳見 [`content/CLAUDE.md`](content/CLAUDE.md)。

查詢 vault 知識時，先讀 [`content/master-index.md`](content/master-index.md) 確認資料夾與 tag 分布，再導航到對應位置。

請遵循以下子模組的規範：
- @content/CLAUDE.md

## 文件同步規則

**修改 `CLAUDE.md` 的 Claude Code 設定清單、symlink 指令、觸發方式、或 vault 協議時，必須同步更新 `README.md` 對應區塊**。兩者面向不同受眾（CLAUDE.md 給 Claude Code、README.md 給使用者），但資訊需一致。新增 agent / command / skill 時尤其要記得同步。

repo 根目錄的 `AGENTS.md` 是 `CLAUDE.md` 的 symlink（給非 Claude Code 的其他 agent 工具讀），改動會自動同步，不需手動複製。

## Claude Code Agent 與指令

此 repo 統一管理 Obsidian 相關的 Claude Code 設定，透過 symlink 掛載至全域，讓這些設定在任何專案目錄都能生效。

依類型分組。「全域路徑」有值 = 需 symlink 掛全域（跨專案可用），`—` = 僅本 repo 生效。

**協議（Config）**

| 檔案 | 全域路徑 | 用途 |
|------|---------|------|
| `.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` | Vault + WebSearch 並行查詢協議 |

**Agents**

| 檔案 | 全域路徑 | 用途 |
|------|---------|------|
| `.claude/agents/obsidian.md` | `~/.claude/agents/obsidian.md` | Obsidian 筆記操作（讀寫） |
| `.claude/agents/vault-query.md` | `~/.claude/agents/vault-query.md` | Vault 唯讀查詢（動態解析 vault 路徑，搭配 WebSearch 並行） |
| `.claude/agents/vault-evaluator.md` | — | 稽核 vault 規則違規 |
| `.claude/agents/vault-fixer.md` | — | 自動修正稽核結果 |

**Slash Commands**

| 檔案 | 全域路徑 | 用途 |
|------|---------|------|
| `.claude/commands/ob.md` | `~/.claude/commands/ob.md` | `/ob` 筆記操作（建檔 + 查詢，使用者唯一入口） |
| `.claude/commands/vault-check.md` | — | `/vault-check` 稽核迴圈 |

**Skills**

| 檔案 | 全域路徑 | 用途 |
|------|---------|------|
| `.claude/skills/vault-youtube-sync/` | `~/.claude/skills/vault-youtube-sync/` | YouTube 頻道影片轉 Obsidian 筆記 |
| `.claude/skills/vault-topic-moc/` | — | 多篇筆記整合為主題 MOC（含 generator/reviewer 迴圈）|

**建議安裝的全域 Skills（非本 repo 管理，需另行安裝至 `~/.claude/skills/`）**

以下 skill 與 vault 工作流深度整合，`/ob`、`vault-youtube-sync` 等流程會依賴它們，強烈建議安裝至全域：

| Skill | 用途 |
|-------|------|
| `obsidian-cli` | 透過 Obsidian CLI 讀寫 vault、搜尋筆記、操作 properties/tasks |
| `obsidian-markdown` | Obsidian Flavored Markdown 語法（wikilinks、callouts、frontmatter） |
| `obsidian-bases` | `.base` 檔案（Obsidian Bases）讀寫、views、filters、formulas |
| `defuddle` | 網頁轉 clean markdown，`vault-youtube-sync` 與 `Clippings/` 流程皆使用 |

未安裝時 `/ob` 仍可退回用 Read/Write 操作，但缺少 CLI / Bases / 網頁抓取的最佳路徑。

**建立 symlink（Windows，需開啟 Developer Mode 或以管理員執行）：**

```powershell
# 在 repo 根目錄執行
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\CLAUDE.md" -Target "$PWD\.claude\CLAUDE.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\agents\obsidian.md" -Target "$PWD\.claude\agents\obsidian.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\agents\vault-query.md" -Target "$PWD\.claude\agents\vault-query.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\commands\ob.md" -Target "$PWD\.claude\commands\ob.md"
```

**建立 symlink（Linux / macOS）：**

```bash
# 在 repo 根目錄執行
mkdir -p ~/.claude/agents ~/.claude/commands
ln -sf "$PWD/.claude/CLAUDE.md" ~/.claude/CLAUDE.md
ln -sf "$PWD/.claude/agents/obsidian.md" ~/.claude/agents/obsidian.md
ln -sf "$PWD/.claude/agents/vault-query.md" ~/.claude/agents/vault-query.md
ln -sf "$PWD/.claude/commands/ob.md" ~/.claude/commands/ob.md
```

觸發方式：
- 對話中提到「ob」、「建立筆記」、「找筆記」→ 啟用 `obsidian` agent（建檔自己處理、查詢委派 `vault-query`）
- 技術/知識性問題 → 依 `.claude/CLAUDE.md` 協議自動並行呼叫 `vault-query` + WebSearch
- `/ob <需求>` → 使用者唯一入口，涵蓋建檔與查詢

## Vault 稽核工作流

`/vault-check` 指令會對 `content/` 執行 vault 規則稽核與自動修正迴圈：

- `vault-evaluator` agent：依 `content/CLAUDE.md` 規則掃描違規與內容錯誤
- `vault-fixer` agent：接收違規清單對 `content/` 執行自動修正
- 修正在獨立 git branch 上進行，最後交用戶審核

## 評估中：搜尋方式比較（WIP）

比較兩種 vault 搜尋方式：**Read/Glob/Grep**（檔案系統）vs **Obsidian CLI**（`obsidian search:context`）。

**測試結論（2026-04-20）：Read/Glob/Grep 組合 100% 覆蓋 Obsidian CLI 搜尋結果，還快約 9 倍。**

量測數據（vault 122 篇 .md，Windows Git Bash）：

| 關鍵字 | Obsidian CLI | Read/Glob/Grep | 備註 |
|--------|-------------|----------------|------|
| claude-code | 575ms / 61 檔 | 30ms / 33 檔 | Grep 漏檔名匹配 |
| claude-code（Grep + Glob 檔名） | — | 66ms / 61 檔 | 與 Obsidian 完全一致 |
| MCP | 581ms / 29 檔 | 33ms / 29 檔 | 覆蓋率相同 |
| skill | 564ms / 44 檔 | 31ms / 44 檔 | 覆蓋率相同 |
| 七層次 | 572ms / 0 檔 | 31ms / 0 檔 | 兩者皆字串比對，無語義搜尋 |

Obsidian CLI 固定成本約 570ms（PowerShell 啟動 ~200ms + CLI 啟動 ~400ms），vault 再大差距不變。唯一實質優勢是檔名 case-insensitive 匹配，補一個 `Glob content/**/*<關鍵字>*.md` 即可等效。

## Vault 作為 Claude Code 資料來源

Vault 同時作為 Claude Code 的優質參考資料來源，與 WebSearch 互補並行：

- **協議**：`.claude/CLAUDE.md`（symlink 至 `~/.claude/CLAUDE.md`）定義 Vault + Web 並行查詢流程
- **路徑解析**：`vault-query` 會先動態解析本機 vault 根目錄（常見為 `~/code/obsidian-memory/content/`），再進行查詢
- **查詢 agent**：`.claude/agents/vault-query.md`（Read/Glob/Grep + 僅限唯讀用途的 Bash），三層搜尋 master-index → tag → 正文 Grep
- **path 契約**：`vault-query` 對外回傳的 `path` 一律正規化為 repo-relative 的 `content/...`
- **手動查詢**：`/ob 找 <主題>` 委派 `obsidian` agent → 再委派 `vault-query`，不做 WebSearch
- **自動觸發**：技術/知識性提問時，依 CLAUDE.md 協議自動並行呼叫 vault-query + WebSearch，綜合雙來源答覆
- **唯讀約束**：vault-query agent 不具 Write/Edit 工具；若需 Bash 也僅限 path discovery 與 grep/cat/find 等唯讀命令；建檔一律由使用者用 `/ob` 手動觸發
