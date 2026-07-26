---
title: "2026-07-26 Daily Updates"
created: 2026-07-26
updated: 2026-07-26
tags:
  - updates
  - codex
---

## OpenAI Codex

### 2026-07-21（[Codex CLI 0.145.0](https://learn.chatgpt.com/docs/changelog#2026-07-21)）

**繁中摘要**：Codex CLI 0.145.0 是一次大改版，新增分頁式對話歷史、跨工具設定遷移、Amazon Bedrock 支援與 multi-agent V2 穩定版，多項變更會直接影響日常 CLI 操作方式。

- **分頁式 thread history**：實驗性支援高效 resume、搜尋、持久命名，並整合 sub-agent 與 memories。
- **`/import` 擴充**：可從 Cursor、Claude Code 遷移設定、MCP servers、plugins、sessions、commands 與 project-scoped memories，換工具成本降低。
- **Amazon Bedrock 支援**：含 managed login、自訂 endpoint、認證，預設模型為 GPT-5.6 Sol。
- **Audio 輸入與 tool output**：支援常見本地音訊格式與 streaming realtime V3 對話。
- **Multi-agent V2 穩定化**：可設定 sub-agent 模型、reasoning level、並行度，角色與導航體驗改善。
- **Terminal UI**：新增安全、可點擊的 inline 視覺化連結。

---

### 2026-07-23（[ChatGPT Voice and multi-folder projects 26.715](https://learn.chatgpt.com/docs/changelog#2026-07-23)）

**繁中摘要**：ChatGPT 桌面版新增以 GPT-Live 驅動的 Voice 功能，可語音跨 Chat／Work／Codex 協調工作；本機 projects 也開放多資料夾管理，影響 Git 操作與設定檔探索的預設行為。

- **ChatGPT Voice**：桌面版可用語音在新對話或既有任務間下指令，涵蓋 Codex 任務調度；macOS 可開啟 Screen context 分享目前視窗畫面。
- **多資料夾 local projects**：可新增多個相關資料夾並指定 primary folder；primary folder 決定新對話、Git 操作與設定檔自動探索，其餘資料夾仍可存取檔案操作。

---
