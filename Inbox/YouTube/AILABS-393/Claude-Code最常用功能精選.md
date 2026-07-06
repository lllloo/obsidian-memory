---
title: AI Labs 精選：最常用的 Claude Code 功能
description: AI Labs 團隊實測後精選最常用的 Claude Code 功能，涵蓋 agent teams、advisor、goal、auto mode、worktree 隔離、code review 系列、loop 與 monitor。
created: 2026-07-06
updated: 2026-07-06
source: https://www.youtube.com/watch?v=ECQA6oOyfIk
published: 2026-06-29
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - workflow
  - sub-agent
---

## 背景脈絡

- Claude Code 半年內已釋出上百個功能，但實際建構時多數設定成本太高、真正常用的沒幾個。
- Claude Code 對非技術者（HR、會計、招募）不友善；為省成本不發每人 $20 方案，改建一個 chat 平台，用 **Claude Agent SDK + Haiku**（便宜、對這些任務表現夠好）透過 API 提供，含 MCP 連接與各部門知識/workflow。
- 建平台最難的是**認證**：影片用 sponsor ScaleKit 當單一登入中間層，讓 agent 以連接使用者身分登入多個 app（Slack、Gmail、Notion），統一管理憑證、做 role-based access，並記錄每個 agent 的每個 action。

## Agent Teams

- 藏在需先設定一次的隱藏 flag 後才出現。
- 用 **tmux** 開多個 Claude Code session 並排在同一視窗，再把任務分派給這些 session。
- 與 sub-agents 的差別：team 內的 agent **能互相溝通**、來回分享發現、協調任務，這是 sub-agent 做不到的。
- 特別適合 adversarial review：一個 agent 找問題、另一個實作修正，兩者協作、平行進行（相對於「一個寫進 doc、另一個讀」的序列做法，會失去 Claude Code 擅長的平行性）。屬 token 很重的 workflow。

## Advisor

- 讓 Claude Code 卡住需要建議時諮詢更強的模型，即使主 agent 用小模型也能提升表現。
- experimental、仍在 preview、token 重。
- 作者設 **Opus 4.8**（錄影時最強）為 advisor、**Sonnet** 為主要實作 agent。建 chatbot 遇到解不了的問題時，弱模型會呼叫 advisor 取得該走的路徑再完成實作；advisor 也會前瞻找出未來可能出問題處並回報。

## Goal

- 為長時間任務而生：指定完成條件與 metric（end state）當作目標，模型持續工作直到達成。
- 由較小、較弱的模型（如 **Haiku**）做 cross-check，確認 app/功能是否照需求建好且實際可運作。
- 跑 `goal` 指令可看目前 active 的 goal。

## Auto mode

- 是 `dangerously-skip-permissions` 的長任務**溫和替代**：給你一個中間地帶——比 skip permissions 少很多 permission prompt、風險也低很多。
- 靠 **classifier** 審查每個 action，攔截危險命令（大量刪資料、敏感資料外洩、跑惡意碼）；skip permissions 則會全部自動放行。

## Sub-agent 隔離（Git worktree 層級）

- 一個 flag，開啟後 sub-agent 預設 spawn 在各自隔離的 **worktree**，每個變更都在自己的獨立目錄、與其他隔離。
- 常用於測試同一功能的多個變體（如 UI）；HTML mock-up 沒接後端，若要測含資料與認證的完整 flow 就用 worktree。
- 設定後給 prompt、指定要 spawn 幾個 sub-agent，等各自完成後回報；再從喜歡的變體 merge 進主設計、其餘丟棄。

## Code review 系列指令

- **security review**：依一組預定 guideline 跑完整安全審查。建 chatbot 時常用，因需防 prompt injection——尤其給了 agent bash 工具（可在系統執行命令）。
- **simplify**：審 reusability、simplification、efficiency，依創作者的嚴格規則精簡程式碼、清掉不再使用的殘餘。
- **code review**：找 bug 與可更有效率之處。
- **ultra review**（近期推出）：啟動 cloud agent 在雲端跑審查，拆成多個 branch、各自獨立驗證，因此比本地檢查抓到更深的問題。
- 這些都基於 Claude Code 創作者自己 workflow 中用的 skill 與指令。

## Loop

- 本質是 cron job：設定時間，讓它按排程重複跑同一個 prompt。
- 只在 session 活著時運行，session 結束就停。
- 例：知識庫存在 **ChromaDB**（公司流程 docs 存成 vector embedding，即把文字轉成數字讓 agent 依語意搜尋），設 loop 每天結束跑 ingest 指令更新；可跑雲端或本地（雲端的好處是不需保持 session 活躍）。
- 相對傳統 cron 的好處：若遇任何錯誤，它能自行 cross-check、修正、確保任務正確完成，不需人介入。

## Monitor

- 給它一個監控目標（logs、running process），它只在發現異常時回報，正常則安靜地背景運行。
- 設定監控前，Claude 會先了解 app 與 agent，判斷可能發生哪些異常（如 agent 偏離預定 workflow、tool call 失敗、一次從 Notion/Gmail 文件載入過多資料、role-based 權限問題）。
- 例：開發測試 app 時讓 agent 留 log、請 Claude 背景 monitor，回報如 Gmail fetch 工具的失敗 tool call，快速定位並修正問題。
