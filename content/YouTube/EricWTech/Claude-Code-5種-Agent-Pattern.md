---
title: Claude Code 搭配這 5 種 Agent Pattern 效果更好
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-10
source: https://www.youtube.com/watch?v=DIHIllggaTw
---

## Pattern 1：Sequential Flow（循序流）

Agent 依序完成任務，每步驟接著一個執行。

**適合情境：** 任務有明確前後依賴關係。

**實際範例 — Bug Fix Pipeline（`fix-tickets` skill）：**
1. 用 Jira MCP 讀取 ticket
2. 觸發 Playwright CLI 重現 bug
3. 研究解法
4. 實作修復
5. 用不同 sub agent（前端、後端、測試）分別 review
6. 再次用 Playwright 驗證
7. Commit → Deploy → 推送到 QA

注意：可以在各步驟內嵌 sub agent（例如讓研究步驟另開 sub agent 節省 context），但整體任務仍依序進行。

## Pattern 2：Split & Merge（拆分合併）

將大任務拆給多個 sub agent 平行執行，完成後合併回 orchestrator。

**適合情境：** 任務可平行化（各部分互相獨立）。

**實際範例 1 — DB Audit（`db-audit` skill）：**
- Sub agent A：審查 schema
- Sub agent B：審查安全性
- Sub agent C：查找 query 效能問題、建議加索引
- 各自透過 Supabase MCP 操作，最後彙整成一份報告

**實際範例 2 — PR Review：**
- 同時觸發多個專項 reviewer agent（code quality、silent failures、tests、design、scalability）
- 也可觸發 8 個平行 reviewer 自動 review + 自動修復（hellas 模式）

## Pattern 3：Agent Teams（代理人團隊）

比 sub agent 更進一步：各 agent 之間有 **shared communication**，可互相溝通。

**關鍵差異：** Sub agent 之間無溝通；Agent Teams 有共享溝通頻道 + double advocate 角色（挑戰其他 agent 的決策，類似 senior/staff engineer 角色）。

**適合情境：** 任務組件互相關聯，需要協調（例如同一功能的前後端需要溝通）。

**不適合情境：** 各 agent 任務完全獨立，不需要溝通（用 Split & Merge 即可）。

**實際範例：**
- `review-teams` skill：4 個專項 reviewer + 1 個 double advocate 共同 review PR
- `spec-teams` skill：多個 agent 平行研究同一主題，彙整後聚合成完整分析

## Pattern 4：Operator（Git Worktrees 隔離環境）

為每個 Claude Code session 建立隔離環境（git worktree），各 session 互不衝突。

**核心用途：**
- 同時開多個 terminal session，每個跑獨立的 Claude Code
- 各 session 可以用前面任何 pattern（sequential、split & merge、agent teams）
- 不喜歡某個 worktree 的結果 → 直接刪掉，不影響其他 session

**實際應用 — A/B 測試：**
- Session A：生成 landing page 版本 1
- Session B：生成 landing page 版本 2
- Session C：生成 landing page 版本 3
- 比較三個結果，選最好的 merge 回 main branch

```bash
# 建立 worktree
git worktree add ../feature-a feature-a
git worktree add ../feature-b feature-b

# 刪除不要的 worktree
git worktree remove ../feature-a
```

## Pattern 5：Headless Mode（無頭自主執行）

最自主的模式，讓 Claude Code 在背景自動執行，不需在互動式 session 中等待。

**基本指令：**
```bash
# 提供 prompt，在背景執行，結果輸出到 terminal
claude -p "你的任務描述"

# 搭配 --dangerously-skip-permissions 完全自動
claude --dangerously-skip-permissions -p "任務"
```

**為何強大：** 可排程執行、觸發條件執行、或搭配 loop 自動循環直到完成。

**實際範例 — Iterative Review（`iterative-review` skill）：**
1. 指定 PR URL 或 branch name，設定迭代 5 次
2. 每次迭代：headless 指令觸發 5–7 個 sub agent 平行 review（每個都有新鮮 context window）
3. 每輪完成後彙整 findings
4. 5 輪全跑完後聚合成單一報告

```bash
# 排程每天 7:00 AM 執行
# 在 Claude session 內下指令讓它排程
claude -p "每天早上7點執行 review-skill on main branch"
```

**搭配 Loop 使用：** 設定「持續執行直到 bug 修復」，讓 Claude 自己循環，直到觸發 breakpoint 條件才停止。

4. **Operator / Git Worktrees**：為每個 Claude Code session 建立隔離環境。可同時開多個 terminal 跑不同 session，各自在獨立 worktree 執行，互不衝突。用途：A/B 測試不同 UI 或功能實作，選最佳結果合回 main branch。

5. **Headless Mode（無頭模式）**：最常用。用 `claude -p "<prompt>"` 在背景執行，不需進入互動 session。可排程、結合 skills 組成全自動流程。搭配 **Ralph Loop** 可讓 agent 持續迴圈直到條件達成（如：iterative review — 跑 5 次 iteration，每次 fresh context window，spin up 5-7 sub agent，最後彙整成單一報告）。
