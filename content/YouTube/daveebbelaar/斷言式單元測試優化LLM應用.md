---
title: 用斷言式單元測試建構更好的 LLM 應用
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2024-11-27
source: https://www.youtube.com/watch?v=bnvOk1fm0tw
---

Dave 分享了一個實用的 LLM 應用評估技巧：在程式碼中用 assertion 進行單元測試，快速驗證 LLM 的 structured output 是否符合預期。這個方法在 Black Friday 生產上線中實際救了他們一次。

## 核心問題

每次修改 prompt 或 application logic，你無法確定 LLM 的輸出是否仍符合預期。傳統單元測試驗證的是程式邏輯，但 LLM 的輸出是機率性的，需要另一種驗證方式。

## 方法：Assertion-Based Unit Tests

**前提**：使用 structured output（Instructor 或 OpenAI structured output）取得 Pydantic model

**步驟：**

1. 收集真實的輸入資料範本（JSON 格式），例如客服 email、用戶訊息
2. 把資料跑過你的 AI pipeline，取得 Pydantic 回應物件
3. 針對回應物件的關鍵欄位寫 assertion

```python
from app.pipeline import process_event
from data.samples import billing_inquiry_event

# 執行 AI pipeline
result = process_event(billing_inquiry_event)
analyze = result.analyze_ticket

# 至少寫 3 個 assertions
assert analyze.customer_intent == "billing_invoice"
assert not analyze.escalate  # 不需要升級
assert analyze.confidence >= 0.9
```

## 實際操作原則

- 一個 test case 至少寫 **3 個** assertion（作者引用文章建議，雖然看似任意，但實際有效）
- 不只準備一個範本，而是 **5-10 個甚至更多** 真實資料範本
- 每次修改 prompt 或 application logic 後，**重新跑所有 test cases**
- 若有 assertion error，立刻知道哪個欄位出問題、往哪個方向 debug

## 專案結構建議

```
project/
├── app/          # 主要 AI 邏輯
├── evals/        # 評估腳本（或命名為 playground）
└── data/
    └── samples/  # 真實輸入範本（.json 檔案）
```

關鍵原則：**evals 與主 application code 分開**，保持關注點分離。

## 自動化

手動執行 assertion 是起點，進一步可以：
- 寫腳本將所有範本 JSON 檔案 loop 過去，自動執行所有 assertions
- 整合 LangFuse（或其他可觀測性平台）監控所有 LLM 呼叫的 trace
- 發展成更正式的評估資料集

## 為何有效

- LLM 的 structured output + assertion = 測試 LLM 行為的最簡單方式
- 在 debug 階段就能發現：是 prompt 改壞了，還是 application logic 有問題
- 不需要複雜的 eval 框架，就能建立基本的 LLM 可靠性保障
