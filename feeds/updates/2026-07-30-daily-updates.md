---
title: "2026-07-30 Daily Updates"
created: 2026-07-30
updated: 2026-07-30
tags:
  - updates
  - copilot
  - opencode
  - gemini-cli
---

## GitHub Copilot

### 2026-07-29（[Copilot code review: Agent skills and MCP now generally available](https://github.blog/changelog/2026-07-29-copilot-code-review-agent-skills-and-mcp-now-generally-available)）

**繁中摘要**：Copilot code review 對 agent skills 與 MCP servers 的支援從 public preview 轉為正式 GA，Pro、Pro+、Business、Enterprise 全數方案皆可用。

- **範圍擴大**：code review 流程現在可掛載自訂 agent skills 與 MCP server 作為審查輸入，非僅 preview 使用者可用。

---

### 2026-07-29（[Default model enablement for Copilot Business and Enterprise](https://github.blog/changelog/2026-07-29-default-model-enablement-for-copilot-business-and-enterprise)）

**繁中摘要**：Business／Enterprise 方案改為全域預設啟用所有 GA 模型，admin 不用再逐一手動開啟新模型。

- **行為變更**：新上線的 GA 模型會自動對組織可見，需要限制模型選項的 admin 須改為主動關閉不要的模型，而非等待手動開啟。

---

## OpenCode

### v1.18.8（2026-07-28）

**繁中摘要**：Core 端改善與新版 MCP 伺服器、OAuth 流程的相容性，並修正舊行為。

- **MCP／OAuth**：MCP 伺服器可自動重新連接、支援自訂 OAuth 回呼埠，且不再送出已棄用的 sampling 預設值，降低與新版 MCP server 對接時的相容性問題。

---

## Gemini CLI

### v0.53.0（2026-07-28）

**繁中摘要**：本版聚焦維運自動化與安全強化，新增 eval 覆蓋率報表指令，並加固 workspace trust 與 loop 防護。

- **Eval Coverage Reporting**：新增指令產生 evaluation coverage report。
- **Security & Loop Mitigations**：強化 workspace trust、在 A2A server 內做 task isolation，並防止無限 ReAct 迴圈／prompt injection 造成的失控迴圈。

---
