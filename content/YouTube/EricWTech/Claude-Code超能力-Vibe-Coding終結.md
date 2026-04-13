---
title: "Claude Code + 超能力 = Vibe Coding 的終結？（完整教學）"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-31
source: https://youtu.be/TX91PdBn_IA
---

EricWTech 完整示範 Agentyk Superpowers 框架，結合測試驅動開發（TDD）與多 Sub-Agent 架構，大幅減少 AI 程式代理的錯誤率。

## 影片描述

Agentyk Superpowers 是一個讓 AI Agent 強制遵循結構化工作流程的框架，核心差異在於引入測試驅動開發（TDD）。作者以實際生產應用 Bookworm.ai 為範例，示範從腦力激盪到功能上線的完整流程。

## 為何選擇 Superpowers

與其他 spec-driven 開發框架（GSD、SpecKit、BDD）的主要差異：

- **測試驅動開發（TDD）**：先寫測試，再寫程式碼，確保功能符合預期
- **Git worktrees 隔離**：每個開發任務在獨立環境進行，避免衝突
- **Sub-agent 委派**：每個任務交由獨立 sub-agent 處理，保持 context 清潔
- **循環至完成**：refactor → test → 再 refactor，直到無需修改

## 完整開發工作流程

### 1. 安裝 Superpowers
```
# 透過 Claude Code 官方 marketplace 安裝
# 或透過 plugins marketplace
```
安裝後用 `plugins` 指令確認安裝狀態。

### 2. 腦力激盪（Brainstorm）
- 觸發 `brainstorm` 技能
- 可輸入 Jira ticket URL 或直接描述需求
- Superpowers 自動探索既有程式架構
- **互動式 UI mockup**：在瀏覽器呈現 HTML 設計稿，讓用戶選擇方向
- 完成後自動在 `docs/` 建立 spec 文件，包含：
  - 設計決策
  - 架構說明
  - API 路由規劃
  - 新元件清單
  - 邊緣案例處理
  - 驗收標準

### 3. 實作計畫（Implementation Plan）
- 觸發 `writing plan` 技能，將 spec 轉換為任務清單
- 每個任務細分為步驟，每步驟含 checkbox
- 明確標示：先執行測試（預期失敗） → 實作 → 再執行測試（預期通過）
- 完成後自動 commit

### 4. Sub-Agent 執行（兩種模式）
- **Sub-agent driven（推薦）**：每個任務派發給獨立 sub-agent，fresh context window
- **Inline execution**：在同一 session 批次執行，設有 checkpoint

執行環境選項：
- Project level worktree（建議）
- Global location

### 5. 自動 Code Review
- 全部任務完成後自動觸發 code review 技能
- 找出 critical 與 important 問題
- 自動派發 fix agent 修正問題

## 實際案例：Bookworm.ai Google Drive 同步功能

需求：讓用戶能重新同步已連接的 Google Drive 資料夾，匯入新上傳的收據檔案

成果：
- 11 個任務全部完成
- 自動 code review 找出 stale credits、selection confirmation、metadata 問題
- 手動 smoke test 驗證：點擊「Sync connected folder」→ 偵測到 Google Drive 新增的 6 個檔案 → 成功匯入

## 補充說明

- Slash commands（`/superpowers plan` 等）已 deprecated，應直接觸發對應的 skills
- 作者預告即將發布「如何讓 AI Agent 達到 100% 準確率」的後續影片
