---
title: "2026-05-27 Daily Updates"
created: 2026-05-27
updated: 2026-05-27
tags:
  - updates
  - copilot
  - codex
---

## GitHub Changelog

### 2026-05-26（[Copilot Memory has more controls for deletion, scope, and the Copilot CLI](https://github.blog/changelog/2026-05-26-copilot-memory-has-more-controls-for-deletion-scope-and-the-copilot-cli)）

> **繁中摘要**：Copilot Memory 新增細粒度刪除控制、repository 層級關閉開關，並將記憶管理功能延伸至 Copilot CLI；目前仍為 public preview。

**變更重點**

- 使用者可對 Copilot Memory 中的個別記憶項目進行精細刪除操作
- 新增 repository 層級的記憶關閉開關，可針對特定 repo 停用 Copilot Memory
- Copilot CLI 納入更多記憶控制指令，無需切換到 Web UI 即可管理

**實務影響**

- 對於有隱私或合規需求的 repo，可在 repo 層級停用記憶功能，不影響其他 repo
- CLI-first workflow 的開發者可直接在終端機管理記憶，不需要打開瀏覽器

---

### 2026-05-26（[Target Copilot models to organizations with model rules](https://github.blog/changelog/2026-05-26-target-copilot-models-to-organizations-with-model-rules)）

> **繁中摘要**：GitHub Enterprise 管理員現在可以透過 model rules，針對不同組織設定不同的可用 Copilot 模型清單，實現細粒度的模型治理。

**變更重點**

- Enterprise owner 可為不同 organization 指定各自允許的 Copilot 模型集合
- 取代了之前只能全企業統一設定的方式，支援 org 層級的差異化模型策略

**實務影響**

- 有多個業務單位的大型企業可按需隔離模型存取，例如讓部分 org 使用較新或實驗性模型
- 對開發者工具選型影響不大，主要是企業 IT 管控面的改進

---

## OpenAI Codex

### v0.134.0 · 2026-05-26（[Codex CLI 0.134.0](https://developers.openai.com/codex/changelog#codex-cli-01340)）

> **繁中摘要**：Codex CLI 0.134.0 帶來本地對話歷史搜尋、MCP 設定強化（per-server 環境變數、OAuth）、read-only MCP 工具並發執行，以及 hook context 延伸，整體提升 MCP 與 extension 的可用性。

**變更重點**

- 新增本地對話歷史搜尋，支援大小寫不敏感匹配與結果預覽
- `--profile` 成為主要 profile 選擇器，統一 CLI、TUI permissions 與 sandbox flows
- MCP 設定改進：支援 per-server 環境變數目標指定，HTTP server 支援 OAuth 選項
- Connector tool schema 強化：保留本地 `$ref`/`$defs` 結構，並自動壓縮過大的 schema
- 標記 `readOnlyHint` 的 MCP 工具現在可以並發執行
- Hook context 延伸，extension tools 和 subagent 現在可取得對話歷史與 subagent identity

**實務影響**

- 有多個 MCP server 的設定中，read-only 工具並發執行可顯著減少等待時間
- OAuth 支援讓 HTTP-based MCP server 的認證流程更完整，適合串接需要授權的外部服務
- Hook context 有對話歷史後，extension 工具可以做更多有狀態的決策

**安裝**

```bash
npm install -g @openai/codex@0.134.0
```

---
