---
title: "2026-06-02 Daily Updates"
created: 2026-06-02
updated: 2026-06-02
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## Claude Code

### v2.1.158 · 2026-05-30（[Update 2.1.158](https://code.claude.com/docs/en/changelog#update-21158)）

> **繁中摘要**：Auto mode 現已在 Bedrock、Vertex、Foundry 上支援 Opus 4.7 與 Opus 4.8，需透過環境變數手動啟用。

**變更重點**

- Auto mode 擴展至 Bedrock、Vertex、Foundry 三大平台，支援 Opus 4.7 與 Opus 4.8 模型
- 啟用方式：設定環境變數 `CLAUDE_CODE_ENABLE_AUTO_MODE=1`（opt-in，非預設開啟）

**實務影響**

- 使用 AWS Bedrock、Google Vertex 或 Azure Foundry 部署 Claude Code 的團隊，現可啟用 Auto mode 自動選擇工具調用策略
- 需主動設定環境變數，適合在基礎設施層統一注入，不影響未設定的現有部署

### v2.1.157 · 2026-05-29（[Update 2.1.157](https://code.claude.com/docs/en/changelog#update-21157)）

> **繁中摘要**：本版本為大型功能集合更新，核心亮點是 plugins 從 `.claude/skills` 自動載入、`claude agents` 工作流程強化，以及大量 worktree、IDE 整合與 TUI bug 修復。

**變更重點**

- `.claude/skills` 目錄內的 plugins 現在自動載入，無需透過 marketplace
- 新增 `claude plugin init <name>` 指令快速建立 plugin 腳手架
- `/plugin` 指令補全：支援子指令、已安裝 plugin 名稱、known marketplace plugins
- `settings.json` 中的 `agent` 欄位現在對 dispatched sessions 生效，可用 `--agent <name>` 覆蓋
- `EnterWorktree` 可在 Claude 管理的 worktrees 之間中途切換
- `OTEL_LOG_TOOL_DETAILS=1` 時，`tool_decision` telemetry event 加入 `tool_parameters`（bash 指令、MCP/skill 名稱）
- Claude 管理的 worktrees 在 agent 結束後不再鎖定，支援 `git worktree remove`/`prune` 清理
- 新增「Workflow keyword trigger」設定，可避免提示中出現 `workflow` 字樣誤觸動態 workflow
- 修復：zero-byte/損壞圖片貼附造成 crash → 改為文字 placeholder
- 修復：auto/bypass-permissions 模式下錯誤出現 sandbox 網路權限提示
- 修復：background agent worktrees 在 30 天 job retention sweep 後遺留孤立
- 修復：sleep/wake 後重連的 background sessions 將錯誤日期傳給模型
- 修復：`--resume` 遺漏上次程序退出時仍在執行的 subagents
- 修復：tmux 環境中 `claude agents` 的 copy-on-select 無法到達系統 clipboard（v2.1.153 regression）
- 修復：WSL 圖片貼附（`alt+v`）、Windows 11 截圖貼附，及支援從 Windows Explorer 拖曳圖片
- 修復：VS Code/Cursor/Windsurf 整合終端右鍵貼上重複 clipboard 內容
- `/terminal-setup` 現在會在 VS Code/Cursor/Windsurf 整合終端停用 GPU 加速，防止亂碼渲染

**實務影響**

- **Plugin 開發者**：skills 無需 marketplace 即可在 `.claude/skills` 自動運作，降低分發門檻
- **Multi-agent / worktree 用戶**：`agent` 欄位與 `EnterWorktree` 改善讓 dispatched session 管理更可靠；worktree 清理不再需要手動解鎖
- **Telemetry / observability**：`OTEL_LOG_TOOL_DETAILS=1` 可取得更細粒度的工具調用記錄
- **WSL 用戶**：圖片貼附問題修復，Windows 11 截圖工作流程恢復正常
- **IDE 整合用戶**：多項 VS Code/Cursor/Windsurf 終端渲染與貼附問題已修復

**待追蹤**

- Sandbox 啟動橫幅已移除，sandbox 狀態改在 `/status` 查看

### v2.1.156 · 2026-05-29（[Update 2.1.156](https://code.claude.com/docs/en/changelog#update-21156)）

> **繁中摘要**：修復使用 Opus 4.8 時 thinking blocks 被修改導致 API 錯誤的問題，影響所有依賴 extended thinking 功能的工作流程。

**變更重點**

- 修復 Opus 4.8 + thinking blocks 組合下，thinking blocks 內容被不當修改，進而觸發 API 錯誤的 bug

**實務影響**

- 使用 Opus 4.8 並啟用 extended thinking 的用戶，升級後應可消除先前出現的 API 錯誤
- 若之前因此 bug 而迴避 Opus 4.8 的工作流程，現可重新評估

---

## OpenAI Codex

### 2026-06-01（[Use Codex with Amazon Bedrock](https://developers.openai.com/codex/changelog#use-codex-with-amazon-bedrock)）

> **繁中摘要**：Codex 現可搭配 Amazon Bedrock 使用，將模型供應商切換至 AWS 管理的基礎設施，享有 AWS 認證、帳號控管與計費整合。

**變更重點**

- Codex 支援 Amazon Bedrock 作為 model provider
- 使用者可將 Bedrock 設為後端，以 AWS 原生認證（IAM 等）執行 Codex
- 計費與帳號管控由 AWS 側負責，而非 OpenAI 帳戶

**實務影響**

- 已在 AWS 生態系的團隊可在現有 Bedrock 合約與 VPC 環境下使用 Codex，無需額外 OpenAI billing 設定
- 與 Claude Code on Bedrock 的 Auto mode 擴展（同期更新）形成平行競爭態勢，值得評估兩者 workflow 整合差異

**待追蹤**

- Bedrock 上支援的具體 OpenAI 模型清單未詳列，需查閱官方文件確認

### v0.136.0 · 2026-06-01（[Codex CLI 0.136.0](https://developers.openai.com/codex/changelog#codex-cli-01360)）

> **繁中摘要**：Codex CLI 0.136.0 為重大功能版本，新增 session 封存、MCP server 狀態可視性、遠端執行設定，以及 Windows sandbox 的 alpha 支援。

**變更重點**

- TUI markdown 改善：web 連結現在可點擊
- Session 封存：新增 `/archive` 指令及 `codex archive`/`unarchive` CLI 子指令
- App-server 整合強化：支援 initial turns page resumption；MCP server 狀態現在在介面可見
- 遠端執行設定：支援 `CODEX_API_KEY` 環境變數登錄
- Windows sandbox provisioning alpha：`codex sandbox setup --elevated`（需提升權限）
- 獨立 image generation 擴充功能
- Bug 修復：ChatGPT token 在過期前更新、Git hooks/PowerShell 的指令安全強化、sandbox 清理改善、Bedrock 認證 fallback

**實務影響**

- **Session 管理**：`/archive` 讓長期 session 可封存再取回，改善多專案切換流程
- **MCP 用戶**：server 狀態可視性提升，方便除錯 MCP 連線問題
- **Windows 用戶**：sandbox alpha 開放測試，可評估是否取代現有隔離方案（需注意需提升權限）
- **遠端執行**：`CODEX_API_KEY` 登錄讓 CI/CD 或遠端環境設定更明確

**待追蹤**

- Windows sandbox provisioning 標註為 alpha，穩定性與功能完整性待後續版本確認

### Windows 26.527 · 2026-05-29（[Computer use and mobile access on Windows 26.527](https://developers.openai.com/codex/changelog#computer-use-and-mobile-access-on-windows-26527)）

> **繁中摘要**：Computer Use 功能擴展至 Windows 桌面應用程式，並支援從 iOS、Android 或 Mac 遠端啟動任務並監控進度。

**變更重點**

- Computer Use 現可操作 Windows 桌面應用程式
- 支援跨裝置遠端控制：從 iOS、Android、Mac 啟動工作，並監控 Windows 端執行進度
- Profile 區塊新增使用者詳情、使用量統計與 token 活動資訊
- 本地專案與 worktrees 的 thread 協調：可按需建立獨立 background threads
- 搜尋功能擴展至對話內容與 Git branch 名稱

**實務影響**

- 需要跨裝置監控長時間任務（如 CI build、批次處理）的用戶，可從行動裝置查看 Windows 端進度
- Git branch 名稱搜尋對管理大量 branch 的工作流程有實際幫助
- Computer Use on Windows 開啟桌面 GUI 自動化的新可能

**待追蹤**

- Computer Use on Windows 的支援範圍（哪些桌面應用可被操作）未詳述

### v0.135.0 · 2026-05-28（[Codex CLI 0.135.0](https://developers.openai.com/codex/changelog#codex-cli-01350)）

> **繁中摘要**：Codex CLI 0.135.0 強化 `codex doctor` 診斷輸出、Vim mode 文字物件編輯、permission profile 顯示，以及非互動式安裝支援，對日常 debug 與 CI 部署流程均有直接影響。

**變更重點**

- `codex doctor` 現在彙報環境、Git、terminal、app-server 與 thread inventory；`/status` 顯示遠端連線詳情與伺服器版本
- Vim mode 新增文字物件編輯（text-object editing）與可設定的 interrupt-turn binding
- Permission profiles 支援具名 profile，並顯示自訂設定內容
- Packaged builds 自動發現 bundled patched zsh helpers
- Python SDK 公開 `Sandbox` presets 友善介面
- 安裝腳本支援非互動模式：設定 `CODEX_NON_INTERACTIVE=1` 即可

**實務影響**

- CI/CD 管線可用 `CODEX_NON_INTERACTIVE=1` 進行無人值守安裝，不需額外 workaround
- `codex doctor` 輸出大幅豐富，troubleshooting 更有效率
- Vim 使用者可用文字物件操作（`ciw`、`da"`…），編輯效率提升
- Python SDK 使用者可直接引用 `Sandbox` presets，減少手動設定 boilerplate

### v0.134.0 · 2026-05-26（[Codex CLI 0.134.0](https://developers.openai.com/codex/changelog#codex-cli-01340)）

> **繁中摘要**：Codex CLI 0.134.0 加入本地對話歷史搜尋、以 `--profile` 為主要選擇器，並大幅改善 MCP 整合（per-server env 設定、OAuth、並發執行 read-only tools），對多 agent 與複雜 MCP 工作流影響顯著。

**變更重點**

- 新增本地對話歷史搜尋：case-insensitive 全文比對，附結果預覽
- `--profile` 成為 CLI、TUI permissions、sandbox 工作流的主要 profile 選擇器
- MCP 設定改進：支援 per-server 環境變數，HTTP server 可選 OAuth 授權
- Connector tool schemas 保留 local references，並壓縮過大的 schema
- 標記 `readOnlyHint` 的 MCP tools 可並發執行
- Extension/hook context 新增對話歷史與 subagent identity 資訊

**實務影響**

- 多個 read-only MCP tools 可同時執行，降低 multi-tool agent 的等待延遲
- OAuth HTTP MCP server 整合更完整，不需額外 proxy 處理授權
- subagent identity 進入 hook context，允許依 agent 身分做差異化行為
- 對話歷史搜尋可快速定位過去指令，適合長工作階段 debug

---

## GitHub Changelog

### 2026-06-01（[Updates to GitHub Copilot billing and plans](https://github.blog/changelog/2026-06-01-updates-to-github-copilot-billing-and-plans)）

> **繁中摘要**：GitHub Copilot 正式啟用 usage-based billing，且 Copilot code review 現在消耗 GitHub Actions minutes，影響所有使用 Copilot 的個人與企業用戶的費用結構。

**變更重點**

- Usage-based billing 對所有 Copilot 使用者正式上線（非 beta）
- Copilot code review 功能改為消耗 GitHub Actions minutes（而非獨立計費）

**實務影響**

- 大量使用 Copilot code review 的 repo，GitHub Actions 月用量可能明顯增加，需重新評估 Actions quota 與費用上限
- 建議審查現有 Actions 預算設定，確認 Copilot code review 頻率是否超出預期成本

**待追蹤**

- Copilot code review 每次消耗多少 Actions minutes 尚未見官方詳細說明，需留意後續文件更新

### 2026-05-28（[Claude Opus 4.8 is generally available for GitHub Copilot](https://github.blog/changelog/2026-05-28-claude-opus-4-8-is-generally-available-for-github-copilot)）

> **繁中摘要**：Claude Opus 4.8 正式在 GitHub Copilot 中 GA，可在 Copilot 介面直接選用，對需要高強度程式碼理解與生成的任務是可用的新選項。

**變更重點**

- Claude Opus 4.8（Anthropic 最新 Opus 模型）在 GitHub Copilot 正式 GA（非 preview）
- Anthropic 內部測試顯示 Opus 4.8 在程式碼理解與生成多項任務有明顯提升

**實務影響**

- Copilot 使用者可在 model selector 選擇 Opus 4.8，用於複雜重構、大型 codebase 理解等高需求場景
- 屬於 GA release，適合生產工作流使用，不需等 preview 穩定

**待追蹤**

- Opus 4.8 在 Copilot 的具體 rate limit 與 usage-based billing 計費單位尚未見詳細說明

### 2026-05-26（[Copilot Memory has more controls for deletion, scope, and the Copilot CLI](https://github.blog/changelog/2026-05-26-copilot-memory-has-more-controls-for-deletion-scope-and-the-copilot-cli)）

> **繁中摘要**：Copilot Memory（public preview）新增記憶刪除、repository 層級關閉開關，以及 CLI 記憶控制，對需要精確管控 AI context 的團隊有實質影響。

**變更重點**

- 支援更細緻的記憶刪除操作（improved memory deletion）
- 新增 repository 層級的 Memory 關閉開關（repo-level off switch）
- Copilot CLI 中可直接管理 Memory 設定
- 適用範圍：Copilot Pro、Pro+、Business、Enterprise

**實務影響**

- 可在特定 repo 關閉 Memory，避免敏感或隔離專案的 context 被跨對話保留
- CLI 控制讓自動化腳本或 CI 環境可程式化管理 Memory 狀態
- 刪除功能改善後，可更安全地清除不準確或過時的記憶條目

**待追蹤**

- 仍為 public preview，功能邊界可能調整；CLI 指令格式尚待官方文件確認

### 2026-05-26（[Target Copilot models to organizations with model rules](https://github.blog/changelog/2026-05-26-target-copilot-models-to-organizations-with-model-rules)）

> **繁中摘要**：GitHub Copilot Enterprise 新增 model rules，允許 enterprise owner 對不同 organization 指定可用的 Copilot 模型，取代原本全企業單一政策。

**變更重點**

- Enterprise owner 可針對特定 organization 設定允許使用哪些 Copilot 模型（targeted model rules）
- 不再限制為整個 enterprise 套用同一模型政策

**實務影響**

- 可讓高風險或合規要求嚴格的 org 限制為特定審核過的模型，其他 org 保持彈性選擇
- 對需要 model governance 的企業（金融、醫療、政府相關開發組織）有直接用途
- Enterprise admin 需重新審視現有模型政策，決定是否分 org 細化設定
