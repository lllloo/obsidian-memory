---
title: "2026-06-11 Daily Updates"
created: 2026-06-11
updated: 2026-06-11
tags:
  - updates
  - copilot
  - codex
---

## GitHub Changelog

### 2026-06-10（[Copilot Chat now sees your agent sessions](https://github.blog/changelog/2026-06-10-copilot-chat-now-sees-your-agent-sessions)）

**繁中摘要**：Copilot Chat 與 Copilot cloud agent 的交接體驗改善，現可搜尋與查詢過去的 agent sessions，降低在 Chat 與 agent 模式間切換的脈絡遺失問題。

- **Agent session 可見性**：Copilot Chat 現可讀取並查詢過去的 cloud agent sessions，方便追蹤與接續進行中的任務。
- **交接體驗改善**：Chat 與 cloud agent 之間的 handoff 流程優化，切換時減少上下文斷層。

### 2026-06-10（[Dedicated security review command now available in Copilot CLI](https://github.blog/changelog/2026-06-10-dedicated-security-review-command-now-available-in-copilot-cli)）

**繁中摘要**：GitHub Copilot CLI 新增 `/security-review` slash command，可直接對 code changes 執行 security review，目前以 experimental public preview 形式發布。

- **`/security-review` 指令**：在 CLI 直接對 diff/code changes 觸發安全審查，無需切換到 web UI，加速 security gate 流程。
- **實驗性 public preview**：功能尚在預覽階段，API 或行為可能變動。

---

## OpenAI Codex

### Codex app 26.608 · 2026-06-09（[Changelog](https://developers.openai.com/codex/changelog)）

**繁中摘要**：Codex app 26.608 新增從 Claude Code 遷移設定的 migration flow，並大幅翻新 plugins 管理介面；同時修復數個 UI bug。

- **Claude Code migration flow**：新增從 Claude Code（與 Claude Cowork）匯入既有設定的遷移流程，降低切換成本。
- **Plugins 介面翻新**：新增分頁、marketplace 篩選器與鍵盤導航，提升插件管理效率。
- **Settings 搜尋擴展**：搜尋範圍擴及更多設定面板。
- **Bug fixes**：修復 goal timer 重疊、notification 處理異常、review diff 排序錯誤，以及不支援透明背景系統的視窗渲染問題。

### ChatGPT for iOS 1.2026.153 · 2026-06-09（[Changelog](https://developers.openai.com/codex/changelog)）

**繁中摘要**：ChatGPT iOS app 大幅強化 Codex 行動端功能，新增 branch 管理、worktree 建立、inline review comments 及 `/goal` 指令，讓 mobile 端可執行完整的 coding agent 工作流程。

- **Branch / worktree 管理**：新執行緒可選擇 branch、建立 worktree 並設定環境，支援完整的 branch-based 開發流程。
- **Codex profile 頁面**：新增使用量統計與 token 活動圖表，方便追蹤配額消耗。
- **`/goal` 指令**：可從行動端直接進行 goal 管理。
- **Inline review comments**：瀏覽 changed files 時支援行內審查評論，行動端 code review 體驗大幅提升。
- **Side chat 與 prompt 編輯**：可從選取的 transcript 文字開啟 side chat，並支援 prompt 編輯。

---
