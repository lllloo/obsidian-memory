---
title: 如何建構有效的 AI Agent（不被炒作牽著走）
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-01-20
source: https://www.youtube.com/watch?v=tx5OapbK-8A
---

## 核心觀念：Workflow vs. Agent

來自 Anthropic 的定義：

- **Workflow**：LLM 和工具透過**預定義程式碼路徑**協作 → 可預測、可控制
- **Agent**：LLM **動態指揮**自己的流程和工具使用 → 靈活但難以控制

作者建議：大多數問題用 **Workflow 模式**就夠了，只在必要時才引入 Agent 模式。

## 增強型 LLM 的三個核心要素

所有 AI 系統都建構在這三個基礎之上：

1. **Retrieval（檢索）**：從外部資料庫取得相關資訊（RAG）
2. **Tools（工具）**：呼叫外部 API 或函式取得資料或執行操作
3. **Memory（記憶）**：保留過去的對話歷史

## 五種常見 Workflow 模式

### 1. Prompt Chaining（提示鏈）
將複雜任務拆分成多個 LLM 呼叫，前一步的輸出作為下一步的輸入。

例：寫文章 = 研究 → 選題 → 大綱 → 各章節 → 校稿

### 2. Routing（路由）
讓 LLM 先分類輸入，再根據類別走不同處理路徑：

```python
category = llm.classify(input)  # 回傳結構化輸出
if category == "order_status":
    handle_order_query(input)
elif category == "refund":
    handle_refund(input)
else:
    route_to_human(input)
```

### 3. Parallelization（平行化）
多個 LLM 呼叫同時執行（async），適合互相獨立的子任務。

例：同時執行「準確性」、「有害性」、「Prompt Injection」三個 guard rail 評估。

### 4. Orchestrator-Worker（協調者-執行者）
Orchestrator LLM 根據 context 決定需要哪些步驟，再分配給 Worker LLM 執行。適合半開放式問題，比純 Workflow 更靈活，但比純 Agent 更可預測。

### 5. Evaluator-Optimizer（評估-優化）
LLM A 生成內容 → LLM B 評估並給出反饋 → LLM A 根據反饋改進。

## Agent 模式

Agent 在一個 loop 中執行：接收指令 → 選擇工具 → 執行 → 評估環境 → 繼續或停止。

適合複雜、開放式任務，但：
- 難以預測行為
- 錯誤難以除錯
- 目前業界（如 Devin）成功率仍有限

## 實用技巧

1. **謹慎使用 Agent Framework**：可快速上手，但理解底層原理更重要
2. **優先選擇確定性 Workflow**：從最簡單的解法開始，只在必要時增加複雜度
3. **垂直深入，再水平擴展**：先完美解決一個問題（如「在哪個訂單」），再擴展到其他場景
4. **別低估規模化的難度**：Demo 好用 ≠ 百萬用戶規模下好用；RAG 隨資料量增加會越來越難維護
5. **從一開始就建立評估系統**：修改 System Prompt 前，能否確定會改善結果？需要系統化測試
6. **加入 Guard Rail**：用額外的 LLM 呼叫檢查輸出，避免輸出不當內容

## 核心心態

> 先找最簡單的解法，只有在真的需要時才增加複雜度——這也意味著有時根本不需要 Agentic 系統。
