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
├── Clippings/  # 網頁剪貼
└── Templates/  # 筆記模板
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

| 檔案 | 全域路徑 | 用途 |
|------|---------|------|
| `.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` | 全域協議：Vault + WebSearch 並行查詢 |
| `.claude/agents/obsidian.md` | `~/.claude/agents/obsidian.md` | Obsidian 筆記操作 agent（讀寫） |
| `.claude/agents/vault-query.md` | `~/.claude/agents/vault-query.md` | Vault 唯讀查詢 agent |
| `.claude/agents/vault-evaluator.md` | — | 稽核 vault 規則違規 |
| `.claude/agents/vault-fixer.md` | — | 自動修正稽核結果 |
| `.claude/commands/ob.md` | `~/.claude/commands/ob.md` | `/ob` 筆記操作 |
| `.claude/commands/vault.md` | `~/.claude/commands/vault.md` | `/vault` 只查 vault（不做 WebSearch） |
| `.claude/commands/vault-check.md` | — | `/vault-check` 稽核迴圈 |
| `.claude/skills/youtube-channel-to-notes/` | `~/.claude/skills/youtube-channel-to-notes/` | YouTube 頻道影片轉 Obsidian 筆記 |

### 觸發方式

- **筆記操作**：對話中提到「ob」、「建立筆記」、「找筆記」→ 啟用 `obsidian` agent，或用 `/ob <需求>`
- **知識查詢（預設）**：技術/知識性提問會依 `.claude/CLAUDE.md` 協議自動並行呼叫 `vault-query` + WebSearch，綜合雙來源答覆
- **只查 vault**：`/vault <問題>` → 不做 WebSearch
- **稽核修正**：`/vault-check` → 用 `vault-evaluator` + `vault-fixer` 迴圈掃描並自動修正，修正在獨立 git branch 上進行

### 全域掛載

**Windows（需開啟 Developer Mode 或以管理員執行）：**

```powershell
# 在 repo 根目錄執行
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\CLAUDE.md" -Target "$PWD\.claude\CLAUDE.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\agents\obsidian.md" -Target "$PWD\.claude\agents\obsidian.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\agents\vault-query.md" -Target "$PWD\.claude\agents\vault-query.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\commands\ob.md" -Target "$PWD\.claude\commands\ob.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\commands\vault.md" -Target "$PWD\.claude\commands\vault.md"
```

**macOS / Linux：**

```bash
# 在 repo 根目錄執行
mkdir -p ~/.claude/agents ~/.claude/commands
ln -sf "$PWD/.claude/CLAUDE.md" ~/.claude/CLAUDE.md
ln -sf "$PWD/.claude/agents/obsidian.md" ~/.claude/agents/obsidian.md
ln -sf "$PWD/.claude/agents/vault-query.md" ~/.claude/agents/vault-query.md
ln -sf "$PWD/.claude/commands/ob.md" ~/.claude/commands/ob.md
ln -sf "$PWD/.claude/commands/vault.md" ~/.claude/commands/vault.md
```

## 發佈

push 到 `main` 後透過 `.github/workflows/deploy.yml` 自動建置並部署至 GitHub Pages。此 vault 為**公開發佈**，commit 前請確認不含敏感資料（API key、密碼、個人隱私等）。
