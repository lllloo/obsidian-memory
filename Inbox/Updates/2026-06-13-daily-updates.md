---
title: "2026-06-13 Daily Updates"
created: 2026-06-13
updated: 2026-06-13
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## Claude Code

### v2.1.175 · 2026-06-12（[Changelog](https://code.claude.com/docs/en/changelog#2-1-175)）

**繁中摘要**：新增 `enforceAvailableModels` managed setting，讓 allowlist 同時約束 Default model 的解析結果，防止使用者或專案設定繞過管理員的模型限制。

- **`enforceAvailableModels` 新設定**：啟用後，若 Default model 解析到不在 `availableModels` 清單的模型，會自動 fallback 到第一個允許的模型；使用者或專案層級設定無法再擴充 managed allowlist，適合企業強制鎖定可用模型時使用。

### v2.1.174 · 2026-06-12（[Changelog](https://code.claude.com/docs/en/changelog#2-1-174)）

**繁中摘要**：大量 bug fix 版本，含 Bedrock GovCloud region 設定錯誤、背景 session 繼承錯誤 provider 環境變數等影響企業部署的問題；VSCode 新增細粒度用量歸因介面。

- **VSCode `/usage` 強化**：新增 cache misses、long context、subagents、per-skill/agent/plugin/MCP 的用量細目（24h / 7d），方便追蹤費用來源。
- **Bedrock GovCloud 修正**：`us-gov-*` region 原本推導出錯誤的 inference profile prefix（`global` 而非 `us-gov`），導致 400 錯誤，現已修正。
- **背景 session 環境隔離**：修正背景 daemon 從啟動 shell 繼承另一個 session 的 `ANTHROPIC_*` 環境變數（gateway URL、custom headers、`/model` aliases）的問題。
- **`/model` picker 修正**：修正 Default model 對應的 model family 被隱藏、Fable 5 計費 banner 錯誤顯示於企業帳號、以及被 allowlist 擋住的 advisor model 被預選等問題。
- **Skill hot-reload 優化**：單一 skill 變更時不再重送完整清單，只重新通知變動的 skill。

### v2.1.170 · 2026-06-09（[Changelog](https://code.claude.com/docs/en/changelog#2-1-170)）

**繁中摘要**：推出 Claude Fable 5（Mythos-class），能力超越既有所有 GA 模型；更新至此版本即可存取。同時修正從 VS Code 整合終端或繼承 Claude Code 環境變數的 shell 啟動時，session transcript 不儲存、無法 `--resume` 的問題。

- **Claude Fable 5 GA**：Mythos-class 模型，Anthropic 稱其能力超越所有既有 GA 模型；已通過安全審核供一般用途，更新至 v2.1.170 即可選用。
- **VS Code 終端 transcript 修正**：修正從 VS Code integrated terminal 啟動的 session 不儲存 transcript 的 regression。

### v2.1.169 · 2026-06-08（[Changelog](https://code.claude.com/docs/en/changelog#2-1-169)）

**繁中摘要**：多項企業與自架部署強化：self-hosted runner 新增 `post-session` hook、`--safe-mode` 除錯模式、`/cd` 切換工作目錄；修正 managed MCP 政策在首次安裝時未強制套用的安全問題。

- **`post-session` lifecycle hook**（self-hosted runner）：session 結束、workspace 刪除前執行，可用於快照未提交工作或匯出 log。
- **`--safe-mode` / `CLAUDE_CODE_SAFE_MODE`**：啟動時停用所有自訂（CLAUDE.md、plugins、skills、hooks、MCP servers），方便除錯。
- **`/cd` 指令**：在不中斷 prompt cache 的情況下切換 session 工作目錄。
- **`disableBundledSkills` 設定**：隱藏內建 skills、workflows 與 slash commands，適合需要完全自訂指令集的部署。
- **Managed MCP 政策修正**（重要安全）：`allowedMcpServers`/`deniedMcpServers` 在 reconnect、IDE 設定、`--mcp-config` 及首次安裝後第一個 session 中未被強制套用的問題已修正。
- **Vertex/Foundry 預設 idle timeout 恢復**：設為 5 分鐘，避免 stream 卡住無限等待；可用 `API_FORCE_IDLE_TIMEOUT=0` 停用。

### v2.1.166 · 2026-06-06（[Changelog](https://code.claude.com/docs/en/changelog#2-1-166)）

**繁中摘要**：新增 `fallbackModel` 設定讓主模型過載時自動切換；強化跨 session 訊息安全性，防止 `SendMessage` 傳遞的訊息攜帶使用者權限。

- **`fallbackModel` 設定**：可指定最多三個備用模型依序嘗試，適用互動與 `-p` 模式；`--fallback-model` CLI flag 同步支援互動 session。
- **跨 session 訊息安全強化**：透過 `SendMessage` 從其他 Claude session 傳入的訊息不再具備 user authority，接收方拒絕轉傳的 permission request，auto mode 也會阻擋，防止 session 間權限升級。
- **Deny rule glob 支援**：tool-name 位置支援 glob pattern（如 `"*"` 拒絕所有工具），增強細粒度控制。
- **Thinking 關閉行為統一**：`MAX_THINKING_TOKENS=0`、`--thinking disabled`、以及 per-model toggle 現在對預設會思考的 Claude API 模型也能正確停用 thinking（第三方 provider 不受影響）。

---

## OpenAI Codex

### v0.139.0 · 2026-06-09（[Changelog](https://developers.openai.com/codex/changelog#codex-cli-0-139-0)）

**繁中摘要**：Code mode 新增直接呼叫 web search 的能力；MCP tool schema 相容性提升；plugin marketplace 自動化更豐富。

- **Code mode web search**：可直接呼叫 standalone web search，包含從巢狀 JavaScript tool call 中呼叫，回傳純文字結果。
- **MCP schema 相容性**：tool 與 connector input schema 現保留 `oneOf`/`allOf`，大型 schema 壓縮時保留更多淺層結構，改善與複雜 MCP tool 的相容性。
- **Plugin marketplace 改進**：`codex plugin marketplace list --json` 現包含各 marketplace 來源；可在背景刷新前先從快取回傳結果。
- **Bug fixes**：`codex resume --last` 與 `codex fork --last` 正確處理 trailing argument；MCP 啟動警告保持在所屬 thread；thread reset 不再丟失 cloud-managed requirements。

### v0.138.0 · 2026-06-08（[Changelog](https://developers.openai.com/codex/changelog#codex-cli-0-138-0)）

**繁中摘要**：`/app` 指令可將 CLI thread 轉移到 Codex Desktop（macOS / Windows）；本機圖片附件與生成圖片現在向模型揭露儲存路徑，改善後續編輯可靠性。

- **`/app` handoff**：可將目前 CLI thread 移交至 Codex Desktop（macOS 與 Windows），保持對話連續性。
- **圖片路徑揭露**：本機附件與 standalone 生成圖片的儲存路徑會傳給模型，讓後續 `file reference` 與編輯更可靠。
- **Reasoning effort 彈性化**：TUI 為遺失 `Alt` binding 的終端補充 fallback 快捷鍵；model-defined effort level 按模型通告的順序傳遞。
- **Plugin 結構化輸出**：add/remove 與 marketplace 指令支援 `--json`。

---

## GitHub Changelog

### 2026-06-12（[Copilot code review: New configurations and controls](https://github.blog/changelog/2026-06-12-copilot-code-review-new-configurations-and-controls)）

**繁中摘要**：Copilot code review 新增組織層級 runner 控制、content exclusion 支援，以及移除 repository custom instructions 的字元限制，讓企業客製化更彈性。

- **Organization runner controls**：管理員可設定 Copilot code review 允許使用的 runner 類型。
- **Content exclusion**：可排除特定檔案或 glob pattern，不納入 Copilot code review 分析。
- **Custom instructions 字元限制移除**：repository 層級的自訂指示不再有字元上限，可提供更詳細的審查指引。

---
