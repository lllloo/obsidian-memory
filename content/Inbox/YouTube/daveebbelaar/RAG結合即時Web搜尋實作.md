---
title: 如何將 RAG 與即時 Web 搜尋結合（單頁、搜尋、允許網域）
tags:
  - youtube
  - rag
  - ai-agent
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-13
source: https://www.youtube.com/watch?v=jqd6_bbjhS8
parent: "[[01.index]]"
---

## 使用情境

客戶常見需求：內部 agent 有 RAG pipeline 存取內部知識庫，同時能在需要時上網補充資訊（通常作為 fallback 機制）。

最終架構：agent 收到使用者查詢後，自行決定使用哪些資料來源：
1. 內部手冊（RAG / 直接載入文件）
2. 指定 URL 的單一頁面
3. 廣泛網路搜尋（可限制允許的網域）

最終回傳：**結構化答案 + 引用來源清單**。

## 模組一：抓取單一網頁

使用 `docling` 將網頁 HTML 轉成 Markdown，再送給 LLM：

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert(url)
markdown = result.document.export_to_markdown()
```

適合場景：使用者提供特定 URL，需要 AI 摘要或回答該頁面內容的問題。

## 模組二：廣泛網路搜尋（含網域過濾）

使用 OpenAI 內建 `web_search` 工具（Responses API）：

```python
from openai import OpenAI
from pydantic import BaseModel

class Citation(BaseModel):
    text: str
    url: str

class SearchResult(BaseModel):
    answer: str
    citations: list[Citation]

client = OpenAI()
response = client.responses.create(
    model="gpt-4.1-nano",  # 或 gpt-5-mini-nano（推理模型）
    tools=[{
        "type": "web_search_preview",
        "search_context_size": "medium",
        # 限制允許的網域（可選）
        "allowed_domains": ["example.gov", "policy.nl"]
    }],
    tool_choice="auto",
    input=[{"role": "user", "content": query}],
    text={"format": {"type": "json_schema", "schema": SearchResult.model_json_schema()}}
)
```

注意事項：
- 推理模型（GPT-5、mini、nano）結果品質更好，但速度較慢
- 若延遲是關鍵，改用非推理模型
- `allowed_domains` 支援子網域，可精確控制搜尋範圍
- 結果包含 `citations`（文字 + URL），方便前端顯示來源

## 模組三：內部知識庫（Handbook）

範例：載入 Markdown 格式的內部手冊作為工具：

```python
def search_handbook(query: str) -> str:
    with open("handbook.md") as f:
        return f.read()  # 文件夠短時直接整份塞入

# 工具定義
handbook_tool = {
    "type": "function",
    "function": {
        "name": "search_handbook",
        "description": "Search the internal company handbook for policies and procedures",
        "parameters": {"type": "object", "properties": {}}
    }
}
```

說明：
- 文件夠短時直接整份塞入 context（不需 RAG）
- 文件量大時需建立完整 RAG pipeline（chunk → embed → retrieve）
- Agent 只在認為需要時才呼叫此工具（不是每次都查）

## 整合：Dynamic Search Agent

將三個模組整理到 `tools/` 資料夾，在主 agent 中匯入：

```
project/
├── tools/
│   ├── web_page.py       # get_web_page()
│   ├── web_search.py     # search_web()
│   └── handbook.py       # search_handbook()
└── search_agent.py       # 整合 agent
```

```python
# search_agent.py
from tools.web_page import get_web_page_tool
from tools.web_search import web_search_tool
from tools.handbook import handbook_tool

tools = [get_web_page_tool, web_search_tool, handbook_tool]

def ask_agent(query: str, message_history: list) -> SearchResult:
    response = client.responses.create(
        model="gpt-4.1",
        tools=tools,
        tool_choice="auto",
        input=message_history + [{"role": "user", "content": query}],
        text={"format": SearchResult.schema()}
    )
    # 處理工具呼叫 → 執行 → 再次呼叫直到得到最終答案
    while response has tool_calls:
        execute_tools(response.tool_calls)
        # 將工具輸出加入 message_history，繼續推理
    return SearchResult.parse(response)
```

Agent 行為範例：
- 「你能做什麼？」→ 直接回答（不呼叫工具）
- 「AI 系統註冊要求？」→ 呼叫 handbook 工具
- 「請分析 https://example.com」→ 呼叫 get_web_page 工具
- 「政府最新 AI 政策？」→ 呼叫 web_search 工具（限定網域）
- 「根據手冊和官網，哪裡合規？」→ 同時呼叫 handbook + web_search

## 互動式 Agent（保留對話歷史）

```python
# interactive_agent.py
message_history = []

while True:
    user_input = input("You: ")
    message_history.append({"role": "user", "content": user_input})
    result = ask_agent(user_input, message_history)
    message_history.append({"role": "assistant", "content": result.answer})
    print(f"Agent: {result.answer}")
```

## 關鍵設計原則

- 用 Pydantic 定義結構化輸出，確保回傳格式一致（answer + citations）
- 工具抽象到 `tools/` 資料夾，讓 agent 主邏輯保持簡潔
- 允許網域過濾（`allowed_domains`）讓搜尋有目的性，避免 agent 亂爬
- 現代模型可同時使用 15-20 個工具，但最佳實踐仍是工具數量適中、職責清晰
