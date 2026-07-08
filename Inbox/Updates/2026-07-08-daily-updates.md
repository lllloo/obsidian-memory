---
title: "2026-07-08 Daily Updates"
created: 2026-07-08
updated: 2026-07-08
tags:
  - updates
  - copilot
  - opencode
  - codex
---

## GitHub Copilot

### 2026-07-02 · 生效 2026-07-31（[Upcoming deprecation of Gemini 2.5 Pro and Gemini 3 Flash](https://github.blog/changelog/2026-07-02-upcoming-deprecation-of-gemini-2-5-pro-and-gemini-3-flash)）

**繁中摘要**：Copilot 將於 2026-07-31 全面下架 Gemini 2.5 Pro 與 Gemini 3 Flash，依賴這兩個 model 的流程需及早切換。

- **Gemini 2.5 Pro / Gemini 3 Flash deprecation**：涵蓋 Copilot Chat、inline edits、ask / agent 模式與 code completions 所有場景；7/31 後這兩個 model 於 Copilot 全數不可選，需改用其他 model。

### 2026-07-07（[GitHub Copilot app available to all](https://github.blog/changelog/2026-07-07-github-copilot-app-available-to-all)）

**繁中摘要**：GitHub Copilot 桌面 app 全面開放到所有 Copilot 方案，可從桌面啟動 agent-driven development，三大平台皆可用。

- **桌面 app 全方案開放**：先前分級限制取消，任何 Copilot 方案登入 GitHub 帳號即可用；支援 macOS / Windows / Linux，把 agent 開發流程從瀏覽器 / IDE 延伸到獨立桌面端。

### 2026-07-07（[Kimi K2.7 now available for Copilot Business and Enterprise](https://github.blog/changelog/2026-07-07-kimi-k2-7-now-available-for-copilot-business-and-enterprise)）

**繁中摘要**：Kimi K2.7 的 Copilot 可用範圍從 Pro / Pro+ / Max 擴到 Business 與 Enterprise，企業方案現在也能選這個 model。

- **Kimi K2.7 擴及 Business / Enterprise**：延續 7/1 對個人方案的開放，企業用戶的 model 選單新增此選項。

---

## OpenCode

完整版本列表見 [opencode.ai/changelog](https://opencode.ai/changelog)。

### v1.17.14 · 2026-07-06

**繁中摘要**：新增 code mode MCP adapter 供 orchestration 腳本呼叫，並修正多項 provider routing 與 reasoning 行為，對接 MCP / OpenRouter / Copilot 的設定更穩。

- **code mode MCP adapter**：可在 orchestration 腳本中驅動 MCP，並修好分頁式 MCP tool catalog 的抓取。
- **provider / model routing 修正**：修正 GitHub Copilot 的 model routing，並在 OpenRouter variant 保留 reasoning effort 設定，避免推理強度被重置。
- **Desktop / TUI**：新增草稿 server 狀態、整合終端機、tab 重開與背景開啟、model 搜尋等；TUI 修好 spinner 導致的 loading 指示遺失。

### v1.17.13 · 2026-07-01

**繁中摘要**：對 OpenAI-compatible model 強制啟用 reasoning mode，並改善 model 選擇與 Copilot 回應處理。

- **強制 reasoning mode**：OpenAI-compatible model 一律走 reasoning 模式，並修好 GitHub Copilot 的 stale response ID 問題。
- **可搜尋 model picker**：Desktop 加入含管理功能的可搜尋 model 選擇器，另修 markdown 對齊與 review 時 pending question 狀態保留。

---

## OpenAI Codex

### ChatGPT for iOS 1.2026.181 · 2026-07-06（[changelog](https://developers.openai.com/codex/changelog)）

**繁中摘要**：ChatGPT for iOS 讓 Codex tasks 可在手機端完整管理，並支援 SSH 連線與私鑰，行動端也能跑 agent 任務。

- **手機端 Codex tasks**：可在對話中建立、搜尋、開啟、fork、管理 Codex task；含 staged / unstaged / branch / last-turn 變更 filter 與 branch 比對。
- **SSH host 支援**：以私鑰或無憑證方式連線 SSH host，並提供 connection 捷徑，擴大行動端可操作環境。
- **task 控制細化**：model / reasoning / Fast 設定改為 scoped 到當前 task；task list 新增「Needs input」狀態、改善載入與前景恢復；可從 task 選單查 usage limit 與 credit。

---
