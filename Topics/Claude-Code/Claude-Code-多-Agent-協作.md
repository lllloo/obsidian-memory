---
title: Claude Code 多 Agent 協作
created: 2026-04-24
updated: 2026-06-23
tags:
  - claude-code
  - workflow
---

四種多 agent 機制按「想做什麼」對應，**不是疊加越多越好**——選錯機制比少用一個更傷效率。版本相依細節（env name、`/branch` vs `/fork` alias 行為、subagent fork 啟用條件）以官方 docs 為準。

## 該怎麼選

| 想做什麼 | 用 | 為什麼 |
|---|---|---|
| 單點研究 / 審查 / 隔離輸出 | **Subagent** | 獨立 context 不繼承主對話，結果回主線；適合用後即丟 |
| 多人分工 / 平行 review-fix / 長任務 | **Agent Teams** | 各自獨立 context 但共享 task list / mailbox 可互傳訊 |
| 中途開支線 / 不想重講背景 | **Forked subagent** | 繼承當前 session 對話，最後回主線；省 prompt-context 重建成本 |
| 多 agent 同時改檔避免互踩 | 上述 + **Git worktrees** | 每 agent 各有 working tree；subagent 沒留下變更時 worktree 自動清掉 |

## 怎麼啟用 / 觸發

- **Subagent**：Claude 依 description 自動 delegate；用 session 內 `/agents` slash command 列出、管理或建立自訂（`claude agents` CLI 則是開 agent view 監控／派發背景 session，不是列 subagent 定義）
- **Agent Teams**：experimental，需先在 settings 啟用；之後自然語言告訴 Claude「create an agent team」即可
- **Forked subagent**：experimental，需啟用 fork mode；用 `/fork <directive>` 觸發（未啟用時 `/fork` = `/branch` 只分對話不 spawn）
- **Git worktrees**：`claude --worktree <name>` CLI flag，或 subagent frontmatter `isolation: worktree`

實際 env var 名、版本要求、`/fork` 在不同 mode 下行為差異請查官方 docs（會隨版本變動）。

## 踩坑

- **Subagent vs Forked subagent 容易混**：差別只在「要不要繼承當前對話」——要從零開始選 Subagent，要接著聊選 Forked subagent
- **Agent Teams 不是跨家族 LLM**：teammate 是獨立 Claude Code session（可混搭 Sonnet / Opus / Haiku），但仍是 Claude 家族；想跨家族（GPT / Gemini）獨立視角看 [[bookmark-codex-plugin-cc-Codex整合外掛|codex-plugin-cc]]
- **worktree 不解決 race condition**：兩個 agent 改不同檔不互踩沒錯，但改同一個邏輯區塊（如 schema migration）還是會撞——分支策略要先想好
- **單一 session 內的模型分層 ≠ 多 agent**：不想開多 agent、只想讓 Opus 在 Sonnet 卡住時介入，採「顧問↔執行者持續諮詢」模式（非平行 spawn）

## 相關

- [[Ticket-驅動的-Agent-協作]] — 比機制層高一層的協作拓撲：人管 ticket 而非管 session，agent 在 ticket 層工作回報
