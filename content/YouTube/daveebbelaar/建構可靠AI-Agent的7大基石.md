---
title: 建構可靠 AI Agent 的 7 大基石
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-07-25
source: https://www.youtube.com/watch?v=T1Lowy1mnEg
parent: "[[01.index]]"
---

本影片目標是幫助開發者從基礎原理理解 AI Agent，跳脫框架噪音，專注於 7 個核心 building block。Dave 以 Python 程式碼示範，並強調在生產環境中盡量減少 LLM API 呼叫，優先使用 deterministic 程式碼。

## 背景：AI 工程師的定位

- AI 工程師的定義：將預訓練模型整合至應用程式，而非從頭訓練模型（那是 ML engineer / data scientist 的工作）
- 99% 的 AI Agent 教學充斥雜訊；核心原則才是關鍵
- 實際生產環境中，tool call 的使用比你想像的少得多

## Building Block 1：Intelligence Layer（LLM API 呼叫）

- 唯一真正的「AI」元件，負責與 LLM 溝通
- 使用 OpenAI Python SDK：建立 client、選擇模型、傳入 prompt、等待回應
- 原則：只有 deterministic 程式碼無法解決問題時，才呼叫 LLM API

## Building Block 2：Memory（記憶體）

- LLM 本質上是 stateless，每次對話都從頭開始
- 解法：手動傳遞對話歷史（conversation history），以交替的 user/assistant 訊息序列呈現
- 實際應用：將對話狀態存入資料庫，每次呼叫時取回

## Building Block 3：Tools（工具）

- 讓 LLM 呼叫外部函式：查詢 API、更新資料庫、讀取檔案
- 工作流程：LLM 判斷是否使用工具 → 選擇工具與參數 → 程式碼執行 → 結果回傳 LLM → LLM 格式化最終回應
- 各大模型供應商都原生支援 tool calling，無需額外框架

## Building Block 4：Validation（驗證）

- LLM 輸出是機率性的，相同問題可能給出不同結果
- 解法：要求 LLM 回傳符合預定 JSON schema 的 structured output，並用 Pydantic 驗證
- 驗證失敗時，可將錯誤訊息回傳 LLM 讓其修正
- 這是「context engineering」最核心的技能

```python
# 使用 Pydantic 定義預期的結構
class TaskResult(BaseModel):
    task: str
    due_date: str
    priority: Literal["low", "medium", "high"]

# 呼叫 OpenAI 時指定 response_format
response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[...],
    response_format=TaskResult,
)
```

## Building Block 5：Control（流程控制）

- 不要讓 LLM 做所有決策，部分邏輯應交給 deterministic 程式碼
- 做法：用 LLM 分類 intent（structured output），再用 if/else 路由到對應函式
- 優點：比 tool call 更容易 debug——可以記錄 LLM 選擇某類別的理由（reasoning 欄位）

```python
class IntentClassification(BaseModel):
    intent: Literal["question", "request", "complaint"]
    confidence: float
    reasoning: str

# 再依 intent 路由
if result.intent == "question":
    handle_question(...)
elif result.intent == "request":
    handle_request(...)
```

## Building Block 6：Recovery（錯誤恢復）

- 生產環境一定會出問題：API 中斷、LLM 輸出亂碼、rate limit
- 標準做法：try/except、retry with backoff、fallback response
- 每個 try/except block 都針對特定問題量身設計

## Building Block 7：Feedback（人工回饋）

- 部分任務目前還無法完全自動化，需要 human-in-the-loop
- 實作方式：在 agent 執行流程中設置暫停點，等待人工核准（例如 Slack 通知 + 核准按鈕）
- 區別：
  - **AI Assistant**（如 ChatGPT、Cursor）：使用者即時參與、即時回饋
  - **Autonomous System**（如自動客服票務）：背景運行，無人參與

## 整合建議

1. 拆解大問題為小問題
2. 每個子問題盡量用 deterministic 程式碼解決
3. 只有當 deterministic 程式碼無法解決時，才引入 LLM API 呼叫
4. 配合 Pydantic 做 structured output，確保資料可預測
