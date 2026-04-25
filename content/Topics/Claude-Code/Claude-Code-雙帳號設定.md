---
title: Claude Code 雙帳號設定
created: 2026-04-09
updated: 2026-04-09
tags:
  - claude-code
  - windows
  - workflow
---

透過 `CLAUDE_CONFIG_DIR` 環境變數指向不同目錄，可以在同一台機器上切換多個 Claude Code 帳號。預設帳號使用 `~/.claude`，第二帳號使用自訂目錄 `~/.claude-p`。

## 原理

Claude Code 讀取 `CLAUDE_CONFIG_DIR` 決定設定目錄。在啟動前切換這個變數，就能用不同身份登入，各帳號的 credentials 獨立存放。

## 設定步驟

### 1. 建立第二帳號的設定目錄

```powershell
mkdir "$env:USERPROFILE\.claude-p"
```

### 2. 建立 PowerShell function

確認 profile 路徑並建立（若已存在可跳過）：

```powershell
echo $PROFILE
New-Item -Path $PROFILE -ItemType File -Force   # 若已存在會覆蓋，可先 Test-Path $PROFILE 確認
```

開啟 profile 並加入 function：

```powershell
notepad $PROFILE
```

貼上：

```powershell
function claude-p { $env:CLAUDE_CONFIG_DIR="$env:USERPROFILE\.claude-p"; claude @args }
```

套用設定：

```powershell
. $PROFILE
```

### 3. 共用主帳號設定（Symlink）

第二帳號預設是空白設定。透過 symlink 共用主帳號的 agents、commands、skills 等，只有登入身份不同：

```powershell
New-Item -ItemType SymbolicLink -Path "$HOME\.claude-p\agents" -Target "$HOME\.claude\agents"
New-Item -ItemType SymbolicLink -Path "$HOME\.claude-p\commands" -Target "$HOME\.claude\commands"
New-Item -ItemType SymbolicLink -Path "$HOME\.claude-p\skills" -Target "$HOME\.claude\skills"
New-Item -ItemType SymbolicLink -Path "$HOME\.claude-p\settings.json" -Target "$HOME\.claude\settings.json"
New-Item -ItemType SymbolicLink -Path "$HOME\.claude-p\statusline.sh" -Target "$HOME\.claude\statusline.sh"
```

> Windows 需開啟 Developer Mode 或以管理員身份執行才能建立 symlink。

### 4. 測試

```powershell
claude-p
```

第一次執行會要求登入第二帳號，登入後即可正常使用。

## 日常使用

| 指令 | 帳號 | 設定目錄 |
|------|------|----------|
| `claude` | 預設帳號 | `~/.claude` |
| `claude-p` | 第二帳號 | `~/.claude-p` |