---
title: "2026-05-09 Daily Updates"
created: 2026-05-09
updated: 2026-05-09
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## OpenAI Codex（v0.130.0，2026-05-08）

> **繁中摘要**：rust-v0.130.0 帶來 `codex remote-control` 新入口、Bedrock AWS console login 支援、app-server thread 分頁 API，以及數個影響 agent 正確性的 bug fix。

**變更重點**

- 新增 `codex remote-control` 指令，作為啟動 headless remotely-controllable app-server 的簡化入口
- Bedrock auth 現支援 `aws login` console-login credentials，不再限於 access key
- App-server clients 可分頁讀取大型 threads（unloaded / summary / full turn item views）
- Turn diff 追蹤修正：`apply_patch` 部分失敗後 diff 仍能保持準確
- Live app-server threads 現在不需重啟即可套用 config 變更
- Windows sandbox 修正：sandbox user 現在能存取 desktop runtime binary cache
- Plugin 詳情頁顯示 bundled hooks；sharing 加入 link metadata 與 discoverability 控制

**實務影響**

- Bedrock 用戶可改用 `aws login` profile，不需額外管理 access key
- `remote-control` 入口簡化 headless/CI 環境下的 agent server 設定流程
- Windows sandbox 用戶的環境穩定性改善

**待追蹤**

- Thread pagination API 與 ThreadStore contract 為新功能，文件與穩定性待觀察

---

## OpenAI Codex — remote-control 定位說明（2026-05-09）

> **繁中摘要**：`codex remote-control` 目前是 headless app-server 入口（供程式控制），尚未達到類似 Claude Code 的 browser UI 遠端追蹤；OAI 暗示有相關計畫但無 timeline。

**變更重點**

- 目前定位為開發者 API building block（headless），非 end-user browser UI
- 社群期望的完整流程（CLI 印 URL → 瀏覽器跟隨 session）尚未實現
- Twitter 上 OAI 員工暗示等效功能正在規劃，無 timeline 或官方確認

**實務影響**

- 可用 `codex remote-control` 作為自訂工具整合的 backend entrypoint
- 手機/平板遠端追蹤 session 目前仍需借助 tmux + SSH 等第三方方案

**待追蹤**

- OAI 官方 browser-based remote control 的正式計畫與 release timeline

---

## OpenAI Codex — Shift+Enter 已知問題與 Workarounds

> **繁中摘要**：Codex CLI 的 Shift+Enter 在多數終端機環境下會直接執行命令，根本原因是 Crossterm library 無法跨終端可靠偵測，目前有多種 workaround，官方 fix 尚未發布。

**變更重點**

- 根本原因：crossterm-rs/crossterm#685，部分終端（tmux 內 Ghostty、Tabby 等）將 Shift+Enter 傳送與 Enter 相同訊號
- 可正常運作的終端：Ghostty standalone、iTerm2、WezTerm
- 長期修法方向：改善 Crossterm 按鍵偵測，或開放使用者自訂換行快捷鍵

**實務影響**

- macOS + tmux：Shift+Enter 失效，改用 Ctrl+J（ASCII LF）
- **WezTerm**：`config.keys` 設定 Shift+Enter → `SendString "\x0a"`
- **Windows Terminal / WSL**：`settings.json` keybindings 加 `sendInput: "
"`
- **Tabby + macOS**：Karabiner-Elements 將 Shift+Enter 重映射為 Ctrl+J

**待追蹤**

- Crossterm#685 修復進度及 Codex CLI 何時採用新版 Crossterm

---

## Claude Code（v2.1.137，2026-05-09）

> **繁中摘要**：v2.1.137 修正 VS Code extension 在 Windows 上無法啟動的問題，Windows 用戶升級後即可恢復正常。

**變更重點**

- VS Code extension 在 Windows 上 activation 失敗的 bug 已修復

**實務影響**

- Windows + VS Code 用戶應升級至 v2.1.137 或更新版本

---

## GitHub Copilot — Code Review 計量 API 新增（2026-05-08）

> **繁中摘要**：Copilot usage metrics REST API 新增 `copilot_suggestions_by_comment_type` 欄位，可按建議類型（security、bug_risk 等）查看 code review 建議量與採用率。

**變更重點**

- `pull_requests` 回應新增 `copilot_suggestions_by_comment_type` array
- 每筆包含：`comment_type`、`total_copilot_suggestions`、`total_copilot_applied_suggestions`
- 支援 single-day 與 28-day rolling window；enterprise 與 organization 層級皆可用
- 目前不支援 repository 層級下鑽（正在評估中）

**實務影響**

- 可用 API 量化各問題類型的 Copilot code review 建議數與被採用數，建立 ROI dashboard
- 需有 Copilot usage metrics 存取權限（enterprise admin 或 org owner）

**待追蹤**

- Repository 層級細分支援的 GA 時程

---

## GitHub Copilot — Cloud Agent org-level Secrets/Variables（2026-05-08）

> **繁中摘要**：Copilot cloud agent 新增 organization 層級的 Agents secrets/variables，一次設定可跨 repo 共享，與 Actions secrets 分離管理。

**變更重點**

- 新增 org-level Agents secrets & variables，可選擇授權給指定 repositories 存取
- Repository 設定頁新增獨立「Agents」區塊，與 Actions 設定分離

**實務影響**

- 共用資源（如 internal package registry token、MCP server 連線資訊）只需在 org 層級設定一次
- 對多 repo 使用 Copilot cloud agent 的團隊可大幅減少維護開銷
