---
title: "2026-06-03 Daily Updates"
created: 2026-06-03
updated: 2026-06-03
tags:
  - updates
  - claude-code
  - copilot
---

## Claude Code

### v2.1.153 · 2026-05-27（[Update 2.1.153](https://code.claude.com/docs/en/changelog#update-21153)）

> **繁中摘要**：v2.1.153 帶來大量 background agent、MCP、及 CLI 可靠性修復，並調整 `/model` 行為讓選擇預設持久化。

**變更重點**

- `/model` 現在會將選擇存為新 session 預設；按 `s` 只套用到當前 session。原 `modelPicker:setAsDefault` keybinding 改名為 `modelPicker:thisSessionOnly`，使用自訂 keybinding 的用戶需手動更新 `keybindings.json`
- `claude agents` autocomplete 現在也建議 native slash commands 和 bundled skills，不限 project skills
- Status line commands 新增 `COLUMNS`/`LINES` 環境變數，可依終端寬高調整輸出
- GitHub/git plugin marketplace source 新增 `skipLfs` 選項，可跳過 Git LFS 下載
- npm global install 無法自動更新時顯示一次性提示；`/doctor` 列出修復步驟
- 修復 custom API gateway 誤收到使用者 Anthropic OAuth credential 而非 gateway 自身 token（安全性回歸修復）
- 修復 subagent 的 `--strict-mcp-config`、`--bare`、remote mode 及 enterprise managed MCP 政策被忽略的問題
- 修復 `Agent` tool 使用 `subagent_type: 'claude'` 時在 gitignored 路徑寫入輸出可能被靜默丟棄
- 修復 stateful MCP servers（無 optional GET SSE stream）在 `tools/list` 上持續 reconnect-loop（v2.1.147 回歸）
- 修復 Windows PowerShell installer 實際失敗時仍顯示「Installation complete!」
- 修復 `claude update` 在 npm 安裝時忽略 release channel 設定，直接裝最新版
- 修復大量 background session bug：`/bg` 切換、`/btw` shortcuts、temp file 觸發敏感檔案提示、worktree 刪除後錯誤訊息截斷、`cmd+k` 重繪、IME 候選視窗位置、256-color 背景色溢出、`/copy` clipboard 失效等
- macOS background agents 現在在 Privacy & Security 顯示為「Claude Code」且升級後保留授權

**實務影響**

- 使用 `/model` 換模型後，選擇會自動持久化為預設——習慣每次手動選的用戶需注意行為改變；若只想換當前 session，按 `s`
- 有自訂 `modelPicker:setAsDefault` keybinding 者需立即更新 `keybindings.json`
- 使用 custom API gateway 的團隊：此版修復了 OAuth token 洩漏給 gateway 的安全問題，建議盡快升級
- `--strict-mcp-config` 現在正確限制 subagent MCP 使用，企業環境 MCP 政策執行更可靠
- npm global install 用戶若看到 update 提示，可按 `/doctor` 指引排查

**待追蹤**

- `modelPicker:thisSessionOnly` keybinding rename 需手動處理，未自動 migrate

### v2.1.161 · 2026-06-02（[Update 2.1.161](https://code.claude.com/docs/en/changelog#update-21161)）

> **繁中摘要**：v2.1.161 改善 parallel tool call 的失敗隔離、修復 MCP secrets 洩漏至終端的問題，並強化 OTEL 可觀測性與 Linux clipboard 支援。

**變更重點**

- Parallel tool calls：單一 Bash 指令失敗不再取消同批次其他 tool call，各自獨立回傳結果
- `OTEL_RESOURCE_ATTRIBUTES` 的值現在作為 metric datapoints 的 label，可依 team、repo 等自訂維度切片使用量
- 修復 `claude mcp` list/get/add 將 secrets 印至終端：`${VAR}` 引用不再展開，credential headers 和 URL secrets 改為遮罩顯示
- 修復 `forceLoginOrgUUID`/`forceLoginMethod` 政策誤封鎖 Bedrock、Vertex、Foundry、Mantle 等第三方 provider session（v2.1.146 回歸）
- 修復 background subagent 輸出污染 `claude -p` stdout（使用 `--output-format text` 或 `json` 時）
- 修復 Workflow agents 使用 `isolation: "worktree"` 在 background session 中被阻擋編輯自身 worktree 內的檔案
- 修復 background session 使用 daemon 環境的舊 model，而非 `settings.json` 指定的 model
- 修復 OpenTelemetry log events 在初始化完成前被靜默丟棄
- Linux fullscreen mode：clipboard 現在支援 `wl-copy`/`xclip`/`xsel`，同時複製到 clipboard 和 PRIMARY selection（支援中鍵貼上）
- `claude agents` 分散任務時顯示 `done/total` 進度；peek 顯示耗時最長的項目
- `/mcp` 折疊從未登入的 claude.ai connectors，減少介面噪音

**實務影響**

- parallel tool call 失敗隔離改善後，multi-tool agent task 更不容易因單一指令失敗而中斷全部
- 使用 OTEL 追蹤 Claude Code 用量的團隊現在可按自訂維度（如 team、repo）篩選，觀測能力大幅提升
- `claude mcp` secrets 洩漏修復屬安全性修補，使用 MCP 且有 credential headers 設定的用戶建議盡快升級
- 使用 Bedrock / Vertex / Foundry / Mantle 的企業用戶若升級至 v2.1.146 後 provider session 被封鎖，此版修復該問題
- `claude -p` 搭配 `--output-format text/json` 的自動化 pipeline 在此版前可能收到被污染的輸出，升級可修復

**待追蹤**

- Linux clipboard 支援新增 PRIMARY selection 行為，若舊腳本預期只寫 clipboard 需注意

---

## GitHub Changelog

### 2026-06-02（[GPT-4.1 deprecated](https://github.blog/changelog/2026-06-02-gpt-4-1-deprecated)）

> **繁中摘要**：GitHub Copilot 已於 2026 年 6 月 1 日正式棄用 GPT-4.1，涵蓋所有 Copilot 使用情境，需改用替代模型。

**變更重點**

- GPT-4.1 已於 2026-06-01 在 GitHub Copilot 全面棄用，包括 Copilot Chat、inline edits、ask/agent modes 及 code completions
- 官方建議遷移至替代模型（具體替代方案文中未明列，但棄用已生效）

**實務影響**

- 任何依賴 GPT-4.1 的 Copilot 工作流程（包括 IDE 外掛、agent mode、CLI）即日起失效，需切換至其他可用模型
- 若有透過 model picker 固定選 GPT-4.1 的設定，應立即調整

### 2026-06-02（[Expanded technical preview availability for the GitHub Copilot app](https://github.blog/changelog/2026-06-02-expanded-technical-preview-availability-for-the-github-copilot-app)）

> **繁中摘要**：GitHub Copilot 獨立 app 的 technical preview 現已開放所有 Copilot Pro、Pro+、Business、Enterprise 用戶存取，支援 Windows、macOS、Linux。

**變更重點**

- Copilot app technical preview 從原有封閉存取擴大至全部付費方案用戶（Pro、Pro+、Business、Enterprise）
- 提供 Windows、macOS、Linux 三平台下載

**實務影響**

- 原本沒有存取權的 Copilot 訂閱用戶現在可以試用獨立 Copilot app，無需等待邀請
- 可評估 Copilot app 作為 IDE 外掛以外的替代工作介面

**待追蹤**

- Technical preview 階段，穩定性與功能完整性尚未達 GA 水準

### 2026-06-02（[Copilot SDK is now generally available](https://github.blog/changelog/2026-06-02-copilot-sdk-is-now-generally-available)）

> **繁中摘要**：GitHub Copilot SDK 正式 GA，開發者現在可以將 Copilot 的 agentic engine 嵌入自己的應用、服務與 developer tools，並取得穩定 API 與正式支援。

**變更重點**

- Copilot SDK 從 preview 升為 generally available，具備穩定 API 與 production-ready 支援
- 允許將 Copilot agentic engine 嵌入第三方應用、服務和 developer tools

**實務影響**

- 可在自建工具中整合 Copilot agentic 能力，不再受限於 GitHub 官方介面
- GA 意味著 API 合約穩定，適合開始投入生產環境整合

### 2026-06-02（[Copilot CLI: Improved UI, rubber duck, prompt scheduling, and voice input](https://github.blog/changelog/2026-06-02-copilot-cli-improved-ui-rubber-duck-prompt-scheduling-and-voice-input)）

> **繁中摘要**：GitHub Copilot CLI 在 Microsoft Build 2026 推出重大更新，Rubber duck 模式、prompt scheduling 及 voice input 正式 GA；新的 tabbed terminal 介面進入 preview。

**變更重點**

- **Rubber duck**（GA）：可對 Copilot 解說問題以協助釐清思路
- **Prompt scheduling**（GA）：可排程執行 prompt，無需手動觸發
- **Voice input**（GA）：支援語音輸入指令
- **Tabbed terminal interface**（preview）：新的實驗性終端介面，支援多 tab

**實務影響**

- Prompt scheduling 對需要長時間執行或批次處理的 agent 任務尤其有用，可減少人工監管
- Voice input 改變 CLI 互動模式，適合 hands-free 或快速指令場景

**待追蹤**

- Tabbed terminal interface 仍為 preview，尚未達 GA 穩定度

### 2026-06-02（[Cloud and local sandboxes for GitHub Copilot now in public preview](https://github.blog/changelog/2026-06-02-cloud-and-local-sandboxes-for-github-copilot-now-in-public-preview)）

> **繁中摘要**：GitHub Copilot 現可在本地或雲端的隔離 sandbox 中執行工具，進入 public preview，降低 agent 執行對宿主環境的風險。

**變更重點**

- Copilot tool execution 現在可在本地 sandbox 或雲端 hosted sandbox 中隔離執行
- 兩種 sandbox 皆為 public preview

**實務影響**

- Agent mode 執行 shell commands、file edits 等工具時可限制在 sandbox，避免誤改本地環境
- 雲端 sandbox 讓 CI/CD 或無本地資源的場景也能安全執行 agentic 任務

**待追蹤**

- Public preview 階段，資源限制、支援平台與費用模型尚未確定

### 2026-06-02（[Shape Copilot code review around your team](https://github.blog/changelog/2026-06-02-shape-copilot-code-review-around-your-team)）

> **繁中摘要**：Copilot code review 現在支援 MCP server 整合與 agent skills 擴充，可在 PR review 過程中即時拉取 ticketing system、文件庫或監控儀表板的脈絡。

**變更重點**

- **MCP server support**（public preview）：code review 期間 Copilot 可連接 MCP server，從 ticketing systems、documentation、monitoring dashboards 拉取上下文
- **Agent skills**（public preview）：可用自定義工具擴充 Copilot 的 review 能力
- Review 深度會依 changeset 複雜度自動調整

**實務影響**

- Code review 流程可整合內部工具（如 Jira、Confluence、Datadog），讓 Copilot 的評論更具業務脈絡
- Agent skills 讓團隊可以客製化 review checklist 或強制特定規範

**待追蹤**

- MCP server support 與 agent skills 均為 public preview，API 與配置方式可能變動

### 2026-06-02（[Extend GitHub with agent apps](https://github.blog/changelog/2026-06-02-extend-github-with-agent-apps)）

> **繁中摘要**：GitHub 推出 Agent Apps 生態，第三方 AI agent 可從 Marketplace 安裝並直接在 issues、pull requests、discussions 中觸發，擴展 GitHub 工作流程的 agentic 能力。

**變更重點**

- Agent apps 作為新的 GitHub App 類型，可從 GitHub Marketplace 安裝
- 可由 issues、pull requests、discussions 觸發，整合進現有協作流程
- 由 GitHub 合作夥伴提供

**實務影響**

- 不需要離開 GitHub 介面即可在 issue/PR 中呼叫外部 AI agent（如自動化 triage、code generation、documentation）
- 開啟將自建或第三方 agent 嵌入 GitHub review/discussion 流程的可能性

**待追蹤**

- 合作夥伴生態與可用 agent apps 清單尚在建立中，實際可用選項有限

### 2026-06-02（[Gemini models in Copilot CLI, cloud agent, and the Copilot app](https://github.blog/changelog/2026-06-02-gemini-models-in-copilot-cli-cloud-agent-and-the-copilot-app)）

> **繁中摘要**：Gemini 3.1 Pro（Preview）與 Gemini 3.5 Flash 現在可在 Copilot CLI、Copilot cloud agent 及 Copilot app 中使用，擴大 GitHub Copilot 的可用模型選擇。

**變更重點**

- **Gemini 3.1 Pro**（Preview）與 **Gemini 3.5 Flash** 新增至以下 surfaces：Copilot CLI、Copilot cloud agent、GitHub Copilot app
- GPT-4.1 同期棄用（見另條），Gemini 系列為可選替代之一

**實務影響**

- 使用 Copilot CLI 或 cloud agent 的開發者可切換至 Gemini 模型，在特定任務上比較效果（如 Gemini 3.5 Flash 的速度優勢）
- Model picker 多了兩個非 OpenAI 選項，讓模型策略更有彈性

**待追蹤**

- Gemini 3.1 Pro 仍為 Preview，生產穩定性尚未確認
