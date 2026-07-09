# Obsidian Memory Vault

個人 Obsidian vault，採 Karpathy [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 工作流：agent 讀不可變的 `raw/` 原料，漸進維護一套互聯的 `wiki/` 活知識庫。`cards/`、`topics/` 是使用者私人策展區，也是對外公開的層。公開版本在 [bugloop.com](https://bugloop.com)。

## 安裝與使用

```bash
git clone <repo-url> obsidian-memory
```

**Prerequisites**：

- [Obsidian](https://obsidian.md/) — 編輯與圖譜瀏覽
- Python 3（純 stdlib）— skill 腳本執行所需
- [Obsidian CLI](https://help.obsidian.md/cli)（選用）— 本地開檔輔助，不影響任何流程

在 Obsidian 直接「Open folder as vault」開啟本 repo 即可閱讀編輯；skill 由 Claude Code 在 repo 根目錄喚起。

> **跨專案呼叫已移除**：原本 `ob-write` / `ob-read` 兩個全域 skill 可從任何專案透過定位鏈（固定路徑 `~/code/obsidian-memory`）呼叫，現已移除。目前所有 vault 操作皆在本 repo 根目錄內進行；跨專案能力待後續重建時再補回路徑約定。

## 結構

- `raw/` — 不可變原始來源（agent 只讀不改，事實來源）
  - `YouTube/` — 影片摘要，依頻道分組
  - `Clippings/` — 網頁剪貼
  - `Archive/` — 保留備查的原料
  - `Updates/` — 日常更新彙整
- `wiki/` — 活知識庫（agent 綜合 raw 維護的摘要/實體/概念/綜合頁，含內容目錄 `01.index.md`）
- `cards/`、`topics/` — **使用者私人策展區，agent 不管理**；同時是 Quartz 唯一對外公開的層。使用者自行從 wiki 撿選內容放入
- 資料夾完整索引見 [`schema/vault-map.md`](./schema/vault-map.md)
- `index.md` — 真人讀者入口（Quartz 網站首頁，列主題與 tag 連結）
- `schema/vault-map.md` — agent 用的全局導航與 tag 查詢
- `.agents/skills/` — repo-local Claude Code skills（`.claude/skills` 為 symlink）

## 規則與工作流

先看 [`schema/SYSTEM-DESIGN.md`](./schema/SYSTEM-DESIGN.md)——系統全貌：Karpathy LLM Wiki 心智模型、人/AI 分工、刻意不做的事。可執行規則（agent 維護規則、Ingest/Query/Lint、寫入慣例、唯一守門）見 [`CLAUDE.md`](./CLAUDE.md)，導航見 [`schema/vault-map.md`](./schema/vault-map.md)。

## Skills

`.agents/skills/` 內提供 vault 操作 skills，在 Claude Code 以 `/<skill>` 喚起：

| 指令 | 用途 |
|---|---|
| `/vault-youtube-sync` | 同步 YouTube 影片摘要至 raw |
| `/vault-updates-daily` | 彙整日常更新至 raw |

**使用契約**：cwd 必須是本 repo 根目錄（含 `CLAUDE.md` 的目錄），所有路徑 cwd-relative，不靠環境變數。從別的專案想呼叫 skill，先 `cd` 進來。

> 原核心 skill `ob-write`、`ob-read`（global）、`vault-wiki-build`、`vault-lint` 已移除；Ingest（wiki 綜合）／Query／Lint 三動作目前由 agent 手動執行，後續按需重建。

## 兩個入口檔的差別

| 檔案 | 給誰看 | 內容 |
|---|---|---|
| `index.md` | 真人讀者（Quartz 訪客） | bugloop.com 首頁，挑感興趣的主題逛 |
| `schema/vault-map.md` | AI / agent | Vault 結構地圖、tag 索引、查詢用地形圖 |
