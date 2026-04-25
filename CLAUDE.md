# CLAUDE.md

**本檔涵蓋**：repo 工程層——專案架構、Quartz 部署、agent/command/skill 清單、symlink 配置。
**不涵蓋**：Vault 內容規則（卡片盒哲學、frontmatter schema、tag/命名、敏感資料）→ 見 [`content/CLAUDE.md`](content/CLAUDE.md)。

**判斷規則寫哪份**：
- 摸 `content/` 會爆炸的（筆記結構、寫入前檢查） → `content/CLAUDE.md`
- 碰 Quartz / scripts / 部署 / agent 配置會爆炸的 → 本檔

## 專案概覽

Obsidian 個人知識庫，以 [Quartz 4](https://quartz.jzhao.xyz/) 發佈至 `ob.bugloop.com`。Vault 內容放在 `content/`，Quartz 框架程式碼在 `quartz/`。

此 repo 由三層構成，修改時先判斷變更屬於哪一層再動：

- **Vault 層**（`content/`）— 筆記本體，規則見 `content/CLAUDE.md`
- **發佈層**（`quartz/`、`quartz.config.ts`、`quartz.layout.ts`、`.github/workflows/`）— Quartz 建置與 GitHub Pages 部署
- **工作流層**（`.claude/` + `scripts/`）— agents（`vault-writer` / `vault-query` / `vault-auditor`）、commands（`/ob`、`/vault-check`）、skills（`vault-youtube-sync`、`vault-topic-moc`）、Node 稽核腳本。`.claude/` 可 symlink 至 `~/.claude/` 跨專案使用

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

- `content/` — Obsidian vault（筆記、模板），Quartz 從此目錄讀取 Markdown 建站；入口索引 `content/master-index.md`
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

## Vault 規則載入

Vault 內容規則（寫入前 Checklist、frontmatter schema、tag/命名、敏感資料等）由子模組規範載入；查詢 vault 時先讀 [`content/master-index.md`](content/master-index.md)。

- @content/CLAUDE.md

## Claude Code Agent 與指令

此 repo 統一管理 Obsidian 相關的 Claude Code 設定。部分透過 symlink 掛載至全域（僅 `/ob` 相關），讓跨專案可用；其餘綁本 repo。

依作用分組。「全域路徑」有值 = 需 symlink 掛全域（跨專案可用），`—` = 僅本 repo 生效。

### 1. 筆記操作（`/ob` 流程）

使用者唯一入口。`/ob <需求>` 或對話中自然提到「建立筆記」、「找筆記」，主 agent 依語意分派：

- 建檔（「建立」、「記一下」、「寫一篇」）→ `vault-writer`
- 查詢（「找」、「搜尋」、「有沒有」、「查」）→ `vault-query`

| 檔案                             | 類型    | 全域路徑                           | 用途                               |
| -------------------------------- | ------- | ---------------------------------- | ---------------------------------- |
| `.claude/commands/ob.md`         | Command | `~/.claude/commands/ob.md`         | `/ob` 入口，依語意分派             |
| `.claude/agents/vault-writer.md` | Agent   | `~/.claude/agents/vault-writer.md` | 寫入：建檔、append、改 frontmatter |
| `.claude/agents/vault-query.md`  | Agent   | `~/.claude/agents/vault-query.md`  | 唯讀查詢：三層搜尋回 JSON          |

### 2. Vault 稽核修正（`/vault-check` 流程）

兩段分工、零重疊：**Script 管格式與敏感資料硬掃（硬規則自動修 + high-precision 敏感資料 flag），Subagent 管語意（建議不改檔）**。command 串接兩段。全程綁本 repo，不需掛全域。

| 檔案                              | 類型        | 全域路徑 | 用途                                                                                                                                          |
| --------------------------------- | ----------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `.claude/commands/vault-check.md` | Command     | —        | `/vault-check` orchestrator：git 前置檢查 → 跑 script → 呼叫 subagent → 合併總結                                                              |
| `scripts/vault-check.mjs`         | Node script | —        | 硬規則自動修（檔名、frontmatter 結構、日期 normalize）＋ high-precision 敏感資料硬掃（只 flag 不修，命中 exit non-zero，作為 CI 最後一道防線） |
| `scripts/vault-schema.mjs`        | Node module | —        | Zod schema 與欄位順序／白名單定義，**硬規則變更改這裡**                                                                                       |
| `.claude/agents/vault-auditor.md` | Agent       | —        | 語意層稽核（wikilink 斷鏈、完整敏感資料、tag 一致性、缺 title/created/tags、parse error），唯讀只 flag 不改檔                                 |

### 3. 批次筆記工作流（Skills）

整批處理特定來源的筆記。手動在本 repo 內觸發，不掛全域。

| 檔案                                 | 類型  | 全域路徑 | 用途                                              |
| ------------------------------------ | ----- | -------- | ------------------------------------------------- |
| `.claude/skills/vault-youtube-sync/` | Skill | —        | YouTube 頻道影片轉 Obsidian 筆記                  |
| `.claude/skills/vault-topic-moc/`    | Skill | —        | 多篇筆記整合為主題 MOC（generator/reviewer 迴圈） |

### 4. 建議安裝的第三方 Skills（非本 repo 管理，需另行安裝至 `~/.claude/skills/`）

以下 skill 與 vault 工作流深度整合，`/ob` 等流程會依賴它們，強烈建議安裝至全域：

| Skill               | 服務於     | 用途                                                                   |
| ------------------- | ---------- | ---------------------------------------------------------------------- |
| `obsidian-cli`      | 筆記操作   | 透過 Obsidian CLI 讀寫 vault、搜尋筆記、操作 properties/tasks          |
| `obsidian-markdown` | 筆記操作   | Obsidian Flavored Markdown 語法（wikilinks、callouts、frontmatter）    |
| `obsidian-bases`    | 筆記操作   | `.base` 檔案（Obsidian Bases）讀寫、views、filters、formulas           |
| `defuddle`          | 批次工作流 | 網頁轉 clean markdown，`vault-youtube-sync` 與 `Clippings/` 流程皆使用 |

未安裝時 `/ob` 仍可退回用 Read/Write 操作，但缺少 CLI / Bases / 網頁抓取的最佳路徑。

### Symlink 安裝

把 `/ob` 相關設定掛到 `~/.claude/` 讓跨專案可用。Windows / macOS / Linux 指令見 [README.md](README.md) 的「全域掛載」段。

## Vault 作為 Claude Code 資料來源

Vault 同時作為 Claude Code 的參考資料來源，與 WebSearch 互補並行：

- **協議**：觸發條件、綜合原則、引用格式寫在全域 `~/.claude/CLAUDE.md` 的 `## Obsidian` 段；技術/知識性提問會自動並行呼叫 `vault-query` + WebSearch
- **搜尋工具**：搜 vault 一律用 `Grep` + `Glob content/**/*<關鍵字>*.md`，不要呼叫 Obsidian CLI 的 `search:context`（慢約 9 倍且覆蓋率較低）
- **跨機器路徑**：各 agent 一律讀 `$OBSIDIAN_VAULT_ROOT`，**必須**在**全域** `~/.claude/settings.json` 的 `env` 段注入絕對路徑（不是 repo 內的 settings）——因為 `/ob` 相關設定已 symlink 到全域供跨專案使用，env 放 repo 內的 settings 只在本 repo 工作時可見，從其他專案呼叫 `/ob` 會讀不到。未設或無效直接中止，不做猜測 fallback。path 契約詳見各 agent 檔。設定時可直接請 Claude Code 用 `update-config` skill 處理，會自動 merge 既有 `env` 不覆蓋
