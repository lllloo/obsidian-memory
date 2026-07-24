---
title: "2026-07-24 Daily Updates"
created: 2026-07-24
updated: 2026-07-24
tags:
  - updates
  - copilot
  - codex
  - gemini-cli
---

## GitHub Copilot

### 2026-07-23（[Copilot cloud agent for Linear is now generally available](https://github.blog/changelog/2026-07-23-copilot-cloud-agent-for-linear-is-now-generally-available)）

**繁中摘要**：GitHub Copilot cloud agent 現可直接透過 Linear 指派 issue 觸發，正式脫離 preview 進入 GA。

- **Linear 整合**：在 Linear 把 issue 指派給 Copilot cloud agent，即可觸發非同步、自主的背景 agent 分析 issue 內容並開始處理。

---

### 2026-07-23（[GitHub MCP Server supports the next MCP specification](https://github.blog/changelog/2026-07-23-github-mcp-server-supports-the-next-mcp-specification)）

**繁中摘要**：MCP 協定將於 2026-07-28 起改為 stateless，GitHub MCP Server 已提前支援新規格；使用 GitHub MCP Server 的 client 需留意此協定轉換以免屆時相容性中斷。

- **Stateless 轉換**：新的 stateless core 提前上線因應官方規格轉換時程。

---

### 2026-07-23（[Agent automation controls in GitHub Issues in public preview](https://github.blog/changelog/2026-07-23-agent-automation-controls-in-github-issues-in-public-preview)）

**繁中摘要**：GitHub Issues 新增 agent automation controls 公開預覽，讓使用者在 agent 自動標籤／指派／關閉 issue 前先看到理由並可審核。

- **可審核性**：每次 agent automation 變更 issue（label、type、assignee、close）都會顯示原因，並可在套用前 review。

---

## OpenAI Codex

### 2026-07-23（[ChatGPT Voice and multi-folder projects 26.715](https://learn.chatgpt.com/docs/changelog)）

**繁中摘要**：ChatGPT desktop app 新增 GPT-Live 語音模式協調 Chat／Work／Codex 間任務，並讓本機 project 支援多資料夾與 primary 資料夾指定。

- **Voice 模式**：可在新 chat 或 task 中啟動語音、跨 thread 下達指令；macOS 支援畫面情境分享（顯示作用中視窗截圖）；涵蓋 Plus/Pro/Business/Edu/Enterprise（desktop 與 iOS Remote）。
- **多資料夾 project**：本機 project 現可關聯多個資料夾並指定 primary，primary 資料夾用於 chat／Git 操作與設定檔自動探索，其餘資料夾仍可做檔案操作。

---

## Gemini CLI

### v0.52.0 · 2026-07-22（[Gemini CLI Changelogs](https://geminicli.com/docs/changelogs/)）

**繁中摘要**：Gemini CLI 補強 caretaker triage/egress 基礎模組、簡化寫入操作的驗證邏輯，並改善帳號權限錯誤訊息。

- **Triage/Egress**：新增 triage worker 模組與 egress action publisher，含 GitHub Action handler 支援。
- **寫入行為**：JSON/IPYNB 寫入跳過 LLM correction；plan mode 的相對路徑寫入政策簡化。
- **Auth**：帳號缺 Code Assist tier access 時提供更明確錯誤訊息；`google-auth-library` 更新至 v10.9.0。

---
