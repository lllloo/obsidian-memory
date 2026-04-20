# obsidian-memory

個人知識庫，以 [Obsidian](https://obsidian.md/) 管理筆記，透過 [Quartz 4](https://quartz.jzhao.xyz/) 發佈至 [ob.bugloop.com](https://ob.bugloop.com)。

## 前置需求

- [Obsidian](https://obsidian.md/) 桌面版
- Obsidian CLI plugin（在 Obsidian 內安裝）
- Node.js 22+（本地預覽用）
- [Claude Code](https://claude.ai/code)（AI 筆記助手，選用）

## Vault 結構

```
content/
├── Cards/      # 單篇筆記
├── Topics/     # MOC 與主題資料夾
├── YouTube/    # YouTube 影片摘要
└── Clippings/  # 網頁剪貼
```

詳細規則見 [content/CLAUDE.md](content/CLAUDE.md)。

## 開發指令

```bash
npx quartz build --serve     # 本地預覽（http://localhost:8080）
npm run check                # TypeScript 型別檢查 + Prettier 格式驗證
npm run format               # 自動格式化
```

## Claude Code 整合

此 repo 統一管理 Obsidian 相關的 Claude Code 設定（agents、slash commands、skills），透過 symlink 掛載至全域後，在任何專案目錄都能使用。

### 設定清單

依作用分組。「全域路徑」有值 = 需 symlink 掛全域（跨專案可用），`—` = 僅本 repo 生效。

> Vault + WebSearch 並行查詢協議寫在全域 `~/.claude/CLAUDE.md` 的 `## Obsidian` 段，不另存檔。

#### 1. 筆記操作（`/ob` 流程）

使用者唯一入口。command 依語意把需求分派給寫入 agent 或唯讀查詢 agent。

| 檔案 | 類型 | 全域路徑 | 用途 |
|------|------|---------|------|
| `.claude/commands/ob.md` | Command | `~/.claude/commands/ob.md` | `/ob` 入口，依語意分派 |
| `.claude/agents/vault-writer.md` | Agent | `~/.claude/agents/vault-writer.md` | 寫入：建檔、append、改 frontmatter |
| `.claude/agents/vault-query.md` | Agent | `~/.claude/agents/vault-query.md` | 唯讀查詢：三層搜尋回 JSON |

#### 2. Vault 稽核修正（`/vault-check` 流程）

稽核 `content/` 規則違規並自動修正，全程綁本 repo（需讀 `content/` 與 git 操作），不需掛全域。

| 檔案 | 類型 | 全域路徑 | 用途 |
|------|------|---------|------|
| `.claude/commands/vault-check.md` | Command | — | `/vault-check` orchestrator |
| `.claude/agents/vault-evaluator.md` | Agent | — | 掃描違規，輸出 JSON 清單 |
| `.claude/agents/vault-fixer.md` | Agent | — | 接收清單自動修正 `content/` |

#### 3. 批次筆記工作流（Skills）

整批處理特定來源的筆記。手動在本 repo 內觸發，不掛全域。

| 檔案 | 類型 | 全域路徑 | 用途 |
|------|------|---------|------|
| `.claude/skills/vault-youtube-sync/` | Skill | — | YouTube 頻道影片轉 Obsidian 筆記 |
| `.claude/skills/vault-topic-moc/` | Skill | — | 多篇筆記整合為主題 MOC（generator/reviewer 迴圈） |

#### 4. 建議安裝的第三方 Skills（非本 repo 管理）

以下 skill 與 vault 工作流深度整合，`/ob` 等流程會依賴它們，建議另行安裝至 `~/.claude/skills/`：

| Skill | 服務於 | 用途 |
|-------|-------|------|
| `obsidian-cli` | 筆記操作 | 透過 Obsidian CLI 讀寫 vault、搜尋筆記、操作 properties/tasks |
| `obsidian-markdown` | 筆記操作 | Obsidian Flavored Markdown 語法（wikilinks、callouts、frontmatter） |
| `obsidian-bases` | 筆記操作 | `.base` 檔案（Obsidian Bases）讀寫、views、filters、formulas |
| `defuddle` | 批次工作流 | 網頁轉 clean markdown，`vault-youtube-sync` 與 `Clippings/` 流程皆使用 |

未安裝時 `/ob` 仍可退回用 Read/Write 操作，但缺少 CLI / Bases / 網頁抓取的最佳路徑。

### 觸發方式

- **筆記操作（唯一入口）**：`/ob <需求>` 依語意分派 — 建檔 → `vault-writer` agent，查詢 → `vault-query` agent。對話中自然提到「建立筆記」、「找筆記」效果等同
- **知識查詢（預設自動）**：技術/知識性提問會依全域 `~/.claude/CLAUDE.md` 的 Obsidian 段規則自動並行呼叫 `vault-query` + WebSearch，綜合雙來源答覆
- **稽核修正**：`/vault-check` → 用 `vault-evaluator` + `vault-fixer` 迴圈掃描並自動修正，修正在獨立 git branch 上進行

### 全域掛載

這個 repo 的 `.claude/` 是**本體**，symlink 到 `~/.claude/` 後，Claude Code 在**任何專案目錄**都能叫到 `/ob`、vault-query agent 等設定。改 repo 內的檔案會即時同步到全域，不需手動複製。

- **不做 symlink**：仍可用，但 command / agent 只在本 repo 目錄內生效
- **做了 symlink**：跨專案可用，`/ob` 到處能叫
- **範圍差異**：上方表格「全域路徑」有值的才掛全域；`—` 的（如 `/vault-check`、`vault-evaluator`、`vault-fixer`）綁本 repo（需讀 `content/` 與 git 操作），不需掛
- **前置條件**：Windows 需開啟 Developer Mode 或以管理員身分執行

**Windows（需開啟 Developer Mode 或以管理員執行）：**

```powershell
# 在 repo 根目錄執行
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\agents\vault-writer.md" -Target "$PWD\.claude\agents\vault-writer.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\agents\vault-query.md" -Target "$PWD\.claude\agents\vault-query.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\commands\ob.md" -Target "$PWD\.claude\commands\ob.md"
```

**macOS / Linux：**

```bash
# 在 repo 根目錄執行
mkdir -p ~/.claude/agents ~/.claude/commands
ln -sf "$PWD/.claude/agents/vault-writer.md" ~/.claude/agents/vault-writer.md
ln -sf "$PWD/.claude/agents/vault-query.md" ~/.claude/agents/vault-query.md
ln -sf "$PWD/.claude/commands/ob.md" ~/.claude/commands/ob.md
```

## 發佈

push 到 `main` 後透過 `.github/workflows/deploy.yml` 自動建置並部署至 GitHub Pages。此 vault 為**公開發佈**，commit 前請確認不含敏感資料（API key、密碼、個人隱私等）。
