---
title: "符號連結:讓 AGENTS.md 與 CLAUDE.md 互相使用"
created: 2026-06-03
updated: 2026-06-04
tags:
  - cli
  - claude-code
  - copilot
  - git
  - windows
---

# 符號連結:讓 AGENTS.md 與 CLAUDE.md 互相使用

透過符號連結(Symbolic Link),可以建立 `AGENTS.md` 指向 `CLAUDE.md`,讓兩個檔案實際上共享同一份內容。這樣大部分的 AI 工具(如 GitHub Copilot、Claude Code 等)都能讀取到相同的專案指令。

## 核心概念

符號連結是一個「指向其他檔案的捷徑」,當你編輯符號連結時,實際上是在修改目標檔案。這讓不同 AI 工具能透過各自偏好的檔名(AGENTS.md 或 CLAUDE.md)讀取相同的內容。

## 建立指令

### Windows PowerShell

```powershell
New-Item -ItemType SymbolicLink -Path "AGENTS.md" -Target "CLAUDE.md"
```

### macOS / Linux

```bash
ln -s CLAUDE.md AGENTS.md
```

## 驗證符號連結

### Windows

```powershell
Get-Item "AGENTS.md" | Select-Object LinkType, Target
```

### macOS / Linux

```bash
ls -l AGENTS.md
```

## 重要提醒

- **只需建立一次**:建立後,編輯任一檔案都會同步更新
- **刪除連結不影響原檔**:刪除 `AGENTS.md` 符號連結不會刪除 `CLAUDE.md`
- **Git 處理**:Git 可以追蹤符號連結,但在不同作業系統間需注意兼容性

## 使用場景

這個技巧特別適合:

- 使用多個 AI 編碼助手的專案
- 需要在不同工具間共享相同的專案指令
- 維護單一來源的專案文檔,避免內容不同步
