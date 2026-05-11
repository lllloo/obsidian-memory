# obsidian-memory

個人知識庫，以 [Obsidian](https://obsidian.md/) 管理筆記，透過 [Quartz 4](https://quartz.jzhao.xyz/) 發佈至 [ob.bugloop.com](https://ob.bugloop.com)。

這個 repo 由三層構成，職責分離：

- **Obsidian vault**（`content/`）— 筆記本體，Obsidian 桌面版的編輯目標
- **Quartz 4 發佈層**（`quartz/` + `quartz.config.ts`）— 將 `content/` 靜態化為 `ob.bugloop.com`
- **Claude Code 工作流層**（`.claude/` symlink 自 `.agents/skills/`，後者為實際維護來源）— skills，管理筆記建立、查詢、稽核；`/ob` 可 symlink 至 `~/.claude/skills/` 跨專案使用

三層各有 `CLAUDE.md`：全域（`~/.claude/`）、repo（本檔）、vault（`content/CLAUDE.md`），規則按作用域分層。

## 前置需求

- [Obsidian](https://obsidian.md/) 桌面版
- Obsidian CLI plugin（在 Obsidian 內安裝）
- Node.js 22+（本地預覽用）
- [Claude Code](https://claude.ai/code)（AI 筆記助手，選用；跨專案使用 `/ob` 時必須設 `OBSIDIAN_VAULT_ROOT`，見下方 [Vault 路徑設定](#vault-路徑設定跨機器)；其他 repo-local skill 用 cwd 不需 env）

## Vault 結構

```
content/
├── Inbox/          # 待消化暫存（不發佈）
│   ├── YouTube/    # YouTube 影片摘要
│   ├── Updates/    # 官方 changelog / GitHub 高信任更新
│   └── Clippings/  # 網頁剪貼
├── Cards/          # 未歸屬的完整概念 Cards
└── Topics/         # 已歸檔主題資料夾（含 MOC）
```

詳細規則見 [content/CLAUDE.md](content/CLAUDE.md)。

## 開發指令

```bash
npx quartz build --serve     # 本地預覽（http://localhost:8080）
npm run check                # TypeScript 型別檢查 + Prettier + skill symlink 驗證
npm run format               # 自動格式化
npm run test                 # 執行所有測試（Node.js 內建 test runner，tsx --test）
npm run vault:check          # 稽核 content/ frontmatter 與檔名（只報告）
npm run vault:fix            # 稽核並自動修正（/vault-check 內部呼叫）
```

## Claude Code 整合

此 repo 的 `.claude/` 管理 Obsidian 相關的 skills（已全 skill 化，不再使用 slash command；skill 內子流程以 `general-purpose` subagent + references prompt 執行，不依賴命名 agent）。主要使用者入口：

- **`/ob <需求>`** — 筆記建立與查詢（依語意分派到建檔流程 `references/write.md` 或查詢流程 `references/query.md`，皆經 general-purpose subagent）
- **`/vault-check`** — vault frontmatter 與語意稽核（script 自動修 + audit reference 經 general-purpose subagent 給建議）
- **`/vault-youtube-sync`、`/vault-distill`、`/vault-updates-daily`、`/vault-reddit-daily`** — 批次工作流

另有一條自動行為：技術／知識性提問時，會自動並行呼叫查詢流程（`/ob` skill + `references/query.md`）+ WebSearch 綜合答覆（協議在全域 `~/.claude/CLAUDE.md` 的 `## Obsidian` 段）。

完整 skill 清單、工作流協議、第三方 Skill 依賴見 [CLAUDE.md](CLAUDE.md)。

### 全域掛載（讓 `/ob` 跨專案可用）

把 `.claude/skills/ob/` symlink 到 `~/.claude/skills/` 後，Claude Code 在任何專案目錄都能叫到 `/ob`。改 repo 內的檔案會即時同步到全域，不需手動複製。

- 不做 symlink 也能用，但 skill 只在本 repo 目錄內生效
- `/vault-check` 與其他批次 skills 綁本 repo（需讀 `content/` 與 git），不需掛全域

**Windows（需開啟 Developer Mode 或以管理員執行）：**

```powershell
# 在 repo 根目錄執行
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\ob" -Target "$PWD\.claude\skills\ob"
```

**macOS / Linux：**

```bash
# 在 repo 根目錄執行
mkdir -p ~/.claude/skills
ln -sf "$PWD/.claude/skills/ob" ~/.claude/skills/ob
```

### `/ob` Vault 路徑設定（跨專案）

**為什麼只有 `/ob` 需要 env**：因為 `/ob` 要 symlink 到 `~/.claude/skills/`，讓你從其他專案的 Claude Code session 也能呼叫 — 此時 cwd 不在本 repo，沒辦法用相對路徑找到 vault，必須靠 env 解析。其他 skill 沒掛全域、永遠 repo-local 觸發（cwd 必為 repo root），用 `content/...` 相對路徑直接讀寫即可，**不依賴此變數**。

啟用 `/ob` 跨專案使用前，**必須**在每台機器的 `~/.claude/settings.json` 注入絕對路徑：

> ⚠️ 此 env **僅供 `/ob` 使用**；其他 repo-local skill 看不到也不需要它。

```json
{
  "env": {
    "OBSIDIAN_VAULT_ROOT": "/absolute/path/to/obsidian-memory/content"
  }
}
```

**Windows 用正斜線**（例 `C:/path/to/obsidian-memory/content`），不要用反斜線——Git Bash 會把反斜線當 escape 吃掉。

> **Tip**：在 Claude Code 內可直接請它用 `update-config` skill 設定（例：「用 update-config 加 `OBSIDIAN_VAULT_ROOT=/絕對路徑/content` 到全域 settings」），它會自動 merge 既有 `env` 欄位，不會覆蓋其他設定。

未設定或路徑無效時，`/ob` 會直接中止並回報錯誤，不做猜測 fallback——避免寫到錯誤位置或回傳錯誤搜尋結果。設定後需重啟 Claude Code session 才會載入。

## Web Clipper 模板

[Obsidian Web Clipper](https://obsidian.md/clipper) 是官方瀏覽器擴充套件，把網頁抓成 Markdown 存進 vault。`.clipper/vault-clipper.json` 是此 vault 使用的 template 匯入檔，定義抓取後的檔名、frontmatter（`title`、`source`、`published`、`created`、`tags`）與儲存路徑。抓下來後跑 `/vault-check` 會把非白名單欄位（例如 clipper 偶爾帶入的 `author`、`description`）自動清掉。

- **抓取路徑**：`Inbox/Clippings/`（不發佈，待消化後依 `content/CLAUDE.md` 的吸收型卡片盒流程歸檔）
- **預設 tag**：`clippings`

**匯入方式**：開啟 Chrome / Firefox Web Clipper 擴充套件 → Settings → Templates → Import → 選 `.clipper/vault-clipper.json`。

修改此檔後記得 commit，跨機器才能同步同一份抓取規則。

## 發佈

push 到 `main` 後透過 `.github/workflows/deploy.yml` 自動建置並部署至 GitHub Pages。此 vault 為**公開發佈**，commit 前請確認不含敏感資料（API key、密碼、個人隱私等）。
