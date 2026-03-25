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

也可以使用 `/ob` 指令直接呼叫。

### 全域掛載（讓所有專案都能使用）

將 agent 與指令 symlink 至全域，不需在此 repo 目錄下也能使用：

```powershell
# 在 repo 根目錄執行（需開啟 Developer Mode 或以管理員執行）
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\agents\obsidian.md" -Target "$PWD\.claude\agents\obsidian.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\commands\ob.md" -Target "$PWD\.claude\commands\ob.md"
```

## 本地預覽

```bash
npx quartz build --serve
```

瀏覽器開啟 `http://localhost:8080`

## 發佈

push 到 `main` 後自動部署至 GitHub Pages。此 vault 為**公開發佈**，commit 前請確認不含敏感資料。
