---
title: "2026-08-02 Daily Updates"
created: 2026-08-02
updated: 2026-08-02
tags:
  - updates
  - codex
  - copilot
  - opencode
---

## OpenAI Codex

### 2026-07-31（[GPT-5.4 and GPT-5.4 mini retire from Codex on August 31](https://learn.chatgpt.com/docs/changelog)）

**繁中摘要**：GPT-5.4 與 GPT-5.4 mini 將於 2026-08-31 從 ChatGPT 登入的 Codex 中下架，API key 驗證的 Codex session 與 OpenAI API 不受影響；官方建議改用 `gpt-5.6-terra`（取代 GPT-5.4）與 `gpt-5.6-luna`（取代 GPT-5.4 mini）。

- **Deprecation**：deadline 前需檢查並更新 workspace 預設模型、已存模型設定、managed configuration、custom agent 與排程任務中沿用舊模型的地方，否則到期會失效。

### 2026-07-30（[Browser upgrades, multi-repository review, and image editing 26.727](https://learn.chatgpt.com/docs/changelog)）

**繁中摘要**：ChatGPT/Codex 桌面用戶端 26.727 版新增跨資料夾的 multi-repository 專案程式碼審查能力，並升級瀏覽器（address bar 歷史搜尋、Google 整合、Chrome 擴充功能 tab mention）與圖片生成/編輯體驗。

- **Multi-repo code review**：可在單一 project 內橫跨多個資料夾（repo）審查程式碼變更，影響多 repo 專案的 workflow。
- 另含 Windows 安裝穩定性與多項效能修復。

### 2026-07-29（[Codex CLI 0.146.0](https://learn.chatgpt.com/docs/changelog)）

**繁中摘要**：Codex CLI 0.146.0 是重點功能釋出：新增具名 session、thread pinning、可分頁且支援 fork 的歷史紀錄，並支援 Agent Plugins manifest、Amazon Bedrock 與 Claude Code marketplace 相容性。

- **Agent Plugins / marketplace 相容**：可載入符合 Agent Plugins manifest 的外掛，並相容 Amazon Bedrock 與 Claude Code marketplace 生態。
- **Session 管理**：具名 session、thread pinning、分頁歷史與 fork，改善長期多任務追蹤。
- 另擴充 standalone web search、executor-provided skills discovery，並強化 proxy 設定（認證、外掛、MCP 授權、遠端執行、WebSocket）。

### 2026-07-29（[Sign in with ChatGPT (beta)](https://learn.chatgpt.com/docs/changelog)）

**繁中摘要**：「Sign in with ChatGPT」開始於 Airtable、GitLab、HubSpot、Notion、Supabase、Vercel 等 plugin 對象進行 beta 推出，讓使用者以 ChatGPT 帳號登入第三方服務；plugin 端僅取得姓名、email 與大頭貼，實際存取權限仍需使用者另行核可。

- **Connector 登入**：涉及 GitLab、Vercel 等開發相關服務的第三方 OAuth 整合，屬 connector 認證變更。

---

## GitHub Copilot

### 2026-07-28（[GitHub Copilot app usage metrics now expand across report rollups](https://github.blog/changelog/2026-07-28-github-copilot-app-usage-metrics-now-expand-across-report-rollups)）

**繁中摘要**：GitHub Copilot app 使用量現在涵蓋更多 Copilot usage metrics API 報表範圍，個別 app 活動會歸戶到 enterprise-user 與 organization-user 報表中的對應使用者。

- **Usage 報表擴大**：管理員可在既有 usage/billing 報表中看到更完整的 app 層級使用歸戶，屬 billing/quota 追蹤相關變更。

---

## OpenCode

### v1.18.11 · 2026-08-01（[Changelog](https://opencode.ai/changelog)）

**繁中摘要**：v1.18.11 修正 MCP SSE 連線在伺服器回錯誤時卡在 reconnect loop 的問題，並修好使用 `reasoning_text` 等自訂欄位名的 interleaved reasoning provider 設定；Desktop 端則是外部連結開啟行為、tab 狀態顯示與檔案樹等多項小修復。

- **MCP 連線穩定性**：修正 SSE reconnect loop 卡死，影響仰賴 MCP server 的工作流程穩定性。
- **Reasoning 欄位相容**：修正部分 provider 使用非標準 reasoning 欄位名時的解析問題。
- 另有多項 Desktop 端 UI/穩定性修復（外部連結開啟方式、tab 狀態、檔案樹 resize、debug gutter 對齊）。

---
