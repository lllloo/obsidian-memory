---
title: Claude Code zshrc 快捷指令三層設定
created: 2026-05-20
updated: 2026-05-20
source: https://www.youtube.com/watch?v=tj2ZI0r-xQ8
published: 2026-05-15
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - terminal
---

> [!info] 影片定位
> Dustin 示範用三層 shell alias 取代每次啟動 Claude Code / Codex 時都要重打的 `--dangerously-skip-permissions` / YOLO mode 等長指令；重點不是 shell 語法本身，而是「請 Claude Code 直接幫你改 `.zshrc`」這個操作模式。

## 痛點

- 每次起 Claude Code 都要打 `claude --dangerously-skip-permissions`（bypass mode）。
- 切到 Codex 還要重打 YOLO flag 或 `-p` 等變數。
- 不同專案還得先 `cd` 過去再執行 → 摩擦累積。

## 第一層：基本 cc / cdx 快捷指令

- 目標：打 `cc` → 等同 bypass mode 完整指令；打 `cdx` → 等同 Codex YOLO mode 完整指令。
- Mac 用 `.zshrc`；Windows 對應 PowerShell profile 或 `.bashrc`。
- 操作方式：直接跟 Claude Code 講「我要設定 alias，打 cc 或 cdx 就執行那一串指令，請寫進 `.zshrc` 並讓它生效」。
- Claude 會自動寫入定義 alias 的那段 shell 程式碼。

## 第二層：cdx + 資料夾名一鍵導航

- 目標：`cdx <資料夾名>` → 不需要先 cd，直接跳到該專案目錄並啟動 Codex 或 Claude Code。
- 操作：先做完第一層基本 alias 後，再請 Claude Code 補上「找路徑」邏輯。
- Claude 會加入一段尋找資料夾路徑的程式碼。
- 對非根目錄專案：明確跟 Claude 講「我的專案放在二層、三層位置」，請它處理多層搜尋。

## 第三層：自訂變數切換多家模型 API

- 痛點：除了 Anthropic 官方 Claude，有時想用 MiniMax M2、GLM、Kimi、DeepSeek、Qwen 等模型透過 Anthropic 相容 endpoint 接 Claude Code。
- 目標：打 `cc mini` → 走 MiniMax；`cc glm` → 走 GLM；無 flag → 走官方 Claude。
- 操作：請 Claude Code 上網查各家 API 的 Anthropic 相容接入方式，再幫你改 alias，加入「依參數設不同環境變數」的邏輯。
- Codex 端可比照辦理。

## 操作關鍵

- 不必懂 shell 語法，全程用自然語言指令給 Claude Code，由它代寫 `.zshrc`。
- 步調是「初階 → 中階 → 進階」分層做：每層都先驗證再進下一層，比一次性 prompt 完整需求穩定。
- 設定完一次，之後啟動 Claude Code / Codex / 切資料夾 / 切模型都剩兩三個字母。

## 核心啟示

- Claude Code 不只是寫專案程式碼的工具，也適合幫你改自己的 dotfiles / shell 環境，是「用 AI 改 AI 的啟動方式」。
- 分層設定是好習慣：先求基礎 alias 對，再加路徑導航，再加多模型切換；每層都讓 Claude 修改後立即在 terminal 驗證。
- Anthropic 相容 endpoint 讓 Claude Code 成為通用 CLI 殼，模型可換但工作介面不變。
