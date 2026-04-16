---
title: 如何為 AI Agent 準備資料：開源文件提取 Pipeline
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-02-13
source: https://www.youtube.com/watch?v=9lBTS5dM27c
parent: "[[01.index]]"
---

## 核心概念

為 AI Agent 建立知識系統的完整 Pipeline：**提取 → 分塊 → 嵌入 → 檢索 → 應用**

使用的核心函式庫：**Docling**（IBM 開源，目前最推薦的文件提取方案）

## 提取（Extraction）

Docling 可以將各種格式（PDF、DOCX、PowerPoint、網頁）統一轉換成 `DoclingDocument` 物件：

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()

# 轉換 PDF
result = converter.convert("path/to/document.pdf")
doc = result.document

# 轉換單一網頁
result = converter.convert("https://example.com/page")

# 轉換整個網站（透過 sitemap.xml）
from docling.utils import get_sitemap_urls
urls = get_sitemap_urls("https://example.com")
results = converter.convert_all(urls)
docs = [r.document for r in results]

# 匯出為 Markdown
print(doc.export_to_markdown())
```

Docling 特別擅長 **表格提取**，能完整還原 Markdown 格式的表格，這是許多其他 PDF 解析庫的弱項。

## 分塊（Chunking）

Docling 提供 HybridChunker，同時處理兩個問題：
1. **階層式分塊**：依段落、列表等邏輯結構切割
2. **Token 限制**：確保每個 chunk 不超過 embedding 模型的 max input

```python
from docling.chunking import HybridChunker

chunker = HybridChunker(
    tokenizer=OpenAITokenizerWrapper(),  # 自訂 tokenizer 包裝器
    max_tokens=8191,  # text-embedding-3-large 的上限
    merge_peers=True  # 合併太小的 chunk
)

chunks = list(chunker.chunk(doc))
# 結果：適合 embedding 模型的 chunk 列表
```

注意：使用 Pydantic sub-model 時，欄位需依字母順序排列，否則會有 bug。

## 嵌入與向量資料庫（Embedding + Vector DB）

以 LanceDB 為例（SQLite-like，文件儲存在本地）：

```python
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

db = lancedb.connect("./data/lancedb")

# 定義嵌入函數（自動處理 embedding）
embed_fn = get_registry().get("openai").create(
    name="text-embedding-3-large"
)

class ChunkSchema(LanceModel):
    text: str = embed_fn.SourceField()
    vector: Vector(3072) = embed_fn.VectorField()
    metadata: dict

# 建立表格
table = db.create_table("docling", schema=ChunkSchema, mode="overwrite")

# 寫入 chunks（自動產生 embedding）
table.add([
    {"text": chunk.text, "metadata": {...}}
    for chunk in chunks
])
```

可用的向量資料庫：LanceDB、Qdrant、PostgreSQL + pgvector 等。

## 檢索（Retrieval）

```python
# 語義搜尋
results = table.search(query="What is Docling?") \
    .metric("vector") \
    .limit(5) \
    .to_pandas()
```

## 完整應用（Chat App）

用 Streamlit 建立文件問答介面：

```bash
streamlit run 05-chat.py
```

流程：
1. 接收用戶問題
2. 向量搜尋取得相關 chunks（附帶檔名、頁碼等 metadata）
3. 將 chunks 注入 LLM context
4. 回傳含來源引用的答案

## 選擇向量資料庫的建議

作者常用：**PostgreSQL + pgvector**（生產環境）、LanceDB（範例/快速開發）
