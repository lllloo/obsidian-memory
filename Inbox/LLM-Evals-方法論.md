---
title: LLM Evals 方法論
created: 2026-05-27
updated: 2026-05-28
source: https://www.youtube.com/watch?v=a3SMraZWNNs
published: 2025-09-04
tags:
  - eval
  - ai-agent
---

**沒有評估機制是 GenAI 專案失敗的核心原因之一**（Gartner 預測 2027 年 40% AI agent 專案被取消、MIT 報告 95% pilot 失敗）。Eval = 對 AI 系統某個面向品質的系統化量測；不是一次性工作，是持續改善循環的一部分。一個系統通常有多個 eval（retrieval 準確率、回覆正確率、語氣符合度…）。

這對應 **agentic 開發生命週期（ADLC）相對傳統 SDLC 的根本轉變**：agent 是非確定性系統，成功指標從布林 pass/fail 變成**分佈**（accuracy distribution、hallucination rate、cost per outcome），無法塌成單一通過與否；且進 production 前需要一個 **Simulation / proof-of-value 階段**——用真實資料與 ground truth 驗證假設、當作 ROI gate，原型階段砍掉比上線後砍便宜得多。

## 為什麼難：三大挑戰

- **資料理解**：測試只跑 happy path，真實用戶行為差異極大，得了解大規模下系統實際在處理什麼。
- **規格落差**：你知道什麼是好答案，但翻成 prompt 指令很難；壞答案的成因（prompt？retrieval？pipeline 邏輯？）也難判斷。
- **行為不一致**：測試集表現好不代表真實輸入穩定，LLM 對措辭細微差異很敏感。

## 三個能力缺一不可

1. **評估品質**：有系統的效能量測。
2. **除錯能力**：trace logging、資料檢視、錯誤分析（Langfuse 這類可觀測性平台負責記錄每次呼叫的 inputs/outputs/latency/cost）。
3. **改變行為**：根據評估結果實際改善系統。

**多數團隊只做第 3 步、跳過 1 和 2，所以卡在 demo 階段過不去**——這是最關鍵的判斷。

## 三層 Evals（由輕到重）

| 層 | 方法 | 特性 | 適用 |
|---|---|---|---|
| **L1 Unit Tests** | 確定性測試，輸入固定、預期輸出明確（答案含關鍵字 Y） | 快、便宜 | 回歸測試 |
| **L2 Human-annotated** | 人類標注對錯，建 ground truth dataset | 成本高、品質可靠 | 建立金標準 |
| **L3 LLM-as-Judge** | 另一個 LLM 自動評分 | 可在生產持續跑 | 難用規則判斷的（語氣、相關性、完整性） |

## L1 的最小可行落地（今天就能寫）

前提：用 structured output（Pydantic model）。步驟：

1. 收集 **5–10 個以上**真實輸入範本（客服 email、用戶訊息，存 JSON）。
2. 跑過 AI pipeline 取得回應物件。
3. 對關鍵欄位寫 assertion，**一個 test case 至少 3 個 assert**（如 `intent == "billing"`、`not escalate`、`confidence >= 0.9`）。
4. **每次改 prompt 或 application logic 後重跑全部** test case——assertion error 立刻告訴你哪個欄位壞、往哪 debug。

關鍵慣例：**evals 與主 application code 分開**（獨立 `evals/` 與 `data/samples/`），保持關注點分離。不需要複雜框架就能建立基本可靠性保障——這招在 Black Friday 上線時實際救過場。

## 改善循環

```
部署 → 追蹤 → 發現問題 → 調 prompt/pipeline
→ 在 eval 資料集上重跑 → 確認沒修好 A 卻弄壞 B/C → 部署
```

每次改動都要對照 eval 資料集，這正是 L1 assertion 套件存在的意義。

## 相關

- [[Production-RAG-架構]] — RAG 的 NDCG / evaluation set 就是 eval 在 retrieval 上的應用
- [[Context-Engineering]] — eval 回饋驅動 prompt / context 調整
