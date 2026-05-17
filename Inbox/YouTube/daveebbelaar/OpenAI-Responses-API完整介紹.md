---
title: OpenAI 剛改變了一切：Responses API 完整介紹
created: 2026-04-15
updated: 2026-04-15
source: https://www.youtube.com/watch?v=0pGxoubWI6s
published: 2025-03-13
parent: "[[01.index]]"
tags:
  - youtube
---

## 開發者必知的 7 個重點

1. **向下相容**：Responses API 是 Chat Completions API 的超集，現有功能全部保留
2. **遷移時間軸**：**Assistants API** 將於 2026 年 8 月下線（非 Chat Completions API，後者無下線計畫）；新專案建議直接使用 Responses API
3. **新功能**：Web 搜尋、File 搜尋、簡化介面、新 developer role、Reasoning 參數控制
4. **本質不變**：沒有帶來 LLM 新能力，只是讓原本需要多步驟的操作用單一 API 呼叫完成
5. **API 結構改變**：`client.responses.create()` 取代 `client.chat.completions.create()`
6. **新 Agent SDK**：取代 Swarm，`pip install openai-agents`，本影片不涵蓋
7. **警告**：API 抽象越多，除錯越難，需謹慎使用內建功能

## API 介面變化

### 簡化輸入格式

```python
# 舊：Chat Completions
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a bad story"}]
)
text = response.choices[0].message.content

# 新：Responses API
response = client.responses.create(
    model="gpt-4o",
    input="Write a bad story"
)
text = response.output_text
```

`input` 同時支援單一字串或舊式 messages 清單格式。

## Developer Role 與訊息層級

新增 `developer` role，並有明確的優先順序（高→低）：
1. `platform`（OpenAI 內部使用）
2. `system`
3. `developer`
4. `user`

實作方式：
```python
response = client.responses.create(
    model="gpt-4o",
    instructions="Talk like a pirate",  # developer role 的簡化語法
    input="What about semicolons in JavaScript?"
)
```

## Conversation State 管理

新方式：用 `previous_response_id` 串接對話，無需手動帶入完整歷史：

```python
r1 = client.responses.create(model="gpt-4o-mini", input="Tell me a joke")
r2 = client.responses.create(
    model="gpt-4o-mini",
    input="Explain why this is funny",
    previous_response_id=r1.id  # 自動取得前次對話 context
)
```

注意：`store=True` 是預設值，對話會儲存在 OpenAI 平台；設 `store=False` 可關閉。

## Function Calling

與 Chat Completions API 相同，只換了 API 路徑：

```python
response = client.responses.create(
    model="gpt-4o",
    input="Send an email to Elon and Kya",
    tools=[send_email_tool_definition]
)
```

## Structured Output

兩種方式皆可用：

```python
# 方式一：JSON Schema
response = client.responses.create(
    model="gpt-4o",
    input="...",
    text={"format": {"type": "json_schema", "schema": {...}}}
)

# 方式二：Pydantic model（非官方文件，但可用）
response = client.responses.parse(
    model="gpt-4o",
    input="...",
    instructions="...",
    text_format=CalendarEvent  # Pydantic model
)
event = response.output_parsed
```

## Web Search

```python
response = client.responses.create(
    model="gpt-4o",
    input="Best restaurants near Dam Square Amsterdam",
    tools=[{"type": "web_search_preview"}]
)
# response 包含 annotations（含來源 URL）
```

可搭配 `user_location` 參數提升搜尋精準度。

## File Search（RAG）

```python
# 1. 上傳檔案
file = client.files.create(file=open("doc.pdf", "rb"), purpose="assistants")

# 2. 建立 vector store
vs = client.vector_stores.create(name="knowledge_base")
client.vector_stores.files.create(vector_store_id=vs.id, file_id=file.id)

# 3. 查詢
response = client.responses.create(
    model="gpt-4o",
    input="What is deep research?",
    tools=[{"type": "file_search", "vector_store_ids": [vs.id]}],
    include=["file_search_results"]
)
```

注意事項：
- 費用：vector store 開啟期間每日計費，實驗後記得刪除
- 缺乏細粒度控制（chunking 策略、embedding 模型不可自訂）
- 可設 `max_num_results` 限制取回的 chunk 數

## Reasoning 模型參數

```python
response = client.responses.create(
    model="o3-mini",
    input="Complex problem...",
    reasoning={"effort": "high"}  # low / medium / high
)
```

## 作者建議

不要把所有邏輯都外包給 OpenAI API——抽象越多，除錯越難。真正的 AI 工程在於控制正確的 context 在正確的時間送入模型。
