---
title: Claude Code 完成提示（Windows）— 方案比較
created: 2026-05-25
updated: 2026-06-02
tags:
  - claude-code
  - hooks
  - windows
  - terminal
---

多視窗時一眼看出哪個 Claude Code 在跑。採用 OSC 9;4 工作列進度條，inline 在 `settings.json` 的 `hooks`，不需外部腳本。

## 設定

Windows 版直接把 hook 指定成 PowerShell。`command` 用 PowerShell 組出 OSC 9;4 escape sequence，再用 `ConvertTo-Json` 回傳 `terminalSequence`；Claude Code 會代為輸出控制序列，不需要 `/dev/tty`，也不依賴 Git Bash 的 `printf`。

```json
"hooks": {
  "SessionStart": [{
    "hooks": [{
      "type": "command",
      "shell": "powershell",
      "command": "$seq=[char]27+']9;4;0;0'+[char]7; @{terminalSequence=$seq}|ConvertTo-Json -Compress"
    }]
  }],
  "UserPromptSubmit": [{
    "hooks": [{
      "type": "command",
      "shell": "powershell",
      "command": "$seq=[char]27+']9;4;3;0'+[char]7; @{terminalSequence=$seq}|ConvertTo-Json -Compress"
    }]
  }],
  "PostToolBatch": [{
    "hooks": [{
      "type": "command",
      "shell": "powershell",
      "command": "$seq=[char]27+']9;4;3;0'+[char]7; @{terminalSequence=$seq}|ConvertTo-Json -Compress"
    }]
  }],
  "Notification": [
    {
      "matcher": "permission_prompt",
      "hooks": [{
        "type": "command",
        "shell": "powershell",
        "command": "$seq=[char]27+']9;4;4;100'+[char]7; @{terminalSequence=$seq}|ConvertTo-Json -Compress"
      }]
    },
    {
      "matcher": "elicitation_dialog",
      "hooks": [{
        "type": "command",
        "shell": "powershell",
        "command": "$seq=[char]27+']9;4;4;100'+[char]7; @{terminalSequence=$seq}|ConvertTo-Json -Compress"
      }]
    }
  ],
  "Stop": [{
    "hooks": [{
      "type": "command",
      "shell": "powershell",
      "command": "$seq=[char]27+']9;4;0;0'+[char]7; @{terminalSequence=$seq}|ConvertTo-Json -Compress"
    }]
  }],
  "StopFailure": [{
    "hooks": [{
      "type": "command",
      "shell": "powershell",
      "command": "$seq=[char]27+']9;4;0;0'+[char]7; @{terminalSequence=$seq}|ConvertTo-Json -Compress"
    }]
  }]
}
```

| event | matcher | state;progress | 視覺效果 |
|---|---|---|---|
| `SessionStart` | — | `0;0` | 清除 |
| `UserPromptSubmit` | — | `3;0` | 旋轉動畫（開始跑） |
| `PostToolBatch` | — | `3;0` | 每批工具後重申旋轉，避免被覆蓋 |
| `Notification` | `permission_prompt` / `elicitation_dialog` | `4;100` | 黃色滿格暫停（等你介入） |
| `Stop` | — | `0;0` | 清除（跑完） |
| `StopFailure` | — | `0;0` | 清除（API error 等失敗結束） |

**Notification 用 `matcher` 精準篩選**：`Notification` 也含 `idle_prompt`（閒置自動觸發），不篩會造成工作列莫名變黃。`permission_prompt` 對應權限確認；`elicitation_dialog` 對應 Claude Code 主動詢問使用者。兩者都算「需要你介入」。

OSC 9;4 state 速查：`0` 清除、`1` 綠色、`2` 紅色、`3` 旋轉、`4` 黃色暫停。格式：`ESC]9;4;<state>;<progress>BEL`。

## 卡住狀態清除

`$PROFILE` 綁 `Esc` 幾乎沒用：Claude Code 執行時 `Esc` 會先送進 Claude Code 本身，不會觸發 PowerShell 的 PSReadLine key handler；真正能觸發時通常已經退出 Claude Code、回到 shell prompt。它不能拿來處理 Claude Code 還開著時的卡住狀態。

唯一還算實用的補救點，是退出 Claude Code 或中斷回到 PowerShell prompt 時自動清一次，避免 Windows Terminal 工作列狀態殘留：

```powershell
function Clear-WTProgress {
    [Console]::Write([char]27 + "]9;4;0;0" + [char]7)
}

if (-not (Test-Path variable:global:__WTProgressOriginalPrompt)) {
    $global:__WTProgressOriginalPrompt = (Get-Command prompt -CommandType Function).ScriptBlock
}

function prompt {
    Clear-WTProgress
    & $global:__WTProgressOriginalPrompt
}
```

## 需求

- CC ≥ 2.1.141
- Windows Terminal
- hook command 支援 `"shell": "powershell"`

## 備選方案

**Git Bash `printf` 版**：可用 `printf '%s' '{"terminalSequence":"\u001b]9;4;3;0\u0007"}'` 直接吐 JSON 字面字串。優點是短；缺點是綁 Git Bash，且和 Windows PowerShell-first 的設定方向相反。

**分頁標題 emoji（OSC 2）**：double-click rename 後鎖死標題；emoji 不可 inline（cp950 亂碼）；`$Host.UI.RawUI.WindowTitle` 在 hook 子進程讀到 PS 自身路徑而非分頁標題。

**桌面 toast 通知（OSC 9）**：用 `ESC]9;訊息BEL` 彈出系統通知，切到其他視窗時也看得到。Windows Terminal 原生支援，可與 OSC 9;4 並用。缺點：每次完成都彈出、較吵。

## 相關

- [[Claude-Code-規則系統設計]] — 規則升級到 Hook 的判斷
- [[Claude-Code-Windows-雙-shell-問題]] — 為何 hook command 要分 PowerShell / Git Bash 寫
