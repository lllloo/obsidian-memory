---
title: Python Windows stdout UTF-8 亂碼
created: 2026-06-12
updated: 2026-06-18
tags:
  - python
  - windows
  - encoding
  - cross-platform
---

繁中 Windows 上，Python 程序輸出被導向 pipe（非互動式 console，例如被工具／腳本捕捉）時，stdout 編碼會跟隨系統 locale 回退成 `cp950`（Big5 變體）。中文以 cp950 bytes 寫出，但接收端常以 UTF-8 解讀，於是亂碼。本質是「寫端 cp950、讀端 UTF-8」的編碼不一致——資料沒壞，只是兩端對 bytes 的解釋不同。

## 兩層解法（可疊加、同向不衝突）

### 1. 全域環境變數 PYTHONUTF8=1

PEP 540 UTF-8 Mode：強制所有 Python 程序的 stdout／stderr 與 `open()` 預設都走 UTF-8，不再回退 cp950。設使用者層級（PowerShell）：

```powershell
[Environment]::SetEnvironmentVariable('PYTHONUTF8','1','User')
```

**生效時機（易踩坑）**：使用者層級環境變數更新後，只有「之後新建、且從已刷新環境的父進程啟動」的程序才繼承。既有 terminal／Claude Code 進程啟動時已 snapshot 舊環境，關視窗或重開對話不夠，必須完整結束父進程後重開，或登出／重新登入 Windows。驗證：新進程 `$env:PYTHONUTF8` 應為 `1`。

**副作用**：UTF-8 Mode 也改 `open()` 預設編碼；若有腳本刻意用 cp950／Big5 讀舊檔會受影響（可在該腳本設 `PYTHONUTF8=0` 或明確 `encoding=`）。

### 2. 腳本內 reconfigure

```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

放在 import 區之後。跨機器／跨設定的保險，不依賴環境變數，換任何電腦都不亂碼。

## 取捨

- **只靠 PYTHONUTF8=1（腳本不加）**：本機乾淨、腳本簡潔；但換沒設此變數的機器／CI／別人 clone 時，繁中 Windows 仍會亂碼。
- **加腳本內 reconfigure**：自包含、跨機器不亂碼；代價是每支 CLI 多兩行。

## PEP 8 細節

`sys.stdout.reconfigure(...)` 若夾在 import 語句中間，linter 會報 `E402`（module level import not at top of file）。放在整個 import 區之後較合規。

## tenpai 專案的決定（2026-06-12）

本機已設 `PYTHONUTF8=1`，決定移除腳本內逐支 reconfigure、統一靠環境變數。此決定與全域規則 `~/.claude/rules/python.md`（要求「所有 Python 腳本開頭一律加 reconfigure」）有出入，後續再調整該規則。

相關：[[Python-直譯器指令名跨平台選擇]]——同屬跨平台 Python 執行的踩坑。

回查線索：原專案 tenpai（C:/code/tenpai）；相關檔 `src/*.py`、`src/status.py`；全域規則 `~/.claude/rules/python.md`。
