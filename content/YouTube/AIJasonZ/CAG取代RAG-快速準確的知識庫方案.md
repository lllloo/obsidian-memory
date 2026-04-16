---
title: CAG 取代 RAG：快速準確的知識庫方案
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-03-26
source: https://www.youtube.com/watch?v=KHDMoQ2Sp2s
parent: "[[01.index]]"
---

## RAG vs CAG 比較

| 面向 | RAG | CAG |
|------|-----|-----|
| 全稱 | Retrieval Augmented Generation | Cache Augmented Generation |
| 做法 | 建立向量資料庫，依查詢取回相關 chunk | 直接將整份文件塞進 context window |
| 準確性問題 | chunk 可能切斷程式碼範例、需要 metadata filtering、query transformation | 完整文件在 context 中，不會遺漏 |
| 實作複雜度 | 需建立 embedding pipeline、向量搜尋、reranking | 極簡，10 行程式碼即可 |
| 成本 | 相對固定 | 取決於 context 大小，Gemini Flash 幾乎可忽略 |

## 為什麼現在 CAG 可行

Context window 成長幅度：
- 24 個月前：4,000 tokens
- 現在主流 flagship：100,000~200,000 tokens
- Gemini：最高 2,000,000 tokens（約 150 萬字，超過《戰爭與和平》）

Gemini 2.0 Flash 成本：$0.10 / 1M input tokens（比 GPT-4o 便宜 96%）

實測：將 Firecrawl 完整 API 文件（27 頁）餵給 Gemini 2.0 Flash，費用 $0.006，3.4 秒內完成。

## Chat with PDF（10 行程式碼）

```python
import google.generativeai as genai

client = genai.GenerativeModel('gemini-2.0-flash')
response = client.generate_content([
    {'inline_data': {'mime_type': 'application/pdf', 'data': pdf_bytes}},
    'Your question here'
])
```

## 建立外部文件 MCP（實際範例）

目標：讓 Cursor / Windsurf 自動取得外部 API 文件中最相關的程式碼範例。

**流程：**
1. 用 Firecrawl 的 `map_url` 取得文件站所有子頁面（例：153 頁）
2. 用 Gemini 篩選出相關頁面（例：縮減到 27 頁）
3. 用 Firecrawl `batch_scrape` 批量抓取 Markdown
4. 將所有 Markdown 餵給 Gemini，附上使用者問題
5. 本地快取已抓取的文件，避免重複請求

```python
# 篩選相關 URL
relevant_pages = gemini.filter_relevant_pages(all_urls, query)

# 批量抓取
docs = firecrawl.batch_scrape_urls(relevant_pages)

# CAG 查詢
answer = gemini.generate_content([*docs, user_query])
```

## 何時還是用 RAG

- 資料庫極大（遠超 context window）
- 資料多樣且持續增長（企業財務報告跨多年）

**混合方案（超大資料集）：**
1. 傳統搜尋（metadata、檔名）找出最可能包含答案的子集
2. 只將這個子集餵給 LLM
3. 甚至可以並行 LLM calls，最後再 summarize

## Gemini 2.0 的其他優勢

- **Context caching**：相同大 context 可以 cache，後續請求更快更便宜（目前不支援 Gemini 2.0，等後續版本）
- **幻覺率**：在 Vectara 測試中，Gemini 2.0 達到極低幻覺率
- **Needle-in-a-haystack**：1M token 中精準找到特定資訊，nearly perfect recall
