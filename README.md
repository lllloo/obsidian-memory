# Obsidian Memory Vault

個人 Obsidian vault，採 Karpathy [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 工作流：agent 讀不可變的 `raw/` 原料，漸進維護一套互聯的 `wiki/` 活知識庫。`Cards/`、`Topics/` 是使用者私人策展區，也是對外公開的層。公開版本在 [bugloop.com](https://bugloop.com)。

## 安裝與使用

```bash
git clone <repo-url> obsidian-memory
```

**Prerequisites**：

- [Obsidian](https://obsidian.md/) — 編輯與圖譜瀏覽
- Python 3（純 stdlib）— skill 腳本執行所需
- [Obsidian CLI](https://help.obsidian.md/cli)（選用）— 僅剩 `ob-write` 本地寫完後 `obsidian open` 立即開檔用，不影響任何流程

在 Obsidian 直接「Open folder as vault」開啟本 repo 即可閱讀編輯；skill 由 Claude Code 在 repo 根目錄喚起。

### vault 路徑約定（跨平台）

跨專案呼叫 `ob-write` / `ob-read` 時，定位鏈只認**固定路徑 `~/code/obsidian-memory`**（Read 該處 `vault-map.md`，含錨點 `title: Vault Map` 即驗明身分，不依賴 obsidian CLI）。各平台對齊方式：

- **macOS / Linux**：clone 到 `~/code/obsidian-memory`，天生成立。
- **Windows**：clone 到 `%USERPROFILE%\code\obsidian-memory`；vault 實體在別處（如 `C:\code\obsidian-memory`）時建連結：`mklink /J "%USERPROFILE%\code" "C:\code"`（免管理員權限，前提該路徑尚不存在）。
- **WSL**：vault 實體通常在 Windows 側，建連結：`ln -s /mnt/c/code ~/code`。

找不到時 skill 不做任何 fallback，直接以上述對齊方式提示。Obsidian 用哪個路徑開啟 vault 不影響定位；手動 `cd` 統一用 `~/code/obsidian-memory`（cmd.exe 不認 `~`，改用 `%USERPROFILE%\code\obsidian-memory`）。

## 結構

- `raw/` — 不可變原始來源（agent 只讀不改，事實來源）
  - `YouTube/` — 影片摘要，依頻道分組
  - `Clippings/` — 網頁剪貼
  - `Archive/` — 保留備查的原料
  - `Updates/` — 日常更新彙整
- `wiki/` — 活知識庫（agent 綜合 raw 維護的摘要/實體/概念/綜合頁，含內容目錄 `01.index.md`）
- `Cards/`、`Topics/` — **使用者私人策展區，agent 不管理**；同時是 Quartz 唯一對外公開的層。使用者自行從 wiki 撿選內容放入
- 資料夾完整索引見 [`vault-map.md`](./vault-map.md)
- `index.md` — 真人讀者入口（Quartz 網站首頁，列主題與 tag 連結）
- `vault-map.md` — agent 用的全局導航與 tag 查詢
- `.agents/skills/` — repo-local Claude Code skills（`.claude/skills` 為 symlink）

## 規則與工作流

先看 [`SYSTEM-DESIGN.md`](./SYSTEM-DESIGN.md)——系統全貌：Karpathy LLM Wiki 心智模型、人/AI 分工、刻意不做的事。可執行規則（agent 維護規則、Ingest/Query/Lint、寫入慣例、唯一守門）見 [`CLAUDE.md`](./CLAUDE.md)，導航見 [`vault-map.md`](./vault-map.md)。

## Skills

`.agents/skills/` 內提供 vault 操作 skills，在 Claude Code 以 `/<skill>` 喚起：

| 指令 | 用途 |
|---|---|
| `/ob-write` | 寫入筆記到 raw/wiki |
| `/ob-read` | 查詢 wiki |
| `/vault-youtube-sync` | 同步 YouTube 影片摘要至 raw |
| `/vault-updates-daily` | 彙整日常更新至 raw |
| `/vault-wiki-build` | Ingest：綜合 raw 維護 wiki 頁 |
| `/vault-lint` | wiki 結構健檢 |

**使用契約**：cwd 必須是本 repo 根目錄（含 `vault-map.md` 的目錄），所有路徑 cwd-relative，不靠環境變數。從別的專案想呼叫 skill，先 `cd` 進來。**例外**：`ob-write` / `ob-read` 為 global skills（symlink/junction 到 `~/.claude/skills/`），任何專案皆可呼叫——cwd 不在 vault 時自動走跨專案模式（定位鏈找本機 clone，見上方「vault 路徑約定」）。

## 兩個入口檔的差別

| 檔案 | 給誰看 | 內容 |
|---|---|---|
| `index.md` | 真人讀者（Quartz 訪客） | bugloop.com 首頁，挑感興趣的主題逛 |
| `vault-map.md` | AI / agent | Vault 結構地圖、tag 索引、查詢用地形圖 |
