---
title: 跨專案內容整理到 Inbox
created: 2026-05-21
updated: 2026-07-09
tags:
  - obsidian
  - claude-code
  - cli
  - workflow
  - sop
---

跨專案做筆記不用設計完整流程。只要使用者在其他專案裡覺得某段內容值得保留，就直接把重點寫進 vault repo（`~/code/obsidian-memory`）的 `raw/`。

其他專案的 agent 只負責收束重點，不負責整理成 Card、不升 Topic、不修改 vault 其他筆記。格式、tag、wikilink、是否內化成 Card，之後回到 vault session 再處理。

## 怎麼做

使用者可以直接說：

```text
把這段值得保留的重點寫到 Obsidian vault 的 raw。
```

agent 就建立一篇 `raw/<主題>.md`，內容只要包含：

- 這次真正值得留下的重點
- 必要時補一行回查線索，例如原專案、檔案、指令或關鍵字

寫入方式：目前在 vault repo（cwd = vault root）內直接用檔案工具寫入。

> 註：原本跨專案由 `/ob-write` 自動判斷 cwd、跨專案時走 CLI／定位鏈寫入的機制已移除。現階段跨專案要保留內容，先 `cd` 進 vault repo 再操作。

不需要把整段對話、完整 log、一次性過程或還沒整理的外部資料搬進來。

## 最低要求

- 寫入前排除 token、API key、密碼、客戶資料、內部 URL 等敏感內容
- 檔名不要有空格
- `title`、`created`、`updated`、`tags` 有基本 frontmatter 即可

raw 收束階段只要之後看得懂。真正的整理（ingest 進 wiki、是否手動撿選成 Card），等回到 `~/code/obsidian-memory` 的 vault session 再決定。

## 相關

- [[Obsidian-CLI-整合指南]]
- [[Obsidian-Skills]]
