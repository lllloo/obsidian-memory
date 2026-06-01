---
title: Claude Code Windows 雙 shell 問題
created: 2026-06-01
updated: 2026-06-01
tags:
  - claude-code
  - windows
  - powershell
  - shell
---

Claude Code 在 Windows（platform=win32）上，模型常反射性吐 bash/Unix 語法——`printf`、`$_`、`[ -f ]`、extglob、`/dev/null` 照抄進 PowerShell 就失敗；拿到「不是 cmdlet」錯誤後還常不自我糾正，反覆重試同一條壞指令。這是官方 repo 大量 open issue 的已知問題（見來源），不是個案。

## 為什麼會有兩個 shell

Windows 原生是 PowerShell，但 Claude Code 的 PowerShell 工具是 **opt-in**——裝了 Git for Windows 又沒設 `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` 時，預設反而走 Git Bash（MinGW/MSYS2 的 bash，POSIX Bash 工具）。沒裝 Git for Windows 才會 fallback 用 PowerShell。兩套語法不通用，模型容易把對話裡某套語法套到實際在跑的另一套 shell。

| 用途 | PowerShell | Bash |
|---|---|---|
| 環境變數 | `$env:VAR` | `$VAR` |
| 丟棄輸出 | `$null` | `/dev/null` |
| 檔案存在 | `Test-Path` | `[ -f ]` |
| 餵 stdin | `$content \| cmd` | `printf ... \| cmd` |

Windows 特有坑：obsidian CLI 實際是 `Obsidian.com` 這個 `.com` terminal redirector。PowerShell 靠 PATHEXT 認得，打 `obsidian` 即可；Git Bash 不認 `.com`，要顯式 `Obsidian.com`，否則 command not found——不是 CLI 壞，是 shell 不同。

## 解法

最直接——在 `~/.claude/settings.json` 設這兩項（需 v2.1.139+），重開 Claude Code 生效：

```json
"env": { "CLAUDE_CODE_USE_POWERSHELL_TOOL": "1" },
"defaultShell": "powershell"
```

- `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`（**核心**）：啟用 PowerShell 工具，Claude 跑指令改走 PowerShell——裝了 Git Bash 時避免預設被翻回 Bash。顯式設才保證生效。
- `defaultShell: "powershell"`：把輸入框 `!` 互動指令也導到 PowerShell，依賴上一項才生效。

Mac 不要加（無 pwsh），各 Windows 機器各自設一次；想讓所有 terminal 都認得，env 改設 Windows 使用者環境變數，而非只放 PowerShell profile。

其餘層級（更徹底到治標）：

1. **更徹底**——整碗端到 **WSL2**（純 bash 環境，雙 shell 問題不存在）。
2. **過渡**——PreToolUse hook 攔截／轉譯 shell 指令。
3. **最弱**——光靠 CLAUDE.md 明寫約束：模型會忘，需 hook 強制才可靠。

## 落地原則：抽掉 shell 依賴

最穩的不是「把範例改對 shell」，而是**先讓動作不經 shell**，分三層：

- **檔案動作**（讀／寫／搜尋／存在檢查）用 harness-native 工具（`Read`/`Write`/`Glob`/`Grep`/`Edit`），不分 PowerShell/bash，沒有「挑錯 shell」失敗點。
- **逃不掉的邏輯**（解析、聚合、fixed-string 比對、跑外部程式）**包進 bundled Python 腳本**（純 stdlib、跨平台），SKILL 只留一行 `python <完整相對路徑> args` 呼叫——複雜度藏進 Python，呼叫行無 shell 方言差異。原本以為「聚合 pipeline／fixed-string 比對」非 shell 不可，實證後都改成了腳本（如 vault-lint 的 `lint.py`、daily-updates 的 `dedup_check.py`），shell 趨近零。腳本須 `sys.stdout.reconfigure(encoding="utf-8")`，且 `subprocess.run` 加 `encoding="utf-8", errors="replace"`，否則 Windows cp950 解碼 UTF-8 會崩。
- **真正逃不掉的**只剩外部 CLI（如 obsidian CLI）：寫對某一支、標明所屬 shell。

具體一坑：**stdin pipe 餵 obsidian CLI（`... | obsidian create --stdin`）在 Windows 經 `.com` redirector 會留 0 bytes 空檔**，PowerShell/bash 皆然——故建檔改用 `Write` 或 `content=` 參數，不走 stdin。

## 相關

- [[Claude-Code-完成提示-Windows-方案比較]] — 同為 Windows + Claude Code 主題，hook 寫法同樣踩 PowerShell vs Git Bash 差異

## 來源

- [issue #45831 — defaults to bash/Unix syntax on Windows](https://github.com/anthropics/claude-code/issues/45831)
- [issue #28670 — repeatedly uses extglob, fails to adapt](https://github.com/anthropics/claude-code/issues/28670)
- [issue #16225 — Bash wrapper mangles PowerShell syntax](https://github.com/anthropics/claude-code/issues/16225)
- [Fixing Claude Code's PowerShell Problem with Hooks (netnerds)](https://blog.netnerds.net/2026/02/claude-code-powershell-hooks/)
