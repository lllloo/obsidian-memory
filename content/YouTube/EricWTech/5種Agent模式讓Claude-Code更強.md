---
title: "用這 5 種 Agent 模式讓 Claude Code 更強"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-10
source: https://youtu.be/DIHIllggaTw
---

Eric W Tech 介紹五種 Claude Code Agent 模式，從最基本到全自動，讓 AI 工具從單一對話模式升級為多 Agent 並行架構。

## 影片描述

大多數人使用 Claude Code 的方式是一次一個任務、等待回應、再給下一個，這形成了瓶頸。本影片示範五種 Agent 模式，從簡單到完全自主，讓你可以在 Claude Code 執行工作的同時去喝咖啡。

## 五大 Agent 模式重點摘要

### 1. Sequential Flow（順序流程）
- 讓 AI Agent 依序完成一個任務接著一個任務
- 範例：`fix tickets` 技能自動化整個 bug 修復流水線
- 流程：讀取 Jira ticket → 用 Playwright 重現問題 → 研究 → 實作 → 多 sub-agent 審查 → 驗證 → commit → 部署 → 推進 QA
- 適用場景：需要按順序完成的自動化工作流程

### 2. Split & Merge（分割與合併）
- 將單一大任務拆分給不同 sub-agent 並行處理，最後合併回 orchestrator
- 範例：`agent-db-audit` 技能讓多個 sub-agent 同時稽核資料庫（schema、安全性、查詢效能）
- 也可用於 Pull Request 審查流程：同時觸發多個專業審查 agent
- 優勢：完成速度更快、避免 context 污染、各 agent 專注特定領域

### 3. Agent Teams（Agent 團隊）
- 與 sub-agent 的差異：各 agent 之間有共享通訊管道
- 適合處理需要跨元件協作的任務（如前後端共同開發同一功能）
- 可設置「devil's advocate」角色，持續挑戰其他 agent 的決策
- 不適用場景：各 agent 各自完成獨立工作、無需溝通時

### 4. Operator（Git Worktrees 隔離環境）
- 為每個 Claude Code session 建立獨立的隔離環境
- 可同時開多個終端機 session，各 session 在不同 Git worktree 中運作
- 實際應用：同時產生多個 UI 設計變體，選擇最佳結果後刪除其他
- 兩大優勢：加速開發、便於 A/B 測試

### 5. Headless Mode（無頭模式）— 作者最愛
- 使用 `claude -p "prompt"` 在背景執行，不需在 Claude session 中互動
- 可搭配 cron job 排程自動執行
- 結合 **Ralph Loop**：讓 AI Agent 持續循環執行直到達成目標
- 作者實際案例：`iterative review` 技能，指定執行 5 次迴圈審查
  - 每次迭代使用全新 context window
  - 每個 headless session 觸發 5-7 個 sub-agent 並行運作
  - 最終將所有迭代的發現彙整成單一報告

## 補充資訊

作者背景：曾任 Amazon、Microsoft 資深 AI 軟體工程師，現在經營付費社群教授 AI agent 與自動化。
