---
title: "2026-05-12 Daily Updates"
created: 2026-05-12
updated: 2026-05-12
tags:
  - updates
  - claude-code
  - copilot
---

## Claude Code

### v2.1.139 · 2026-05-11（[changelog](https://code.claude.com/docs/en/changelog#may-11-2026)）

> **繁中摘要**：v2.1.139 是大版本：新增 `claude agents` 跨 session 列表、`/goal` 持續到完成條件達成的長任務模式，以及 hook `args: string[]` exec form、`continueOnBlock` 等 agent setup 相關擴充；同時當 `ANTHROPIC_API_KEY` 設定時 Remote Control / `/schedule` / claude.ai connectors 會自動 disable。

**變更重點**
- 新增 agent view（Research Preview）：`claude agents` 列出所有 session（running / blocked on you / done）
- 新增 `/goal`：設定完成條件後跨 turn 持續工作，支援 interactive、`-p`、Remote Control，overlay 顯示 elapsed/turns/tokens
- 新增 `claude plugin details <name>`：顯示 plugin component inventory 與 per-session token cost 預估
- Hook 新增 `args: string[]`（exec form，直接 spawn 不經 shell，path placeholder 不需引號）與 `continueOnBlock`（PostToolUse 把 rejection reason 餵回 Claude 繼續 turn）
- MCP stdio servers 現在會收到 `CLAUDE_PROJECT_DIR` 環境變數（與 hooks 對齊）；plugin configs 可在 commands 中引用 `${CLAUDE_PROJECT_DIR}`
- Subagent API request 帶 `x-claude-code-agent-id` / `x-claude-code-parent-agent-id` header，OTEL `claude_code.llm_request` span 含 `agent_id` / `parent_agent_id`
- `ANTHROPIC_API_KEY` / `apiKeyHelper` / `ANTHROPIC_AUTH_TOKEN` 設定時，Remote Control、`/schedule`、claude.ai MCP connectors、notification preferences 自動停用（即使有 Claude.ai login）
- `/mcp` Reconnect 不需重啟即吃 `.mcp.json` edits；HTTP/SSE MCP server response body cap 16 MB per SSE frame（修無上限記憶體成長）
- `Skill(name *)` wildcard 修為 prefix match；symlinked `~/.claude/settings.json` settings hot-reload 修好
- 修 `autoAllowBashIfSandboxed` 對 `$VAR` / `$(cmd)` shell expansion 不自動核准
- 修 hook 寫 terminal 會破壞 interactive prompt（hook 現在無 terminal access）
- 修 `claude_code.active_time.total` OTEL metric 在 `--print` 模式不發出
- 修 Grep Windows drive-letter 路徑相對化與 single-file 路徑 count 模式總數錯誤
- VSCode：`Cmd/Ctrl+Shift+T` 重開最近關閉的 session tab，可由 `claudeCode.enableReopenClosedSessionShortcut` 設定

**實務影響**
- Long-running task workflow 變了：`/goal` 取代以往「請繼續到 X 完成」需手動推進的 pattern，可在 `-p` 與 Remote Control 跑
- 多 session 管理可用 `claude agents` 一次列出，不再需要切 terminal 找哪個 session 在等回應
- API key 與 Claude.ai login 共存的環境要注意：設了 `ANTHROPIC_API_KEY` 就用不到 Remote Control / `/schedule` / connectors，要 unset 才能切回
- Hook 作者要注意：原本依賴 hook 寫 terminal 顯示訊息的會失效，改走 hook output 機制
- Plugin 開發者：commands 可用 `${CLAUDE_PROJECT_DIR}` 寫 portable 路徑；MCP stdio server 也能讀到此 env
- OTEL 觀測升級：subagent 可用 `agent_id` / `parent_agent_id` 串成 trace，分析 multi-agent 工作流耗時

---

## GitHub Copilot

### v1.0.45 · 2026-05-11（[release](https://github.com/github/copilot-cli/releases/tag/v1.0.45)）

> **繁中摘要**：Copilot CLI 1.0.45 補上 `/autopilot` 與 `/fork` 兩個 session 控制指令、Windows 缺 pwsh 時 fallback 到 PowerShell 5、OTEL 對齊 GenAI semantic conventions，並修好 extension permission session 無法 resume 與 `agentStop` hook 在 `task_complete` 不觸發的 bug。

**變更重點**
- `/autopilot` slash command：在 interactive 與 autopilot 模式間切換
- `/fork` slash command：把現有 session fork 成新的獨立 session
- Windows 上找不到 PowerShell 7+（pwsh）時自動 fallback 到 Windows PowerShell（powershell.exe）
- OTEL 對齊 GenAI semantic conventions：MCP tool calls 改用標準 `tool_call` span，新增 `gen_ai.client.operation.duration` metric 追 tool 執行時間
- 修：有 extension permission prompt 的 session 不再回報 "Session file is corrupted" 而能正常 resume
- 修：`agentStop` hook 在 agent 透過 `task_complete` 停止時正確觸發
- CLI 啟動時間在 OSC color query 支援有限的 terminal 上最多省 1.5s

**實務影響**
- Windows 用戶不再需要先裝 pwsh 才能跑 Copilot CLI，預設 PowerShell 5 即可運作
- 想分支 session 試新方向不用複製整段對話，`/fork` 直接拆出獨立 session
- 接 OTEL 觀測的團隊要注意 span / metric 名稱換成 GenAI 標準（`tool_call`、`gen_ai.client.operation.duration`），既有 dashboard 可能要更新 query
- 用 `agentStop` hook 做收尾的工作流現在能可靠收到 `task_complete` 觸發

---
