---
title: "2026-07-01 Daily Updates"
created: 2026-07-01
updated: 2026-07-01
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## Claude Code

### v2.1.197 · 2026-06-30（[Release](https://github.com/anthropics/claude-code/releases/tag/v2.1.197)）

**繁中摘要**：Claude Sonnet 5 成為 Claude Code 的預設模型，帶原生 1M-token context window；升到此版即可使用。發表時附促銷定價（$2/$10 per Mtok），有期限，實際費率以官方公告為準。

- **預設模型換成 Sonnet 5**：升版後不指定模型即用 Sonnet 5；原生 1M-token context 讓長脈絡工作不必再靠外部拆分。
- **促銷定價有時效**：發表時標示 $2/$10 per Mtok 的限時優惠，屬階段性方案；長期成本規劃以 Anthropic pricing 頁為準，不要把促銷價當常態。

---

### v2.1.196 · 2026-06-29（[Release](https://github.com/anthropics/claude-code/releases/tag/v2.1.196)）

**繁中摘要**：這版重點在組織治理與背景工作可靠度——新增組織預設模型、收緊 `claude mcp list/get` 對 repo 自我核可 MCP server 的信任，並讓長時間背景 session／agent 在程序被停止或更新後自動接續（含 Windows）。另有一批 CLI 與 UI 修補。

- **組織預設模型**：admin 於 org console 設定後，使用者未自選模型時 `/model` 會顯示為「Org default」／「Role default」，統一團隊模型基準。
- **MCP 信任收緊（security）**：`claude mcp list`/`get` 不再自動啟動由 repo committed `.claude/settings.json` 自我核可的 `.mcp.json` server；未受信任的 workspace 顯示 `⏸ Pending approval`，避免被 repo 夾帶啟動未授權 server。
- **背景工作存活性**：長跑命令／workflow 在 session 程序被停止、重啟或更新後仍存活（Windows 改用交接而非直接砍背景 shell）；被 daemon 重啟砍掉的背景 agent 下次開啟 agents view 會從中斷點自動 resume。
- **streaming idle watchdog 全 provider 預設開啟**：回應串流 5 分鐘無事件即中止並重試；以 `CLAUDE_ENABLE_STREAM_WATCHDOG=0` 關閉。
- **Remote Control 限縮到 Anthropic host**：`ANTHROPIC_BASE_URL` 指向非 Anthropic host 時停用 Remote Control，與 Bedrock／Vertex／Foundry 既有行為一致。
- **一批 CLI 修補**：修 `/context` 在 Bedrock 顯示 0 tokens、`/deep-research` 把 verifier 失敗誤報成「all claims refuted」、MCP OAuth 在未指定 scope 時索取整份 `scopes_supported` 導致 GitLab 自架等 IdP `invalid_scope`、PowerShell `git diff`/`grep` 等 exit 1 被誤判為失敗。

---

## OpenAI Codex

### rust-v0.142.2 · 2026-06-25（[Release](https://github.com/openai/codex/releases/tag/rust-v0.142.2)）

**繁中摘要**：穩定版新功能以 MCP 與代理設定為主——MCP tools 在支援時預設走 tool search 改善工具發現，macOS client 可尊重系統 proxy（含 PAC／WPAD），並修一批 remote MCP／image 與權限相關問題。

- **MCP tool search 預設啟用**：在支援的 model／provider 上，MCP tools 預設用 tool search 做工具發現，同時保留對舊 model／provider 的相容性。
- **macOS 系統 proxy 支援**：macOS 認證 client 在啟用 `respect_system_proxy` 時可套用系統 proxy、PAC、WPAD 設定。
- **remote MCP／image 修補**：remote stdio MCP server 接受遠端平台格式的絕對工作目錄路徑；remote image 輸入改回傳 model 可見的驗證錯誤（本地 image 仍支援）。
- **權限與安全**：PowerShell 指令若含無法檢視的 AST 區段一律要求使用者核可；Bedrock 憑證過期改給可操作的復原指引而非泛用授權錯誤；同步更新 OpenSSL、esbuild 至修補版本。

---

### rust-v0.142.1 · 2026-06-25（[Release](https://github.com/openai/codex/releases/tag/rust-v0.142.1)）

**繁中摘要**：新增 opt-in 的 Windows 系統 proxy 支援，涵蓋 PAC、WPAD、靜態 proxy 與 bypass 規則，讓企業網路環境下的認證更順。

- **Windows 系統 proxy（opt-in）**：認證流程可套用 Windows 系統 proxy 設定，含 PAC／WPAD 自動偵測、靜態 proxy 與 bypass rules。

---

## GitHub Copilot

### 2026-06-30（[Claude Sonnet 5 is generally available for GitHub Copilot](https://github.blog/changelog/2026-06-30-claude-sonnet-5-is-generally-available-for-github-copilot)）

**繁中摘要**：Anthropic 最新的 Sonnet-class 模型 Claude Sonnet 5 對 GitHub Copilot GA，補上一個兼顧日常開發與 agentic workflow 的 Sonnet 級選項。

- **Sonnet 5 上架 Copilot**：可在 model picker 選用，定位為日常 coding 與 agentic workflow 的 Sonnet-class 選項；企業環境仍受管理員模型政策約束。

---

### 2026-06-30（[Copilot Agent is now available in JetBrains AI Assistant](https://github.blog/changelog/2026-06-30-copilot-agent-is-now-available-in-jetbrains-ai-assistant)）

**繁中摘要**：JetBrains 與 GitHub 深化整合，讓 GitHub Copilot 的 agent 能力進入 JetBrains AI Assistant，既有 Copilot plugin 使用者可在 JetBrains IDE 內用 agentic 流程。

- **Copilot Agent 進 JetBrains**：在 JetBrains AI Assistant 內取得 Copilot 的 agent 能力，讓 IntelliJ 系 IDE 使用者不必離開 IDE 就能跑 agentic coding。
