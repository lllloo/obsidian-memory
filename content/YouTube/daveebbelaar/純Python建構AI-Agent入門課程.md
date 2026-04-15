---
title: 用純 Python 建構 AI Agent：入門完整課程
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 
source: https://www.youtube.com/watch?v=bZzyPscbtI8
---

## 核心理念

- 不需要任何 Framework，直接用 Python + LLM API 就能建構 AI 系統
- 基於 Anthropic 的《Building Effective Agents》blog post
- 先理解原理，再看 Framework

## 增強型 LLM 三大基礎

1. **Retrieval**：用向量搜尋從外部知識庫取得相關內容
2. **Tools**：讓 LLM 決定是否呼叫外部 API（LLM 只提供參數，你自己呼叫函式）
3. **Memory**：維護對話歷史的訊息清單

## 基本 API 呼叫

```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a limerick about Python."}
    ]
)
print(response.choices[0].message.content)
```

## Structured Output（結構化輸出）

```python
from pydantic import BaseModel

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Alice and Bob are going to Science Fair on Friday."}],
    response_format=CalendarEvent
)
event = completion.choices[0].message.parsed
```

## Tool Use（工具呼叫）

重要觀念：**LLM 只決定呼叫哪個工具並提供參數，實際執行由你的程式完成**。

```python
# 定義工具
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"]
        }
    }
}]

# 第一次 API 呼叫：LLM 決定要呼叫哪個工具
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)
# finish_reason == "tool_calls" 時，解析參數並自行呼叫函式

# 第二次 API 呼叫：把工具結果加入 context，取得最終回應
```

## 四種 Workflow 模式

### Prompt Chaining（提示鏈）

將任務拆成多個步驟，每步驟都有獨立的 Pydantic 模型和 system prompt：

```python
# 以日曆代理為例
def process_calendar_request(user_input: str):
    # Step 1: 判斷是否為日曆事件
    extraction = extract_event_info(user_input)
    
    # Gate：信心分數不足則停止
    if not extraction.is_calendar_event or extraction.confidence < 0.7:
        return None  # 停止流程
    
    # Step 2: 提取事件細節
    details = parse_event_details(user_input)
    
    # Step 3: 生成確認訊息
    confirmation = generate_confirmation(details)
    return confirmation
```

### Routing（路由）

LLM 先分類輸入，再用 if/else 走不同路徑：

```python
route = classify_request(user_input)  # 返回 "new_event" / "modify_event" / "other"
if route.type == "new_event":
    handle_new_event(user_input)
elif route.type == "modify_event":
    handle_modify_event(user_input)
```

### Parallelization（平行化）

多個 LLM 呼叫同時執行（適合 Guard Rail）：

```python
import asyncio

async def check_with_guardrails(request: str):
    calendar_check, security_check = await asyncio.gather(
        check_if_calendar_event(request),
        check_security(request)
    )
    return calendar_check, security_check
```

### Orchestrator-Worker

Orchestrator 決定步驟，Worker 執行 — 比純 Workflow 更靈活但仍可控。

## 關鍵技巧

- **當日期注入 context**：`f"Today is {datetime.now().strftime('%Y-%m-%d')}"`，讓 LLM 能理解「下週五」
- **Gate（閘門）**：每個 step 加信心分數，低於閾值則提前終止
- **純 if/else 就是 Router**：不需要特殊 Framework
- **在 Cursor 中用互動式 Python session** 逐步測試每個步驟

## 建議學習順序

1. 先理解這個影片的基礎原理
2. 再看 17 個 AI 工程師必備 Python 函式庫（頻道另一支影片）
3. 最後才考慮使用 Production Framework
