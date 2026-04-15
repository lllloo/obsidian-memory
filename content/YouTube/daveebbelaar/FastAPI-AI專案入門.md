---
title: FastAPI 入門：為 AI 專案建立後端
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-05-22
source: https://www.youtube.com/watch?v=-IaCV5-mlSk
---

本影片介紹如何用 FastAPI 把本地 AI demo 轉成可對外服務的後端 API。Dave 展示了他在 Data Lumina 實際用於客戶專案的模組化結構，強調 FastAPI 原生整合 Pydantic 的優勢。

## FastAPI 的定位與優勢

- 作為「整合層」：讓外部應用程式、webhook 等能夠呼叫你的 AI 邏輯
- 相較於 Flask：更簡潔、更快速，且原生整合 Pydantic
- 配合 Pydantic 做資料驗證，確保進入 AI 系統的資料格式正確

## 啟動方式

```bash
uvicorn main:app --reload
```

- `uvicorn`：ASGI server，負責處理 HTTP 連線
- `main`：指向 `main.py` 檔案
- `app`：該檔案中的 FastAPI 實例變數
- `--reload`：開發時自動重新載入

## 模組化架構（三層結構）

Dave 將應用拆分為三個檔案，以模擬生產環境的結構：

**main.py（入口點）**
- 建立 FastAPI app 實例
- 引入 router，保持此檔案精簡

**router.py（路由層）**
- 建立 `APIRouter` 實例
- 設定路由前綴（prefix），例如 `/events`
- 將請求路由到對應的 endpoint handler

**endpoint.py（業務邏輯層）**
- 定義 Pydantic 資料模型（即 request schema）
- 實作 endpoint 函式，這裡放 AI 處理邏輯的入口

## Pydantic 資料驗證整合

```python
from pydantic import BaseModel
from typing import dict

class EventSchema(BaseModel):
    event_id: str
    event_type: str
    data: dict  # 若傳入非 dict，自動回傳 422 錯誤
```

- 資料不符合 schema 時，FastAPI 自動回傳 `422 Unprocessable Entity`
- 錯誤訊息詳細說明哪個欄位不符合（如「input should be a valid dictionary」）

## 回應格式

```python
from starlette.responses import Response

async def handle_event(data: EventSchema):
    # 在這裡接入 AI 處理邏輯
    print(data)
    return Response(status_code=202, content="Data received")
```

## 同步 vs 非同步 Endpoint

```python
# 同步（預設）
def handle_event(data: EventSchema):
    ...

# 非同步（提升可擴展性）
async def handle_event(data: EventSchema):
    result = await process_ai_logic(data)
    ...
```

## 自動文件

- 啟動後訪問 `http://localhost:8000/docs`
- FastAPI 自動根據 endpoint 定義生成互動式 API 文件

## 安全性（Bearer Token）

生產環境應加入 API token 驗證，Dave 提供了一個練習範例供自行實作。

## 搭配 Celery 處理長時任務

當 AI pipeline 需要多個 LLM 呼叫（可能耗時數秒至數分鐘）時：
- Endpoint 快速儲存資料到資料庫，立即回應 202
- 將任務送入 Celery task queue
- Worker 非同步執行 AI 邏輯，保持 endpoint 不阻塞
