---
title: "Claude Code + 超能力 = Vibe Coding 的終結？（完整教學）"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-31
source: https://youtu.be/TX91PdBn_IA
---

**影片描述**：Agentyk Superpowers 是一個讓 AI Agent 強制遵循結構化工作流程的框架，與其他 spec-driven 框架（GSD、SpecKit、BDD）最大差異在於引入**測試驅動開發（TDD）**。作者以實際生產應用 Bookworm.ai 為範例，完整示範從腦力激盪到功能上線的工作流程。

**重點摘要：**
- **為何選 Superpowers**：唯一強制執行 TDD 的 spec-driven 框架。TDD 的核心邏輯是「先寫測試（預期失敗）→ 再實作（讓測試通過）→ 反覆 refactor 直到無需修改」，確保 AI 實作前先明確定義期望行為，避免實作後才發現不符預期。
- **額外優勢**：結合 Git worktrees 隔離開發環境 + 每個任務委派給獨立 sub-agent（fresh context window）+ 最終自動 code review，三層機制共同提升準確率。
- **安裝方式**：透過 Claude Code 官方 marketplace 或 plugins marketplace 安裝，安裝後用 `plugins` 指令確認，slash commands（`/superpowers plan` 等）已 deprecated，應直接觸發對應的 skills。
- **Brainstorm 技能**：可輸入 Jira ticket URL 或直接描述需求，Superpowers 自動探索現有程式架構，並在瀏覽器呈現互動式 HTML UI mockup 讓用戶選擇設計方向，完成後自動在 `docs/` 建立含設計決策、架構說明、API 路由、新元件清單、邊緣案例、驗收標準的完整 spec 文件。
- **Writing Plan 技能**：將 spec 轉換為任務清單，每個任務細分為含 checkbox 的步驟，明確標示「先跑測試（應失敗）→ 實作 → 再跑測試（應通過）」的順序，完成後自動 commit。
- **執行模式**：推薦使用「sub-agent driven」模式，每個任務派一個獨立 sub-agent 執行，保持 fresh context window；另有「inline execution」模式在同一 session 批次執行（有 checkpoint）。
- **自動 Code Review**：全部 11 個任務完成後，自動觸發 code review skill，找出 critical/important 問題並派發 fix agent 修正，作者案例中找出了 stale credits、selection confirmation、metadata 等問題。
- **實際示範結果（Bookworm.ai）**：Google Drive 重新同步功能，11 個任務全部完成，smoke test 驗證點擊「Sync connected folder」後成功偵測並匯入 Google Drive 新增的 6 個檔案，功能完整運作。
