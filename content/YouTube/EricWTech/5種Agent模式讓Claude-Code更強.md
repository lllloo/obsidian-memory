---
title: "用這 5 種 Agent 模式讓 Claude Code 更強"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-10
source: https://youtu.be/DIHIllggaTw
---

**影片描述**：本影片介紹五種 Claude Code Agent 模式，從最簡單到完全自主，幫助開發者告別「一次一個任務」的瓶頸，改以多 Agent 並行架構大幅提升效率。作者曾任 Amazon、Microsoft 資深 AI 軟體工程師，以實際使用案例逐一示範每種模式的觸發方式與應用場景。

**重點摘要：**
- **Sequential Flow（順序流程）**：讓 Agent 依序執行任務，範例為 `fix tickets` 技能，自動完成讀取 Jira ticket → Playwright 重現 bug → 研究實作 → 多 Agent 審查 → 驗證 → commit → 部署 → 推進 QA 的完整流水線。
- **Split & Merge（分割合併）**：將大任務拆給多個 sub-agent 並行處理後合併，範例包括資料庫稽核（schema/安全性/查詢效能同時跑）及 PR 多角度並行審查，優勢是速度更快且避免 context 污染。
- **Agent Teams（Agent 團隊）**：與 sub-agent 最大差異在於各 Agent 之間有**共享通訊管道**，適合跨元件協作任務（如前後端同步開發同一功能），可設置 devil's advocate 角色持續挑戰決策；若各 Agent 工作完全獨立則不適合。
- **Operator（Git Worktrees 隔離）**：為每個 Claude Code session 建立獨立環境，可同時開多個 worktree 各跑不同任務，實用於 A/B 測試 UI 變體，選出最佳結果後直接丟棄其他，同時降低出錯風險。
- **Headless Mode（無頭模式）**：作者最愛的模式，用 `claude -p "prompt"` 在終端機背景執行，不需進入互動 session；可搭配 cron 排程或 Ruff Loop 讓 Agent 持續迴圈執行直到達成目標。
- **實際案例 — iterative review**：作者封裝的技能指定執行 5 次迭代，每次 headless session 觸發 5-7 個 sub-agent 並行審查，每個 session 擁有全新 context window，最終彙整所有迭代發現成單一報告。
- 各 Agent 模式可**任意組合**，例如在 headless session 內同時跑 split & merge，進一步提升自動化程度。
- 作者強調使用這些模式的核心目標：讓 Claude Code 在你離開後仍能自行運作，把手動干預降到最低。
