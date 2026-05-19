# Obsidian Memory Vault

個人 Obsidian vault，採「吸收型卡片盒」工作流。公開版本在 [ob.bugloop.com](https://ob.bugloop.com)。

## 結構

- `Inbox/` — 待消化暫存（AI 抄錄外部原料，消化完刪除）
  - `YouTube/` — 影片摘要，依頻道分組
  - `Clippings/` — 網頁剪貼
  - `RedditDaily/` — Reddit 每日摘要
  - `Updates/` — 日常更新彙整
- `Cards/` — 未歸屬的完整概念 Card（累積同主題後批次升 Topic）
- `Topics/<主題>/` — 已歸檔主題；目前 6 個（Claude-Code、AI-Agent-工作流、UI設計、前端技術、Obsidian、部署）
- `master-index.md` — 全局導航與 tag 查詢
- `.agents/skills/` — repo-local Claude Code skills（`.claude/skills` 為 symlink）

## 規則與工作流

詳見：

- [`CLAUDE.md`](./CLAUDE.md) — vault 規則、寫入 Checklist、frontmatter schema
- [`topics-review.md`](./topics-review.md) — 升 Topic 品質門檻與反指標
