---
title: Claude Code 完成提示（Windows）— 方案比較
created: 2026-05-25
updated: 2026-05-27
tags:
  - claude-code
  - hooks
  - windows
  - terminal
---

多視窗時一眼看出哪個 Claude Code 在跑。採用 OSC 9;4 工作列進度條，inline 在 `settings.json`，不需外部腳本。

## 設定

```json
"hooks": {
  "SessionStart":    [{"hooks": [{"type": "command", "command": "powershell.exe", "args": ["-NoProfile", "-Command", "$e=[char]27;$b=[char]7;@{terminalSequence=\"$e]9;4;0;0$b\"}|ConvertTo-Json -Compress"]}]}],
  "UserPromptSubmit":[{"hooks": [{"type": "command", "command": "powershell.exe", "args": ["-NoProfile", "-Command", "$e=[char]27;$b=[char]7;@{terminalSequence=\"$e]9;4;3;0$b\"}|ConvertTo-Json -Compress"]}]}],
  "Stop":            [{"hooks": [{"type": "command", "command": "powershell.exe", "args": ["-NoProfile", "-Command", "$e=[char]27;$b=[char]7;@{terminalSequence=\"$e]9;4;0;0$b\"}|ConvertTo-Json -Compress"]}]}]
}
```

| event | state | 視覺效果 |
|---|---|---|
| `SessionStart` | 0 | 清除 |
| `UserPromptSubmit` | 3 | 旋轉動畫 |
| `Stop` | 0 | 清除 |

**Notification 不加**：包含 `idle_prompt`（閒置自動觸發），會造成工作列莫名變黃。需要的話加 `"matcher": "permission_prompt"` 篩選。

OSC 9;4 state 速查：`0` 清除、`1` 綠色、`2` 紅色、`3` 旋轉、`4` 黃色暫停。格式：`ESC]9;4;<state>;<progress>BEL`。

## 需求

- CC ≥ 2.1.141
- Windows Terminal

## 備選方案

**分頁標題 emoji（OSC 2）**：double-click rename 後鎖死標題；emoji 不可 inline（cp950 亂碼）；`$Host.UI.RawUI.WindowTitle` 在 hook 子進程讀到 PS 自身路徑而非分頁標題。

**桌面 toast 通知（OSC 9）**：用 `ESC]9;訊息BEL` 彈出系統通知，切到其他視窗時也看得到。Windows Terminal 原生支援，可與 OSC 9;4 並用。缺點：每次完成都彈出、較吵。

## 相關

- [[Claude-Code-規則系統設計]] — 規則升級到 Hook 的判斷
