---
title: AI 工程師必備的 17 個 Python 函式庫
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2024-12-12
source: https://www.youtube.com/watch?v=p4G0coRey9w
---

Dave 整理了在 Data Lumina 實際用於客戶專案的 17 個 Python 函式庫，涵蓋專案設定、後端、資料管理、AI 整合、向量資料庫、可觀測性，以及三個進階工具。

## 專案設定

**Pydantic**
- 最廣泛使用的 Python 資料驗證函式庫
- AI 系統中資料往往雜亂不可靠，Pydantic 讓你可以結構化並驗證資料流

**Pydantic Settings**
- 獨立套件（`pip install pydantic-settings`），使用 `BaseSettings` 代替 `BaseModel`
- 用於集中管理設定（如 LLM config、API keys）
- 啟動時若必要設定缺失，自動拋出驗證錯誤

**python-dotenv**
- 將 `.env` 檔案中的 API keys 和 secrets 載入環境變數
- 與 Pydantic Settings 搭配使用：載入環境變數 + 同步驗證

## 後端

**FastAPI**
- 連結前端/用戶輸入與後端 AI 邏輯的整合層
- 原生整合 Pydantic，確保進入 AI 系統的資料已驗證
- 相較 Flask：更簡潔、更快、Pydantic 整合更深

**Celery**
- 分散式任務佇列，用於跨執行緒或跨機器分配工作
- 當 AI pipeline（多個 LLM 呼叫）耗時過長時，Celery 確保 endpoint 不阻塞
- 模式：endpoint 快速儲存資料 + 交由 Celery 非同步處理

## 資料管理

**PostgreSQL 相關：psycopg2 / PyMongo**
- Dave 偏好 PostgreSQL（SQL 方案）
- `psycopg2`：PostgreSQL Python driver
- `PyMongo`：MongoDB Python driver（NoSQL 替代方案）

**SQLAlchemy**
- 用純 Python 操作 SQL 資料庫（定義模型、CRUD 操作）
- 專案的 Python ORM 首選

**Alembic**
- 配合 SQLAlchemy 管理資料庫 migration
- 直接從程式碼定義 schema 變更（加欄位、刪欄位），無需手寫 SQL

**Pandas**
- Dave 的最常用函式庫（來自資料科學背景）
- 用途：建立評估資料集、結構化非結構化資料、以 rows/columns 形式檢視資料

## AI 整合

**LLM 模型供應商 SDK**
- OpenAI、Anthropic、Google（Gemini）
- 建議：深入閱讀 API 文件，探索 function calling、structured output、vision、image generation 等進階功能
- Ollama：統一介面，用於執行和實驗開源模型

**Instructor**
- Dave 目前最愛的 structured output 函式庫
- 優勢：更複雜的資料驗證機制、model agnostic（可輕鬆換模型）
- 建立在 Pydantic 之上，指定 response model 後確保 LLM 回傳符合 schema 的資料

**LangChain / LlamaIndex**
- 爭議性工具：Dave 個人不在生產系統中使用，但建議 AI 工程師要熟悉
- 它們涵蓋大量核心概念（embeddings、vector DB、RAG、prompt management），學習價值高
- 觀察：目前沒有客戶在生產系統中使用這些框架

## 向量資料庫

- **Pinecone**：熱門雲端向量資料庫
- **Weaviate**
- **Qdrant**
- **pgvector / pgvectorscale**（Dave 使用）：PostgreSQL 擴充套件，直接在 Postgres 中儲存向量 embedding 並做相似度搜尋，簡化架構（一個資料庫搞定）

## 可觀測性與監控

- **Langfuse**（Dave 使用）：開源，可自架，追蹤所有 LLM 呼叫的 prompt、output、latency、cost
- **LangSmith**：另一個常見選項
- 重要性：生產環境必備，用於 debug 和效能監控

## 進階工具

**DSPy**
- 「programming not prompting」的新範式
- 從基礎 prompt 出發，讓 AI 自動找出最佳 prompt
- 適合已有完整專案後，要優化 prompt 效能時使用

**PyMuPDF / PyPDF2**
- 從 PDF/Word 文件提取文字
- 適合公司有大量非結構化文件需要餵給 AI 系統的場景
- 複雜文件可考慮 Amazon Textract 或 Azure Document Intelligence

**Jinja2**
- Python 模板引擎，用於程式化填充模板
- AI 工程師用途：建立動態 prompt template，將 prompt 版本化儲存並用 prompt manager 載入
