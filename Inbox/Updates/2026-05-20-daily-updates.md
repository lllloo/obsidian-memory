---
title: "2026-05-20 Daily Updates"
created: 2026-05-20
updated: 2026-05-20
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## OpenAI Codex

### v0.132.0 · 2026-05-20（[release](https://github.com/openai/codex/releases/tag/rust-v0.132.0)）

> **繁中摘要**：Codex CLI 0.132.0 強化 Python SDK 認證、文字 turn API、resume 結構化輸出、TUI 啟動速度與 remote executor 註冊。

**變更重點**

- Python SDK 新增 first-class authentication：API key login、ChatGPT browser / device-code 流程、account inspection、logout APIs。
- Python turn APIs 支援純字串輸入、`TurnResult` 包含 collected items、timing、usage data。
- `codex exec resume` 新增 `--output-schema`，resumed automation 可保留 session context 同時強制 JSON 結構化輸出。
- TUI 啟動更快：terminal capability probes 改為批次執行，不再序列等待。
- Remote executor 註冊支援標準 Codex auth，不再需要單獨秘鑰。

**實務影響**

- Python SDK 進階 auth 與 turn API 讓 Codex 更容易被嵌進企業 / orchestration 服務。
- `--output-schema` for resume 對需要持續產出結構化 JSON 的 long-running automation 是必要保證。
- TUI 啟動加速雖小但影響每天反覆開新 session 的 hands-on workflow。

---

## Claude Code

### v2.1.145 · 2026-05-19（[release](https://github.com/anthropics/claude-code/releases/tag/v2.1.145)）

> **繁中摘要**：Claude Code v2.1.145 偏向 agent 可觀測性、plugin metadata 預覽、status line 增強與 UX 修正。

**變更重點**

- 新增 `claude agents --json`，可列出實時 Claude sessions 為 JSON，供 tmux-resurrect、status bar、session picker 等腳本化場景使用。
- `claude_code.tool` OTEL spans 新增 `agent_id` 與 `parent_agent_id` 屬性，並修正背景 subagent span 的 trace parenting，讓 background subagent spans 嵌套在 dispatching Agent tool span 之下。
- Status line JSON input 在偵測到時包含 GitHub repo 與 PR 資訊。
- `/plugin` Discover 與 Browse 在安裝前顯示 plugin 的 commands、agents、skills、hooks 與 MCP/LSP servers。
- `claude agents` terminal tab title 顯示等待輸入的 session 數，alt-tabbed window 可看出 agent 是否需要注意。
- Slash command 與 @-mention 建議列表在 fullscreen mode 支援滑鼠 hover / click。

**實務影響**

- `--json` 與 OTEL trace 修正讓 multi-agent 觀測與診斷更可程式化處理。
- Plugin 安裝前看到完整 capability 清單，可降低盲裝 plugin 的風險。
- Status line 出 PR / repo 資訊對在 PR review 上下文工作的人很方便。

### v2.1.142 · 2026-05-14（[release](https://github.com/anthropics/claude-code/releases/tag/v2.1.142)）

> **繁中摘要**：Claude Code v2.1.142 補強 background agents 設定旗標、預設 fast model 升級到 Opus 4.7、root-level SKILL.md plugin 識別與 MCP timeout 修正。

**變更重點**

- 新增 `claude agents` 多個 flags：`--add-dir`、`--settings`、`--mcp-config`、`--plugin-dir`、`--permission-mode`、`--model`、`--effort`、`--dangerously-skip-permissions`，可全面設定被 dispatch 的背景 session。
- Fast mode 預設模型升級為 Opus 4.7；設 `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1` 可釘住 Opus 4.6。
- 帶 root-level `SKILL.md` 但無 `skills/` 子目錄的 plugin 現會被識別為 skill。
- `/plugin` 詳情面板與 `claude plugin details` 顯示 plugin 提供的 LSP servers。
- `/web-setup` 在替換既有 GitHub App 連線前先警告。
- 修正 `MCP_TOOL_TIMEOUT` 對 HTTP / SSE MCP servers 無效（被卡 60 秒）的問題。

**實務影響**

- Background agent 可控性大幅提升，無需仰賴主 session 設定繼承。
- Fast mode 預設 Opus 4.7 會讓 throughput 與 cost 結構同步移動；對成本敏感的場景需顯式 override。
- MCP timeout 修正對使用較慢遠端 MCP server 的 workflow 是 unblock 級別的修補。

### v2.1.141 · 2026-05-13（[release](https://github.com/anthropics/claude-code/releases/tag/v2.1.141)）

> **繁中摘要**：Claude Code v2.1.141 引入 hook 端 desktop notification 能力、HTTPS plugin clone、workspace ID 環境變數、agents 目錄範圍與 rewind 摘要等改進。

**變更重點**

- Hook JSON output 新增 `terminalSequence` 欄位，可不依賴 controlling terminal 直接送 desktop notification、視窗標題與 bell。
- `CLAUDE_CODE_PLUGIN_PREFER_HTTPS` 環境變數讓沒有 GitHub SSH key 的環境改用 HTTPS clone plugin。
- 新增 `ANTHROPIC_WORKSPACE_ID`，在 workload identity federation 涵蓋多個 workspace 時可指定 minted token 範圍。
- `claude agents --cwd <path>` 讓 session list 範圍限於指定目錄。
- `/feedback` 可附最近 24 小時或 7 天的 sessions，便於回報跨 session 問題。
- Rewind menu 新增 "Summarize up to here"，壓縮較早 context 同時保留近期 turns。

**實務影響**

- Hook desktop notification 對 background / remote-run 場景的人機回饋很有用。
- HTTPS plugin clone 適合 CI、container、沒有 SSH key 的 dev box。
- 多 workspace federation 的企業情境終於有顯式的 workspace scoping 工具。

---

## GitHub Copilot

### 2026-05-19（[Gemini 3.5 Flash is generally available for GitHub Copilot](https://github.blog/changelog/2026-05-19-gemini-3-5-flash-is-generally-available-for-github-copilot)）

> **繁中摘要**：Google 同日釋出 Gemini 3.5 Flash，GitHub Copilot 即刻 GA 此模型，宣稱 Flash-tier 速度與成本下接近 Pro 級 coding 品質；社群同時注意到 14x premium request multiplier 與 Flash 級該有的定價落差大。

**變更重點**

- Gemini 3.5 Flash 在 GitHub Copilot 全面可用，列入可選模型清單。
- 官方早期測試聲稱 Flash 3.5 在編碼任務上接近 Gemini Pro 的品質但採 Flash 等級的延遲與成本。

**實務影響**

- 評估 multi-model Copilot 策略的團隊需對照 14x premium multiplier 是否值得（社群早期回饋偏負面）。
- 可作為 Google 模型線在 agentic harness 上表現的觀察點，與 GPT-5.5、Opus 4.7 直接比較。

**待追蹤**

- Microsoft 自註 pricing tentative，後續 multiplier 是否下調。
- 實際 token cost 與 effective TPS 在 GA 後是否與 Pro 拉開差距。

### 2026-05-19（[Easily apply Copilot code review feedback with Copilot cloud agent](https://github.blog/changelog/2026-05-19-easily-apply-copilot-code-review-feedback-with-copilot-cloud-agent)）

> **繁中摘要**：Copilot code review 將原本的 `Implement suggestion` 按鈕改名為 `Fix with Copilot`，並擴充為對話框讓使用者更細控套用建議的方式。

**變更重點**

- Copilot code review 中的 `Implement suggestion` 按鈕改名為 `Fix with Copilot`。
- 套用建議現在會開 UI dialog，提供更多套用控制（不再只是一鍵套用）。

**實務影響**

- 對 review-driven workflow 的人，可避免「點下一鍵後悔」造成 PR diff 爆炸。
- 命名一致化（all `Fix with Copilot`）讓 cloud agent 在不同 surface（Actions / Code review）上有相同入口語彙。
