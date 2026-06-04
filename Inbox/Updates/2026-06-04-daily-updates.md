---
title: "2026-06-04 Daily Updates"
created: 2026-06-04
updated: 2026-06-04
tags:
  - updates
  - claude-code
  - copilot
  - codex
---

## Claude Code

### v2.1.162 · 2026-06-03（[Update 2.1.162](https://code.claude.com/docs/en/changelog#2116)）

> **繁中摘要**：2.1.162 包含多項 agents 可觀測性改進、工具路由修正、slash command UX 調整，以及多個影響 Windows、SDK、MCP、LSP 的 bug fix。

**變更重點**
- `claude agents --json` 新增 `waitingFor` 欄位，顯示 session 被什麼阻塞（如 permission prompt）
- `--tools` 明確列出 Grep/Glob 現在可在 embedded search 的 native build 上正確啟用（原先靜默忽略）
- `/effort` 選定後會確認該 level 是否將成為新 session 的預設
- Slash command autocomplete：點選條目只填入、不立即執行；需按 Enter 才觸發
- Remote Control 改為常駐 footer pill 顯示（含 session 連結），不再是啟動訊息
- Windsurf 在 `/ide`、`/terminal-setup`、`/scroll-speed` 選單中更名為 Devin Desktop

**Bug Fixes（影響日常使用）**
- 修正 config 目錄不可寫時靜默卡住 → 現在以 in-memory config 啟動並顯示錯誤
- 修正 WebFetch permission rules 未套用到預批准 domain
- 修正 Windows permission rules 使用反斜線或大小寫路徑時永遠不匹配；Read deny rules 未對 Glob/Grep 隱藏檔案
- 修正 stream-json/SDK session 在 turn 開始時發送 Esc 被靜默丟棄
- 修正含 emoji 的 classifier side-query 在截斷邊界觸發 API 400 錯誤
- 修正 MCP per-server timeout 低於 1000ms 時被強制 floor 到 1 秒
- 修正 LSP tool `workspaceSymbol` 回傳空結果
- 修正 `claude agents` 在寬終端截斷 live status；截斷長 session name；attach 偶爾彈回清單；Ctrl+V 圖片貼上無效
- 修正背景 session 無法啟動時靜默丟失對話
- 修正 `SendMessage` 跨 session 訊息在 CLAUDE_CODE_TMPDIR/TMPDIR 指向深層目錄時靜默失效

**實務影響**
- `waitingFor` 讓監控腳本可精確判斷 agent 卡在哪一步（permission vs. 計算）
- Windows 用戶的路徑匹配問題修正後，permission rules 才能正確運作
- MCP timeout 修正影響所有設定低於 1 秒超時的 server 配置
- SDK/stream-json 用戶的 Esc interrupt 現在可靠

---

### v2.1.161 · 2026-06-02（[Update 2.1.161](https://code.claude.com/docs/en/changelog#21161)）

> **繁中摘要**：2.1.161 帶來 OTEL 自訂標籤切分指標、agents 進度顯示改進、平行工具呼叫失敗隔離，以及多個影響 managed-policy、背景 agent、Windows 的 bug fix。

**變更重點**
- `OTEL_RESOURCE_ATTRIBUTES` 的值現在作為 metric datapoint 的 label，可依 team/repo 等自訂維度切分使用量指標
- `claude agents` 列表顯示 `done/total` 進度；peek 顯示最長執行項目
- `/mcp` 折疊未登入的 claude.ai connector，改以「Show unused connectors」收納
- 平行工具呼叫：單一 Bash 指令失敗不再取消同 batch 的其他呼叫，各自回傳獨立結果
- Linux fullscreen 剪貼簿改進（wl-copy/xclip/xsel），同時寫入 clipboard 與 PRIMARY selection 以支援 middle-click paste

**Bug Fixes（影響日常使用）**
- 修正 `forceLoginOrgUUID`/`forceLoginMethod` managed-settings policies 封鎖第三方 provider session（Bedrock、Vertex、Foundry、Mantle）
- 修正背景 subagent 輸出污染 `claude -p` stdout（`--output-format text/json` 模式）
- 修正 `/autofix-pr` 在 git worktree 內誤報「cannot run on the default branch」
- 修正 `--resume` picker 在當前目錄不是 git worktree 時不顯示該目錄的 session
- 修正 Windows hooks 明確呼叫 bash 時失敗
- 修正 OpenTelemetry log events 在 telemetry 初始化前靜默丟棄
- 修正 `claude mcp list/get/add` 將 secrets 印至終端（`${VAR}` 不再展開，credential headers 與 URL secrets 自動遮蔽）
- 修正 Workflow agents 在 `isolation: "worktree"` 模式下被阻擋編輯自己 worktree 內的檔案
- 修正背景 session 使用 daemon 環境中的過時 model 啟動
- 修正 Write tool 結果在 resume session 後渲染時可能 crash

**實務影響**
- OTEL label 切分對多團隊共用 Claude Code 的組織有直接用途，可做成本歸因
- MCP secrets 不再外洩至終端 log，安全性提升
- Bedrock/Vertex/Foundry 用戶若使用 managed-settings policy 需確認此修正是否解除封鎖
- 平行工具失敗隔離改善多工具並發的穩定性

---

### v2.1.160 · 2026-06-02（[Update 2.1.160](https://code.claude.com/docs/en/changelog#21160)）

> **繁中摘要**：2.1.160 在寫入 shell startup 檔案與 build-tool config 前新增確認提示，收緊 `acceptEdits` 安全邊界；同時修正多個 Windows、背景 agent、WSL 相關問題。

**變更重點**
- 寫入 shell startup 檔案（`.zshenv`、`.zlogin`、`.bash_login`）及 `~/.config/git/` 前現在會提示確認，防止非預期指令執行
- `acceptEdits` 模式在寫入可授予程式碼執行權限的 build-tool config 前會提示：`.npmrc`、`.yarnrc*`、`bunfig.toml`、`.bazelrc`、`.pre-commit-config.yaml`、`.devcontainer/` 等
- Edit 不再需要在 grep 查看後再做獨立 Read：單一檔案 grep/egrep/fgrep 命令現在滿足 read-before-edit 檢查
- Dynamic workflow 觸發關鍵字重新命名（`workflow` → `ultracode`）

**Bug Fixes（影響日常使用）**
- 修正 WSL 上 copy-on-select 未寫入 Windows clipboard
- 修正從 `claude agents` 還原已完成 session 時丟失對話歷程並重跑原始 prompt
- 修正背景 session 在 sleep/wake 後重新 attach 時丟失對話並重跑 prompt
- 修正 `claude --bg` 在 background daemon cold-start 時偶爾報「socket missing」
- 修正 Windows 上背景 session 的起始目錄在 `claude rm` 後無法刪除
- 修正 `claude agents` 退出 session 時因 auto-updater 重複檢查導致凍結數秒
- 修正 Windows attached session 的 Esc、方向鍵、輸入無回應
- 修正背景 agent 向不支援的終端（Apple Terminal、tmux）發送 sync-output marker
- 修正 CJK IME 組字位置顯示在螢幕左下角而非輸入游標處
- 修正 `file:///C:/...` 連結在 Windows 上被改寫為錯誤路徑
- 修正 project 目錄或分支名含非 ASCII/特殊字元時 voice mode 無法連線
- 修正 `/effort ultracode` 錯誤歸咎於 dynamic workflows 設定

**實務影響**
- `acceptEdits` 模式下的安全邊界收緊，自動化流程中若有寫入 `.npmrc` 等檔案需預期多一個確認步驟
- Windows/WSL 用戶的多項體驗問題在此版本集中修正
- CJK 用戶 IME 輸入位置修正改善可用性

---

### v2.1.158 · 2026-05-30（[Update 2.1.158](https://code.claude.com/docs/en/changelog#21158)）

> **繁中摘要**：Auto mode 現在可在 Bedrock、Vertex、Foundry 上用於 Opus 4.7 與 Opus 4.8，需透過環境變數 opt-in。

**變更重點**
- Auto mode 擴展至 Bedrock、Vertex、Foundry，支援 Opus 4.7 與 Opus 4.8
- 需設定 `CLAUDE_CODE_ENABLE_AUTO_MODE=1` 才能啟用

**實務影響**
- 在 AWS/GCP 等托管環境使用 Opus 4.7/4.8 的團隊現在可使用 Auto mode 的動態 effort 調整
- 需手動設定環境變數，不會自動啟用

---

### v2.1.157 · 2026-05-29（[Update 2.1.157](https://code.claude.com/docs/en/changelog#21157)）

> **繁中摘要**：Plugins 現在從 `.claude/skills` 自動載入，不需 marketplace；新增 `claude plugin init` scaffold 指令與 autocomplete；agents 設定、worktree 管理與 OTEL tool 遙測均有改進。

**變更重點**
- `.claude/skills` 目錄下的 plugin 自動載入，不需透過 marketplace
- 新增 `claude plugin init <name>` 指令，在 `.claude/skills` scaffold 新 plugin
- Plugin autocomplete 支援 subcommands、已安裝 plugin 名稱、已知 marketplace plugin
- `settings.json` 的 `agent` 欄位現在對 dispatched session 生效；可用 `--agent <name>` 覆蓋
- `EnterWorktree` 可在 session 中途切換 Claude-managed worktrees
- `tool_decision` 遙測事件在 `OTEL_LOG_TOOL_DETAILS=1` 時包含 `tool_parameters`（bash 指令、MCP/skill 名稱）
- Claude 管理的 worktree 完成後不再鎖定，`git worktree remove/prune` 可正常清理
- Plugins 可宣告 `defaultEnabled: false`
- Stdio MCP server subprocess 現在收到 `CLAUDE_CODE_SESSION_ID` 與 `CLAUDECODE=1` 環境變數
- `claude mcp list/get` 顯示未批准的 `.mcp.json` server 為「Pending approval」

**Bug Fixes**
- 修正無效圖片（零位元組、損毀）透過 paste/MCP/dialog 附加時使 request crash
- 修正 desktop app/IDE/SDK 的沙箱 network permission prompt 在 auto/bypass 模式下不應出現卻出現
- 修正 `claude agents` 已完成 session 因有 idle subagent 未 retire
- 修正 `.claude/worktrees/` 下的背景 agent worktree 在 30 天 retention sweep 後孤立
- 修正背景 session sleep/wake 後重連時模型收到錯誤日期

**實務影響**
- `.claude/skills` 自動載入讓本地 plugin 開發流程更直接，不需 marketplace 審核
- `OTEL_LOG_TOOL_DETAILS=1` 對需要細粒度 tool 追蹤的 CI/監控場景有用
- MCP server 現在可讀取 `CLAUDE_CODE_SESSION_ID`，適合需要 session 隔離的 server 設計
- `/terminal-setup` 在 VS Code/Cursor/Windsurf integrated terminal 中停用 GPU 加速

---

### v2.1.154 · 2026-05-28（[Update 2.1.154](https://code.claude.com/docs/en/changelog#21154)）

> **繁中摘要**：Opus 4.8 正式推出，預設 high effort，Fast mode 大幅降價；Dynamic workflows 讓 Claude 可協調數十至數百個背景 agent；lean system prompt 成為多數 model 的預設。

**變更重點**
- **Opus 4.8** 發布，預設 high effort；`/effort xhigh` 適用最難任務
- **Dynamic workflows**：可要求 Claude 建立 workflow，在背景協調數十至數百個 agent；`/workflows` 查看執行狀態
- Opus 4.8 Fast mode 降至標準費率 2x（速度 2.5x），相比前一版本大幅降價
- Lean system prompt 成為除 Haiku、Sonnet、Opus 4.7 及更早版本以外所有 model 的預設
- Claude 保留 multiple-choice prompt 僅用於真正無法自行決定的情況（減少不必要的確認）
- `/simplify` 現在執行 cleanup-only review（reuse、simplification、efficiency、altitude）並自動套用
- `/effort` slider 標籤從 Speed/Intelligence 改為 Faster/Smarter
- `claude agents`：`! <command>` 以背景 session 執行 shell 指令
- Streaming tool execution 永遠啟用，包括 Bedrock/Vertex/Foundry
- Stdio MCP server subprocess 收到 `CLAUDE_CODE_SESSION_ID` 與 `CLAUDECODE=1`
- `claude mcp list/get` 顯示未批准 server 為「Pending approval」
- 棄用 `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE`（已於 06/01 移除）

**Bug Fixes**
- 修正 `rm -rf $HOME` 在 HOME 有尾斜線時未被 dangerous path 攔截
- 修正背景 session 中的 subagent 繞過 worktree-isolation guard
- 修正孤立 `claude --bg-pty-host` process 100% CPU 佔用
- 修正 `worktree.baseRef: "head"` 解析到錯誤 HEAD

**實務影響**
- Dynamic workflows 是此版本最大功能變更，適合需要大規模平行 agent 的複雜任務；`/workflows` 是新的監控入口
- Opus 4.8 Fast mode 降價讓高速推理的成本門檻顯著降低
- Lean system prompt 預設化可能影響現有依賴詳細系統 prompt 行為的 workflow，需測試
- `ultracode` 關鍵字取代 `workflow` 避免意外觸發，現有 prompt 若含「workflow」字詞需留意

---

## GitHub Changelog

### v1.120–v1.123 · 2026-06-03（[GitHub Copilot in Visual Studio Code, May releases](https://github.blog/changelog/2026-06-03-github-copilot-in-visual-studio-code-may-releases)）

> **繁中摘要**：GitHub Copilot for VS Code 在 5 月正式推出 Agents mode（GA）、加入 MCP image input 支援與 agent skills marketplace，並新增 GitHub Copilot Search、`/fix` diagnostics 指令及 notebook `Ask` 指令，大幅擴展 agentic workflow。

**變更重點**
- Agents mode 正式 GA，提供 real-time streaming 回應與 thinking indicators
- VS Code Marketplace 開放安裝 agent skills；custom instructions 支援 agent mode
- MCP 新增 image input 支援
- GitHub Copilot Search 上線
- Smart context selector 改進 + 自動從 open files 取 context
- Inline edits：新增 inline follow-ups、Next Edit Suggestions 支援更多 model
- 新增 `/fix` command（diagnostics）、notebook `Ask` command、改良 test generation flow

**實務影響**
- Agents mode GA 代表 agentic 任務流程可用於生產環境，不再 preview 限制
- MCP image input 讓 multimodal context 可直接進 Copilot agent；skills marketplace 提供可擴充的工具鏈
- `/fix` 與 notebook `Ask` 填補診斷修復與 notebook 互動的操作缺口

---

### 2026-06-02（[GPT-4.1 deprecated](https://github.blog/changelog/2026-06-02-gpt-4-1-deprecated)）

> **繁中摘要**：GitHub Copilot 已於 2026 年 6 月 1 日在所有體驗（Chat、inline edits、ask/agent mode、code completions）中棄用 GPT-4.1，官方建議改用 gpt-4o 或 o4-mini。

**變更重點**
- GPT-4.1 deprecation 日期：2026-06-01
- 影響範圍：所有 Copilot 體驗（Chat、inline edits、ask/agent mode、code completions）
- 建議替代模型：gpt-4o 或 o4-mini

**實務影響**
- 若工作流程或設定中明確指定 GPT-4.1，需立即切換至 gpt-4o 或 o4-mini
- 現有 agent/automation 若依賴 GPT-4.1 的行為特性，需重新評估 o4-mini 的適用性（cost vs capability tradeoff）

---

### 2026-06-02（[Expanded technical preview availability for the GitHub Copilot app](https://github.blog/changelog/2026-06-02-expanded-technical-preview-availability-for-the-github-copilot-app)）

> **繁中摘要**：GitHub Copilot 桌面 app technical preview 現向所有 Copilot Pro、Pro+、Business、Enterprise 訂閱用戶開放，支援 Windows、macOS、Linux，讓 Copilot 可在瀏覽器與 IDE 之外獨立運作。

**變更重點**
- Technical preview 擴大至所有現有 Copilot 付費方案用戶（Pro / Pro+ / Business / Enterprise）
- 支援平台：Windows、macOS、Linux

**實務影響**
- 訂閱用戶可立即下載並在 IDE 外使用 Copilot，適合 terminal-centric 或多視窗工作流

**待追蹤**
- Technical preview 轉 GA 的時程未公告

---

### 2026-06-02（[Copilot SDK is now generally available](https://github.blog/changelog/2026-06-02-copilot-sdk-is-now-generally-available)）

> **繁中摘要**：GitHub Copilot SDK 正式 GA，開發者可將 Copilot agentic engine 嵌入自製應用程式、服務與開發工具，提供穩定 API 與生產環境支援。

**變更重點**
- Copilot SDK 從 preview 升至 GA
- 用途：將 Copilot agentic engine 嵌入自訂 app、服務、developer tools
- 提供 stable API 與 production-ready 支援

**實務影響**
- 可用 Copilot SDK 在自建工具中整合 agentic 能力，不再受 preview 不穩定性限制

---

### 2026-06-02（[Copilot CLI: Improved UI, rubber duck, prompt scheduling, and voice input](https://github.blog/changelog/2026-06-02-copilot-cli-improved-ui-rubber-duck-prompt-scheduling-and-voice-input)）

> **繁中摘要**：GitHub Copilot CLI 大改版：rubber duck 模式與 voice input 今日 GA，prompt scheduling 與新 terminal UI 進入 public preview；rubber duck 模式讓 Copilot CLI 只討論不執行，適合 codebase 探索與問題釐清。

**變更重點**
- **Rubber duck mode（GA）**：與 Copilot CLI 對話但不執行任何指令，用於 codebase 探索或思路整理
- **Voice input（GA）**：語音輸入 prompt 取代打字
- **Prompt scheduling（Public Preview）**：排程 prompt，讓任務在離開時自動執行
- **新 terminal UI（Public Preview）**：重新設計的實驗性終端介面

**實務影響**
- Rubber duck mode 提供低風險的 CLI 互動情境，適合在敏感環境下思考問題而不誤觸指令
- Prompt scheduling 讓長跑任務可排程執行，減少人工守候

**待追蹤**
- 新 terminal UI 仍為實驗性，功能完整度與穩定性待觀察

---

### 2026-06-02（[Cloud and local sandboxes for GitHub Copilot now in public preview](https://github.blog/changelog/2026-06-02-cloud-and-local-sandboxes-for-github-copilot-now-in-public-preview)）

> **繁中摘要**：GitHub Copilot 的工具執行現可在隔離 sandbox 中進行，本地用 Docker container、雲端用 GitHub Actions，目前為 public preview，可降低 agentic 任務的副作用風險。

**變更重點**
- 本地 sandbox：使用 Docker container 隔離 Copilot 工具執行環境
- 雲端 sandbox：使用 GitHub Actions 隔離雲端執行環境
- 目前為 public preview

**實務影響**
- Agentic 任務（如 file edit、shell 指令）可在隔離環境執行，降低對本地系統的意外影響
- 與 GitHub Actions 整合讓 CI/CD 場景的 agentic workflow 更安全

**待追蹤**
- Public preview 轉 GA 的時程與 sandbox 功能限制未公告

---

### 2026-06-02（[Shape Copilot code review around your team](https://github.blog/changelog/2026-06-02-shape-copilot-code-review-around-your-team)）

> **繁中摘要**：Copilot code review 新增兩項 public preview：agent skills 讓 Copilot 在回饋前執行指定工具（linter、type-checker、test runner），MCP servers 讓外部服務提供審查 context，使 code review 更貼近團隊實際工具鏈。

**變更重點**
- **Agent skills for code review（Public Preview）**：設定 Copilot 在給意見前執行特定工具（如 linter、type-checker、test runner）
- **MCP servers for code review（Public Preview）**：連接外部服務以取得更豐富的審查 context
- 審查深度會根據變更複雜度自動調整

**實務影響**
- 可將既有 CI 工具的輸出納入 Copilot 審查流程，減少人工補充 context 的成本
- MCP 整合讓 code review 可存取外部知識庫（如 issue tracker、文件）

**待追蹤**
- 兩項功能均為 public preview，API 與設定方式可能調整

---

### 2026-06-02（[Extend GitHub with agent apps](https://github.blog/changelog/2026-06-02-extend-github-with-agent-apps)）

> **繁中摘要**：GitHub 推出 Agent apps，可從 Marketplace 安裝 AI agent，整合至 Copilot Chat、PR reviewer、issue assignee 及 comment mention，擴展 GitHub 原生 agentic 能力。

**變更重點**
- Agent apps 可從 GitHub Marketplace 安裝，安裝方式與 GitHub App 相同
- 安裝後可在以下場景呼叫：Copilot Chat 中調用、PR 加入為 reviewer、指派給 issue、在 comment 中 mention

**實務影響**
- 第三方 AI agent 可深度整合 GitHub 原生工作流（PR review、issue triage、chat）
- 對建立或使用 GitHub-native automation 的團隊是重要擴充點

---

### 2026-06-02（[Introducing Copilot CLI and agentic capabilities enhancements in JetBrains IDEs](https://github.blog/changelog/2026-06-02-introducing-copilot-cli-and-agentic-capabilities-enhancements-in-jetbrains-ides)）

> **繁中摘要**：JetBrains IDE 版 GitHub Copilot 新增 Copilot CLI 整合（終端式 AI 協助無需離開 IDE），以及 multi-file editing、custom instructions 支援與改良的 agent mode tool use。

**變更重點**
- Copilot CLI 現可在 JetBrains IDE 內使用，提供終端風格 AI 協助
- 新增 agentic 能力：multi-file editing、custom instructions 支援、agent mode tool use 改良

**實務影響**
- JetBrains 使用者可在 IDE 內直接使用 Copilot CLI，不需切換到獨立終端
- Multi-file editing 與 custom instructions 讓 JetBrains agentic workflow 與 VS Code 功能對齊

---

## OpenAI Codex

### 2026-06-02（[Build and deploy websites with Sites](https://developers.openai.com/codex/changelog#build-and-deploy-websites-with-sites)）

> **繁中摘要**：Codex app 新增 Sites plugin（preview），可直接在 app 內建立、部署、管理 OpenAI 托管的網站與 web app；ChatGPT Business workspace 預設開啟，Enterprise 由管理員以 role-based controls 管控。

**變更重點**
- Sites plugin 進入 preview，支援建立、儲存、部署、查看網站、dashboard、內部工具、web app、遊戲
- 專案管理透過 app sidebar 操作
- ChatGPT Business workspace 預設包含此功能；Enterprise 管理員可控存取權限

**實務影響**
- 若使用 Codex app 進行 web prototype 或 internal tooling，可直接在同一介面內部署，不需另起 hosting 流程
- Enterprise 環境需留意 admin 是否已開放 Sites 存取

**待追蹤**
- Preview 階段，正式 GA 時間未定；功能邊界（如自訂 domain、版本管理）尚未揭露

---

### 2026-06-01（[Use Codex with Amazon Bedrock](https://developers.openai.com/codex/changelog#use-codex-with-amazon-bedrock)）

> **繁中摘要**：Codex 現在可透過 Amazon Bedrock 使用 AWS-managed OpenAI 模型，認證、帳號管理、計費由 AWS 負責，本地 Codex 執行流程不變。

**變更重點**
- 整合 Amazon Bedrock，支援 AWS-managed OpenAI 模型
- 認證與計費走 AWS 側，不需另外管理 OpenAI API key
- 本地 Codex 執行方式維持不變

**實務影響**
- 已在 AWS 生態系的團隊可統一帳號與計費，降低多供應商管理成本
- 適合需要 AWS 合規（VPC、IAM、CloudTrail）環境的企業用戶

---

### 2026-05-29（[Computer use and mobile access on Windows 26.527](https://developers.openai.com/codex/changelog#computer-use-and-mobile-access-on-windows-26527)）

> **繁中摘要**：Computer Use 功能擴展至 Windows 桌面應用程式，可從 ChatGPT iOS/Android 或 Mac Codex 遠端操控 Windows 裝置；新增 threading 改進支援背景任務協調。

**變更重點**
- Computer Use 擴展至 Windows，可操作桌面應用程式
- Remote control 支援 Windows 裝置，入口為 ChatGPT iOS/Android 或 Mac Codex
- Profile 區段顯示用戶資訊與使用統計
- Threading 改進：本地 projects 與 worktrees 可在獨立 thread 中協調背景任務

**實務影響**
- Windows 用戶現在也能使用 Computer Use 進行桌面自動化
- 行動裝置遠端控制覆蓋 Windows，適合跨平台 remote agent 工作流程
- Worktree 背景任務協調改進有助於平行開發流程
