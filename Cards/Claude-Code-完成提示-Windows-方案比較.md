---
title: Claude Code 完成提示（Windows）— 方案比較
created: 2026-05-25
updated: 2026-06-01
tags:
  - claude-code
  - hooks
  - windows
  - terminal
---

多視窗時一眼看出哪個 Claude Code 在跑。採用 OSC 9;4 工作列進度條，inline 在 `settings.json` 的 `hooks`，不需外部腳本。

## 設定

`command` 用 `printf` 直接吐 JSON 字面字串——ESC、BEL 以 JSON unicode escape 寫進字串原樣輸出，交給 Claude Code 解析成控制字元，省掉每次起 `powershell.exe` 子進程，啟動更快。Windows 走 Git Bash 內建的 `printf`。

```json
"hooks": {
  "SessionStart":     [{"hooks": [{"type": "command", "command": "printf '%s' '{\"terminalSequence\":\"\\u001b]9;4;0;0\\u0007\"}'"}]}],
  "UserPromptSubmit": [{"hooks": [{"type": "command", "command": "printf '%s' '{\"terminalSequence\":\"\\u001b]9;4;3;0\\u0007\"}'"}]}],
  "PostToolUse":      [{"hooks": [{"type": "command", "command": "printf '%s' '{\"terminalSequence\":\"\\u001b]9;4;3;0\\u0007\"}'"}]}],
  "Notification":     [{"matcher": "permission_prompt", "hooks": [{"type": "command", "command": "printf '%s' '{\"terminalSequence\":\"\\u001b]9;4;4;100\\u0007\"}'"}]}],
  "Stop":             [{"hooks": [{"type": "command", "command": "printf '%s' '{\"terminalSequence\":\"\\u001b]9;4;0;0\\u0007\"}'"}]}]
}
```

| event | matcher | state;progress | 視覺效果 |
|---|---|---|---|
| `SessionStart` | — | `0;0` | 清除 |
| `UserPromptSubmit` | — | `3;0` | 旋轉動畫（開始跑） |
| `PostToolUse` | — | `3;0` | 旋轉（每次工具後重申，避免被覆蓋） |
| `Notification` | `permission_prompt` | `4;100` | 黃色滿格暫停（等你點頭） |
| `Stop` | — | `0;0` | 清除（跑完） |

**Notification 用 `matcher` 精準篩選**：`Notification` 也含 `idle_prompt`（閒置自動觸發），不篩會造成工作列莫名變黃。`"matcher": "permission_prompt"` 只在等待權限確認時亮黃色暫停，正是想要的「需要你介入」訊號。

OSC 9;4 state 速查：`0` 清除、`1` 綠色、`2` 紅色、`3` 旋轉、`4` 黃色暫停。格式：`ESC]9;4;<state>;<progress>BEL`。

## 卡住狀態清除

`$PROFILE` 綁 `Esc` 目前實測無效，不列入可靠方案。Claude Code 執行時 `Esc` 會先送進 Claude Code 本身，不會觸發 PowerShell 的 PSReadLine key handler，因此下面這種設定不能用來穩定清掉 Windows Terminal 的 OSC 9;4 狀態：

```powershell
Set-PSReadLineKeyHandler -Key Escape -BriefDescription ClearTerminalProgress -LongDescription "Clear Windows Terminal OSC 9;4 progress indicator and revert the current line." -ScriptBlock {
    [Console]::Write([char]27 + "]9;4;0;0" + [char]7)
    [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
}
```

比較實用的補救點是在回到 shell prompt 時清除：如果 Claude Code 已退出或中斷後進度仍卡住，讓 prompt 每次重新顯示時送一次清除序列。

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
- hook `command` 經 `sh` 執行，Windows 用 Git Bash 內建 `printf`

## 備選方案

**PowerShell 產生序列**：舊版用 `powershell.exe -Command "$e=[char]27;...|ConvertTo-Json"` 產真 ESC 再轉 JSON。可行但每次 hook 都起 PowerShell 子進程，慢。`printf` 版把 escape 當字面字串丟給 CC 自己解析，更輕。

**分頁標題 emoji（OSC 2）**：double-click rename 後鎖死標題；emoji 不可 inline（cp950 亂碼）；`$Host.UI.RawUI.WindowTitle` 在 hook 子進程讀到 PS 自身路徑而非分頁標題。

**桌面 toast 通知（OSC 9）**：用 `ESC]9;訊息BEL` 彈出系統通知，切到其他視窗時也看得到。Windows Terminal 原生支援，可與 OSC 9;4 並用。缺點：每次完成都彈出、較吵。

## 相關

- [[Claude-Code-規則系統設計]] — 規則升級到 Hook 的判斷
- [[Claude-Code-Windows-雙-shell-問題]] — 為何 hook command 要分 PowerShell / Git Bash 寫
