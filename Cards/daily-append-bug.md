---
tags:
  - obsidian
  - cli
  - bug
created: 2026-03-17
updated: 2026-03-17
---

# daily:append 失效

`daily:append` 會回傳 exit code 127 導致失敗。

## 解法

拆成兩步驟：

1. `obsidian daily:path` 取得今日路徑
2. `obsidian append path="<date>.md" content="內容"`

## 相關
- [[Claude Code 整合]]
