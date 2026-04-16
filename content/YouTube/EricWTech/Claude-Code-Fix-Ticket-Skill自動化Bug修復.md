---
title: AI Skill 取代 90% 初階工程師工作（Claude Code Agent Teams）
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-09
source: https://www.youtube.com/watch?v=PjenU4zwY5U
parent: "[[01.index]]"
---

## Fix Ticket Skill 概覽

一個自動化整個 bug fix pipeline 的 Claude Code skill，從 Jira ticket 到 Vercel 部署全自動：

1. 讀取 Jira ticket，理解 bug 描述
2. 用 Playwright CLI skill 在本機重現 bug
3. 研究 + 分析根因
4. 多 Agent 團隊協作規劃和實作修復
5. 多 Agent 程式碼審查（多角度、邊界情況）
6. Playwright CLI 驗證修復是否成功
7. 自動 commit 並 push
8. 監控 Vercel 部署狀態
9. 更新 Jira ticket，指派給 QA 工程師

## Skill 參數

```
/fix-ticket CAN-191
  --branch: main | new-branch | feature-branch | worktree
  --skip-review: false
  --skip-jira: false
  --skip-vercel: false
  --skip-qa-check: false
  --auto-commit: true
  --assign-to: <user>
```

## 八個執行階段

| 階段 | 說明 |
|------|------|
| 1. Branch Strategy | 確認在哪個 branch 操作 |
| 2. Read Ticket | 讀取 Jira ticket 和所有評論 |
| 3. QA Verify | 用 Playwright CLI 重現 bug，拍截圖確認 |
| 4. Research & Planning | 分析根因，生成 bug flow diagram，與用戶確認方向 |
| 5. Implementation | 實作修復，執行 build 和 linting 確認通過 |
| 6. Multi-Agent Review | 3 個 review agent 分別從不同角度審查（找 race condition、silent failure、edge case）|
| 7. QA Check | Playwright CLI 再次驗證修復有效 |
| 8. Vercel Deploy + Jira | 每 45 秒輪詢 Vercel 部署狀態，完成後在 Jira 留下詳細評論並指派 |

## 實際 Demo（BookZero.AI）

**Bug（CAN-191）：** 在交易頁面點擊「View」按鈕，應開啟收據詳情 dialog，但實際上跳轉到另一個頁面。

**根因分析：** agent 生成 bug flow diagram，找出觸發導航的 function，提出修復方案（直接在頁面 fetch receipt by ID 並開啟 dialog，避免跨頁導航）。

**Review 發現：**
- Agent 1：找到 race condition — view receipt 未清除舊資料
- Agent 2：找到 silent failure — 表單未正確處理空白欄位邊界情況
- Agent 3：額外邊界情況

所有問題修復後，Playwright 驗證通過，自動 commit 到 main branch。

## Skill 依賴項

- **Jira MCP** — 讀取和更新 ticket
- **Vercel MCP** — 監控部署狀態
- **Supabase MCP** — 管理測試用戶
- **Playwright CLI skill** — 瀏覽器自動化 QA

skill 結構：fix-ticket（mega skill）包含 dev-teams（規劃/實作/PR）、review-team（5 個 agent PR review）、review-fix（並行 review）、playwright-cli skill。

## 下載

作者 GitHub（startup cloud skills）提供所有 skills，可依自己的 Jira prefix（如把 `CAN` 改成自己的專案前綴）設定後直接使用。
