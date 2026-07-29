---
title: "2026-07-29 Daily Updates"
created: 2026-07-29
updated: 2026-07-29
tags:
  - updates
  - copilot
  - opencode
---

## GitHub Copilot

### 2026-07-28（[Grok 4.5 is now available in GitHub Copilot](https://github.blog/changelog/2026-07-28-grok-4-5-is-now-available-in-github-copilot)）

**繁中摘要**：GitHub Copilot 新增 xAI 的 Grok 4.5 作為可選模型，主打快速的 agentic coding 與複雜多步驟工作流，多了一個模型選擇。

- **新模型上線**：Grok 4.5 現於 GitHub Copilot 中逐步開放，設計用於快速、agentic 的程式撰寫與複雜多步驟工作流，官方稱其支援長達 2M tokens 的上下文窗口。

### 2026-07-27（[GitHub Copilot for JetBrains adds improved OpenTelemetry configuration and model management](https://github.blog/changelog/2026-07-27-github-copilot-for-jetbrains-adds-improvved-opentelemetry-configuration-and-model-management)）

**繁中摘要**：GitHub Copilot for JetBrains 更新強化了 MCP 伺服器／自訂 agent 整合、telemetry 設定與模型管理，讓 JetBrains 內的 agent workflow 更好調整與觀測。

- **MCP 與自訂 agent**：可在 Claude agent flows 中連接 MCP 伺服器與自訂 agent。
- **OpenTelemetry 設定**：新增更細緻的 telemetry 配置選項，方便觀測與除錯。
- **模型管理**：提供更直接的模型管理介面，方便切換與設定可用模型。

---

## OpenCode

### v1.18.9 · 2026-07-28

**繁中摘要**：OpenCode v1.18.9 修復了與舊版 MCP SDK client 的相容性問題，桌面應用端也修了多個穩定性與 UI bug，並預覽新的 V2 桌面側邊欄與模型 provider 分區。

- **MCP 相容性修復**：核心層恢復與舊版 MCP SDK clients 的相容性，避免舊版 MCP client 連線失敗。
- **桌面穩定性修復**：修正 Solid cleanup 錯誤與主頁會話加載問題，避免桌面導航損壞、會話列表需暫停頁面才能更新，另移除 V2 項目檢視多餘的垂直邊框。
- **V2 介面預覽**：新增選擇性 V2 桌面側邊欄（由捆綁 CLI 服務支援）與 V2 設置中可折疊的模型 provider 分區。

---
