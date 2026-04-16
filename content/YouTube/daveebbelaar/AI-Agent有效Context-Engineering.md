---
title: AI Agent 有效的 Context Engineering（為何 Agent 在實踐中仍然失敗）
tags:
  - youtube
  - ai-agent
created: 2026-04-13
updated: 2026-04-13
published: 2025-12-19
source: https://www.youtube.com/watch?v=nkJXADeI62c
parent: "[[01.index]]"
---

## 問題的根源：不是模型，是 Context

AI Agent 在 demo 表現優異但在實際產品中失敗，大多數情況下問題不是模型能力不足，也不是工具或 agent loop 本身，而是 **context engineering 做得不夠好**。

Context Engineering 定義（Anthropic）：「在 LLM 推理過程中，策略性地篩選與維護最佳 token 集合的一套策略。」

Context 的範疇包含：
- 系統提示（system prompt）
- 對話歷史（message history）
- 工具定義與工具輸出（tool descriptions & outputs）
- 文件與擷取的知識（documents, RAG chunks）
- 記憶體（memory files）
- 中間推理（intermediate reasoning）
- 環境回饋（environment feedback）

## Context 的核心挑戰

研究發現（Needle-in-a-Haystack 測試）：隨著 context 膨脹，模型效能明顯下降。這個特性在所有模型上都存在，差別只在退化曲線的斜率。

核心目標：**找到能最大化目標輸出機率的最小高訊號 token 集合。**

## System Prompt 的校準

常見陷阱：
1. **太模糊**：初始版本只有基本指令，使用者回饋後開始堆積限制
2. **太具體**：大量 if/else 式語句，例如「不要這樣說」、「如果使用者說 X 就回 Y」

正確做法：
- 讓 prompt **足夠具體但保留創意空間**，不要變成 if/else 清單
- 遇到需要大量規則的情況，優先考慮**拆分問題**：加一個 router，讓 AI 先分流再用更小的 prompt 處理各子問題
- 使用結構化格式（XML 或 Markdown）組織 system prompt：
  ```
  ## Background
  ## Instructions
  ## Tool Guidance
  ## Output Format
  ```

## 常見的工程錯誤

### 使用負面範例而非正面範例

錯誤：「不要做 X」、「避免 Y」
LLM 不擅長處理負面指令，應改為「要做什麼」、提供正面示例（few-shot examples）。

### 不看資料與 trace

解決方案：從第一天就接入追蹤工具（如 **Langfuse**），可視化完整的：
- System prompt
- 所有訊息歷史
- 工具呼叫過程

大多數的 LLM 行為異常，只要看完整 trace 幾乎立刻能發現問題所在。

### 混淆 Workflow 與 Agent

- **Workflow**（DAG）：確定性強、可測試，適合後端自動化、客戶服務等不允許錯誤的場景
- **Agent**（LLM + 工具迴圈）：彈性強，適合有人在回路的聊天介面（使用者可即時糾錯）

不要因為「agent」這個詞很流行就對每個問題都用 agent 方案。

## 各類 Context 的管理策略

### 文件（Documents）
- 文件太大時不要整份塞入，使用 RAG
- RAG 策略：先廣撈 50 個 chunk，再用 reranker 取最相關 8 個

### 工具（Tools）
- 工具描述要簡短、聚焦、不重疊
- 工具數量太多時，拆分成 sub-agent（讓一個 agent 作為另一個的工具）

### 記憶體與對話歷史（Memory）
- 開發階段不容易發現問題（只有幾輪測試）
- 使用者到第 10-20 輪時開始出問題
- 策略：
  - **Pruning**：直接移除較早的訊息
  - **Summarization**：將前 N 輪摘要成一段文字插回對話歷史
  - **State Machine**：用資料庫追蹤使用者所在的流程階段，依階段動態注入不同的 system prompt 片段

### 動態 System Prompt 注入

例：引導使用者完成多階段評估的 agent，不要把所有階段規則都塞進一個大 system prompt。改為：
1. 在資料庫記錄使用者目前的階段（state）
2. 每次使用者傳訊時從資料庫拉取對應的 context
3. 根據 state 動態組合 system prompt

優點：每個階段的 prompt 更小更聚焦，不會互相干擾。

## 建立正確的測試思維

傳統軟體工程：寫功能 → 寫單元測試 → 測試通過即可。

AI 系統的挑戰：不只要第 1 輪通過，第 10 輪、第 20 輪也必須通過。Context 是隨對話積累的，問題往往在深度互動後才浮現。

解決方式：定期審視真實使用者的完整 trace，而不是只在開發環境跑幾輪短測試。
