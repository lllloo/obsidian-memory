---
title: 這樣用 Claude Code 準確度更高：七個實用技巧
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-01
source: https://www.youtube.com/watch?v=D5bRTv6GhXk
---

## 重點摘要

七個提升 Claude Code 準確度的技巧：

1. **Context 管理**：底部狀態列顯示 context 使用百分比；達 50% 時執行 `/clear` 重置；狀態列可自訂（emoji meter、fraction、hash bar），在 VS Code terminal 也同步顯示

2. **Sub Agents**：Orchestrator 分派任務給不同 Sub Agent（後端 API、測試、Review），各自擁有獨立 context window，可並行執行，減少 bug 與幻覺

3. **Superpowers 框架**：Claude Code 的 agentic skill framework，流程：澄清需求 → 生成 spec → to-do list → TDD（先寫測試、再寫 app logic → 重構循環）

4. **Agent Teams**：不同 Sub Agent 之間建立共享通訊頻道（前端 ↔ 後端 ↔ 資料庫），解決傳統 sub agents 之間無法互相溝通的問題

5. **Context7**：提供最新版本文件給 LLM，避免使用過時訓練資料、幻覺 API。設定：contextseven.com/dashboard 取得 API key → 透過 CLI + skills 安裝，在 prompt 中要求「用 Context7 fetch 相關文件進行 fact-check」

6. **NotebookLM 知識庫**：將研究資料（YouTube、Google Drive、PRD、web sources）存入 NotebookLM，在 `CLAUDE.md` system prompt 中指示查詢，避免一開始就把所有文件塞入 context。優點：context window 更小、資訊更準確、跨 session 持久共享

7. **CLI 優於 MCP**：CLI + skills 比 MCP 更省 token，因為 skills 只在相關時才載入，不會在 context 啟動時全部注入。Playwright CLI 測試結果比 MCP 版本 token 更少且更準確
