---
title: 用 PydanticAI 建構 AI Agent：入門教學
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2024-12-05
source: https://www.youtube.com/watch?v=zcYtSckecD8
---

PydanticAI 是 Pydantic 團隊推出的 AI Agent 框架，將 Pydantic 的資料驗證哲學帶入 Agent 開發。Dave 走過 5 個實作範例，並在最後給出框架評估。

## PydanticAI 的核心特點

- **出自 Pydantic 團隊**：其他框架（LangChain、LlamaIndex、Instructor）幾乎都在底層使用 Pydantic
- **Model agnostic**：支援多家 LLM 供應商，可自由切換
- **Type safety**：以純 Python 做 control flow 和 agent composition
- **Structured responses**：內建 streaming 支援
- **Dependency injection**：類型安全的依賴注入系統（最值得關注的特性）
- **Logfire 整合**：可觀測性工具（類似 LangSmith / Langfuse）

## 基本 Agent 設定

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel("gpt-4o")

agent = Agent(
    model=model,
    system_prompt="You are a helpful customer support agent."
)
```

三種執行方式：
- `agent.run()`：async
- `agent.run_sync()`：同步
- `agent.run_stream()`：串流回應

result 物件包含：data（回應內容）、messages（完整對話歷史）、usage（token 用量與費用）

## 範例 1：結構化輸出

```python
class ResponseModel(BaseModel):
    response: str
    needs_escalation: bool
    follow_up_required: bool
    sentiment: str

agent = Agent(
    model=model,
    system_prompt="...",
    result_type=ResponseModel,  # 指定 result type
)
```

與 Instructor library 或 OpenAI structured output 的用法類似。

## 範例 2：Dependency Injection（最值得關注）

依賴注入讓你在 runtime 動態注入驗證過的資料，作為 LLM 的 context：

```python
class CustomerDetails(BaseModel):
    id: str
    name: str
    email: str
    orders: list[Order]

agent = Agent(
    model=model,
    deps_type=CustomerDetails,  # 宣告依賴類型
    result_type=ResponseModel,
)

@agent.system_prompt
async def add_customer_context(ctx: RunContext[CustomerDetails]) -> str:
    return f"Customer details:\n{pydantic_to_markdown(ctx.deps)}"
```

執行時傳入依賴：
```python
result = agent.run_sync(user_prompt, deps=customer_details)
```

若依賴資料格式不符合 Pydantic schema（如 `customer_id` 傳入 int 而非 str），會立即拋出 validation error，系統不執行。

## 範例 3：Tools（工具）

兩種工具類型：
- `@agent.tool`：工具需要 agent context（RunContext）
- `@agent.tool_plain`：工具不需要 context

兩種注冊方式：
```python
# 方式 1：在 Agent 初始化時傳入
agent = Agent(model=model, tools=[get_shipping_info])

# 方式 2：使用 decorator
@agent.tool
async def get_shipping_info(ctx: RunContext[CustomerDetails]) -> str:
    order_id = ctx.deps.orders[0].order_id
    return shipping_db.get(order_id, "Not found")
```

## 範例 4：Self-Correction with ModelRetry

```python
from pydantic_ai import ModelRetry

@agent.tool_plain
async def get_shipping_status(order_id: str) -> str:
    result = shipping_db.get(order_id)
    if result is None:
        raise ModelRetry(
            "No info found. Order ID must start with '#'. "
            "Please retry with the correct format."
        )
    return result
```

- 工具遇到錯誤時拋出 `ModelRetry`，帶入具體修正指示
- LLM 收到後自我修正，重新呼叫工具（最多重試 `retries` 次）
- 可在 Agent 層級、tool 層級或 result validator 層級設定

## Dave 的評估

**喜歡的地方：**
- 把 Pydantic 的驗證哲學帶入 agent 開發，對生產系統非常重要
- 低層次抽象，對底層運作仍有清晰掌握
- Dependency injection 設計優雅

**擔心的地方（撰文時）：**
- 仍是早期 beta，API 可能改變
- 無法輕鬆調整 temperature 等模型參數
- 使用 message history + tools 時出現錯誤

**建議：**
- 實驗看看，從中學習有用的概念（特別是 dependency injection 模式）
- 不要過度依賴任何特定框架
- Dave 當前策略：繼續用 Instructor 取得 structured output，並採用類似的 dependency injection 概念自行實作
