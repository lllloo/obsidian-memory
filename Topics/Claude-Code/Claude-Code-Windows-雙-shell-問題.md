---
title: Claude Code Windows 雙 shell 問題
created: 2026-06-01
updated: 2026-06-02
tags:
  - claude-code
  - windows
  - powershell
  - shell
---

Claude Code 在 Windows（platform=win32）上，模型常反射性吐 bash/Unix 語法——`printf`、`$_`、`[ -f ]`、extglob、`/dev/null` 照抄進 PowerShell 就失敗；拿到「不是 cmdlet」錯誤後還常不自我糾正，反覆重試同一條壞指令。這是官方 repo 多個公開 issue 都踩到的已知問題（見來源），不是個案。

## 為什麼會有兩個 shell

Windows 原生 PowerShell，但 Claude Code 的 PowerShell 工具：沒裝 Git Bash 時自動啟用，裝了則走漸進式 rollout（未輪到前仍走 Git Bash），Linux/macOS/WSL 純 opt-in。兩套語法不通用，模型容易把對話裡某套語法套到實際在跑的另一套 shell——故顯式設定鎖定（`1` 強制、`0` 退出）。

| 用途 | PowerShell | Bash |
|---|---|---|
| 環境變數 | `$env:VAR` | `$VAR` |
| 丟棄輸出 | `$null` | `/dev/null` |
| 檔案存在 | `Test-Path` | `[ -f ]` |
| 餵 stdin | `$content \| cmd` | `printf ... \| cmd` |

Windows 特有坑：obsidian CLI 實際是 `Obsidian.com` 這個 `.com` terminal redirector。PowerShell 靠 PATHEXT 認得，打 `obsidian` 即可；Git Bash 不認 `.com`，要顯式 `Obsidian.com`，否則 command not found——不是 CLI 壞，是 shell 不同。

## 解法

最直接——在 `~/.claude/settings.json` 設這兩項；官方文件已支援 PowerShell tool，啟用後 Claude 會把 PowerShell 當主要 shell。重開 Claude Code 生效：

```json
"env": { "CLAUDE_CODE_USE_POWERSHELL_TOOL": "1" },
"defaultShell": "powershell"
```

- `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`（**核心**）：啟用 PowerShell 工具，鎖定 Claude 走 PowerShell，不被 Git Bash rollout 翻掉。
- `defaultShell: "powershell"`：把輸入框 `!` 互動指令也導到 PowerShell，依賴上一項。

Mac/Linux 要先裝 `pwsh` 上 PATH；env 變數要全域生效得設 Windows 使用者環境變數（工具不載入 profile）。**hook 另有捷徑**：`"shell": "powershell"` 寫在單一 command hook 上會直接 spawn PowerShell，**不依賴上面的環境變數**——這是 hook 踩 shell 差異的最乾淨解（見相關卡）。

其他選項：WSL2（純 bash，問題不存在）；PreToolUse hook 轉譯指令（過渡）；光靠 CLAUDE.md 約束最弱，模型會忘。

## 落地原則：抽掉 shell 依賴

最穩的不是「把範例改對 shell」，而是**先讓動作不經 shell**，分三層：

- **檔案動作**（讀／寫／搜尋／存在檢查）用 harness-native 工具（`Read`/`Write`/`Glob`/`Grep`/`Edit`），不分 PowerShell/bash，沒有「挑錯 shell」失敗點。
- **逃不掉的邏輯**（解析、聚合、fixed-string 比對、跑外部程式）**包進 bundled Python 腳本**（純 stdlib、跨平台），SKILL 只留一行 `python <完整相對路徑> args` 呼叫，shell 方言差異藏進 Python。腳本須 `sys.stdout.reconfigure(encoding="utf-8")`、`subprocess.run` 加 `encoding="utf-8", errors="replace"`，否則 Windows cp950 解碼 UTF-8 會崩。
- **真正逃不掉的**只剩外部 CLI（如 obsidian CLI）：寫對某一支、標明所屬 shell。

具體一坑：**用 shell 管線或多行參數餵 obsidian CLI 在 Windows 容易 silent fail，甚至留下 0 bytes 空檔**；官方 `create` 沒有 `--stdin`，建檔後要驗 size，失敗就改用 harness-native `Write` 或 CLI 的 `content=` 參數，不靠 stdin。

## 相關

- [[Claude-Code-完成提示-Windows-方案比較]] — 同為 Windows + Claude Code 主題，hook 寫法同樣踩 PowerShell vs Git Bash 差異

## 來源

- [issue #45831 — defaults to bash/Unix syntax on Windows](https://github.com/anthropics/claude-code/issues/45831)
- [issue #28670 — repeatedly uses extglob, fails to adapt](https://github.com/anthropics/claude-code/issues/28670)
- [issue #16225 — Bash wrapper mangles PowerShell syntax](https://github.com/anthropics/claude-code/issues/16225)
- [Fixing Claude Code's PowerShell Problem with Hooks (netnerds)](https://blog.netnerds.net/2026/02/claude-code-powershell-hooks/)
