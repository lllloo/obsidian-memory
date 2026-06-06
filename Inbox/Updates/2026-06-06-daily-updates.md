---
title: "2026-06-06 Daily Updates"
created: 2026-06-06
updated: 2026-06-06
tags:
  - updates
  - claude-code
  - codex
---

## Claude Code

### v2.1.163 · 2026-06-04（[Version 2.1.163](https://code.claude.com/docs/en/changelog#version-21163-june-4-2026)）

> **繁中摘要**：此版本新增多項 managed settings、plugin 管理、hooks 與 skills 的實用擴充，並修復多個影響 CI、Windows、Bedrock/Vertex、bazel 環境的 bug，整體可靠性大幅提升。

**變更重點**
- 新增 `requiredMinimumVersion` / `requiredMaximumVersion` managed settings，可透過 org policy 鎖定 Claude Code 版本範圍。
- 新增 `/plugin list` 指令，支援 `--enabled` / `--disabled` 過濾。
- `/btw` 新增「c to copy」快捷鍵，保留 markdown 格式複製。
- Hooks 新增 `hookSpecificOutput.additionalContext`，可在 continued turns 中傳遞額外上下文。
- Skills 支援 `\$` 跳脫語法，允許在 `$` 後接數字時輸出字面值 `$`（不展開變數）。
- Stdio MCP servers 現可讀取 `CLAUDE_CODE_SESSION_ID` 環境變數。
- Background agents 會靜默自動更新。
- 修復 `claude -p` 在有 backgrounded commands 時掛住的問題。
- 修復 Bedrock / Vertex / Foundry 搭配 `CI=true` 時 API key 錯誤。
- 修復 bazel / EDR 環境下 bash 失敗。
- 修復 Windows session-env 目錄問題。
- 修復 org-managed permission rules 時序問題。
- 修復 background session reattach 時 task 遺失。
- 修復 hook conditions 使用 subshell / backtick 時的解析錯誤。
- 修復 deny rules 中 `$HOME` 參照失效。

**實務影響**
- Org 管理員可強制員工使用特定版本範圍，避免引入不穩定版本或鎖定已驗證版本。
- CI 環境（含 Bedrock/Vertex）的 API key 錯誤修復後，自動化流程穩定性提升。
- Skills 的 `\$` 跳脫修復後，含數字參數的 shell script template 行為更可預測。
- Hook 條件使用 subshell / backtick 的既有設定現可正常運作，不需繞路。
- bazel / EDR 環境用戶可直接升級，不再需要額外 workaround。

---

### v2.1.162 · 2026-06-03（[Version 2.1.162](https://code.claude.com/docs/en/changelog#version-21162-june-3-2026)）

> **繁中摘要**：此版本改善 multi-agent 狀態可視性與 UX 細節，並修復多個跨平台、MCP、WebFetch、LSP 的問題。

**變更重點**
- `claude agents --json` 輸出新增 `waitingFor` 欄位，可得知 agent 目前等待哪個子任務。
- 明確列出 Grep / Glob 工具時，提供獨立的 dedicated search tools（而非通用工具）。
- `/effort` 指令現在會確認設定已持久化。
- Slash commands 改為填入 input bar 而非立即執行，可先編輯再送出。
- Remote Control 顯示為持久 footer pill。
- Windsurf 改名為 Devin Desktop。
- 修復 config directory 唯讀時的 startup hang。
- 修復 WebFetch preapproved domain rules 不生效。
- 修復 Windows permission rule matching。
- 修復 turn 開頭 interrupt 被忽略。
- 修復 API 400 emoji 錯誤。
- 修復 MCP timeout 設定低於 1000ms 被忽略。
- 修復 LSP `workspaceSymbol` 無結果回傳。
- 修復 session 名稱在 40 字元處截斷。
- 修復跨 session 訊息傳遞在深層目錄失敗。
- 修復 5 秒 attach stall。

**實務影響**
- `waitingFor` 欄位讓 orchestration script 可程式化監控 fan-out agent 的進度，不再只能靠輪詢狀態。
- Slash commands 改為先填入再執行，降低誤觸風險，適合複雜指令需臨時調整參數的情境。
- WebFetch preapproved domain rules 修復後，既有 `.claude/settings.json` 設定可正常生效，不需手動繞路。
- MCP timeout 低於 1000ms 的設定現在受尊重，對低延遲工具有影響。

---

### v2.1.161 · 2026-06-02（[Version 2.1.161](https://code.claude.com/docs/en/changelog#version-21161-june-2-2026)）

> **繁中摘要**：此版本強化 OpenTelemetry 指標、multi-agent 可視性，並修復多個安全與穩定性問題，包含 `claude mcp` 洩漏 secrets 的重要安全修復。

**變更重點**
- `OTEL_RESOURCE_ATTRIBUTES` 現在納入 metric labels，方便 observability 平台做資源標記。
- `claude agents` 顯示 fan-out 工作的 `done/total` 進度。
- `/mcp` 折疊未使用的 claude.ai connectors，減少 UI 噪音。
- Parallel tool calls：Bash 失敗不再取消其他並行工具呼叫。
- Fullscreen clipboard 在 Linux 改用 `wl-copy` / `xclip` / `xsel`。
- **安全修復**：`claude mcp` 指令不再印出 secrets。
- 修復 managed-settings policies 封鎖 third-party sessions。
- 修復 background subagent output 污染 stdout。
- 修復 Workflow isolation guard bypasses。
- 修復 background sessions 中 stale model 問題。
- 修復 Write tool 潛在 crash。
- 修復 EADDRINUSE（socket 工具重複綁定端口）。
- 修復 OpenTelemetry log events 在初始化前被丟棄。
- 改善大量寫入時的 terminal 渲染效能。

**實務影響**
- `claude mcp` 洩漏 secrets 的修復屬安全層級問題，使用 MCP 且有命令列輸出日誌的環境應儘速升級。
- Parallel tool calls 中 Bash 失敗不取消其他工具，agent 整體執行更有韌性，減少因單一工具失敗導致整批重跑。
- Background subagent output 污染 stdout 的修復對有 CI/CD pipeline 解析 stdout 的場景有直接影響。
- OTEL 指標現包含 resource attributes，對有部署 observability stack 的 org 有助於更精細的 metrics 分組。

---

### v2.1.160 · 2026-06-02（[Version 2.1.160](https://code.claude.com/docs/en/changelog#version-21160-june-2-2026)）

> **繁中摘要**：此版本新增寫入 shell startup files 與 build-tool configs 前的確認提示，提升安全性；同時修復多個 Windows、WSL、CJK IME、vim mode 問題，並移除 Opus 4.6 override 變數。

**變更重點**
- 新增：寫入 shell startup files（如 `.bashrc`、`.zshrc`）及 build-tool configs（授予 code execution 的檔案）前會先提示確認。
- `acceptEdits` 模式在危險 config 寫入前同樣會提示。
- Edit tool 在單一檔案 grep 後不再需要先執行獨立 Read。
- **移除** Opus 4.6 override 變數。
- **重命名**：「workflow」trigger 改名為「ultracode」。
- 修復 WSL 上 copy-on-select 無法到達 Windows clipboard。
- 修復 completed session restore 遺失 history。
- 修復 background sessions 在 retire 時丟失 conversation。
- 修復 `claude --bg` socket missing failures。
- 修復 Windows 上 `claude rm` 後目錄刪除失敗。
- 修復 CJK IME 定位問題。
- 修復 Windows file links。
- 修復 vim mode `p` paste 位置。
- 修復 non-ASCII 路徑下 voice mode 失敗。
- 改善 auto classifier 延遲。
- 改善 background teardown（使用 SIGTERM）。

**實務影響**
- Shell startup files 寫入確認提示是安全邊界強化，使用 `acceptEdits` 模式的自動化流程若有寫入 `.bashrc` 等場景，需確認新版行為不會中斷 CI。
- Opus 4.6 override 變數移除：若有依賴此變數的腳本或設定需清理。
- 「ultracode」重命名：原本使用 `workflow` trigger 的 hooks / settings 需更新為 `ultracode`。
- CJK IME 修復對使用中文輸入的工作流有直接幫助。

**待追蹤**
- `acceptEdits` 模式在危險 config 寫入時的具體提示行為與哪些檔案被視為「危險 config」，官方文件尚未完整說明，實際行為需測試確認。

---

## OpenAI Codex

### 2026-06-01（[Use Codex with Amazon Bedrock](https://developers.openai.com/codex/changelog#2026-06-01-bedrock)）

> **繁中摘要**：Codex 現在支援透過 Amazon Bedrock 執行，讓使用 AWS 基礎設施的團隊可沿用現有的 IAM 認證、帳號控管與 AWS 帳單，而無需直接持有 OpenAI API key。

**變更重點**
- Codex 整合 Amazon Bedrock，可在 Bedrock 管理的基礎設施上執行支援的 OpenAI 模型。
- 認證方式改用 AWS-managed authentication（IAM），不需另外管理 OpenAI API key。
- 計費走 AWS 帳單整合。

**實務影響**
- 已在 AWS 生態系的企業團隊可透過既有 IAM 角色與 AWS 帳單管控 Codex 使用，降低 vendor 整合複雜度。
- 對需要資料落地於 AWS 或已有 Bedrock 合規框架的組織，此整合降低導入門檻。

**待追蹤**
- 目前支援的 OpenAI 模型範圍（Bedrock 上的 model availability）尚未在公告中完整列出，需查閱 Bedrock 服務頁確認。

---

### CLI v0.136.0 · 2026-06-01（[Codex CLI 0.136.0](https://developers.openai.com/codex/changelog#2026-06-01-cli-0136)）

> **繁中摘要**：Codex CLI 0.136.0 是功能密集的大版本，新增 TUI 可點擊連結、session 封存、遠端執行設定、Windows sandbox alpha，以及獨立圖片生成擴充。

**變更重點**
- TUI markdown 可點擊網頁連結（透過 OSC 8 metadata），終端支援時自動啟用。
- `/archive` 指令與對應 CLI 選項可封存 session，方便管理長期累積的 session 歷史。
- App-server 整合：thread resume 時可帶入 initial turns page。
- 遠端執行設定：支援 `CODEX_API_KEY` 環境變數進行 registration。
- Windows sandbox provisioning alpha path。
- 新增獨立圖片生成 extension。

**實務影響**
- Session 封存（`/archive`）讓長期使用者可清理 active session 列表，同時保留歷史紀錄，管理多專案 session 的工作流受惠。
- `CODEX_API_KEY` 遠端執行設定讓 CI/CD 環境或多機設定更容易管理認證，不依賴互動式登入。
- OSC 8 連結在支援的終端（如 iTerm2、kitty、WezTerm）中直接可點擊，減少複製 URL 的摩擦。
- Windows sandbox alpha 開放測試，Windows 用戶可開始評估沙箱執行環境。

---

### CLI v0.137.0 · 2026-06-04（[Codex CLI 0.137.0](https://developers.openai.com/codex/changelog#2026-06-04-cli-0137)）

> **繁中摘要**：Codex CLI 0.137.0 新增 F13–F24 keybinding、multi-agent v2 runtime 持久化、hosted web/image tools，以及企業用月度額度顯示與 remote-control client management RPC。

**變更重點**
- 支援 F13–F24 鍵位綁定，擴充客製化快捷鍵空間。
- 企業帳號可在 CLI 顯示月度 credit limit。
- Remote-control client management RPCs（可程式化管理遠端控制客戶端）。
- Plugin list 支援 JSON 輸出（`--json`）。
- Multi-agent v2 runtime persistence：跨 session 保留 multi-agent 執行狀態。
- Hosted web tools 與 image tools 整合進 code-mode flows。
- 多項穩定性修復。

**實務影響**
- Multi-agent v2 runtime persistence 是架構層變更：長時間 fan-out agent 任務可在 session 中斷後恢復，減少需要完整重跑的情況，對大型自動化任務有直接價值。
- Plugin list JSON 輸出讓腳本化管理 plugin 狀態成為可能（配合 `claude agents --json` 等 JSON-first 工具鏈）。
- Remote-control client management RPCs 為 orchestration layer 提供程式化控制入口，適合需要動態管理多個 Codex 客戶端的場景。
- Hosted web/image tools 進入 code-mode flows，代表 agentic 任務中可直接呼叫這些工具而不需切換模式。

**待追蹤**
- Multi-agent v2 runtime persistence 的具體持久化機制（本地 vs 雲端、跨機器支援程度）官方尚未完整說明。
