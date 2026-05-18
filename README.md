# Obsidian Memory Vault

個人 Obsidian vault，採「吸收型卡片盒」工作流。公開版本在 [ob.bugloop.com](https://ob.bugloop.com)（部署機制屬上層容器，見下方）。

## 結構

- `Inbox/` — 待消化暫存（AI 抄錄外部原料，消化完刪除）
- `Cards/` — 未歸屬的完整概念 Card（累積同主題後批次升 Topic）
- `Topics/<主題>/` — 已歸檔主題；目前 6 個（Claude-Code、AI-Agent-工作流、UI設計、前端技術、Obsidian、部署）
- `master-index.md` — 全局導航與 tag 查詢
- `scripts/` — vault 稽核工具
- `.agents/skills/` — repo-local Claude Code skills（`.claude/skills` 為 symlink）

## 安裝

需要 Node.js 20+。

```bash
git clone https://github.com/lllloo/obsidian-memory.git
cd obsidian-memory
npm install
```

## 常用指令

```bash
npm run vault:check                       # 稽核 frontmatter / 敏感資料 / 日期（唯讀）
npm run vault:fix                         # 同上，並自動修正可修部分
node scripts/vault-schema.test.mjs        # 執行 schema 單元測試
node scripts/verify-skill-symlinks.mjs    # 驗證 .claude/skills symlink
```

## 規則與工作流

詳見：

- [`CLAUDE.md`](./CLAUDE.md) — vault 規則、寫入 Checklist、frontmatter schema
- [`topics-review.md`](./topics-review.md) — 升 Topic 品質門檻與反指標
- 上層容器 [`../CLAUDE.md`](../CLAUDE.md) — 部署機制與 sibling repo 關係
