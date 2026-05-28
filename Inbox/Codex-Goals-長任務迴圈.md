---
title: Codex Goals 長任務迴圈
created: 2026-05-27
updated: 2026-05-28
source: https://www.youtube.com/watch?v=nOFordZCyzs
published: 2026-05-09
tags:
  - codex
  - claude-code
  - agentic
  - harness
---

Codex 的實驗性 `/goal` 指令把 **RALF loop**（Read-Act-Loop-Feedback，俗稱 Ralph loop）封裝成一行 slash command，不需外掛 orchestration layer 就能跑數小時的自主編碼任務——**目前最低門檻的長時間 agentic harness**。

## RALF loop 原理與 /goal 的升級

裸 RALF loop 在 Claude Code 裡就是一行 bash：`while true; do claude < prompt.md; done`。agent 每輪讀 `prompt.md`（目標 + 完成條件）與 `state.md`（已完成、還剩、嘗試到哪），跑一 turn 寫回 state，直到達成 completion criteria。優點是簡單，缺點是沒有 budget 管理、crash recovery、deliverable audit。

`/goal` 的關鍵升級是**停止條件從「程式化迭代上限」改成「LLM 判斷目標達成」**。持續提示明確要求：不要把代理信號當完成依據，只有目標真正達成、無待完成工作時才標 complete。並補上裸 loop 缺的 scaffolding（兩個對使用者隱形的 markdown：`continuation.md`、`budget_limit.md`），每個 turn 走四條路徑之一：

- 還有工作、budget 充足 → 續跑下一 turn
- 接近 token cap → 注入 `budget_limit.md`，優雅收尾出 final report 列剩餘工作，升額後可續
- 完成 → 呼叫 `update_goal` audit deliverables，全數通過才標 complete
- 暫停 / 編輯 goal / crash → graceful handling（裸 loop 會直接斷）

## 成敗不在 /goal，在前置 plan

跑很久 ≠ 結果好（有人跑 50 小時但完成度未必更高）。**人類價值集中在 plan 階段鎖定 acceptance criteria**：

- 用 plan mode 把模糊想法收斂成非常具體的 end result。
- **完成條件必須可量化**，不能是「make me a SaaS that makes a billion dollars」。
- **verification 段落要列真正能驗的步驟**（`npm run build`、起 dev server、Playwright 互動驗證）——沒收緊，goal 會在「看似完成」就停手出半成品。
- **前期對齊**：不要直接貼 prompt，先跟 agent 訪談（專案是什麼、自己在意什麼、壞 UX 長怎樣、試過的解法、常見 bug），讓 model 提問確認理解再開始。
- 好的目標規模：大於單一 prompt，但小於開放性 backlog。

陷阱：每個 goal run 綁定當前 thread，同專案跑第二次**必須開新 thread**（想像成開新 terminal）。

## 範圍邊界：Mission 概念

`/goal` 適合數小時的 coding 任務。**數週/數月、無即時可驗證結果的長期水平目標**（SEO 策略、廣告 ROI）超出其範圍 → 用 Mission：`mission.md` 定義要優化的指標，agent 提假設、執行一步、輸出 artifacts，然後**排程下次執行**（數小時到數週後）而非立即重複；新 session 接收 mission.md + 上次步驟摘要，不確定時向人發訊。

## 與 Claude Code 並用

不該二選一。推薦組合：**Claude Code 做 plan → 丟 Codex `/goal` 跑 → Claude Code review → 來回協作**。Codex 桌面版 inline 顯示 asset / 狀態，比純 terminal 觀察 long-running task 順手；Codex 是 OpenAI 產品內建 image gen。Claude Code 要做到一樣需自接 orchestration layer（如串 Higgsfield 補圖像生成）。

## 相關

- [[Harness-Engineering]] — `/goal` 是長任務 harness 的最低門檻封裝
- [[Ticket-驅動的-Agent-協作]] — 更高一層的多 ticket 協作拓撲
- [[codex-plugin-cc]] — Codex 在 Claude Code 內的整合
