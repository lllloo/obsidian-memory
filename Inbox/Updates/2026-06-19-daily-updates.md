---
title: "2026-06-19 Daily Updates"
created: 2026-06-19
updated: 2026-06-19
tags:
  - updates
  - copilot
---

## GitHub Changelog

### 2026-06-18（[Copilot code review: AGENTS.md support and UI improvements](https://github.blog/changelog/2026-06-18-copilot-code-review-agents-md-support-and-ui-improvements)）

**繁中摘要**：Copilot code review 正式支援 repository 層級的 AGENTS.md，讓 agent 行為可透過標準化規格檔控制；draft PR 的 review 入口也更易發現。

- **AGENTS.md 支援（GA）**：在 repo 根目錄放 AGENTS.md 即可定義 Copilot code review 行為，與其他支援 AGENTS.md 的 agent 工具規格統一。
- **Draft PR UI 改善**：新增 Request 按鈕，對 draft PR 發起 Copilot review 不再需要繞路。

### 2026-06-18（[Detecting Duplicate Issues – Public Preview and issue fields MCP support for GitHub Issues](https://github.blog/changelog/2026-06-18-duplicate-detection-and-issue-fields-mcp-support-for-github-issues)）

**繁中摘要**：GitHub Issues 新增兩項 AI 整合功能：重複 issue 自動偵測（Public Preview）與 issue fields 的 MCP 工具支援（GA），後者讓 AI agent 可透過 MCP 直接讀寫 issue 欄位。

- **重複 issue 偵測（Public Preview）**：GitHub 自動標記疑似重複的 issue，減輕大型 repo 維護者的 triage 負擔。
- **Issue fields MCP 支援（GA）**：AI agent 可透過 Model Context Protocol 存取與操作 issue fields，適合需要自動化 issue 管理的 agent workflow。

### 2026-06-18（[MAI-Code-1-Flash available on more Copilot surfaces](https://github.blog/changelog/2026-06-18-mai-code-1-flash-available-on-more-copilot-surfaces)）

**繁中摘要**：Microsoft 自研小型 coding model MAI-Code-1-Flash 現已擴展至更多 GitHub Copilot 介面，可直接在日常開發工具中切換使用。

- **新增支援介面**：Copilot CLI、GitHub Copilot app、Copilot Chat on GitHub、VS Code（Copilot Chat）均可選用 MAI-Code-1-Flash，過去僅限特定情境。
