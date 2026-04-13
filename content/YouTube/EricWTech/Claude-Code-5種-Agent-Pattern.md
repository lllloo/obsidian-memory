---
title: Claude Code 搭配這 5 種 Agent Pattern 效果更好
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-10
source: https://www.youtube.com/watch?v=DIHIllggaTw
---

## 重點摘要

5 種 Claude Code Agent Pattern，從簡單到全自動：

1. **Sequential Flow（循序流）**：Agent 依序完成任務，每步驟一個接著一個。適合有明確前後依賴的工作流（如：bug fix pipeline — Jira ticket → Playwright 重現 → 研究 → 修復 → 審查 → 部署）。仍可內嵌 sub agent，但任務必須依序執行。

2. **Split & Merge（拆分合併）**：將大任務拆給多個 sub agent 平行執行，完成後合併回 orchestrator。適合可平行化的任務（如：DB audit — 分別審查 schema、安全性、query 效能，各自用 Supabase MCP 操作，最後彙整報告）。可用於 PR review，同時觸發多個專項 reviewer agent。

3. **Agent Teams（代理人團隊）**：比 sub agent 多了 shared communication，各 agent 間可互相溝通。有 double advocate 角色挑戰其他 agent 的決定。適合任務組件彼此關聯（如前後端需協調的功能）；若任務互相獨立則不適用。

4. **Operator / Git Worktrees**：為每個 Claude Code session 建立隔離環境。可同時開多個 terminal 跑不同 session，各自在獨立 worktree 執行，互不衝突。用途：A/B 測試不同 UI 或功能實作，選最佳結果合回 main branch。

5. **Headless Mode（無頭模式）**：最常用。用 `claude -p "<prompt>"` 在背景執行，不需進入互動 session。可排程、結合 skills 組成全自動流程。搭配 **Ralph Loop** 可讓 agent 持續迴圈直到條件達成（如：iterative review — 跑 5 次 iteration，每次 fresh context window，spin up 5-7 sub agent，最後彙整成單一報告）。
