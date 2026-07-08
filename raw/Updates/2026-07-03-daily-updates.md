---
title: "2026-07-03 Daily Updates"
created: 2026-07-03
updated: 2026-07-03
tags:
  - updates
  - claude-code
  - copilot
---

## Claude Code

### v2.1.199 · 2026-07-02（[Changelog](https://code.claude.com/docs/en/changelog#2-1-199)）

**繁中摘要**：以錯誤處理與背景 agent 穩定性修復為主的維護版；stacked slash-skill 疊用行為變更值得注意。

- **Stacked slash-skill**：一次疊用多個 skill 現可載入最多 5 個（原本只載第一個）。
- **串流錯誤保留**：串流回應遇 mid-stream error 時保留 partial output；subagent 現正確把 API 錯誤與部分成果回報給 parent。
- **重試韌性**：transient 429 對訂閱者自動 backoff 重試；`CLAUDE_CODE_RETRY_WATCHDOG` 預設重試次數提高到 300。
- **背景 agent daemon**：修復 Linux 50 秒 kill cycle、macOS SSH 冷啟動失敗、`claude stop` 與 daemon respawn race 等一批問題；SSL 憑證錯誤改為即時給出可行動指引。

---

## GitHub Copilot

### 2026-07-02（[Copilot CLI no longer needs a personal access token in GitHub Actions](https://github.blog/changelog/2026-07-02-copilot-cli-no-longer-needs-a-personal-access-token-in-github-actions)）

**繁中摘要**：在 GitHub Actions 跑 Copilot CLI 現可直接用內建 `GITHUB_TOKEN`，不必再建立、儲存 PAT，簡化 CI pipeline 設定與 secret 管理。

- **CI 認證簡化**：workflow 內以內建 token 授權 Copilot CLI，少一組要輪替的長期憑證。

---

### 2026-07-02（[Copilot agent session streaming is now in public preview](https://github.blog/changelog/2026-07-02-copilot-agent-session-streaming-is-now-in-public-preview)）

**繁中摘要**：GitHub Enterprise Cloud（enterprise managed users）客戶現可跨所有 Copilot client 存取 agent session 資料，含 github.com 上運作的 cloud agent，public preview。

- **稽核與觀測**：agent session data 可集中匯出，供 enterprise 稽核 agent 活動；範圍限 EMU 環境。

---

### 2026-07-01（[Enterprises can default to auto model selection](https://github.blog/changelog/2026-07-01-enterprises-can-default-to-auto-model-selection)）

**繁中摘要**：Enterprise 管理員可在 `managed-settings.json` 將 model 設為 `auto`，讓 Copilot 自動選模型成為新對話的預設。

- **模型預設**：於 `.github-private/.github/copilot/managed-settings.json` 加 `auto`，新開對話即走 auto model selection，不需使用者逐次切換。

---
