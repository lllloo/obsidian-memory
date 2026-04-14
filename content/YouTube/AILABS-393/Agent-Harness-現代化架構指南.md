---
title: Anthropic 實驗後的 Agent Harness 現代化架構指南
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: 2026-03-31
source: https://www.youtube.com/watch?v=nBH07G-zayk
---

## 核心結論：大部分 Harness 已成過時包袱

Anthropic 對自家 harness 逐一移除元件並測量影響，發現以 Opus 4.6 為基礎的現代 agent 系統只需要三件事：

1. **Planner**（規劃）
2. **Generator**（實作）
3. **Evaluator**（評估）

其餘元件（context isolation、詳細微任務拆分等）在 Opus 4.5/4.6 下已成多餘負擔。

## 規劃層（Planning）的改變

**舊做法（BMAD、SpecKit 等）：**
- 要求用戶提供詳盡規格
- 將任務拆解成微任務，幾乎不需要 agent 自己思考
- 問題：規格一個錯誤就會向下傳播，agent 難以自行修正

**新做法（Opus 4.5+ 後）：**
- 規劃只需要**產品層級**，不需要技術實作細節
- 告訴 agent 需要什麼「交付物」，讓它自己找路徑
- 計畫應包含完整功能拆分與每個 phase 的用戶故事（User Stories）

**實際影響：**
- BMAD 可用於產出 PRD，但不需要進入技術 sharding 階段
- Superpowers 的「提問 session」在識別 edge case 方面比多層文件更有效
- Claude 內建 plan mode 仍偏向技術實作，不適合純產品規劃

## 評估層（Evaluation）的重要性

**核心原則：寫程式的 agent 不能自己評估自己的程式**

Self-evaluation 的問題：
- Agent 傾向自信地稱讚自己的輸出，即使品質明顯不佳
- 對可量化指標（API 是否正常運作）還好，但主觀任務（UI 品質）問題更嚴重

**解決方式：Generator 與 Evaluator 完全分離**
- 所有框架（GSD、BMAD、Superpowers）都有這個機制，但實作方式不同

## Sprint Contract（任務合約）

- Generator 與 Evaluator 在實作前先議定「完成」的定義
- **Opus 4.6 後可省略**：模型夠強，Generator 已能自行完成大部分工作
- Sonnet、Haiku 仍需要：完整任務文件、sprint 結構、明確的完成標準

## Context 管理的改變

**「Context 焦慮」（Context Anxiety）：**
- 較小模型在長任務中，context 越填越滿時，會過早宣稱任務完成
- 舊解法：context reset + 外部文件持續任務狀態

**Opus 4.5+ 之後：**
- 不再出現 context 焦慮行為
- Claude 的 compaction 機制已足夠
- 不需要 context reset，也不需要 BMAD/SpecKit 的詳細任務拆分

## Generator Agent

- 功能：逐功能實作 app，整合 git 版本控制
- 工作流程：理解任務 → 實作 → 精煉實作
- 實作階段分四個子階段
- 完成功能後交給 Evaluator，接收回饋後繼續改進

## Evaluator Agent

- 功能：從對立角度驗證實作，假設 bug 存在，主動找問題
- 工具：Playwright 測試 UI 用戶流程
- 讀取 plan 以了解「完成」應該長什麼樣子

**各框架 Evaluator 比較：**
- BMAD：專門的 code review + QA agents，多角度測試
- GSD：verifier sub-agent，比對計畫生成文件報告（pass/fail）
- Superpowers：嚴格 TDD，測試寫完才能寫程式，否則被阻擋
- SpecKit：以 spec 為真相來源，驗證程式碼是否符合文件
- Anthropic harness：**評分機制最嚴格**，最接近真正的實作執行強制

## Graded Evaluation（評分制評估）

對於主觀性任務（如 UI），需要明確的評分標準讓 agent 知道「對」長什麼樣。

**Anthropic 的前端評分四維度：**
1. **Design quality**：各元件是否有整體視覺一致性
2. **Originality**：是否避開 AI 慣用的紫白藍白配色，是否有刻意的設計選擇
3. **Craft**：字型、間距、一致性、配色對比（創意優先，不只是技術正確）
4. **Functionality**：每個 UI 元件是否發揮視覺功能

Claude 在 craft 和 functionality 表現已很好，originality 和 design quality 是主要弱點。

可為程式架構、前端、UX、用戶流程等不同面向設置類似評分標準。

## 現在應該怎麼做

**使用現有框架：**
- 推薦 **GSD**，因為它本身就包含 planner-generator-evaluator 迴圈
- 但 GSD 的 evaluator 只比對計畫，用 pass/fail 機制，不夠嚴格
- 改進做法：替換 GSD 的 evaluator，加入 Anthropic 的評分標準

**自行建立：**
- 用 agent teams 實作（agent team 成員可互相溝通，sub-agents 只能寫文件）
- 一個 agent team 成員作 generator，另一個作 evaluator
- Generator 實作，Evaluator 用 Playwright MCP 同步測試，互相溝通修正
