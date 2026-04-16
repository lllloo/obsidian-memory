---
title: Agent Threads：如何像 Boris Cherny 一樣出貨，Thread-Based Engineering 框架
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 
source: https://www.youtube.com/watch?v=-WBHNFAB0OE
parent: "[[01.index]]"
---

## 核心概念：什麼是 Thread？

Thread = 一個由你和 agent 共同完成的工程工作單位，包含兩個必要節點：

1. **Prompt/Plan**（你出現）
2. **Agent 執行工具呼叫**（中間段）
3. **Review/Validate**（你出現）

衡量進步的指標：agent 代表你執行的 tool calls 總量。

## 六種 Thread 類型

### Base Thread（基礎）
- 最基本單位：下 prompt → agent 做工 → 你 review
- 是所有其他 thread 的基礎

### P Thread（並行）
- 同時執行多個 base threads
- Boris Cherny（Claude Code 創始人）預設開 5 個 Claude Code 並行
- 另外在 Claude Code web 介面跑 5-10 個背景 agents
- 工具：fork terminal skill、Pthread alias

### C Thread（鏈式）
- 將大型工作拆成多個階段，逐段 review 再繼續
- 適用：context 太大撐不住一次、高風險生產工作（migration 等）
- 工具：`ask_user_question` tool、系統通知、TTS hook

### F Thread（融合）
- 向多個 agents 下相同或相似 prompt，收集結果後合併
- 用途：取最佳結果（best-of-N）或從多個版本中挑選合適元素
- 最適合快速原型設計（rapid prototyping）
- 工具：Pthread skill（可同時跑 Claude、Gemini、Codex）

### B Thread（大型/巢狀）
- 你的 agent 觸發其他 agents（sub agents、orchestrator agents）
- 從工程師視角：只看到 prompt 和 review，中間是黑盒
- Ralph Wiggum pattern = 在 agent 外加一層 loop，讓 agent 對同一問題持續跑

### L Thread（長時間高自主性）
- 無人介入的長時間執行，數百到數千次 tool calls
- Boris 曾跑超過 1 天 2 小時的單一 thread
- Stop hook：agent 嘗試停止時，執行驗證腳本決定是否繼續

### Z Thread（隱藏第七種：零觸碰）
- 最高信任等級：移除 review 節點
- 工程師不需要 review，因為知道不必 review
- 目標終態，非 vibe coding

## Boris Cherny 的設定

- 5 個 Claude Code 在 terminal 並行（編號 tab 1-5）
- 額外 5-10 個在 Claude Code web 介面跑背景工作
- 永遠用 Opus 4.5
- 不用 `--dangerously-skip-permissions`，設定具體權限
- 最重要原則：給 agent 一個能驗證自己工作的方式（closed loop / validation loop）

## 四個進步維度

1. 跑**更多** threads
2. 跑**更長**的 threads
3. 跑**更厚**的 threads（巢狀更多工作）
4. **更少**的人工介入 checkpoints

## 核心公式

**Core Four**：Context × Model × Prompt × Tools

一切 agentic engineering 最終都歸結於此。提升這四個要素，threads 自然變得更長、更厚、更自主。
