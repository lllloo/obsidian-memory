# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概覽

Obsidian 個人知識庫，以 [Quartz 4](https://quartz.jzhao.xyz/) 發佈至 `ob.bugloop.com`。Vault 內容放在 `content/`，Quartz 框架程式碼在 `quartz/`。

此 repo 由三層構成，修改時先判斷變更屬於哪一層再動：

- **Vault 層**（`content/`）— 筆記本體。規則寫在 `content/CLAUDE.md`（命名、frontmatter、tag、敏感資料）
- **發佈層**（`quartz/`、`quartz.config.ts`、`quartz.layout.ts`、`.github/workflows/`）— Quartz 建置與 GitHub Pages 部署
- **工作流層**（`.claude/` + `scripts/`）— agents（`vault-writer` / `vault-query`）、commands（`/ob`、`/vault-check`）、skills（`vault-youtube-sync`、`vault-topic-moc`）、Node 稽核腳本（`scripts/vault-check.mjs`）。`.claude/` 可 symlink 至 `~/.claude/` 跨專案使用

CLAUDE.md 依作用域分三層：全域（`~/.claude/CLAUDE.md`）→ repo（本檔）→ vault（`content/CLAUDE.md`）。規則放到最窄的作用域即可。

## 常用指令

需要 Node.js 22+、npm 10.9.2+（`package.json` engines）。

```bash
npx quartz build --serve         # 本地預覽（localhost:8080）
npm run check                    # TypeScript 型別檢查 + Prettier 格式驗證
npm run format                   # 自動格式化
npm run vault:check              # 稽核 content/ 的 frontmatter 與檔名（只報告）
npm run vault:fix                # 稽核並自動修正（/vault-check 內部呼叫這個）
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

- `ignorePatterns` 包含 `private`、`.obsidian`、`CLAUDE.md`、`Inbox`（整個 `Inbox/` 含 YouTube 與 Clippings 都不發佈）
- frontmatter 加 `draft: true` 的筆記會被 `RemoveDrafts` plugin 過濾，不發佈
- 日期優先順序：frontmatter → git → filesystem（`CreatedModifiedDate` plugin）
- Plugin pipeline：transformers（解析 Markdown）→ filters（篩選頁面）→ emitters（產生 HTML/靜態資源）
- Wikilink 以 `shortest` 解析（`CrawlLinks`），連結目標需在 `content/` 下存在對應檔案

## Obsidian Vault 規則

筆記結構、命名規則、tag 格式、安全規範等詳見 [`content/CLAUDE.md`](content/CLAUDE.md)。

查詢 vault 知識時，先讀 [`content/master-index.md`](content/master-index.md) 確認資料夾與 tag 分布，再導航到對應位置。

請遵循以下子模組的規範：
- @content/CLAUDE.md

## Claude Code Agent 與指令

此 repo 統一管理 Obsidian 相關的 Claude Code 設定，透過 symlink 掛載至全域，讓這些設定在任何專案目錄都能生效。

依作用分組。「全域路徑」有值 = 需 symlink 掛全域（跨專案可用），`—` = 僅本 repo 生效。

### 1. 筆記操作（`/ob` 流程）

使用者唯一入口。command 依語意把需求分派給寫入 agent 或唯讀查詢 agent。

| 檔案 | 類型 | 全域路徑 | 用途 |
|------|------|---------|------|
| `.claude/commands/ob.md` | Command | `~/.claude/commands/ob.md` | `/ob` 入口，依語意分派 |
| `.claude/agents/vault-writer.md` | Agent | `~/.claude/agents/vault-writer.md` | 寫入：建檔、append、改 frontmatter |
| `.claude/agents/vault-query.md` | Agent | `~/.claude/agents/vault-query.md` | 唯讀查詢：三層搜尋回 JSON |

### 2. Vault 稽核修正（`/vault-check` 流程）

稽核 `content/` 規則違規並自動修正。硬規則（frontmatter schema、檔名）由 Node + Zod 執行；command 負責前置 git 檢查與總結。全程綁本 repo，不需掛全域。

| 檔案 | 類型 | 全域路徑 | 用途 |
|------|------|---------|------|
| `.claude/commands/vault-check.md` | Command | — | `/vault-check` orchestrator：git 前置檢查、跑 Node script、印總結 |
| `scripts/vault-check.mjs` | Node script | — | 掃描 + 自動修正（可獨立跑 `npm run vault:check` / `vault:fix`） |
| `scripts/vault-schema.mjs` | Node module | — | Zod schema 與欄位順序／白名單定義，規則變更改這裡 |

### 3. 批次筆記工作流（Skills）

整批處理特定來源的筆記。手動在本 repo 內觸發，不掛全域。

| 檔案 | 類型 | 全域路徑 | 用途 |
|------|------|---------|------|
| `.claude/skills/vault-youtube-sync/` | Skill | — | YouTube 頻道影片轉 Obsidian 筆記 |
| `.claude/skills/vault-topic-moc/` | Skill | — | 多篇筆記整合為主題 MOC（generator/reviewer 迴圈） |

### 4. 建議安裝的第三方 Skills（非本 repo 管理，需另行安裝至 `~/.claude/skills/`）

以下 skill 與 vault 工作流深度整合，`/ob` 等流程會依賴它們，強烈建議安裝至全域：

| Skill | 服務於 | 用途 |
|-------|-------|------|
| `obsidian-cli` | 筆記操作 | 透過 Obsidian CLI 讀寫 vault、搜尋筆記、操作 properties/tasks |
| `obsidian-markdown` | 筆記操作 | Obsidian Flavored Markdown 語法（wikilinks、callouts、frontmatter） |
| `obsidian-bases` | 筆記操作 | `.base` 檔案（Obsidian Bases）讀寫、views、filters、formulas |
| `defuddle` | 批次工作流 | 網頁轉 clean markdown，`vault-youtube-sync` 與 `Clippings/` 流程皆使用 |

未安裝時 `/ob` 仍可退回用 Read/Write 操作，但缺少 CLI / Bases / 網頁抓取的最佳路徑。

**建立 symlink（Windows，需開啟 Developer Mode 或以管理員執行）：**

```powershell
# 在 repo 根目錄執行
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\agents\vault-writer.md" -Target "$PWD\.claude\agents\vault-writer.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\agents\vault-query.md" -Target "$PWD\.claude\agents\vault-query.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\commands\ob.md" -Target "$PWD\.claude\commands\ob.md"
```

**建立 symlink（Linux / macOS）：**

```bash
# 在 repo 根目錄執行
mkdir -p ~/.claude/agents ~/.claude/commands
ln -sf "$PWD/.claude/agents/vault-writer.md" ~/.claude/agents/vault-writer.md
ln -sf "$PWD/.claude/agents/vault-query.md" ~/.claude/agents/vault-query.md
ln -sf "$PWD/.claude/commands/ob.md" ~/.claude/commands/ob.md
```

觸發方式：
- `/ob <需求>` → 使用者唯一入口。command 依語意分派：
  - 建檔（「建立」、「記一下」、「寫一篇」）→ `vault-writer` agent
  - 查詢（「找」、「搜尋」、「有沒有」、「查」）→ `vault-query` agent
- 對話中自然提到「建立筆記」、「找筆記」→ 主 agent 依上述規則分派（效果等同 `/ob`）
- 技術/知識性問題 → 依全域 `~/.claude/CLAUDE.md` 的 Obsidian 段規則，自動並行呼叫 `vault-query` + WebSearch

## Vault 稽核工作流

`/vault-check` 指令會對 `content/` 執行 vault 規則稽核與自動修正：

- 由 `scripts/vault-check.mjs` 以 Zod schema（`scripts/vault-schema.mjs`）驗證 frontmatter 與檔名
- 可自動修：
  - `FILENAME_HAS_SPACE`（檔名含空格 → rename，壓縮連續 `-`、trim 頭尾 `-`）
  - `MISSING_REQUIRED_FIELD`（僅 `updated` 缺失 → 補今日）
  - `UNKNOWN_FIELD` / `EMPTY_OPTIONAL_FIELD`（白名單外欄位 / 選填空值 → 刪除）
  - `FIELD_ORDER`（欄位順序 → 重排）
  - `INVALID_VALUE`（僅 `created` / `updated` / `published` 日期格式可推斷時 → normalize 為 `YYYY-MM-DD`，如 `2026/04/01`、`2026.04.01`、`2026-4-1`）
- 偵測但不自動修（需手動）：
  - `INVALID_VALUE`（非 `YYYY-MM-DD` 日期、URL 格式錯、`parent` 非 wikilink 格式等；訊息會帶上實際值方便定位）
  - `MISSING_REQUIRED_FIELD`（`title` / `created` / `tags` 缺失）
  - `FRONTMATTER_PARSE_ERROR`（YAML 解析失敗）
  - `BROKEN_WIKILINK`（正文與 `parent` 的 wikilink 斷鏈；Quartz `shortest` 語義，code fence 內忽略）
  - `SENSITIVE_DATA`（API key / token / private key 等 high-precision regex；code fence 內忽略）
- 尚未實作：`MISPLACED_NOTE`（新筆記位置錯誤）— 規則由用戶自審
- command 不自動 commit，變更留 worktree 交用戶審核

**規則變更請改 `scripts/vault-schema.mjs` 的 Zod schema**（`FIELD_ORDER` 常數 + `frontmatterSchema` 物件），不要另寫規則。

## Vault 搜尋方式

搜尋 vault 一律用 `Grep` + `Glob content/**/*<關鍵字>*.md`，不要呼叫 Obsidian CLI 的 `search:context`（慢約 9 倍且覆蓋率較低）。

## Vault 作為 Claude Code 資料來源

Vault 同時作為 Claude Code 的優質參考資料來源，與 WebSearch 互補並行：

- **協議**：自動並行查詢流程（觸發條件、綜合原則、引用格式）寫在全域 `~/.claude/CLAUDE.md` 的 `## Obsidian` 段，供主 agent 每次對話載入
- **路徑解析**：`vault-query` 與 `vault-writer` 皆先動態解析本機 vault 根目錄。優先順序：`$OBSIDIAN_VAULT_ROOT`（建議在 `~/.claude/settings.local.json` 的 `env` 注入，跨機器獨立）→ `<cwd>/content` → Git 根 + `/content` → 舊候選清單
- **查詢 agent**：`.claude/agents/vault-query.md`（Read/Glob/Grep + 僅限唯讀用途的 Bash），三層搜尋 master-index → tag → 正文 Grep
- **path 契約**：`vault-query` 對外回傳的 `path` 一律正規化為 repo-relative 的 `content/...`
- **手動查詢**：`/ob 找 <主題>` 由 command 直接分派 `vault-query`，不做 WebSearch
- **自動觸發**：技術/知識性提問時，依全域 CLAUDE.md 規則自動並行呼叫 vault-query + WebSearch，綜合雙來源答覆
- **唯讀約束**：vault-query agent 不具 Write/Edit 工具；若需 Bash 也僅限 path discovery 與 grep/cat/find 等唯讀命令；建檔一律由使用者用 `/ob` 手動觸發

## 文件同步規則

**修改 `CLAUDE.md` 的 Claude Code 設定清單、symlink 指令、觸發方式、或 vault 協議時，必須同步更新 `README.md` 對應區塊**。兩者面向不同受眾（CLAUDE.md 給 Claude Code、README.md 給使用者），但資訊需一致。新增 agent / command / skill 時尤其要記得同步。

repo 根目錄的 `AGENTS.md` 是 `CLAUDE.md` 的 symlink（給非 Claude Code 的其他 agent 工具讀），改動會自動同步，不需手動複製。
