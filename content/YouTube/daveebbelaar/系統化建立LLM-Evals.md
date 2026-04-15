---
title: 系統化建立 LLM Evals
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-09-04
source: https://www.youtube.com/watch?v=a3SMraZWNNs
---

## 為什麼需要 Evals

Gartner 預測 2027 年 40% AI agent 專案會被取消；MIT 報告 95% GenAI pilot 失敗。沒有評估機制是核心原因之一。

Evals 幫你回答：
- 改了 system prompt 後效果有沒有變好？
- RAG pipeline 的 retrieval 準確嗎？
- 分類步驟是否正確？
- 語氣是否符合品牌？
- 系統在真實用戶輸入下表現如何？
- 有沒有抓到 prompt injection？

## LLM 開發三大核心挑戰

### 1. 資料理解問題

測試階段只跑 happy path 和少數範例，但真實用戶行為差異很大。需要了解大規模下系統實際在處理什麼。

### 2. 規格落差問題

你知道什麼是好答案，但把它翻成 prompt 指令很難。什麼原因造成壞答案（prompt 問題？retrieval 問題？pipeline 邏輯？）很難判斷。

### 3. 行為不一致問題

在測試集表現良好，但在真實輸入表現不穩定。LLM 對措辭細微差異很敏感。

## 三個關鍵能力

成功的 AI 系統開發需要三者配合：
1. **評估品質**：有系統的效能量測（自動化測試、人工標注、成功指標）
2. **除錯能力**：trace logging、資料檢視、錯誤分析（Langfuse 負責這塊）
3. **改變行為**：能根據評估結果實際改善系統

大部分團隊只做第 3 步，跳過 1 和 2，導致無法超越 demo 階段。

## Eval 定義

**Evaluation（Eval）= 對 AI 系統品質的系統化量測**

- 一個 eval = 量測一個特定面向的指標
- 一個 AI 系統可能有多個 eval（retrieval 準確率、回覆正確率、語氣符合度等）
- eval 不是一次性工作，是持續改善循環的一部分

## 三個層級的 Evals

### Level 1：Unit Tests（單元測試）

- 確定性測試，輸入固定、預期輸出明確
- 例：給定問題 X，確認答案包含關鍵字 Y
- 快速、便宜、適合回歸測試

### Level 2：Human-annotated Datasets（人工標注資料集）

- 由人類標注正確/錯誤的樣本
- 建立 ground truth 資料集
- 成本較高，但品質可靠

### Level 3：LLM-as-a-Judge（LLM 作為評判）

- 用另一個 LLM 自動評分系統輸出
- 適合難以用規則判斷的問題（語氣、相關性、完整性）
- 可在生產環境持續自動執行

## 工具鏈

- **Langfuse**：trace logging、prompt management、資料集管理、實驗追蹤
  - 開源可自架，也有 cloud 版本
  - 記錄所有 LLM 呼叫的 inputs、outputs、latency、token cost

## 改善循環

```
部署 → Langfuse 追蹤 → 發現問題 → 調整 prompt/pipeline 
→ 在 eval 資料集上跑測試 → 確認改善 → 部署
```

每次改動都要對照 eval 資料集，確認沒有因為修好 A 問題而破壞 B、C 問題。
