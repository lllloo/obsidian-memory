---
title: "2026-06-07 Daily Updates"
created: 2026-06-07
updated: 2026-06-07
tags:
  - updates
  - claude-code
  - copilot
---

## Claude Code

### v2.1.166 · 2026-06-06（[Version 2.1.166](https://code.claude.com/docs/en/changelog#2-1-166)）

> **繁中摘要**：此版本新增 `fallbackModel` 設定、deny rule 萬用 glob、跨 session 訊息安全強化、thinking 控制統一，以及 API 拒絕時的 fallback 自動重試，實務上提升了高可用性與安全邊界。

**變更重點**

- 新增 `fallbackModel` 設定：可設定最多三個後備模型，依序在主模型過載或不可用時嘗試；`--fallback-model` 現在也適用於互動 session
- Deny rule 的 tool-name 位置支援 glob pattern（`"*"` 可一次 deny 所有工具）；allow rules 拒絕非 MCP glob；deny rules 中的未知工具名在啟動時給出警告
- 跨 session 訊息安全強化：透過 `SendMessage` 從其他 Claude session 轉發的訊息不再帶有 user authority——接收端拒絕轉發的 permission request，auto mode 也封鎖此類訊息
- `MAX_THINKING_TOKENS=0`、`--thinking disabled`、及 per-model thinking toggle，現在可在 Claude API 上停用預設會 thinking 的模型的 thinking 行為（3P provider 不受影響）
- API 回傳非預期 non-retryable 錯誤時，Claude Code 會在 fallback model 上自動重試一次；auth、rate-limit、request-size、transport 錯誤仍直接浮出
- `claude update` 在下載前現在先公告目標版本，而非靜默進行
- `claude agents`：在清單輸入 URL 現在可過濾到第一個 prompt 包含該 URL 的 session
- 修復 20+ 個 bug，含圖片處理錯誤、remote session 穩定性、JetBrains IDE 終端渲染、Kitty keyboard protocol、PowerShell validation hang、孤立 process、voice mode 認證、managed settings 強制執行、MCP server 匹配、git worktree 處理、thinking text 重複等問題

**實務影響**

- `fallbackModel` 設定適合 Opus 4.8 過載期間設定 Sonnet 4.6 作為後備，保持互動不中斷，不需手動切換 `--model`
- Deny rule 支援 `"*"` glob 可快速鎖定 agent 到純讀模式（所有工具 deny 再選擇性 allow）
- 跨 session 訊息安全強化對 multi-agent orchestration 有直接影響：轉發 session 不再能繼承原 session 的 permission authority，需重新確認
- `--thinking disabled` 統一後，對 claude-opus-4-8 這類預設 thinking 的模型可確保無 thinking token 消耗（影響 cost 控制與 latency 預期）
- API 非預期 non-retryable 錯誤的自動 fallback 重試，對偶發性 API 拒絕有韌性提升

---

## GitHub Changelog

### 2026-06-05（[GPT-5.2 and GPT-5.2-Codex deprecated](https://github.blog/changelog/2026-06-05-gpt-5-2-and-gpt-5-2-codex-deprecated)）

> **繁中摘要**：GitHub 自 2026-06-05 起在大多數 Copilot 體驗中廢棄 GPT-5.2 與 GPT-5.2-Codex 模型，涵蓋 Chat、inline edits、ask/agent mode 與 code completions。

**變更重點**

- GPT-5.2 與 GPT-5.2-Codex 自 2026-06-05 起在絕大多數 GitHub Copilot 體驗中廢棄
- 受影響範圍：Copilot Chat、inline edits、ask 與 agent mode、code completions

**實務影響**

- 有明確指定 GPT-5.2 系列模型的 Copilot 設定或 API 整合，需更新為現行可用模型
- 若依賴 GPT-5.2-Codex 的 code completions 行為（如回應風格、長度偏好），切換後需重新評估提示設計
