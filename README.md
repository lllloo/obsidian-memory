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

此 repo 內建兩個 Claude Code 設定，讓你在對話中直接操作 Obsidian vault：

### `/ob` 指令（`.claude/commands/ob.md`）

`/ob` 是一個 slash command，輸入後會把你的需求轉交給 Obsidian agent 處理：

```
/ob 記一下今天完成了 XXX
/ob 新增一篇關於 React hooks 的筆記
/ob 找跟 CSS 有關的筆記
```

### Obsidian Agent（`.claude/agents/obsidian.md`）

Agent 是實際執行操作的角色，透過 Obsidian CLI 與 vault 互動。收到需求後會自動判斷模式：

| 說了什麼 | 動作 |
|---------|------|
| 「今天」、「日記」、「記一下」 | 追加到今日日記 |
| 主題、概念、「筆記」、「建立」、「新增」 | 建立新筆記 |
| 「找」、「搜尋」、「查」 | 搜尋 vault |

也可以不用 `/ob`，直接在對話中提到「ob」、「筆記」、「日記」即會自動觸發。

### 全域掛載（讓所有專案都能使用）

預設只有在此 repo 目錄下才能使用上述設定。透過 symlink 掛載至全域後，在任何專案的 Claude Code 對話中都能呼叫：

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
