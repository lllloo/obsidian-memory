---
title: "2026-06-12 Daily Updates"
created: 2026-06-12
updated: 2026-06-12
tags:
  - updates
  - claude-code
  - copilot
  - codex
---

## Claude Code

### 2.1.173 · 2026-06-11（[Changelog](https://code.claude.com/docs/en/changelog#2-1-173)）

**繁中摘要**：修正 Fable 5 model ID 帶 `[1m]` suffix 時無法正規化的問題（Fable 5 預設包含 1M context，suffix 現在自動移除）；另修 Windows 上 sandbox 啟用時的誤報啟動警告。

- **Fable 5 model name 正規化**：`[1m]` suffix 現在自動 strip，避免 model ID 因 suffix 變體而辨識失敗。

### 2.1.172 · 2026-06-10（[Changelog](https://code.claude.com/docs/en/changelog#2-1-172)）

**繁中摘要**：最重要的新功能是 sub-agent 現在可以遞迴生成 sub-agent（最深 5 層），大幅擴展多層代理協調的可能性；同時修復 Amazon Bedrock region 讀取、marketplace 搜尋、以及 20+ 個 bug。

- **Sub-agent 遞迴**：sub-agent 可生成自己的 sub-agent，最深 5 層，支援更複雜的 multi-agent 協調架構。
- **Amazon Bedrock**：`AWS_REGION` 未設時自動讀 `~/.aws` config 取 region，無需再手動設環境變數。
- **`/plugin` 搜尋**：marketplace 新增 search bar，快速篩選 plugin。
- **Bug fixes**：修正 1M context session 卡住、重複錯誤訊息、WebFetch wildcard domain 規則、`availableModels` 限制未套用到 subagent 等 20+ 個問題。

---

## GitHub Changelog

### 2026-06-11（[Copilot CLI: Configure everything from one place with /settings](https://github.blog/changelog/2026-06-11-copilot-cli-configure-everything-from-one-place-with-settings)）

**繁中摘要**：Copilot CLI 新增 `/settings` slash command，把原本分散的 `/theme`、`/streamer-mode`、`/experimental` 等設定整合成一個 schema-driven 的統一入口。

- **`/settings` 指令**：集中管理所有 CLI 設定，取代多個散落指令；schema-driven 設計讓設定欄位有明確型別與驗證。

### 2026-06-11（[GitHub Agentic Workflows is now in public preview](https://github.blog/changelog/2026-06-11-github-agentic-workflows-is-now-in-public-preview)）

**繁中摘要**：GitHub Agentic Workflows 進入 public preview，可在 GitHub 內用 coding agents 自動化 issue triage、CI failure analysis、documentation updates 等推理型任務。

- **Public preview 開放**：任何 repo 可開始使用 agentic workflows，無需等待邀請。
- **涵蓋場景**：issue triage、CI 失敗分析、文件更新等推理任務可交由 agent 處理，在 GitHub Actions 環境內執行。

### 2026-06-11（[Agentic workflows no longer need a personal access token](https://github.blog/changelog/2026-06-11-agentic-workflows-no-longer-need-a-personal-access-token)）

**繁中摘要**：GitHub Agentic Workflows 現在可以用 GitHub Actions 的內建 `GITHUB_TOKEN`，不再需要建立與儲存 personal access token（PAT），降低安全風險與設定複雜度。

- **無需 PAT**：用 `GITHUB_TOKEN` 替代，消除 token 洩漏風險，也免去 token 輪換維護。
- **即時影響**：既有設定了 PAT 的 agentic workflow 可移除 PAT 依賴，簡化 secret 管理。

---

## OpenAI Codex

### Codex app 26.609 · 2026-06-11（[Changelog](https://developers.openai.com/codex/changelog#codex-app-26609)）

**繁中摘要**：Codex app 26.609 新增 rate-limit reset 銀行制度（Plus/Pro 用戶可儲存配額重置）、Browser 用 Developer mode（CDP 除錯）、macOS Dock icon 切換，並將 Browser use 速度提升 2 倍。

- **Rate-limit reset banking**：Plus/Pro 用戶可儲備 rate-limit reset，並透過推薦取得額外重置次數。
- **Developer mode for Browser use**：開啟 Chrome DevTools Protocol（CDP），可 debug 網路活動與 console 輸出，方便開發與除錯 browser-based 工作流。
- **`/init` 指令**：在 app composer 內直接觸發 project 初始化工作流。
- **Browser use 2x 速度提升**：透過優化 CDP 與 DOM snapshot 減少網路往返，顯著加速 browser 任務執行。
- **Computer Use 擴展**：Enterprise 成員（EEA/UK/CH 除外）現可使用 Computer Use；Windows 新增 per-app access control。

---
