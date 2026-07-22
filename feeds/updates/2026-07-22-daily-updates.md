---
title: "2026-07-22 Daily Updates"
created: 2026-07-22
updated: 2026-07-22
tags:
  - updates
  - copilot
  - codex
---

## GitHub Copilot

### 2026-07-21（[Gemini 3.6 Flash is now available in GitHub Copilot](https://github.blog/changelog/2026-07-21-gemini-3-6-flash-is-now-available-in-github-copilot)）

**繁中摘要**：GitHub Copilot 新增 Gemini 3.6 Flash 模型選項，鎖定網頁／應用程式開發、程式撰寫與長時程 agentic 任務。

- **Gemini 3.6 Flash 上線**：Google 最新 Flash 模型現於 Copilot 逐步推出，具可設定選項，適合長時程 agent 任務。

### 2026-07-20（[Copilot users can now see AI credits used per billing cycle](https://github.blog/changelog/2026-07-20-copilot-users-can-now-see-ai-credits-used-per-billing-cycle)）

**繁中摘要**：Copilot Business／Enterprise 使用者現可在用量頁查看本計費週期已用掉的 AI credits，即使沒有個人預算上限也能看到。

- **AI credits 用量可視化**：新增查看本期已用 AI credits 的入口，方便追蹤用量與預算規劃。

---

## OpenAI Codex

### v0.145.0 · 2026-07-21（[Codex CLI 0.145.0](https://learn.chatgpt.com/docs/changelog#2026-07-21-codex-cli-0-145-0)）

**繁中摘要**：Codex CLI 0.145.0 是一次大更新，新增分頁式對話歷史、跨工具設定搬遷、Amazon Bedrock 登入支援與穩定版多代理 V2，全面強化長時間工作流與多來源整合。

- **Paginated thread history**：實驗性分頁式對話歷史，支援高效 resume、搜尋、命名與 sub-agent。
- **`/import` 擴充**：可搬遷 Cursor 與 Claude Code 的設定、MCP servers、plugins、sessions、commands 與 project-scoped memories。
- **Amazon Bedrock 支援**：新增 Bedrock 登入、自訂 endpoint 與驗證，預設模型為 GPT-5.6 Sol。
- **多代理 V2 穩定版**：可設定 sub-agent 模型、reasoning 等級與並行數，導覽體驗改善。
- **音訊輸入／輸出與 realtime V3**：支援本機音訊格式與串流 realtime 對話。
- 另修復多項問題，包含分支保留對話狀態、MCP 啟動可靠性，與 Windows 執行／沙箱穩定性。

### v0.144.6 · 2026-07-18（[Codex CLI 0.144.6](https://learn.chatgpt.com/docs/changelog#2026-07-18-codex-cli-0-144-6)）

**繁中摘要**：Codex CLI 0.144.6 更正 GPT-5.6 Sol／Terra／Luna 的官方 context window 為 272,000 tokens，並同步刷新內建說明。

- **Context window 更正**：先前文件標示錯誤，實際上限為 272,000 tokens，規劃長對話或大量上下文時應以此為準。

### v0.144.5 · 2026-07-16（[Codex CLI 0.144.5](https://learn.chatgpt.com/docs/changelog#2026-07-16-codex-cli-0-144-5)）

**繁中摘要**：Codex CLI 0.144.5 強化危險指令偵測，涵蓋更多強制刪除（`rm` 系列）變體，並讓指令被拒絕時的說明更清楚。

- **危險指令偵測加強**：新增對多種 forced `rm` 變體的偵測，降低誤放行破壞性操作的風險。

---
