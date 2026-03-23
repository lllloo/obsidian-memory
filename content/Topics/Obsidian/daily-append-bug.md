---
title: daily:append 失效
tags:
  - obsidian
  - cli
  - bug
created: 2026-03-17
updated: 2026-03-21
---

`daily:append` 在特定環境下回傳 exit code 127 導致失敗。

## 根本原因

`daily:append` 內部會 spawn 子程序，在某些 shell 環境中找不到對應的執行檔，導致 exit code 127（bash 的「找不到命令」代碼）。

其他指令如 `append path=...`、`daily:path` 透過 Obsidian IPC/API 直接執行，不 spawn 子程序，所以不受影響。

## 解法

### Windows（Git Bash）：用 PowerShell 包一層

```bash
powershell.exe -Command "obsidian daily:append content='內容'"
```

### 備用：拆成兩步驟

1. `obsidian daily:path` 取得今日路徑
2. `obsidian append path="<date>.md" content="內容"`

## 相關
- [[Obsidian-CLI-整合指南]]
