# obsidian-memory

個人知識庫，以 [Obsidian](https://obsidian.md/) 管理筆記，透過 [Quartz](https://quartz.jzhao.xyz/) 發佈至 [ob.bugloop.com](https://ob.bugloop.com)。

## 前置需求

- [Obsidian](https://obsidian.md/) 桌面版
- Obsidian CLI plugin（在 Obsidian 內安裝）
- Node.js 22+（本地預覽用）
- [Claude Code](https://claude.ai/code)（AI 筆記助手，選用）

## Vault 結構

```
content/
├── Inbox/      # 日記
├── Cards/      # 單篇筆記
├── Topics/     # MOC 與主題資料夾
└── Templates/  # 筆記模板
```

## 使用 Claude Code

對話中提到「ob」、「筆記」、「日記」即可觸發助手：

```
記一下今天...        → 追加到今日日記
新增一篇關於...的筆記  → 建立新筆記
找 <關鍵字>          → 搜尋 vault
```

## 本地預覽

```bash
npx quartz build --serve
```

瀏覽器開啟 `http://localhost:8080`

## 發佈

push 到 `main` 後自動部署至 GitHub Pages。此 vault 為**公開發佈**，commit 前請確認不含敏感資料。
