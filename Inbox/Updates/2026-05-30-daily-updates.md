---
title: "2026-05-30 Daily Updates"
created: 2026-05-30
updated: 2026-05-30
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## Claude Code

### v2.1.157 · 2026-05-29（[Release v2.1.157](https://github.com/anthropics/claude-code/releases/tag/v2.1.157)）

> **繁中摘要**：`.claude/skills` 目錄的 plugin 現在自動載入，無需 marketplace；`claude agents` 的 `agent` 欄位正式生效，並修復多項 worktree、背景 session、WSL 圖片貼上等關鍵問題。

**變更重點**
- Plugins in `.claude/skills` directories 自動載入，不需 marketplace
- 新增 `claude plugin init <name>` 指令來 scaffold plugin
- `/plugin` 指令新增 autocomplete
- `settings.json` 的 `agent` 欄位現在對 dispatched session 生效；可用 `--agent <name>` 覆蓋
- `EnterWorktree` 可在同一 session 中切換 Claude-managed worktrees
- `tool_decision` telemetry 事件在 `OTEL_LOG_TOOL_DETAILS=1` 時附帶 `tool_parameters`
- Claude 管理的 worktrees 完成後保持 unlocked 狀態
- `/terminal-setup` 現在對 VS Code / Cursor / Windsurf integrated terminal 停用 GPU acceleration
- `/config` 新增「Workflow keyword trigger」設定
- WSL：修復 image paste、Windows 11 截圖貼上，支援從 Windows Explorer 拖曳圖片

**實務影響**
- Plugin 開發流程大幅簡化：無需 marketplace 即可本地使用
- `claude agents` 派發的子 session 現在能正確沿用 `settings.json` 指定的 agent
- 修復背景 session 在睡眠/喚醒後向 model 回報錯誤日期的 bug（影響所有長時間背景任務）
- 修復 `--worktree` 回到 canonical repo root 而非當前 linked worktree 的問題
- 修復 VS Code / Cursor / Windsurf 右鍵貼上重複剪貼簿內容的問題
- 修復長對話與 resumed 對話的效能問題

**待追蹤**
- `OTEL_LOG_TOOL_DETAILS=1` 為 opt-in flag，需手動設定才能取得完整 telemetry

---

### v2.1.156 · 2026-05-29（[Release v2.1.156](https://github.com/anthropics/claude-code/releases/tag/v2.1.156)）

> **繁中摘要**：修復使用 Opus 4.8 時 thinking blocks 被修改導致 API 400 錯誤的問題，升 Opus 4.8 的使用者需盡快更新。

**變更重點**
- 修復 Opus 4.8 下 thinking blocks 被改動後觸發 API errors 的 regression

**實務影響**
- 使用 Opus 4.8 遇到無法解釋的 API errors 的使用者，升版後問題應消失
- 此版本為 hotfix，無其他功能變更

---

### v2.1.154 · 2026-05-28（[Release v2.1.154](https://github.com/anthropics/claude-code/releases/tag/v2.1.154)）

> **繁中摘要**：Opus 4.8 正式推出，預設開啟 high effort（`/effort xhigh`）；動態 workflows 上線，可協調數十至數百個背景 agent；Lean system prompt 成為多數模型的預設值。

**變更重點**
- Opus 4.8 推出，預設 `/effort xhigh`（高努力模式）
- Dynamic workflows：可讓 Claude 建立 workflow，在背景協調大量 agents；用 `/workflows` 查看執行狀態
- Opus 4.8 Fast mode：標準費率的 2 倍，速度 2.5 倍
- Lean system prompt 現在是 Haiku、Sonnet、Opus 4.7 及更早版本以外的所有模型預設值
- `/simplify` 改為只跑 cleanup-only review 並直接套用，不再執行完整 `/code-review --fix`
- `claude agents` 新增 `! <command>` 語法，以背景 session 執行 shell 指令
- Plugin 支援在 `plugin.json` 宣告 `defaultEnabled: false`
- Streaming tool execution 現在在 Bedrock / Vertex / Foundry 上全面啟用
- Stdio MCP server subprocesses 收到 `CLAUDE_CODE_SESSION_ID` 和 `CLAUDECODE=1` 環境變數
- `claude mcp list` / `get` 顯示 unapproved `.mcp.json` servers 為 `⏸ Pending approval`
- 棄用 `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE`，預計 06/01 移除
- 修復 `rm -rf $HOME` 帶尾斜線時未被攔截的安全問題
- 修復 subagents 繞過 worktree isolation 的問題

**實務影響**
- 需要高品質輸出時，Opus 4.8 的預設 high effort 可能增加延遲與成本，需注意
- Dynamic workflows 對大型自動化任務（multi-agent orchestration）是重大新功能
- Bedrock / Vertex / Foundry 用戶現在獲得 streaming tool execution，行為與標準 API 對齊
- Lean system prompt 預設開啟可能影響現有 prompt engineering，需測試確認行為一致性
- 06/01 前須移除對 `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` 的依賴

**待追蹤**
- Dynamic workflows 的詳細 quota 與限制尚待官方文件說明
- Lean system prompt 預設切換對現有 agent setup 的實際影響需實測

---

### v2.1.153 · 2026-05-28（[Release v2.1.153](https://github.com/anthropics/claude-code/releases/tag/v2.1.153)）

> **繁中摘要**：修復多項 MCP 與 subagent 問題，含 stateful MCP reconnect-loop regression、自訂 API gateway 憑證錯誤送出，以及 BREAKING CHANGE：model picker keybinding 名稱更名。

**變更重點**
- Git LFS 支援：github/git plugin marketplace sources 新增 `skipLfs` 選項
- Status line commands 收到 `COLUMNS` 和 `LINES` 環境變數
- `claude doctor` 顯示上次 update 嘗試結果
- macOS：背景 agents 在「隱私權與安全性」顯示為「Claude Code」
- 修復 stateful MCP servers 在 `tools/list` 後無限 reconnect-loop（v2.1.147 regression）
- 修復自訂 API gateway 收到使用者 OAuth credential 而非 gateway token 的安全問題
- Subagent MCP 修復：現在尊重 `--strict-mcp-config`、`--bare`、remote mode、enterprise config
- 修復 `claude update` 安裝最新版而非設定的 channel 版本
- 修復 resume session 時因大量 stored sessions 造成數 GB 記憶體佔用
- **BREAKING CHANGE**：model picker keybinding `modelPicker:setAsDefault` 更名為 `modelPicker:thisSessionOnly`；`keybindings.json` 中的 action `d` 改為 `s`

**實務影響**
- 有自訂 `keybindings.json` 並使用 model picker 快捷鍵的使用者，升版後需手動更新 binding 名稱
- 自訂 API gateway 使用者的安全漏洞已修復，建議盡快升版
- stateful MCP server 用戶（v2.1.147 後遭遇 reconnect-loop）此版本修復
- 在儲存大量 sessions 的機器上 resume 的效能問題已解決

**待追蹤**
- BREAKING CHANGE 的 `keybindings.json` 需手動遷移，官方未提供自動 migration script

---

### v2.1.152 · 2026-05-27（[Release v2.1.152](https://github.com/anthropics/claude-code/releases/tag/v2.1.152)）

> **繁中摘要**：`/code-review --fix` 可直接將 review 建議套用到 working tree；Skills 新增 `disallowed-tools` 控制；`SessionStart` hook 獲得更多控制能力，包含設定 session title 與重新載入 skills。

**變更重點**
- `/code-review --fix` 現在直接套用 review findings（reuse、simplification、efficiency）到 working tree
- `/simplify` 改為呼叫 `/code-review --fix`
- Skills 可在 frontmatter 宣告 `disallowed-tools` 來移除特定工具
- 新增 `/reload-skills` 指令，不重啟即可重新掃描 skill 目錄
- `SessionStart` hook 可回傳 `reloadSkills: true` 以在同一 session 啟用新安裝的 skills
- `SessionStart` hook 可透過 `hookSpecificOutput.sessionTitle` 設定 session 標題
- 新增 `MessageDisplay` hook event，可在顯示時轉換或隱藏 assistant message 內容
- `pluginSuggestionMarketplaces` managed setting 供企業控制 plugin 建議來源
- Fallback model 改為在找不到 primary model 時切換到 `--fallback-model`
- Auto mode 不再需要 opt-in consent
- Vim mode：NORMAL 模式的 `/` 開啟反向歷史搜尋
- `/usage` 對大型 session 檔案使用 streaming memory-efficient scan
- OpenTelemetry 新增 `app.entrypoint` 屬性（需 `OTEL_METRICS_INCLUDE_ENTRYPOINT=true` opt-in）

**實務影響**
- `/code-review --fix` 的行為重大改變：現在會直接修改 working tree，執行前確認 git 狀態
- Skill 開發者可用 `disallowed-tools` 精確控制 skill 執行環境，提升安全性與可預測性
- `SessionStart` hook 的 `reloadSkills` 對自動安裝 plugin 的 onboarding 流程很實用
- `MessageDisplay` hook 為企業合規場景（過濾特定輸出）提供新的擴充點
- Auto mode opt-in consent 移除可簡化 CI/CD 與無人值守腳本的設置

**待追蹤**
- `MessageDisplay` hook 的完整 API schema 尚待官方文件補充

---

## OpenAI Codex

### v0.135.0 · 2026-05-28（[Release v0.135.0](https://github.com/openai/codex/releases/tag/v0.135.0)）

> **繁中摘要**：v0.135.0 強化了診斷工具與 TUI 編輯體驗，`codex doctor` 現可輸出更完整的環境與 Git 診斷資訊，對 debug 環境問題有直接幫助。

**變更重點**
- `codex doctor` 提供更豐富的環境診斷與 Git 診斷輸出
- Vim mode 新增 text-object 編輯支援，改善 word motion 行為
- `/permissions` 指令現在顯示命名的 permission profiles
- Markdown 表格在 TUI 中可讀性提升

**實務影響**
- `codex doctor` 診斷輸出更完整，排查 CLI 環境問題時可取得更多上下文
- Vim mode 使用者的編輯效率提升（text-object 支援是常用操作）
- Permission profiles 可在 TUI 內直接檢視，減少切換設定檔時的摸索成本

---

### v0.134.0 · 2026-05-26（[Release v0.134.0](https://github.com/openai/codex/releases/tag/v0.134.0)）

> **繁中摘要**：v0.134.0 新增本地對話歷史搜尋，並改善 MCP 多伺服器管理與遠端連線穩定性，對重度使用 MCP 工具的 agent workflow 有明顯影響。

**變更重點**
- 新增本地對話歷史搜尋，支援大小寫不敏感比對
- `--profile` 成為 CLI 與 sandbox 流程的主要選擇器
- MCP 設定新增 per-server 環境變數指定
- 標記為 `readOnlyHint` 的 MCP 工具現可並行執行
- 遠端連線加入重連與重試機制

**實務影響**
- 本地歷史搜尋讓舊對話的查找更快，不需翻捲長對話
- MCP per-server 環境變數讓多伺服器設定更精細，降低全域污染風險
- `readOnlyHint` 並行執行可顯著縮短多工具查詢的等待時間
- 遠端重連機制改善長時間 session 的穩定性

**待追蹤**
- `readOnlyHint` 並行執行的條件與限制尚待官方文件確認

---

## GitHub Changelog

### 2026-05-29（[Copilot usage metrics API adds cohorts for AI adoption](https://github.blog/changelog/2026-05-29-copilot-usage-metrics-api-adds-cohorts-for-ai-adoption)）

> **繁中摘要**：Copilot 使用量 API 新增 AI adoption cohort 分類，企業與組織管理員可區分「主動採用 AI 建議」與「偶發觸發補全」的使用者，提供更細粒度的採用分析。

**變更重點**
- Copilot usage metrics REST API 新增 cohort 欄位，對每位已參與使用者進行 AI adoption 分類
- 分類邏輯區分主動使用 AI 建議 vs. 偶發觸發補全
- 透過既有 REST API endpoints 即可取得，無需更換 endpoint

**實務影響**
- 企業 / 組織管理員可用 cohort 資料說明 AI 採用深度，而非僅報告活躍用戶數
- 既有 API 整合不需改動 endpoint，只需解析新增欄位

**待追蹤**
- Cohort 的具體分類定義與邊界條件尚未在 Body 中詳述，實作前建議查閱完整 API 文件
