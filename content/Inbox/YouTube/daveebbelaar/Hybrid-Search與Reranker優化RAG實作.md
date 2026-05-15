---
title: Hybrid Search 與 Reranker 優化 RAG 實作（BM25 + Embeddings + Reranker）
created: 2026-05-15
updated: 2026-05-15
source: https://www.youtube.com/watch?v=XvKiTfd6Xvo
published: 2026-05-14
parent: "[[01.index]]"
tags:
  - youtube
  - rag
  - hybrid-search
  - bm25
  - embeddings
  - reranker
---

## 影片定位

從零打造一條 production-ready 的 hybrid retrieval pipeline：BM25（sparse / 關鍵字）＋ dense embeddings（語意）→ Reciprocal Rank Fusion（RRF）合併 → cross-encoder reranker 重排，並用 NDCG 評估每一次改動。目標讀者是已懂 RAG 基本概念、要把 retrieval 推到 production 的工程師。

作者明確反對「丟給 Claude Code one-shot 出一套 RAG」的作法，主張理解每一塊機制才能針對自家資料調優。

## 為什麼需要 Hybrid

單一檢索方式都有死角，組合才能互補：

- **BM25（sparse / keyword）**：擅長精確詞、識別碼、罕見詞；遇到 paraphrase 就失效
- **Dense embeddings**：抓 paraphrase、語意相近；對精確詞與識別碼反而較弱
- 兩者「贏在對方輸的地方」，自然適合 fusion

整條 pipeline 的順序：

```
Query → [BM25 top-K] + [Dense top-K]
      → Reciprocal Rank Fusion 合併
      → Cross-encoder reranker 重排
      → 最終 top-N
```

## 資料集與 Ground Truth

用 BEIR benchmark 中的 **Finance QA** 資料集，三張 parquet：

- `corpus`：約 57,000 篇文件（id / title / text；本資料集 title 為空）
- `queries`：自然語言問題
- `qrels`（query relevance）：問題與文件的對應關係，`score=1` 表示該文件可回答該問題

沒有 ground truth 就無從評估與優化；把自家文件做成這種三檔結構（documents / questions / relationships）是套用本流程的前置條件。後段提到現在用 LLM 就能半自動生成這種 evaluation set。

## BM25（Sparse Retrieval）

實作要點：

- 套件：`BM25S`（純 Python，預設 Lucene 變體）
- Tokenization：去 stopwords、建立 `vocabulary`（字串 → 整數 id），corpus 變成 id 序列
- 建索引後直接 `retriever.save("<path>")` 序列化到磁碟；57k 文件約 33 MB，**通常不需要 vector DB**，本機檔案就夠
- 查詢端走同一套 tokenization 把 query 變 token，再對整個 corpus 檢索

範例查詢：`"where should I park my rainy day funds"`，預設取 top-K = 10。BM25 對「rainy day funds」這種詞面接近的文件命中率高，但若提問換句話說（如 "emergency savings"）就會掉。

## Dense Embeddings（Semantic Retrieval）

實作要點：

- 模型：`text-embedding-3-small`（OpenAI），輸出 1536 維向量
- 對整個 corpus 走 batch embedding，**會產生少量 API 成本**，但 embedding 結果 cache 到磁碟、只算一次
- 教學用 OpenAI，實務可換成 open-source 模型（自架）省成本
- 查詢端對 query 做同樣的 embedding；本模型不強制 normalize，但教學示範了 L2 normalize 流程供其他模型參考
- 搜尋 = 對 corpus embedding 算相似度，取 top-K

Dense 的強項在 paraphrase：query 跟文件用不同字面表達同一個意思，dense 還是能配對。

## Reciprocal Rank Fusion（RRF）

把 BM25 與 dense 兩條結果合併成一條排序，公式：

```
score(d) = Σ  1 / (k + rank_i(d))
         i
```

- `k = 60`：原始論文採用的 smoothing factor，社群預設都用 60
- `rank_i(d)`：文件 d 在第 i 條結果（BM25 或 dense）中的名次
- 沒出現在某條結果中的文件，那一項貢獻為 0

關鍵實作細節：fusion 前要把每條 retriever 的 K **撐大**（影片用 K = 50），把候選池放大，RRF 才有東西可融；最終要的 top-N 從融合後的排序裡取。

直觀效果：兩邊都排前面的文件分數會被推上去；只有一邊命中的會落到中段。

## Cross-Encoder Reranker

RRF 之後加一層「真正讀 query + document」的 reranker：

- Dense embedding 用的是 **bi-encoder**：query 與 document 各自獨立向量化後算相似度（快、但相對粗）
- **Cross-encoder** 把 (query, document) 一起餵進模型，由模型直接打分（慢、但精準）
- 影片用 **Cohere rerank** API；輸入 = RRF 後 50 個 candidates，輸出 = 重排的 top-10

流程定型：

```
BM25 top-50  ─┐
              ├─ RRF ─→ 50 candidates ─→ Cohere rerank ─→ top-10
Dense top-50 ─┘
```

實作上一條 `rerank()` 包進去就好，候選池大、最終回傳少，是 production 預設架構。

## 用 NDCG 衡量檢索品質

`NDCG`（Normalized Discounted Cumulative Gain）= 資訊檢索的黃金標準：

- 看 retrieved 文件的「位置」與「是否相關」算 0–1 分數
- 純 Python 實作就能算，不需要外掛
- **越高越好**：每次換 embedding 模型、換 chunk 策略、換 reranker、調 K 都重跑 NDCG，誰高用誰

沒有 NDCG（或等價指標）就沒有客觀依據說某個改動有沒有變好；憑感覺優化就是憑感覺退化。

## 應用到自家資料

幾個關鍵搬移點：

- **文件來源**：Notion、Zendesk、客戶文件、support tickets…自選；先決定 chunking 策略（受 embedding 模型 token 上限限制，且 chunk 大小直接影響檢索粒度）
- **建 evaluation set**：用 LLM 半自動生成 query + 正確文件 id 的對應表，套進 BEIR 風格三檔結構（corpus / queries / qrels）就能沿用同一條 pipeline
- **持續迭代**：evaluation set 不是一次做完，是邊用邊補；NDCG 變動就是改動的客觀回饋
- **實驗空間**：作者順帶提到，有時拿掉 BM25、純 dense + 拉大 top-K + 加 reranker 反而分數更高——沒有絕對最佳組合，要靠自家資料測

## 重點啟示

- **產線級 RAG 不是 vector DB + 一個 embedding model**，是 sparse + dense + fusion + rerank 四段
- BM25 在許多場景仍是 production 的關鍵組件，且**不需要 DB**，磁碟檔案就行
- RRF 是免訓練、無參數可調（k=60 就好）、跨檢索器通用的合併方式，CP 值極高
- Cross-encoder reranker 是「以時間換精準度」的關鍵一層，候選池放大它的價值才出得來
- **沒有 NDCG 就沒有優化**；建 evaluation set 跟建檢索 pipeline 一樣重要
