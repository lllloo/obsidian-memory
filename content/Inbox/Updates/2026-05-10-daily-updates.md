---
title: "2026-05-10 Daily Updates"
created: 2026-05-10
updated: 2026-05-10
tags:
  - updates
  - claude-code
  - codex
  - gemini-cli
  - copilot
  - opencode
---

## Claude Code

### v2.1.133 · 2026-05-07（[changelog](https://code.claude.com/docs/en/changelog#21133)）

> **繁中摘要**：v2.1.133 新增 worktree branch 起點設定、sandbox binary 路徑自訂、hooks effort level 注入，並修正多個並發 session、MCP OAuth、skill 探索等重要 bug。

**變更重點**
- 新增 `worktree.baseRef` 設定（`fresh` | `head`）：控制 `--worktree`、`EnterWorktree`、agent-isolation worktree 從 `origin/<default>` 或 local HEAD 分支
- 新增 `sandbox.bwrapPath` 與 `sandbox.socatPath` managed settings（Linux/WSL）：自訂 bubblewrap 與 socat binary 路徑
- 新增 `parentSettingsBehavior` admin-tier key：讓 admin 可將 SDK `managedSettings` 納入 policy merge
- Hooks 現在透過 `effort.level` JSON 欄位與 `$CLAUDE_EFFORT` env var 接收目前的 effort level
- 修正並發 session 在 refresh-token race 後全部 401 dead-end 的問題
- 修正 Edit/Write allow rules 對 drive root 的錯誤匹配
- 修正 HTTP(S)_PROXY/NO_PROXY/mTLS 在完整 MCP OAuth flow 中未被尊重的問題
- 修正 subagents 無法透過 Skill tool 探索 project、user、plugin skills 的問題
- 修正 `/effort` 在某個 session 意外改動其他並發 session effort level 的問題
- 修正 Remote Control stop/interrupt 無法完全取消 CLI session 的問題

**實務影響**
- `worktree.baseRef: head` 讓 worktree 從本地 HEAD 分支，適合多層 agent 並行開發流程
- Hooks 可依 effort level 動態調整行為（如 max effort 時觸發更嚴格的稽核 hook）
- Subagent skill 探索修正對使用 `/ob`、`/vault-check` 等 skill 的 subagent 流程有直接影響
- 多並發 session 用戶不再被 token race 打斷

### v2.1.132 · 2026-05-06（[changelog](https://code.claude.com/docs/en/changelog#21132)）

> **繁中摘要**：v2.1.132 主要修正多個終端機顯示、輸入處理、記憶體洩漏等問題，並新增 session ID env var 與 alternate-screen opt-out。

**變更重點**
- 新增 `CLAUDE_CODE_SESSION_ID` env var 注入 Bash tool subprocess 環境
- 新增 `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` opt-out fullscreen alternate-screen renderer
- 修正 stdio MCP server 寫非 protocol 資料到 stdout 時造成的無上限記憶體增長（10GB+ RSS）
- 修正 `--resume` 在 emoji 截斷後拋出 "no low surrogate in string" 的問題
- 修正 `--permission-mode` flag 在 plan-mode session resume 時被忽略的問題
- 修正 fullscreen 在 laptop sleep/wake 或 Ctrl+Z/fg 後顯示空白的問題
- 修正 Vim operator 在含 NFD 分解重音字元時損壞文字的問題
- 修正 mouse wheel 在 Cursor 和 VS Code 1.92–1.104 滾動過快的問題
- 修正 JetBrains IDE 2025.2 terminal 的滾輪處理
- 修正 Alt+T（thinking toggle）在沒開 "Option as Meta" 的 macOS terminal 無法使用的問題

**實務影響**
- MCP stdio server 記憶體洩漏修正對長時間運行的 MCP 整合（如 obsidian-cli MCP）很重要
- `CLAUDE_CODE_SESSION_ID` 讓 hooks 可識別所在 session，支援更細粒度的 hook 邏輯
- `--permission-mode` 修正確保 plan-mode resume 時 permission 行為一致

### v2.1.129 · 2026-05-06（[changelog](https://code.claude.com/docs/en/changelog#21129)）

> **繁中摘要**：v2.1.129 新增 plugin URL 安裝、自動更新機制、skillOverrides 生效，並修正 1 小時 prompt cache TTL 被靜默降級的重要 bug。

**變更重點**
- 新增 `--plugin-url <url>` flag：直接從 URL 安裝 plugin .zip，當前 session 生效
- 新增 `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE`：Homebrew / WinGet 安裝自動背景升級並提示重啟
- `skillOverrides` 設定正式生效：`off` 從 model 和 `/` 隱藏、`user-invocable-only` 只從 model 隱藏、`name-only` 折疊 description
- Gateway `/v1/models` discovery 改為 opt-in（`CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1`）
- Ctrl+R history picker 預設搜尋所有 project 的所有 prompt
- 修正 1 小時 prompt cache TTL 被靜默降級為 5 分鐘的問題
- 修正 agent panel 在 subagent 運行時被隱藏的問題（v2.1.122 regression）
- 修正 `Bash(mkdir *)` 等 glob allow rules 在 in-project paths 不被尊重的問題

**實務影響**
- prompt cache TTL 修正對長對話成本影響顯著，1 小時 TTL 靜默降級意味著之前 cache hit 比預期少
- `skillOverrides` 生效讓 skill 能見度控制真正可用，對管理大量 skill 的 repo 有幫助
- Bash glob allow rules 修正讓腳本 permission 設定行為一致

**待追蹤**
- Gateway model discovery 改 opt-in 的原因未說明，使用 gateway 的用戶需注意

### v2.1.128 · 2026-05-04（[changelog](https://code.claude.com/docs/en/changelog#21128)）

> **繁中摘要**：v2.1.128 修正 EnterWorktree 分支來源行為、MCP tool result 掉 image、plugin 支援 .zip 格式，以及多個 UX 小修正。

**變更重點**
- `EnterWorktree` 現在從 local HEAD 建立新 branch（與文件一致），修正之前從 `origin/<default-branch>` 建的錯誤行為
- `--plugin-dir` 現在接受 .zip plugin archive（不限 directory）
- MCP: `workspace` 成為 reserved server name
- MCP: reconnect 時不再每次把完整 tool 名單 flood 到 conversation
- SDK hosts 現在收到 persistent `localSettings` suggestion 用於 Bash permission prompts
- 修正 MCP tool results 在 server 同時回傳 structured content 和 content blocks 時掉 image 的問題
- 修正 piping 超大 stdin（>10 MB）到 `claude -p` 造成 crash loop 的問題
- Subprocesses（Bash、hooks、MCP、LSP）不再繼承 `OTEL_*` env vars

**實務影響**
- `EnterWorktree` 行為修正讓 worktree 分支行為可預測（v2.1.133 進一步新增 `worktree.baseRef` 設定）
- MCP image 掉落修正對使用 multimodal MCP tool 的 workflow 有影響
- `OTEL_*` 隔離避免 observability 設定意外洩漏到子 process

---

## OpenAI Codex

### v0.130.0 · 2026-05-08（[changelog](https://developers.openai.com/codex/changelog#github-release-319777370)）

> **繁中摘要**：Codex CLI 0.130.0 新增 `remote-control` headless 模式、Bedrock AWS console-login 支援、plugin 分享機制，並修正 app-server thread 的 config 更新問題。

**變更重點**
- 新增 `codex remote-control` 指令：啟動可遠端控制的 headless app-server，更簡便的進入點
- App-server clients 可對大型 thread 分頁（`unloaded`、`summary`、`full` turn item view）
- Bedrock auth 支援 AWS console-login credentials（`aws login` profiles）
- Plugin 詳情頁顯示 bundled hooks；plugin 分享暴露 link metadata 與 discoverability 控制
- `view_image` 可透過 multi-environment session 的 selected environment 解析檔案
- 修正 live app-server thread 在 config 變更後不需重啟即可 pick up 新設定
- 修正 turn diffs 在 apply-patch 操作（含 partial failure）後保持準確

**實務影響**
- `codex remote-control` 讓 Codex 可作為 CI/CD 或外部系統的 headless agent backend
- Bedrock AWS console-login 支援擴展企業環境的認證選項

### 2026-05-07（[Codex for Chrome](https://developers.openai.com/codex/changelog#codex-2026-05-07)）

> **繁中摘要**：Codex 推出 Chrome extension，可在背景跨多個分頁並行運行，使用者保有對哪些網站可存取的控制權。

**變更重點**
- 新 Chrome extension：Codex 在背景跨分頁並行工作，不佔用瀏覽器前景
- 使用者自行決定哪些網站 Codex 可存取

**實務影響**
- 瀏覽器內 coding agent 能力擴展，可在網頁操作情境下使用 Codex
- 與 Claude Code 的 claude-in-chrome MCP 形成競品

**待追蹤**
- Extension 的權限模型與網站存取控制細節尚未公開完整說明

---

## Gemini CLI

### v0.41.0 · 2026-05-05（[changelog](https://geminicli.com/docs/changelogs/#announcements-v0410---2026-05-05)）

> **繁中摘要**：Gemini CLI v0.41.0 新增即時語音模式（雲端與本地後端）、強化 headless 模式安全性，並改善 shell 指令驗證。

**變更重點**
- 新增 real-time voice mode：支援雲端與本地後端
- Headless 模式強制執行 workspace trust，並加固 `.env` 載入安全性
- 強化 shell command validation，新增 core tools allowlist

**實務影響**
- Voice mode 讓 Gemini CLI 支援語音驅動開發流程，功能面顯著擴展
- Headless 安全加固（workspace trust + `.env`）影響在 CI/CD 或自動化腳本中使用 Gemini CLI 的設定方式

**待追蹤**
- Local voice backend 的技術依賴與支援平台未詳述

### 2026-05-09（[Addressing Antigravity Bans & Reinstating Access](https://github.com/google-gemini/gemini-cli/discussions/20632)）

> **繁中摘要**：Google 官方確認已全面解封近期因 Antigravity 封禁而無法使用 Gemini CLI 的帳戶，正規使用（不經第三方 proxy）即可恢復存取。

**變更重點**
- 上週對違反 Antigravity ToS 的帳戶執行封禁，但封禁層在 backend，導致 Gemini CLI 與 Gemini Code Assist 連帶被封
- 官方已與 Antigravity 協調，對近期被封帳戶執行系統全自動解封，立即生效
- 正規使用 Gemini CLI 在符合 ToS 前提下不受限制
- 使用第三方軟體或 proxy 存取 Antigravity 資源仍屬 ToS 違規

**實務影響**
- 若帳戶曾無法連線 Gemini CLI，現應已自動恢復，無需手動操作
- 不得透過第三方 proxy 或工具掛接 Gemini CLI 的 OAuth token 存取 Antigravity quota

### 2026-05-09（[Service update: mitigating abuse and prioritizing traffic](https://github.com/google-gemini/gemini-cli/discussions/22970)）

> **繁中摘要**：Gemini CLI 後端調整流量優先順序，並強化濫用偵測，使用第三方軟體搭接 OAuth 將被標記；依授權類型與帳戶信譽分級路由，部分用戶可能遭遇降速。

**變更重點**
- 強化對 policy-violating 用途的偵測，重點為「以 Gemini CLI OAuth 搭接第三方軟體」
- 流量依帳戶授權類型（license type）與帳戶信譽（account standing）分優先級路由
- 低優先級帳戶可能出現較慢 response time 或 reduced throughput

**實務影響**
- 使用 Gemini CLI 本身 CLI 工具正常使用不受影響；以其 OAuth token 串接其他 agent/proxy 工具有被標記風險
- 免費或試用授權帳戶在流量高峰時可能體感降速

**待追蹤**
- 帳戶被誤判時需聯繫 support team，無自助申訴入口

---

## GitHub Copilot

### v1.0.44 · 2026-05-08（[release](https://github.com/github/copilot-cli/releases/tag/v1.0.44)）

> **繁中摘要**：Copilot CLI v1.0.44 支援 mid-input slash commands 與多 skill 同時呼叫、`userPromptSubmitted` hook 可直接回傳不走 LLM、修正 Free 方案 quota 顯示錯誤。

**變更重點**
- Slash commands 可在輸入中段插入；單一訊息可呼叫多個 skills
- `userPromptSubmitted` hooks 可直接處理請求並回傳，繞過 LLM（不發 model call）
- 新增 `copilot update` 與 `/update` 的 `prerelease` 參數，可抓最新 prerelease build
- Free 方案用戶 quota 顯示修正（之前永遠顯示 100% used）
- autopilot mode 授予的 tool permissions 在 `/clear` 後保留
- Shell aliases 與 rc file 設定在 `!` 命令中正確生效
- Multi-account 用戶的 `/user list` 和 `/user switch` 速度提升

**實務影響**
- `userPromptSubmitted` hook bypass LLM 讓 Copilot CLI 可作為自訂 router，實作本地快取或規則型回應
- 多 skill 單訊息呼叫提升 CLI 互動效率
- Free 用戶 quota 顯示修正影響自我管理使用量的判斷

---

## Claude Code

### v2.1.137 · 2026-05-09（[changelog](https://code.claude.com/docs/en/changelog#21137)）

> **繁中摘要**：v2.1.137 是 Windows / VS Code extension hotfix，修正 extension 無法啟動的問題。

**變更重點**
- 修正 VS Code extension 在 Windows 上 activation 失敗。

**實務影響**
- Windows 使用者若在 VS Code 內啟動 Claude Code extension 失敗，先升到 v2.1.137 以上再排查設定。

### v2.1.136 · 2026-05-08（[changelog](https://code.claude.com/docs/en/changelog#21136)）

> **繁中摘要**：v2.1.136 強化 enterprise telemetry、auto mode hard deny 規則，並修正 MCP、Plan Mode、WSL2 image paste、plugin hooks 與多個 TUI/IDE workflow bug。

**變更重點**
- 新增 `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL`，讓 enterprise 透過 OpenTelemetry 收集 session quality survey。
- 新增 `settings.autoMode.hard_deny`，可設定 auto mode classifier 的無條件阻擋規則。
- 修正 `.mcp.json`、plugins、claude.ai connectors 內的 MCP servers 在 VS Code extension、JetBrains plugin、Agent SDK `/clear` 後消失的問題。
- 修正多個 remote MCP server 同時 refresh 時 OAuth refresh token 遺失，導致頻繁重新登入的問題。
- 修正 Plan Mode 在已有 `Edit(...)` allow rule 時未阻擋檔案寫入的問題。
- WSL2 image paste 新增 PowerShell fallback，當 `xclip` / `wl-paste` 無法讀圖時仍可貼上 Windows clipboard 圖片。
- 修正 plugin `Stop` / `UserPromptSubmit` hooks 在 cache cleanup 刪掉仍被 session 使用的版本後失敗。
- 修正 MCP tool results 回傳 content blocks 時不可見、`/doctor` MCP schema error 缺少來源路徑、`CronList` 缺少排程提示等問題。

**實務影響**
- 多 MCP server 使用者應減少每日重登與 `/clear` 後 connector 消失的情況。
- Plan Mode 與 auto mode 的安全邊界更明確，適合 enterprise / managed settings 環境。
- WSL2 與 IDE extension 使用者會直接受益於 image paste、extension、TUI rendering 修正。

---

## GitHub Copilot

### 2026-05-08（[More flexible secrets and variables for Copilot cloud agent](https://github.blog/changelog/2026-05-08-more-flexible-secrets-and-variables-for-copilot-cloud-agent)）

> **繁中摘要**：Copilot cloud agent 新增專屬的 Agents secrets / variables，可在 organization 層級集中配置，不再只能逐 repo 綁在 Actions `copilot` environment。

**變更重點**
- 新增 Agents 類型的 secrets 與 variables，與 Actions、Codespaces、Dependabot 分開管理。
- 支援 organization-level secrets / variables，並可指定哪些 repositories 可存取。
- Repository settings 內新增專屬 Agents 區塊，避免和 Actions 設定混在一起。

**實務影響**
- 內部 package registry token、共用 MCP server 設定等可集中下發給 Copilot cloud agent。
- 多 repo rollout 時不必逐一建立 `copilot` environment，agent 基礎設施維護成本下降。

### 2026-05-08（[Copilot code review comment types now in usage metrics API](https://github.blog/changelog/2026-05-08-copilot-code-review-comment-types-now-in-usage-metrics-api)）

> **繁中摘要**：Copilot usage metrics API 現在可依 comment type 統計 Copilot code review suggestions，協助 enterprise / org owner 追蹤 code review 建議的類型與採納情況。

**變更重點**
- `pull_requests` 報表新增 `copilot_suggestions_by_comment_type` array。
- 每個 comment type 提供 `total_copilot_suggestions` 與 `total_copilot_applied_suggestions`。
- 支援 enterprise 與 organization 層級的單日與 28 天 rolling window 報表。

**實務影響**
- 可量化 Copilot code review 主要抓到哪些類型的問題，例如 security 或 bug risk。
- 可比較各類建議的提出量與採納量，用於評估 code review agent 的實際價值。

**待追蹤**
- 目前不能 drill down 到 repository level；GitHub 表示仍在調查。

### 2026-05-08（[Upcoming deprecation of GPT-4.1](https://github.blog/changelog/2026-05-07-upcoming-deprecation-of-gpt-4-1)）

> **繁中摘要**：GitHub Copilot 將於 2026-06-01 在所有 Copilot experiences 停用 GPT-4.1，建議改用 GPT-5.5。

**變更重點**
- GPT-4.1 將於 2026-06-01 在 Copilot Chat、inline edits、ask / agent modes、code completions 等體驗中 deprecated。
- 建議替代模型為 GPT-5.5。
- Copilot Enterprise admins 可能需要在 model policies 中啟用替代模型。

**實務影響**
- 使用固定 GPT-4.1 的 workflow、教學、團隊設定與 integrations 需要在 2026-06-01 前更新。
- Enterprise 環境需確認 GPT-5.5 policy 已開，否則使用者可能在 model selector 看不到替代模型。

### 2026-05-07（[Claude Sonnet 4 deprecated](https://github.blog/changelog/2026-05-07-claude-sonnet-4-deprecated)）

> **繁中摘要**：GitHub Copilot 已於 2026-05-06 在所有 Copilot experiences 停用 Claude Sonnet 4，建議改用 Claude Sonnet 4.6。

**變更重點**
- Claude Sonnet 4 已於 2026-05-06 deprecated。
- 影響 Copilot Chat、inline edits、ask / agent modes、code completions 等所有 Copilot experiences。
- 建議替代模型為 Claude Sonnet 4.6。

**實務影響**
- 固定使用 Claude Sonnet 4 的 Copilot 設定需切換到 Claude Sonnet 4.6。
- Enterprise admins 需確認替代模型 policy 已啟用，使用者才會在 VS Code / github.com model selector 看到可用模型。

### 2026-05-07（[Rubber Duck in GitHub Copilot CLI now supports more models](https://github.blog/changelog/2026-05-07-rubber-duck-in-github-copilot-cli-now-supports-more-models)）

> **繁中摘要**：Copilot CLI 的 Rubber Duck cross-family review agent 擴大模型組合；GPT orchestrator 可搭配 Claude critic，Claude orchestrator 則升級 GPT-5.5 作為 second opinion。

**變更重點**
- GPT model 作為 orchestrator 且 `/experimental` 開啟時，可派出 Claude-powered Rubber Duck agent 給第二意見。
- Claude orchestrator sessions 的 Rubber Duck model 升級為 GPT-5.5。

**實務影響**
- Copilot CLI 的跨模型 review 能覆蓋 GPT-driven sessions，不再只偏向 Claude orchestrator。
- 對需要 architecture、cross-file conflict、subtle bug second opinion 的 CLI workflow 有直接幫助。

---

## opencode

### v1.14.42-v1.14.46 · 2026-05-09–2026-05-10（[release](https://github.com/anomalyco/opencode/releases/tag/v1.14.46)）

> **繁中摘要**：opencode 連續 releases 補強 agent workflow、HTTP API、workspace handling、MCP discovery 與 Plan Mode security；其中 v1.14.42 與 v1.14.46 對日常 agent 使用影響最大。

**變更重點**
- [v1.14.42](https://github.com/anomalyco/opencode/releases/tag/v1.14.42)：新增 Scout agent，用於 repo research、docs lookup、dependency-source inspection。
- [v1.14.42](https://github.com/anomalyco/opencode/releases/tag/v1.14.42)：新增 workspace sync、`opencode run` interactive split-footer mode、HTTP API large non-streaming response compression。
- [v1.14.42](https://github.com/anomalyco/opencode/releases/tag/v1.14.42)：修正 Gemini、Anthropic Opus 4.5、OpenAI deep research / GPT-5 reasoning variants 的 reasoning effort options。
- [v1.14.45](https://github.com/anomalyco/opencode/releases/tag/v1.14.45)：Read tool permission rules 現在會 match worktree-relative paths，read allowlists / denylists 行為更一致。
- [v1.14.46](https://github.com/anomalyco/opencode/releases/tag/v1.14.46)：新增內建 `customize-opencode` skill，降低修改 opencode config 後啟動失敗的機率。
- [v1.14.46](https://github.com/anomalyco/opencode/releases/tag/v1.14.46)：修正 broken `outputSchema` MCP server 造成 tool discovery 失敗，以及 subagents 可忽略 parent-agent deny rules 的 Plan Mode security bypass。

**實務影響**
- 使用 opencode 做 repo 探索或依賴源碼檢查時，Scout agent 是新的核心能力。
- 若 workflow 依賴 worktree、subagents、MCP servers 或 Plan Mode deny rules，建議升級到 v1.14.46。
- reasoning effort options 修正可避免模型支援能力與 UI / config 暴露選項不一致。
