---
title: symlink 讓一份內容多個入口
created: 2026-06-04
updated: 2026-06-04
tags:
  - git
  - cli
  - workflow
---

symlink（符號連結）是一個指向另一個檔案的捷徑：編輯捷徑等於改到目標本身，刪掉捷徑不影響目標。它讓「一份內容」能同時掛在「多個檔名」底下。

## 用途：一份內容、多個工具入口

不同 AI 工具各認各的指令檔名——Claude Code 讀 `CLAUDE.md`，GitHub Copilot 與 Codex 讀 `AGENTS.md`。讓 `AGENTS.md` symlink 到 `CLAUDE.md`，就是一份內容、多個入口：各工具讀各自偏好的檔名，內容永遠同步，不必手動維護兩份。

本 vault 自己也用同招：`.claude/skills` 與 `.codex/skills` 都指向 `.agents/skills`，Claude Code 與 Codex 共用同一份 skill。

## 建立

```bash
# mac / Linux
ln -s CLAUDE.md AGENTS.md
```

```powershell
# Windows（PowerShell，需系統管理員）
New-Item -ItemType SymbolicLink -Path "AGENTS.md" -Target "CLAUDE.md"
```

## 驗證

```bash
# mac / Linux
ls -l AGENTS.md
```

```powershell
# Windows
Get-Item "AGENTS.md" | Select-Object LinkType, Target
```

## 注意

- 只需建一次，之後編輯任一檔名都同步
- 刪 symlink 不會刪到目標檔
- 跨平台 repo 用 symlink 共享時，clone 到 Windows 常變成純文字檔失效，修復見 [[Windows-上讓-git-symlink-真的生效]]
