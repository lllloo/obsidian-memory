---
title: daily:append 失效
created: 2026-03-17
updated: 2026-05-29
tags:
  - obsidian
  - cli
  - bug
---

`daily:append` 在 Windows（Git Bash）回傳 exit code 127 導致失敗，macOS 未觀察到此問題。

## 根本原因

exit 127 是 bash 的「command not found」代碼。實際成因是執行檔解析：Git Bash（MSYS）不套用 Windows 的 `PATHEXT`，`obsidian` 會被解析到 `.exe` 而非 CLI 真正需要的 `.com` console redirector；缺了 `.com`，帶參數的 colon-subcommand（如 `daily:append content=...`）就失敗。這不是 `daily:append` 特有，而是 Git Bash 下「帶參數的 `obsidian xxx:yyy`」通病；macOS 不走 PATHEXT / redirector 這條，故不受影響。

（實測觀察：`append path=...`、`daily:path` 在同環境未復現失敗，但這比較像個別指令的觸發差異，根因仍是上述 `.com` 解析問題，而非「某些指令 spawn 子程序、某些不 spawn」。）

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
