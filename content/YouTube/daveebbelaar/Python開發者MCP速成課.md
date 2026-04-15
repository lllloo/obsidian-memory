---
title: MCP 速成課：Python 開發者完整指南
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-04-19
source: https://www.youtube.com/watch?v=5xqFjh56AwM
---

## MCP 是什麼

MCP（Model Context Protocol）由 Anthropic 於 2024 年 11 月發布，是連接 AI 助理與外部系統的標準化協議。

- **本質**：不引入新功能，而是統一 LLM 工具整合的介面標準
- **舊做法**：開發者各自為 Slack、GitHub、Google Drive 等服務寫 function calling 整合
- **新做法**：透過 MCP 統一定義 schema、文件與參數，讓 AI 應用無縫整合

2025 年 3 月爆紅原因：OpenAI 在其 Agent SDK 支援 MCP，確立業界標準地位。

## 核心架構術語

| 元件 | 說明 |
|------|------|
| Host | 存取 MCP 的程式（如 Claude Desktop、自製 Python backend） |
| MCP Client | 維護與 Server 一對一連線的 protocol client |
| MCP Server | 輕量程式，暴露 tools、resources、prompts |

Server 可連接本地資料來源或遠端服務（透過 HTTP API）。

## 兩種 Transport 機制

**Standard IO（標準輸入輸出）**：
- 所有元件在同一台機器上執行
- 適合個人 AI 助理情境（Claude Desktop、Cursor 等）
- 對自製 Python backend 而言：只是複雜化工具定義，實用性有限

**Server-Sent Events（HTTP SSE）**：
- Server 部署在遠端機器，透過 HTTP 連線
- 可讓多個 client 應用共用同一個 Server
- **作者認為這才是 MCP 對開發者最有價值的使用情境**

## 建立 MCP Server（Python SDK）

安裝：
```bash
pip install mcp[cli]
# 或使用 uv（推薦）
```

最簡單的 server（類似 FastAPI 語法）：
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server", host="0.0.0.0", port=8000)

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

if __name__ == "__main__":
    mcp.run(transport="sse")  # HTTP 模式
    # mcp.run()               # stdio 模式
```

## MCP Server vs Function Calling 比較

| | Function Calling | MCP |
|--|--|--|
| 定義位置 | 直接在 Python 程式內 | 獨立 Server |
| 共用性 | 僅限當前專案 | 多個 client 可共用 |
| 適合情境 | 簡單工具、單一應用 | 跨應用共享工具 |

作者建議：若工具不多且只用於單一應用，直接用 function calling 更簡單。

## 在 Python 應用中連線 MCP Server

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client

# HTTP 連線
async with sse_client("http://localhost:8000/sse") as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()
        result = await session.call_tool("add_numbers", {"a": 1, "b": 2})
```

## Docker 部署

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server.py"]
```

```yaml
# docker-compose.yml
services:
  mcp-server:
    build: .
    ports:
      - "8000:8000"
```

## Lifecycle 管理

使用 lifespan context manager 管理資源初始化與清理：

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # 初始化（如建立 DB 連線）
    db = await create_db_connection()
    yield {"db": db}
    # 清理
    await db.close()

mcp = FastMCP("my-server", lifespan=lifespan)
```

## 重點整理

- MCP Server 可暴露 **tools**（函式）、**resources**（資料）、**prompts**（提示模板）
- 開發起步：`pip install mcp[cli]`，參考官方 Python SDK 文件
- 作者建議優先考慮 HTTP transport + Docker 部署，而非 stdio
