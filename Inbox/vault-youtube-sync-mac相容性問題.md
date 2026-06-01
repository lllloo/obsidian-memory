---
title: vault-youtube-sync Mac 相容性問題
created: 2026-06-01
updated: 2026-06-01
tags:
  - vault-youtube-sync
  - bug
---

## 問題紀錄（2026-06-01 sync 發現）

### 1. `python` 指令在 macOS 不存在

Skill 流程呼叫 `python .agents/skills/...`，macOS 預設只有 `python3`，`python` 找不到直接失敗。

這次靠 fallback 手動改 `python3` 才繼續，但 skill 原文沒有自動 fallback。

### 2. `pip install` 被 macOS 系統擋

```
python3 -m pip install -q youtube-transcript-api
```

macOS Homebrew 管理的 Python 環境預設拒絕系統級安裝，需加 `--break-system-packages`。這次沒出事是因為套件已裝過，但乾淨環境會導致所有 transcript 失敗、全走 draft 占位。

## 待修方案

### 問題一：`python` vs `python3`

`vault-lint` 已修（改為 `python3` 優先，不行 fallback `python`）。`vault-youtube-sync` 同理，SKILL.md 第 176 行需同步更新。

### 問題二：pip 跨平台方案

原本的 shell fallback 寫法有問題：

```
python3 -m pip install -q youtube-transcript-api --break-system-packages 2>/dev/null || python -m pip install -q youtube-transcript-api
```

`2>/dev/null ||` 是 bash 語法，Windows PowerShell 不認。

依 skill-writing 原則（複雜邏輯包進 Python 腳本），建議新增 `scripts/ensure_deps.py`：

```python
import subprocess, sys
subprocess.run(
    [sys.executable, "-m", "pip", "install", "-q",
     "youtube-transcript-api", "--break-system-packages"],
    capture_output=True
)
```

SKILL.md 的 pip 安裝那行改為：

```
python3 .agents/skills/vault-youtube-sync/scripts/ensure_deps.py
```

`sys.executable` 永遠指向目前執行的 Python，不需要 `python`/`python3` 判斷；`--break-system-packages` 在 pip 23.0+ 全平台通用，非 Homebrew 環境靜默忽略。
