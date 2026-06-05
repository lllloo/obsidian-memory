---
title: "2026-06-05 Daily Updates"
created: 2026-06-05
updated: 2026-06-05
tags:
  - updates
  - copilot
  - codex
  - claude-code
---

## GitHub Changelog

### 2026-06-04（[Fix with Copilot for failing Actions now in Pro, Pro+, and Max](https://github.blog/changelog/2026-06-04-fix-with-copilot-for-failing-actions-now-in-pro-pro-and-max)）

> **繁中摘要**：Copilot Pro、Pro+、Max 訂閱者現在可在 Actions job 失敗時一鍵呼叫 Copilot cloud agent 自動診斷並修復，直接整合進 CI 失敗流程。

**變更重點**
- Fix with Copilot 按鈕現已開放給 Pro、Pro+、Max 方案（先前僅限更高階方案）
- 背後使用 Copilot agentic engine 自動診斷失敗原因並產生修復

**實務影響**
- CI 失敗後不需手動切換視窗分析 log，可直接從 Actions 頁面啟動 agent 修復
- 適用個人訂閱者（Pro/Pro+）與團隊訂閱者（Max），覆蓋範圍擴大

### 2026-06-04（[Agent tasks REST API now available for Copilot Pro, Pro+, and Max](https://github.blog/changelog/2026-06-04-agent-tasks-rest-api-now-available-for-copilot-pro-pro-and-max)）

> **繁中摘要**：Copilot cloud agent 現提供 REST API（public preview），可程式化啟動任務、輪詢狀態、取回結果，適合整合進自動化 pipeline。

**變更重點**
- Agent tasks REST API 開放給 Pro、Pro+、Max 用戶（public preview）
- 支援非同步模式：kick off task → check status → retrieve results

**實務影響**
- 可在 CI/CD pipeline 或外部腳本中以 API 呼叫觸發 Copilot agent 任務，不需人工點擊
- Public preview 階段，API 介面仍可能變動，不宜直接用於生產關鍵流程

**待追蹤**
- API 文件與 rate limit 細節尚待確認；public preview 期間介面有破壞性變更風險

### 2026-06-04（[Larger context windows and configurable reasoning levels for GitHub Copilot](https://github.blog/changelog/2026-06-04-larger-context-windows-and-configurable-reasoning-levels-for-github-copilot)）

> **繁中摘要**：GitHub Copilot 支援最高 100 萬 token context window，並可調整 reasoning level（速度 vs 深度），適合處理大型 codebase 或複雜任務。

**變更重點**
- Context window 擴展至 1 million tokens，可載入整個 codebase 或大量檔案
- 新增 configurable reasoning levels，可依任務複雜度在速度與深度之間調整

**實務影響**
- 大型 monorepo 或跨模組重構任務可一次帶入更完整的上下文，減少分批查詢
- Reasoning level 設定讓簡單任務可優先回應速度、複雜任務可換取更深入分析

**待追蹤**
- 具體 reasoning level 選項與對應模型/計費方式尚待官方說明

### 2026-06-04（[GitHub Copilot in Visual Studio — May update](https://github.blog/changelog/2026-06-04-github-copilot-in-visual-studio-may-update)）

> **繁中摘要**：Visual Studio 2026 的 Copilot 五月更新強化了 agent mode 規劃、code review 流程與 PR 管理整合，適用所有 Copilot 訂閱者。

**變更重點**
- Agent mode 的規劃流程獲得改善
- Code review 流程與 PR 管理整合強化

**實務影響**
- 在 Visual Studio 環境中使用 Copilot 進行 PR review 與任務規劃的效率有所提升
- 適用全體 Copilot 用戶，無需額外設定

**待追蹤**
- Body 未列出具體功能細節，需查閱 Visual Studio 2026 release notes 確認完整變更清單

### 2026-06-04（[Copilot Chat brings richer context to pull requests](https://github.blog/changelog/2026-06-04-copilot-chat-brings-richer-context-to-pull-requests)）

> **繁中摘要**：Copilot Chat 在 github.com 上處理 PR 時現已 GA，可理解完整 diff、review comments 與 CI 狀態，讓 PR 問答更有脈絡。

**變更重點**
- 從 public preview 升至 GA
- Copilot Chat 可理解完整 PR diff、review comments、CI context
- 適用 github.com 上的 PR 工作流程

**實務影響**
- Code review 時可直接對 Copilot Chat 問「這段變更為什麼這樣寫」或「CI 失敗原因」，不需手動整理上下文
- GA 後穩定性提升，可納入日常 review 流程

---

## OpenAI Codex

### 26.602 · 2026-06-04（[Codex app updates 26.602](https://developers.openai.com/codex/changelog#codex-app-updates-26602)）

> **繁中摘要**：Codex app 26.602 新增 Profile 頁面的 activity insights 與 share cards，並修復 Computer Use 啟動問題與多項 browser/review UI bug。

**變更重點**
- Profile 新增 activity insights（使用量統計）與 share cards
- 修復 Computer Use 啟動錯誤與 appshot error reporting
- 修復 browser/review UI 問題
- Onboarding 流程新增更多角色選項

**實務影響**
- Computer Use 功能的啟動穩定性改善，使用 browser automation 任務較不易卡在初始化
- UI bug fix 改善 review 流程的可靠性

---

## Claude Code

### v2.1.163 · 2026-06-04（[2.1.163](https://code.claude.com/docs/en/changelog#2026-06-04-2-1-163)）

> **繁中摘要**：Claude Code 2.1.163 新增 managed settings 版本限制、`/plugin list`、Stop hook 回傳 `additionalContext`，並修復多個 `claude -p`、Windows、hook 條件匹配的關鍵 bug。

**變更重點**
- Managed settings 新增 `requiredMinimumVersion` / `requiredMaximumVersion`：版本不符時 Claude Code 拒絕啟動並導引用戶至核可版本
- `/plugin list` 命令上線，支援 `--enabled` / `--disabled` filter
- `/btw` 新增 "c to copy" 快捷鍵，複製原始 markdown 到剪貼簿
- Stop 與 SubagentStop hook 可回傳 `hookSpecificOutput.additionalContext`，讓 Claude 繼續對話而不觸發 hook error
- Skills：新增 `\$` 跳脫語法，可在指令主體中插入字面量 `$`（不被視為變數展開）
- stdio MCP server 現在與 hooks/Bash 共享相同的 `CLAUDE_CODE_SESSION_ID`（`--resume` 時）
- 背景 agent session 現在在背景自動更新版本，重新連線時不再需要 cold restart 等待
- 修復 `claude -p` 在背景指令從未結束時永久 hang
- 修復 `claude -p` 在 Bedrock/Vertex/Foundry + `CI=true` 下誤報 `ANTHROPIC_API_KEY required`
- 修復 bazel / EDR 保護的 Go workflow 下 `$TMPDIR` 被覆寫到 `/tmp/claude-{uid}` 的問題
- 修復 Windows OneDrive 目錄或唯讀 session-env 目錄的 EEXIST 錯誤
- 修復 org managed permission rules 在全新 config 目錄啟動時未在整個 session 生效
- 修復 hook `if: "Bash(...)"` 條件對含 `$()` / `$VAR` 的所有指令誤觸發；現在正確匹配子 shell 與反引號內容
- 修復 home directory 路徑 deny rule 未阻擋透過 `$HOME` 展開的相同路徑

**實務影響**
- 企業/團隊管理員可用版本限制 managed setting 鎖定可用版本範圍，避免用戶跑在未核准版本
- Stop hook 用 `additionalContext` 可實作「hook 失敗後給 Claude 建議並繼續」的流程，不再必須讓 hook error 中斷 turn
- Skills 指令內現在可安全使用帶數字的 `$` 字元（如 `$1`、`$2` 參數）不被誤判為變數
- Bazel / Go EDR workflow 使用者可升版解除 `$TMPDIR` 破壞問題
- hook 條件匹配修復後，子 shell 內的 Bash pattern 不再濫觸，hook rule 精準度提高

### v2.1.162 · 2026-06-03（[2.1.162](https://code.claude.com/docs/en/changelog#2026-06-03-2-1-162)）

> **繁中摘要**：Claude Code 2.1.162 改善 `claude agents` 可觀測性、修復多個 Windows 路徑匹配與 MCP timeout bug，並讓 startup 噪音大幅降低。

**變更重點**
- `claude agents --json` 新增 `waitingFor` 欄位，顯示 session 卡在什麼（如 permission prompt）
- `--tools` 顯式列出 Grep/Glob 時，native build 現在提供專屬搜尋工具
- `/effort` 現在在設定 persist default 時給予確認提示
- Slash command autocomplete 選單點擊後填入 prompt 而非直接執行
- Remote Control 改為常駐 footer pill 顯示
- Windsurf 在 `/ide` 選單等處重新命名為 Devin Desktop
- 修復 config 目錄唯讀/不可寫時 silent startup hang；現在改用 in-memory config 並顯示錯誤
- 修復 WebFetch permission rules 未套用到預先核准域名；明確的 deny/ask/allow 規則現在優先於 preapproved-host 自動允許
- 修復 Windows 下反斜線或大小寫變體路徑的 permission rule 從未匹配；修復 Read deny rules 未從 Glob/Grep 結果隱藏檔案
- 修復 stream-json/SDK session 在 turn 剛開始送 Esc 中斷時被靜默丟棄
- 修復 MCP per-server `timeout` 設定值低於 1000 ms 時被強制提高到 1 秒導致所有 tool call 被中止
- 修復 LSP tool 的 `workspaceSymbol` 操作無回傳；現接受 `query` 參數
- 修復跨 session 訊息（`SendMessage`）在 `CLAUDE_CODE_TMPDIR` 或 `$TMPDIR` 指向深層目錄時靜默失敗
- 修復用 ← 將 session 移至背景時若 background service 無法啟動則對話靜默丟失
- Startup 通知改為按嚴重度分組，警告重寫為更精簡；失敗 turn 改用單行警告
- 背景服務啟動改善，現在等待 endpoint-security 掃描新 binary 完成後再繼續
- 移除 "Claude in Chrome enabled" 和 "marketplace installed" 啟動訊息

**實務影響**
- `waitingFor` 欄位讓腳本可偵測 agent session 是否卡在 permission prompt，方便自動化監控
- MCP timeout 修復：設定 < 1s timeout 的 server 不再因 1s 強制下限而讓所有 tool call 超時失敗
- Windows 用戶 permission rule 路徑匹配修復後，含反斜線或大小寫差異的 deny/allow 規則終於正確生效
- WebFetch deny rule 現在可覆蓋預先核准域名，安全策略更完整

### v2.1.161 · 2026-06-02（[2.1.161](https://code.claude.com/docs/en/changelog#2026-06-02-2-1-161)）

> **繁中摘要**：Claude Code 2.1.161 支援 OTEL 自訂標籤切分用量指標、平行工具呼叫容錯改善，並修復 `claude -p` stdout 污染、MCP secrets 外洩與多個背景 agent 問題。

**變更重點**
- `OTEL_RESOURCE_ATTRIBUTES` 值現在作為 metric datapoint 的 label 輸出，可按 team / repo 等自訂維度切分用量指標
- `claude agents` rows 現在在 fan-out 時顯示 `done/total`；peek 顯示最長執行中的項目
- `/mcp` 收合從未登入的 claude.ai connector，改為 "Show unused connectors" row
- 平行工具呼叫：Bash 指令失敗不再取消同 batch 其他呼叫，每個工具各自回傳結果
- Linux fullscreen mode：clipboard 現在使用 `wl-copy`/`xclip`/`xsel`，同時寫入 clipboard 與 PRIMARY selection（支援中鍵貼上）
- 修復 `forceLoginOrgUUID`/`forceLoginMethod` managed-settings 封鎖第三方 provider session（Bedrock, Vertex, Foundry, Mantle）的 regression（自 2.1.146 引入）
- 修復背景 subagent 輸出污染 `claude -p` stdout（`--output-format text` 或 `json`）
- 修復 `claude mcp list/get/add` 將 secrets 印到終端：`${VAR}` 不再展開，credential header 與 URL secrets 改為 redact
- 修復 `isolation: "worktree"` 的 Workflow agents 在背景 session 中無法編輯自己 worktree 內的檔案
- 修復背景 session 從 `claude agents` 啟動時使用 daemon 環境的舊 model 而非 `settings.json` 中設定的 model

**實務影響**
- Bedrock/Vertex/Foundry 用戶若曾升級到 2.1.146–2.1.160 的 `forceLoginOrgUUID` regression，升版後可恢復正常
- `claude -p` 腳本整合用戶：修復背景 subagent 污染 stdout，JSON/text 輸出解析不再受背景輸出干擾
- `claude mcp` 操作中 secrets 不再洩漏到終端 log，安全性提升
- OTEL 用戶可設定 `OTEL_RESOURCE_ATTRIBUTES` 加上 team/repo 標籤後切分 usage dashboard

### v2.1.160 · 2026-06-02（[2.1.160](https://code.claude.com/docs/en/changelog#2026-06-02-2-1-160)）

> **繁中摘要**：Claude Code 2.1.160 在寫入 shell startup 檔與 build-tool config 前新增提示確認，重新命名 `ultracode` 觸發關鍵字取代 `workflow`，並大量修復 Windows / background agent 問題。

**變更重點**
- 寫入 `.zshenv`、`.zlogin`、`.bash_login`、`~/.config/git/` 前新增提示，避免非預期指令執行
- `acceptEdits` 模式寫入可授予執行權的 build-tool config（`.npmrc`、`.yarnrc*`、`bunfig.toml`、`.bazelrc`、`.pre-commit-config.yaml`、`.devcontainer/` 等）前現在先提示
- Edit 工具：單一檔案的 `grep`/`egrep`/`fgrep` 現在滿足 read-before-edit 檢查，不再需要另外 Read
- **Dynamic workflow 觸發關鍵字從 `workflow` 改名為 `ultracode`**；`workflow` 這個詞不再觸發；用自己的話描述仍可觸發
- 移除 `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE`，該環境變數現在是 no-op
- 修復 WSL copy-on-select 未寫入 Windows clipboard
- 修復從 `claude agents` 還原已完成 session 丟失聊天紀錄並重跑原始 prompt
- 修復隔夜 retire 後重新連線的背景 session 丟失對話並重跑原始 prompt
- 修復 Windows 下背景 session 在高 CPU 負載時 Esc / 方向鍵 / 輸入失去回應
- 修復 voice mode 在專案目錄或分支名含非 ASCII 或特殊字元時連線失敗
- 修復 `/effort ultracode` 誤指 dynamic workflows 設定為原因
- 修復 model-not-found 錯誤建議使用 `--model`（在 SDK 執行情境下不適當）

**實務影響**
- **`ultracode` 取代 `workflow` 為觸發關鍵字**：現有腳本或 prompt template 若硬編碼 `workflow` 觸發字，需更新為 `ultracode`
- `acceptEdits` 用戶：build-tool config 寫入現有安全提示，避免自動修改 `.npmrc` 等影響執行環境的檔案
- Windows / WSL 用戶多項操作修復，background session 穩定性大幅提升

**待追蹤**
- `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` 已移除，若有依賴此環境變數的腳本需清理

### v2.1.158 · 2026-05-30（[2.1.158](https://code.claude.com/docs/en/changelog#2026-05-30-2-1-158)）

> **繁中摘要**：Claude Code 2.1.158 將 Auto mode 擴展到 Bedrock、Vertex 和 Foundry，支援 Opus 4.7 和 Opus 4.8，需手動設定環境變數啟用。

**變更重點**
- Auto mode 現在可用於 Bedrock、Vertex、Foundry，model 限定 Opus 4.7 和 Opus 4.8
- 啟用方式：設定環境變數 `CLAUDE_CODE_ENABLE_AUTO_MODE=1`

**實務影響**
- 透過 AWS Bedrock、Google Vertex 或 Foundry 使用 Claude Code 的企業用戶，現在可在 Opus 4.7/4.8 上啟用 Auto mode
- 預設不啟用，需明確 opt-in

### v2.1.157 · 2026-05-29（[2.1.157](https://code.claude.com/docs/en/changelog#2026-05-29-2-1-157)）

> **繁中摘要**：Claude Code 2.1.157 讓 `.claude/skills` 目錄的 plugin 不需 marketplace 即自動載入，並新增 `claude plugin init` 腳手架指令與多項 agents/worktree 修復。

**變更重點**
- `.claude/skills` 目錄內的 plugin 現在自動載入，不需透過 marketplace 安裝
- 新增 `claude plugin init <name>`，在 `.claude/skills` 下建立 plugin 骨架
- 新增 `/plugin` 參數 autocomplete：子命令、已安裝 plugin 名稱、已知 marketplace 的 plugin
- `claude agents`：`settings.json` 的 `agent` 欄位現在套用到 dispatched sessions；可用 `--agent <name>` 覆蓋
- `EnterWorktree` 現在可以在 Claude-managed worktrees 之間中途切換
- `tool_decision` telemetry events 在 `OTEL_LOG_TOOL_DETAILS=1` 時包含 `tool_parameters`（bash commands、MCP/skill names）
- Claude 管理的 worktrees 在 agent 完成後現在解除鎖定，`git worktree remove`/`prune` 可正常清理
- 修復使用 desktop app、IDE extensions、SDK 在 auto/bypass-permissions 模式下出現 sandbox network permission prompts
- 修復 `claude agents` 已完成 session 在 idle subagent 仍存在時無法 retire
- 修復 `.claude/worktrees/` 下的背景 agent worktrees 在 30 天 job retention sweep 後成為孤立目錄
- 修復背景 session 在 sleep/wake 後重新連線時模型拿到錯誤日期
- 修復 `--worktree` / `--worktree --tmux` 返回到 canonical repo root 而非當前 linked worktree
- WSL：修復圖片貼上、Windows 11 截圖貼上，並支援從 Windows Explorer 拖入圖片
- `/terminal-setup` 現在在 VS Code/Cursor/Windsurf integrated terminal 中停用 GPU 加速
- `/config` 新增 "Workflow keyword trigger" 設定，可停用 `workflow` 關鍵字觸發 dynamic workflow

**實務影響**
- **Local plugin 開發**：`.claude/skills/` 放的 skill 不再需要 marketplace 即可使用，本機 repo 可直接自帶 skills 供 Claude Code 呼叫
- `claude plugin init` 讓建立新 plugin 有標準骨架，不必手動複製結構
- OTEL 用戶設定 `OTEL_LOG_TOOL_DETAILS=1` 可在 telemetry 中看到每次工具呼叫的具體參數，方便 audit
- `EnterWorktree` mid-session 切換讓複雜多 worktree 工作流更流暢
