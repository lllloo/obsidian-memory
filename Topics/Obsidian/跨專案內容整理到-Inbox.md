---
title: 跨專案內容整理到 Inbox
created: 2026-05-21
updated: 2026-05-28
tags:
  - obsidian
  - claude-code
  - cli
  - workflow
  - sop
---

跨專案做筆記不用設計完整流程。只要使用者在其他專案裡覺得某段內容值得保留，就直接把重點寫進 `C:\code\obsidian-memory\Inbox\`。

其他專案的 agent 只負責收束重點，不負責整理成 Card、不升 Topic、不修改 vault 其他筆記。格式、tag、wikilink、是否內化成 Card，之後回到 vault session 再處理。

## 怎麼做

使用者可以直接說：

```text
把這段值得保留的重點寫到 Obsidian Inbox。
```

agent 就建立一篇 `Inbox/<主題>.md`，內容只要包含：

- 這次真正值得留下的重點
- 必要時補一行回查線索，例如原專案、檔案、指令或關鍵字

如果當前環境可用 Obsidian CLI，就用 CLI 寫入；不可用就直接用檔案工具寫到 vault 路徑，不需要卡在工具選擇。

不需要把整段對話、完整 log、一次性過程或還沒整理的外部資料搬進來。

## 最低要求

- 寫入前排除 token、API key、密碼、客戶資料、內部 URL 等敏感內容
- 檔名不要有空格
- `title`、`created`、`updated`、`tags` 有基本 frontmatter 即可

Inbox 階段只要之後看得懂。真正的整理、合併、刪除或升級成 Card，等回到 `C:\code\obsidian-memory` 再決定。

## 相關

- [[Obsidian-CLI-整合指南]]
- [[Obsidian-Skills]]
