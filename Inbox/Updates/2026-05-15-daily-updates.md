---
title: "2026-05-15 Daily Updates"
created: 2026-05-15
updated: 2026-05-15
tags:
  - updates
  - claude-code
  - codex
  - copilot
  - opencode
  - storybook
  - skills
---

## OpenAI Codex

### 2026-05-14（[Work with Codex from anywhere](https://openai.com/index/work-with-codex-from-anywhere/)）

> **繁中摘要**：Codex 進入 ChatGPT mobile app 預覽，讓使用者從手機連回本機、devbox 或 managed remote environment 的 live Codex sessions，處理 approvals、diffs、terminal output、screenshots 與模型切換。

**變更重點**

- Codex mobile preview 於 iOS / Android 的 ChatGPT mobile app 逐步推出，涵蓋 Free、Go 等所有方案與支援地區。
- 手機端透過 secure relay 連回 Codex 運行的可信機器，不直接把本機暴露到 public internet。
- Codex 可從手機查看 active threads、approvals、plugins、project context、terminal output、test results 與 diffs。
- Remote SSH 與 Hooks 已可在所有方案使用；programmatic access tokens 限 Enterprise / Business；Windows app 手機連線支援仍在後續。

**實務影響**

- 長時間 Codex 任務可以改成「桌機執行、手機決策」的協作節奏，適合通勤、會議間隙或遠端環境。
- 團隊若要導入 mobile steering，應同步檢查 secure relay、workspace identity、approvals、secrets 與本機環境權限邊界。

### 2026-05-15（[Deprecating `chat/completions` support in Codex](https://github.com/openai/codex/discussions/7782)）

> **繁中摘要**：OpenAI Codex discussion 宣布 Codex 將棄用 `chat/completions` protocol 支援，理由是 agentic coding / reasoning workflow 需要 Responses API 的多輪、tool-rich 與 reasoning 模型能力。

**變更重點**

- Codex 團隊表示 legacy `chat/completions` 支援增加複雜度、regressions 與 support overhead。
- 未來 Codex 功能會更集中在 Responses API，而不是維持 GPT-3.5 時代的 chat completions protocol。
- 這會影響仍透過舊 protocol 串接 Codex 或相容代理層的使用者。

**實務影響**

- 自建 Codex wrapper、proxy 或 model provider adapter 應優先確認是否仍依賴 `chat/completions`。
- 需要規劃 Responses API migration，特別是 multi-turn state、tool calling、reasoning settings 與 streaming 行為。

---

## Claude Code

### v2.1.142 · 2026-05-14（[changelog](https://code.claude.com/docs/en/changelog)）

> **繁中摘要**：Claude Code v2.1.142 主要更新 background sessions、fast mode 預設模型、plugin skill discovery、plugin details 與 MCP timeout 行為，並修正 worktree 偵測問題。

**變更重點**

- `claude agents` 新增 `--add-dir`、`--settings`、`--mcp-config`、`--plugin-dir`、`--permission-mode`、`--model`、`--effort`、`--dangerously-skip-permissions` 等 flags，可設定 dispatched background sessions。
- Fast mode 預設改用 Opus 4.7；可用 `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1` pin 回 Opus 4.6。
- root-level `SKILL.md` 且沒有 `skills/` 子目錄的 plugin 現在會被 surfaced as a skill。
- `/plugin` details pane 與 `claude plugin details` 會顯示 plugin 提供的 LSP servers。
- `/web-setup` 在替換既有 GitHub App connection 前會警告。
- 修正 `MCP_TOOL_TIMEOUT` 對 remote HTTP / SSE MCP servers 未提高 per-request fetch timeout 的問題。
- 修正 background sessions 未辨識既有 git worktrees，導致 Edit 被 EnterWorktree duplicate creation 擋住的問題。

**實務影響**

- background session dispatch 現在更可被 script / automation 精準配置，適合多目錄、多 MCP config、多模型或不同 permission mode 的 workflow。
- plugin 作者可用 root-level `SKILL.md` 暴露單一 skill，降低 plugin 結構負擔。
- 使用 remote MCP 或 background agents 的團隊應升級，以避免 timeout 上限與 worktree 偵測造成的 false failure。

---

## GitHub Copilot

### 2026-05-14（[GitHub Copilot app technical preview](https://github.blog/changelog/2026-05-14-github-copilot-app-is-now-available-in-technical-preview/)）

> **繁中摘要**：GitHub Copilot app technical preview 提供 GitHub-native desktop agentic development experience，讓使用者從 GitHub work item 啟動、隔離、引導與追蹤 agentic work。

**變更重點**

- Copilot app 以 desktop app 形式提供 agentic development workflow。
- 更新焦點在從 GitHub 工作上下文啟動任務、隔離工作、保持可 steer 與可追蹤。
- 這是 Copilot agent workflow 從 IDE / web 延伸到獨立 app 的產品線訊號。

**實務影響**

- 使用 Copilot coding agent 的團隊需要重新評估 IDE agent、cloud agent、CLI agent、desktop app 之間的任務邊界。
- 這可能使 GitHub issue / PR / project context 更直接成為 agent task 的入口。

### 2026-05-14（[Copilot cloud agent supports auto model selection](https://github.blog/changelog/2026-05-14-copilot-cloud-agent-supports-auto-model-selection)）

> **繁中摘要**：Copilot cloud agent 支援 auto model selection，選擇 Auto 後會根據 system health 與 model availability 自動挑選模型。

**變更重點**

- Copilot cloud agent model picker 新增 Auto 選項。
- Auto 會依據系統健康狀態與可用模型選擇最佳模型。
- 這把模型選擇從使用者手動決策部分移回平台端。

**實務影響**

- 對追求穩定完成率的 cloud agent workflow，Auto 可降低模型故障或容量波動造成的中斷。
- 對需要可重現 benchmark 或固定模型成本的團隊，仍應明確記錄 task 使用模型，避免 Auto 造成行為差異。

### 2026-05-14（[Team-level Copilot usage metrics API](https://github.blog/changelog/2026-05-14-team-level-copilot-usage-metrics-now-available-via-api)）

> **繁中摘要**：Copilot usage metrics API 新增 user-teams report，可把每個 Copilot licensed user 對應到所屬 teams，方便 team-level adoption 與 usage 分析。

**變更重點**

- 新增 `user-teams` report，將 Copilot licensed users 對應到 GitHub teams。
- 可和既有 usage metrics join，產出 team-level 報表。

**實務影響**

- Enterprise / Business 管理者可以把 Copilot adoption、active usage 與成本治理細分到 team。
- 內部報表與 chargeback / showback 流程可從 user-level 進一步聚合到 team-level。

### 2026-05-14（[Copilot CLI agent and unified sessions view in JetBrains IDEs](https://github.blog/changelog/2026-05-13-introducing-copilot-cli-agent-and-unified-sessions-view-in-github-copilot-for-jetbrains-ides)）

> **繁中摘要**：JetBrains IDEs 的 GitHub Copilot 加入 Copilot CLI agent 與 unified sessions view，讓使用者在 IDE 內查看 running / queued sessions 並使用 ask mode。

**變更重點**

- Copilot CLI agent 整合到 JetBrains IDEs。
- Unified sessions view 可顯示 running 與 queued sessions 的 live status。
- 加入 ask mode 相關更新，讓 JetBrains 使用者更接近 VS Code / CLI 的 agent workflow。

**實務影響**

- JetBrains 使用者可在 IDE 內管理 Copilot CLI agent sessions，不必完全切回 terminal。
- 對多 session agent 工作流，狀態可視性改善會降低重複啟動或遺漏 queued work 的風險。

### v1.0.48 · 2026-05-14（[github/copilot-cli release](https://github.com/github/copilot-cli/releases/tag/v1.0.48)）

> **繁中摘要**：Copilot CLI 1.0.48 修正 instruction file glob、CJK / emoji 輸入渲染、`/context` token limit 顯示、Azure DevOps-only workspace 的 prompt/headless 行為，以及 ACP config update。

**變更重點**

- Model picker 對 token-based billing users 顯示實際 token prices。
- `applyTo` frontmatter 中未加引號的 glob patterns 現在能正確套用。
- CJK characters 或 emoji 輸入不再造成行距空洞。
- `/context` 會顯示各模型正確 token limits，不再固定顯示 128k。
- Azure DevOps-only workspaces 在 prompt/headless mode 會自動停用內建 `github-mcp-server`。
- ACP clients 會在 active model 變更時收到更新後的 config options。

**實務影響**

- 中文 / emoji 輸入與 instruction glob 是日常 CLI UX 的直接修正，尤其適合 Windows / 多語系團隊升級。
- Headless automation 在 Azure DevOps-only repo 會少遇到錯誤 GitHub MCP server 啟動。

---

## OpenCode

### v1.14.51 · 2026-05-15（[release](https://github.com/anomalyco/opencode/releases/tag/v1.14.51)）

> **繁中摘要**：OpenCode v1.14.51 加入 experimental background subagents，修正 worktree creation、interrupted assistant messages、auto-compaction、LiteLLM compatibility 與多個 provider / API edge cases。

**變更重點**

- 新增 experimental background subagents，讓 task 可在背景持續執行。
- 修正 worktree creation requests 缺少 POST body。
- 修正 cancellation 後 sessions 卡在 interrupted assistant messages 的問題。
- 修正 compaction reordered messages 後 repeated auto-compaction。
- LiteLLM compatibility 更新到支援目前 GPT-5 與 tool-call 行為的版本。
- 修正 Azure `gpt-5.5` completions API requests、truncated shell output streams、image resizing 等問題。

**實務影響**

- OpenCode 也開始往 background subagents 推進，值得和 Claude Code / Codex 的背景工作模型比較。
- 使用 LiteLLM、Azure GPT-5.5 或長 session compaction 的使用者，這版偏向可靠性升級。

---

## Storybook

### v10.4.0 · 2026-05-14（[release](https://github.com/storybookjs/storybook/releases/tag/v10.4.0)）

> **繁中摘要**：Storybook 10.4 加入 AI-assisted setup、change-aware review、sidebar review tools、TanStack React framework、React MCP docgen 與 React Native zero-config initialization。

**變更重點**

- Agentic Setup：新的 CLI workflow 協助 AI-assisted Storybook setup / onboarding。
- Change review：sidebar filtering 可高亮 new、modified、related stories。
- Sidebar review tools：status filtering、URL-persisted filters、review signals。
- 新增 `@storybook/tanstack-react` framework，支援 routing 與 server functions。
- React MCP 使用 TypeScript Language Server 改善 component docgen。
- React Native 支援 zero-config project initialization。

**實務影響**

- Storybook 開始把 AI-assisted setup 與 review workflow 納入核心 DX，適合 frontend agent workflow 追蹤。
- 對設計系統與 component review，change-aware filtering 可以降低大型 story tree 的審查成本。

---

## Skills

### v1.5.7 · 2026-05-14（[vercel-labs/skills release](https://github.com/vercel-labs/skills/releases/tag/v1.5.7)）

> **繁中摘要**：vercel-labs/skills v1.5.7 支援 v2 well-known skill discovery、lazy GitHub token fallback、project-level update respect local folders，並修正 symlink skill discovery 與大型 repo clone 等問題。

**變更重點**

- 支援 v2 well-known skill discovery。
- GitHub token 改成 lazy use，只在 rate-limit fallback 時使用。
- Project-level update 尊重 local folders。
- 偵測 agent running `npx skills`。
- 修正 symlinked skill directories discovery。
- clone 大型 repo 時提高 timeout，並停用 LFS filter 以避免缺少 git-lfs 失敗。

**實務影響**

- 對跨工具 skills registry / discovery workflow，v2 well-known discovery 與 symlink discovery 修正值得追蹤。
- Lazy GitHub token 行為降低安裝或探索階段不必要的 credential 使用。

---

## 跳過與待追蹤

已跳過：

- Gemini CLI official changelog：最新 official announcement 仍是 v0.42.0 / 2026-05-12，已在前次日報覆蓋，今日沒有新 official entry。
- OpenAI Codex changelog：2026-05-13 mobile documentation entry 較 OpenAI 2026-05-14 product post資訊少，今日改收 product post。
- Storybook alpha / beta releases：已有 10.4.0 stable release，跳過 alpha / beta 重複項。
- Copilot CLI v1.0.48-1 / v1.0.48-2：被 v1.0.48 stable release 包含。
- GSD v1.42.x：內容偏特定工具 release，和 coding agent general workflow 相關但訊號較窄，先不收。

需要人工追蹤：

- OpenAI Codex `chat/completions` deprecation discussion 後續是否發布正式 migration timeline。
- Codex mobile Windows support 時程。
- GitHub Copilot app 與 VS Code / CLI / cloud agent 的產品邊界是否會清楚化。
