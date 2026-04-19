# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概覽

Obsidian 個人知識庫，以 [Quartz 4](https://quartz.jzhao.xyz/) 發佈至 `ob.bugloop.com`。Vault 內容放在 `content/`，Quartz 框架程式碼在 `quartz/`。

## 常用指令

```bash
npx quartz build --serve         # 本地預覽（localhost:8080）
npm run check                    # TypeScript 型別檢查 + Prettier 格式驗證
npm run format                   # 自動格式化
```

## 架構

- `content/` — Obsidian vault（筆記、日記、模板），Quartz 從此目錄讀取 Markdown 建站
- `quartz/` — Quartz 框架原始碼（不需修改）
- `quartz.config.ts` — 站台設定（外觀、plugins、ignorePatterns）
- `quartz.layout.ts` — 版面配置
- `.github/workflows/deploy.yml` — push 到 `main` 自動建置並部署至 GitHub Pages

## Quartz 重要行為

- `ignorePatterns` 包含 `private`、`Templates`、`.obsidian`、`CLAUDE.md`、`Inbox`、`YouTube`、`Clippings`，這些不會發佈至網站
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

## Claude Code Agent 與指令

此 repo 統一管理 Obsidian 相關的 Claude Code 設定，透過 symlink 掛載至全域，讓這些設定在任何專案目錄都能生效。

| 檔案 | 全域路徑 | 用途 |
|------|---------|------|
| `.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` | 全域協議：Vault + WebSearch 並行查詢 |
| `.claude/agents/obsidian.md` | `~/.claude/agents/obsidian.md` | Obsidian 筆記操作 agent（讀寫） |
| `.claude/agents/vault-query.md` | `~/.claude/agents/vault-query.md` | Vault 唯讀查詢 agent（動態解析 vault 路徑，搭配 WebSearch 並行） |
| `.claude/agents/vault-evaluator.md` | — | 稽核 vault 規則違規 |
| `.claude/agents/vault-fixer.md` | — | 自動修正稽核結果 |
| `.claude/commands/ob.md` | `~/.claude/commands/ob.md` | `/ob` 筆記操作 |
| `.claude/commands/vault.md` | `~/.claude/commands/vault.md` | `/vault` 只查 vault（不做 WebSearch） |
| `.claude/commands/vault-check.md` | — | `/vault-check` 稽核迴圈 |
| `.claude/skills/youtube-channel-to-notes/` | `~/.claude/skills/youtube-channel-to-notes/` | YouTube 頻道影片轉 Obsidian 筆記 |

**建立 symlink（Windows，需開啟 Developer Mode 或以管理員執行）：**

```powershell
# 在 repo 根目錄執行
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\CLAUDE.md" -Target "$PWD\.claude\CLAUDE.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\agents\obsidian.md" -Target "$PWD\.claude\agents\obsidian.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\agents\vault-query.md" -Target "$PWD\.claude\agents\vault-query.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\commands\ob.md" -Target "$PWD\.claude\commands\ob.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\commands\vault.md" -Target "$PWD\.claude\commands\vault.md"
```

**建立 symlink（Linux / macOS）：**

```bash
# 在 repo 根目錄執行
mkdir -p ~/.claude/agents ~/.claude/commands
ln -sf "$PWD/.claude/CLAUDE.md" ~/.claude/CLAUDE.md
ln -sf "$PWD/.claude/agents/obsidian.md" ~/.claude/agents/obsidian.md
ln -sf "$PWD/.claude/agents/vault-query.md" ~/.claude/agents/vault-query.md
ln -sf "$PWD/.claude/commands/ob.md" ~/.claude/commands/ob.md
ln -sf "$PWD/.claude/commands/vault.md" ~/.claude/commands/vault.md
```

觸發方式：
- 對話中提到「ob」、「日記」、「daily」、「記一下」、「建立筆記」、「找筆記」→ 啟用 `obsidian` agent
- 技術/知識性問題 → 依 `.claude/CLAUDE.md` 協議自動並行呼叫 `vault-query` + WebSearch
- `/vault <問題>` → 只查 vault，不做 WebSearch

## Vault 稽核工作流

`/vault-check` 指令會對 `content/` 執行 vault 規則稽核與自動修正迴圈：

- `vault-evaluator` agent：依 `content/CLAUDE.md` 規則掃描違規與內容錯誤
- `vault-fixer` agent：接收違規清單對 `content/` 執行自動修正
- 修正在獨立 git branch 上進行，最後交用戶審核

## Vault 作為 Claude Code 資料來源

Vault 同時作為 Claude Code 的優質參考資料來源，與 WebSearch 互補並行：

- **協議**：`.claude/CLAUDE.md`（symlink 至 `~/.claude/CLAUDE.md`）定義 Vault + Web 並行查詢流程
- **路徑解析**：`vault-query` 會先動態解析本機 vault 根目錄（常見為 `~/code/obsidian-memory/content/`），再進行查詢
- **查詢 agent**：`.claude/agents/vault-query.md`（Read/Glob/Grep + 僅限唯讀用途的 Bash），三層搜尋 master-index → tag → 正文 Grep
- **path 契約**：`vault-query` 對外回傳的 `path` 一律正規化為 repo-relative 的 `content/...`
- **手動指令**：`/vault <問題>` 只查 vault，不做 WebSearch
- **自動觸發**：技術/知識性提問時，依 CLAUDE.md 協議自動並行呼叫 vault-query + WebSearch，綜合雙來源答覆
- **唯讀約束**：vault-query agent 不具 Write/Edit 工具；若需 Bash 也僅限 path discovery 與 grep/cat/find 等唯讀命令；建檔一律由使用者用 `/ob` 手動觸發
