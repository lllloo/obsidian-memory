# Obsidian Memory Vault

個人 Obsidian vault，採 Karpathy [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 工作流：agent 讀不可變的 `raw/` 原料，漸進維護一套互聯的 `wiki/` 活知識庫。`cards/`、`topics/` 是使用者私人策展區，也是對外公開的層。公開版本在 [bugloop.com](https://bugloop.com)。

## 安裝與使用

```bash
git clone <repo-url> obsidian-memory
```

**Prerequisites**：

- [Obsidian](https://obsidian.md/) — 編輯與圖譜瀏覽
- Python 3（純 stdlib）— skill 腳本執行所需；Windows 建議先設機器級 `PYTHONUTF8=1`，避免 cp950 編碼問題
- [Obsidian CLI](https://help.obsidian.md/cli)（選用）— 本地開檔輔助，不影響任何流程

在 Obsidian 直接「Open folder as vault」開啟本 repo 即可閱讀編輯；skill 由 Claude Code 在 repo 根目錄喚起。

> **跨專案呼叫已移除**：原本 `ob-write` / `ob-read` 兩個全域 skill 可從任何專案透過定位鏈（固定路徑 `~/code/obsidian-memory`）呼叫，現已移除。目前所有 vault 操作皆在本 repo 根目錄內進行；跨專案能力待後續重建時再補回路徑約定。

## 結構

三層系統（資料夾完整索引見 [`schema/vault-map.md`](./schema/vault-map.md)）：

- `raw/` — 原始來源，write-once（agent 可新增、不可修改，事實來源）
  - `Clippings/` — 網頁剪藏
- `wiki/` — 活知識庫（agent 綜合 raw 維護的摘要/實體/概念/綜合頁，含內容目錄 `01.index.md`）
- `CLAUDE.md` + `schema/` — 治理規範層：`CLAUDE.md`（可執行規則）、`schema/SYSTEM-DESIGN.md`（系統全貌）、`schema/vault-map.md`（agent 用全局導航與 tag 查詢）、`schema/MEMORY.md`（agent 跨 session 操作記憶，checked-in 以確保跨工具可攜）

三層之外：

- `feeds/` — 自動產物層，**不屬三層系統、預設不是 ingest 原料**
  - `youtube/` — 自動同步的候選來源；僅在使用者明確指定時綜合進 wiki
  - `updates/` — 每日工具更新日報，純消費
  - `lint/` — vault 健檢報告，純消費
- `cards/`、`topics/` — **使用者私人策展區，agent 不管理**；同時是 Quartz 唯一對外公開的層。使用者自行從 wiki 撿選內容放入（Quartz 發佈設定與流程不在本 repo）
- `index.md` — 真人讀者入口（Quartz 網站首頁，列主題與 tag 連結）
- `.agents/skills/` — repo-local skills，遵循 [Agent Skills](https://agentskills.io) 開放標準（`.claude/skills` 為 symlink）

## 規則與工作流

先看 [`schema/SYSTEM-DESIGN.md`](./schema/SYSTEM-DESIGN.md)——系統全貌：Karpathy LLM Wiki 心智模型、人/AI 分工、刻意不做的事。可執行規則（agent 維護規則、Ingest/Query/Lint、寫入慣例、唯一守門）見 [`CLAUDE.md`](./CLAUDE.md)，導航見 [`schema/vault-map.md`](./schema/vault-map.md)。

**非 Claude Code 的 AI 工具**（Cursor、Codex 等）從 `AGENTS.md` 進入——它是 `CLAUDE.md` 的 symlink，內容完全相同（checkout 需 git 支援 symlink；Windows 請開 `core.symlinks`，否則會退化成只含檔名字串的純文字檔）。跨 session 操作記憶在 `schema/MEMORY.md`，checked-in 進 repo，任何工具打開 vault 都讀得到。

## Skills

`.agents/skills/` 內提供 vault 操作 skills，遵循 [Agent Skills](https://agentskills.io) 開放標準、可被支援該標準的其他 AI 工具載入；在 Claude Code 以 `/<skill>` 喚起：

| 指令 | 用途 |
|---|---|
| `/vault-youtube-sync` | 同步 YouTube 影片摘要至 `feeds/youtube/` |
| `/vault-updates-daily` | 彙整日常工具更新日報至 `feeds/updates/` |
| `/vault-lint-daily` | 產出 vault 健檢報告至 `feeds/lint/`（機械項自動修、語意項只報告） |

**使用契約**：cwd 必須是本 repo 根目錄（含 `CLAUDE.md` 的目錄），所有路徑 cwd-relative，不靠環境變數。從別的專案想呼叫 skill，先 `cd` 進來。

> 原核心 skill `ob-write`、`ob-read`（global）、`vault-wiki-build`、`vault-lint` 已移除；Ingest（wiki 綜合）與 Query 由 agent 手動執行，Lint 的掃描面已按需重建為報告制的 `/vault-lint-daily`。

## 兩個入口檔的差別

| 檔案 | 給誰看 | 內容 |
|---|---|---|
| `index.md` | 真人讀者（Quartz 訪客） | bugloop.com 首頁，挑感興趣的主題逛 |
| `schema/vault-map.md` | AI / agent | Vault 結構地圖、tag 索引、查詢用地形圖 |
