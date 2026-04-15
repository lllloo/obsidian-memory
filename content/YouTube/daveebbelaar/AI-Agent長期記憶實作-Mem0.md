---
title: 如何用 Python 建構自我學習的 AI Agent（Mem0 長期記憶實作）
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-05-08
source: https://www.youtube.com/watch?v=ynhl8KjjS3Y
---

## Mem0 框架概覽

- Mem0 是開源記憶框架，讓 AI agent 能記住對話中的重要事實
- 支援雲端版（app.mem0.ai）與本地開源版，介面一致
- 相較於 ChatGPT 的記憶功能，Mem0 宣稱更低延遲、更省 token

## 兩階段記憶 Pipeline

Mem0 採用兩階段流程，而非直接把所有對話塞進向量資料庫：

1. **摘要萃取**：將對話歷史用 LLM 產生摘要，再從中萃取關鍵事實
2. **動態決策**：另一個 LLM 決定要 add / update / delete 哪些記憶

這讓記憶系統可以隨時間修正，例如「我不喜歡披薩了，改喜歡義大利麵」→ 自動更新偏好記錄。

Mem0 開放的核心 prompt 可在 GitHub 找到：
- `memory_answer_prompt`
- `fact_retrieval_prompt`
- `update_memory_prompt`（支援 add / update / delete / none 四種操作）

## 使用方式

### 雲端版

```python
from mem0 import MemoryClient

client = MemoryClient(api_key="YOUR_MEM0_API_KEY")
messages = [{"role": "user", "content": "My name is Dave"}]
client.add(messages, user_id="dave")
results = client.search("What shall we build today?", user_id="dave")
```

### 開源版（本地）

```python
from mem0 import Memory

memory = Memory()
memory.add(messages, user_id="dave")
memories = memory.get_all(user_id="dave")
related = memory.search("What is my name?", user_id="dave")
```

### 搭配 Qdrant 向量資料庫持久化

用 Docker 啟動 Qdrant：
```bash
docker compose up -d
```

設定 config 指定向量資料庫：
```python
config = {
    "vector_store": {"provider": "qdrant", "config": {"host": "localhost", "port": 6333}},
    "llm": {"provider": "openai", "config": {"model": "gpt-4o-mini"}},
}
memory = Memory.from_config(config)
```

## 整合進 AI 對話系統

基本模式：每輪對話前先 `memory.search()` 取出相關記憶注入 context，對話後再 `memory.add()` 更新記憶：

```python
while True:
    query = input("You: ")
    memories = memory.search(query, user_id=user_id, limit=3)
    # 將 memories 注入 system prompt
    response = openai_client.chat(...)
    memory.add([{"role": "user", "content": query}, {"role": "assistant", "content": response}], user_id=user_id)
```

## 注意事項與建議

- 記憶萃取不是完美的，LLM 決策有時會出錯（如衝突事實未即時覆蓋）
- 可透過 config 覆寫 `custom_fact_extraction_prompt` 和 `custom_update_memory_prompt` 調整行為
- 作者建議：了解 Mem0 的底層實作後，考慮只取用需要的部分自行實作，避免多層抽象造成後續維護困難
- Mem0 支援多種 LLM 與向量資料庫，但抽象層越多，越難存取底層 API 的進階功能
