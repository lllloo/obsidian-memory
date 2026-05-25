---
title: Claude Code 完成提示（Windows）— 方案比較
created: 2026-05-25
updated: 2026-05-25
tags:
  - claude-code
  - hooks
  - windows
  - terminal
---

同時開多個 Claude Code 視窗時，要能一聲分辨「哪個跑完、哪個在等我」。Windows 上比較過三種做法，只有「鈴聲」穩定可行。

## 採用：單一 BEL 鈴聲 + 分頁鈴鐺圖示

完成或需要我注意時響一聲，Windows Terminal 會在對應分頁標上鈴鐺圖示，掃一眼就知道是哪個視窗。

做法：hook 輸出 `terminalSequence` 為單一 BEL（char 7），Claude Code 幫你寫到終端（需 v2.1.141+）。掛兩個事件才完整：

- `Stop` — 我回完話、等你輸入下一句
- `Notification`（不設 matcher）— 我中途跳權限確認或問你問題、暫停等你

兩個 hook 命令相同。只設 `Stop` 會漏掉掛機時跳出的權限提示。

Windows 撰寫兩個坑：①hook 用 args exec form 直接指定 `powershell.exe`（本機沒裝 `pwsh`；`shell:"powershell"` 的實際行為文件與版本說法不一——官方文件稱會 fallback 到 `powershell.exe`，明確指定最保險）；②命令維持純 ASCII（含中文／emoji 會被 Big5 弄壞，需改 `.ps1` + `-File` 並存 UTF-8 BOM）。

## 否決的方案

- **終端標題顯示進行中／完成** — Windows 上 Claude Code 會覆蓋 hook 設的標題（推測是它自己持續寫 title 序列，未經官方證實）；關閉用的 `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` 在 Windows 失效（issue #16572）、唯一可行工具只支援 macOS。
- **桌面 toast 通知** — 技術可行（WinRT `ToastNotificationManager`），但每次彈出太吵、不好讀。

## 來源

- GitHub issue [#4765](https://github.com/anthropics/claude-code/issues/4765)（標題覆蓋）、[#16572](https://github.com/anthropics/claude-code/issues/16572)（`DISABLE_TERMINAL_TITLE` 在 Windows 失效）、#22578 / #23355 / #44590
- [franzvill/claude-code-tab-title](https://github.com/franzvill/claude-code-tab-title)（macOS-only 工具）
- [Claude Code hooks reference](https://code.claude.com/docs/en/hooks-guide)（`terminalSequence` 欄位）

## 相關

- [[Claude-Code-規則系統設計]] — 規則升級到 Hook 的判斷
