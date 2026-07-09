---
title: "2026-07-09 Daily Updates"
created: 2026-07-09
updated: 2026-07-09
tags:
  - updates
  - copilot
  - gemini-cli
---

## GitHub Copilot

### VS Code v1.123–v1.127 · 2026-07-08（[GitHub Copilot in Visual Studio Code, June 2026 releases](https://github.blog/changelog/2026-07-08-github-copilot-in-visual-studio-code-june-2026-releases)）

**繁中摘要**：VS Code 版 Copilot 六月更新一次補齊 agentic 能力：Integrated Browser 工具 GA、可並排跑多 agent、並把 session credit 用量攤開來看，Anthropic 與 OpenAI 模型同步支援 1M context window。

- **Integrated Browser 工具 GA**：agent 可自主導覽頁面、擷取截圖、驗證 web app，新增 web search、相機／位置／麥克風權限控制；remote workspace 可 proxy HTTP(S)（public preview），也能把區域截圖丟進 agent chat。
- **Parallel Sessions**：同時並排跑多個 agent 任務、把大改動拆成聚焦 workstream，並以 grouping／drag-and-drop 重整 sessions。
- **Cost Visibility**：改看整段對話的 session credit 總用量（非單一 request），subagent 消耗分開追蹤，並有 status dashboard。
- **Model Management**：從 Language Models editor 探索並自 Marketplace 安裝 model provider 擴充，統一 picker 內調 context size 與 reasoning effort；官方 Ollama 擴充整合、Anthropic／OpenAI 模型支援 1M context window。
- **workflow 雜項**：session 同步到 GitHub 帳號可跨機器搜尋 coding history、自動生成 PR 標題與描述、MCP OAuth 憑證設定、擴充 auto-update 加兩小時安全延遲。

### 2026-07-07（[Codex as agent provider and agentic enhancements in JetBrains IDEs](https://github.blog/changelog/2026-07-07-codex-as-agent-provider-and-agentic-enhancements-in-jetbrains-ides)）

**繁中摘要**：JetBrains IDE 版 Copilot 把 Codex 納為新的 agent provider（public preview），並大幅擴充 CLI／MCP 與 approval 控制，等於在 JetBrains 裡把 Codex CLI 與 Copilot CLI 的 agent 設定收進同一介面。

- **Codex as agent provider**：安裝 Codex CLI、在 settings 設定路徑後即可從 agent picker 選 Codex。
- **Agent Customizations editor**：可管理 Hooks、直接管理 Copilot CLI 的 MCP servers（command／HTTP，含 start/stop/restart/uninstall），以 `.github/mcp.json` 定義 workspace 層級 MCP，並用 `/create-instruction`、`/create-prompt`、`/create-skill`、`/create-agent`、`/create-hook` 由 AI 生成檔案。
- **CLI approval 三模式**：Default Approvals（依政策）、Bypass Approvals（自動核准 tool call）、Autopilot Preview（自動核准並自動回答問題）；Claude sessions 另加 permission modes 與 debug logs。
- **其他**：Inline Chat GA、Next Edit Suggestions 加入 suggestion caching、Business/Enterprise 的 custom model 支援。

### 2026-07-07（退役日 2026-08-03）（[Copilot Billing Preview app will be retired on August 3](https://github.blog/changelog/2026-07-07-copilot-billing-preview-app-will-be-retired-on-august-3)）

**繁中摘要**：Copilot Billing Preview app 將於 2026-08-03 退役；原本靠它看 Copilot 花費的人要改用整合進 billing UI 的可見度功能。

- **Deprecation**：Billing Preview app 停用，花費檢視改走原生 billing UI（功能更完整），退役前記得把既有查花費流程搬過去。

---

## Gemini CLI

### v0.50.0 · 2026-07-08（[Gemini CLI changelog](https://geminicli.com/docs/changelogs/)）

**繁中摘要**：Gemini CLI 新增 Tool Registry Discovery，agent 啟動時會自動偵測並註冊環境中可用的 tools，減少手動設定 tool 的步驟；其餘為 release 驗證與 CI 穩定性的內部強化。

- **Tool Registry Discovery**：透過新的 discovery 能力自動偵測並註冊可用 tools，agent / tool 設定不再需要逐一手動掛載。
- **Release Verification & CI Stability**：驗證流程強化（檢查忽略 scripts、避免 workspace binary 衝突、阻擋有問題的 NPM releases），屬 CI 內部改善，對日常使用無直接影響。

---
