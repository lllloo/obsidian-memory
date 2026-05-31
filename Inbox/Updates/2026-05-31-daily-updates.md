---
title: "2026-05-31 Daily Updates"
created: 2026-05-31
updated: 2026-05-31
tags:
  - updates
  - claude-code
  - codex
---

## Claude Code

### 2026-05-30（[Auto mode now available on Bedrock, Vertex, and Foundry for Opus 4.7 and 4.8](https://code.claude.com/docs/en/changelog)）

> **繁中摘要**：Auto mode 現已開放給 Bedrock、Vertex、Foundry 上的 Opus 4.7 和 Opus 4.8 使用者，需透過環境變數 opt-in；使用 cloud provider 的 Claude Code 用戶可開始評估是否切換。

**變更重點**
- Auto mode 在 Bedrock、Vertex、Foundry 上支援 Opus 4.7 與 Opus 4.8
- 啟用方式：設定環境變數 `CLAUDE_CODE_ENABLE_AUTO_MODE=1`

**實務影響**
- 透過 Bedrock / Vertex / Foundry 使用 Claude Code 的用戶，現可啟用 auto mode 讓模型自動選擇思考深度
- 需手動 opt-in，不影響既有 session 預設行為

---

## OpenAI Codex

### 26.527 · 2026-05-29（[Computer use and mobile access on Windows](https://developers.openai.com/codex/changelog)）

> **繁中摘要**：Codex 新增 Windows Computer Use，可操控桌面應用程式；同時支援從 iOS/Android/Mac 遠端控制 Windows 上的 Codex 工作，並強化 thread 協調與歷史搜尋能力。

**變更重點**
- **Computer Use on Windows**：Codex 可與 Windows 桌面應用程式互動，擴展自動化範疇
- **遠端控制**：從 iOS、Android 或 Mac 上的 ChatGPT 啟動及管理 Windows 裝置上的 Codex 工作
- **Profile section 強化**：顯示使用者詳細資訊、使用統計與 token 活動
- **Thread 協調改善**：本地專案與 worktrees 現有獨立背景 thread，減少互相干擾
- **搜尋擴展**：歷史對話搜尋現在涵蓋對話內容與 Git branch 名稱

**實務影響**
- Windows 使用者可讓 Codex 直接操控桌面 GUI 應用，適合需要 UI 自動化的開發任務
- 行動裝置使用者可從 iOS/Android 遠端啟動並監控 Windows 上的 Codex 任務
- 本地 git worktree 工作流程獲得更好的 thread 隔離，多個並行任務的狀態更清楚
- 歷史搜尋加入 Git branch 名稱，有助查詢特定功能開發期間的 Codex 對話記錄
