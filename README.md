# Obsidian Memory Vault

個人 Obsidian vault，採「吸收型卡片盒」工作流。公開版本在 [ob.bugloop.com](https://ob.bugloop.com)。

## 結構

- `Inbox/` — 待消化暫存（AI 抄錄外部原料，消化完刪除）
  - `YouTube/` — 影片摘要，依頻道分組
  - `Clippings/` — 網頁剪貼
  - `Updates/` — 日常更新彙整
- `Cards/` — 未歸屬的完整概念 Card（累積同主題後批次升 Topic）
- `Topics/<主題>/` — 已歸檔主題；目前 6 個（Claude-Code、AI-Agent-工作流、UI設計、前端技術、Obsidian、部署）
- `index.md` — 真人讀者入口（Quartz 網站首頁，列主題與 tag 連結）
- `master-index.md` — agent 用的全局導航與 tag 查詢
- `.agents/skills/` — repo-local Claude Code skills（`.claude/skills` 為 symlink）

## 規則與工作流

詳見：

- [`vault-model.md`](./vault-model.md) — 系統全貌：模式血緣、核心賭注、刻意不做的事（先看這份建立整體心智模型）
- [`CLAUDE.md`](./CLAUDE.md) — vault 規則、寫入 Checklist、frontmatter schema
- [`topics-review.md`](./topics-review.md) — 升 Topic 品質門檻與反指標

## Skills

`.agents/skills/` 內提供 vault 操作 skills（`ob` 筆記操作、`vault-distill` 主題整合、`vault-youtube-sync` 影片摘要同步等）。完整清單見 [`CLAUDE.md` § 可用 Skills](./CLAUDE.md#可用-skills)。

**使用契約**：cwd 必須是本 repo 根目錄（含 `master-index.md` 的目錄），所有路徑 cwd-relative，不靠環境變數。從別的專案想呼叫 skill，先 `cd` 進來。

## 兩個 index 的差別

| 檔案 | 給誰看 | 內容 |
|---|---|---|
| `index.md` | 真人讀者（Quartz 訪客） | ob.bugloop.com 首頁，挑感興趣的主題逛 |
| `master-index.md` | AI / agent | Vault 結構地圖、tag 索引、查詢用地形圖 |
