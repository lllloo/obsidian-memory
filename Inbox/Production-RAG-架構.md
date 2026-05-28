---
title: Production RAG 架構
created: 2026-05-27
updated: 2026-05-28
source: https://www.youtube.com/watch?v=XvKiTfd6Xvo
published: 2026-05-14
tags:
  - rag
  - agentic-rag
  - hybrid-search
  - ai-agent
---

**Production RAG 不是「vector DB + 一個 embedding model」，而是一條依延遲、成本與資料結構選形態的光譜。** 把三種實作擺在同一條軸線上看，才知道什麼場景該用哪一段。

## RAG 形態光譜

| 形態 | 機制 | 延遲/成本 | 何時用 |
|---|---|---|---|
| **CAG（全塞）** | 不檢索，整份文件直接進 context window（Cache Augmented Generation） | 最低延遲；成本隨 context 大小，大 window 廉價模型幾乎可忽略 | 文件總量可一次塞入 window，要精確、不容遺漏（chunk 會切斷程式碼、需 metadata filtering） |
| **Semantic RAG** | 線性：取資料後呼叫 LLM 一次 | 低 | 即時 chatbot、單次 QA、預算敏感 |
| **Hybrid retrieval** | 四段 pipeline 拚召回品質（見下） | 中 | 召回品質是瓶頸、文件量大 |
| **Agentic RAG** | 迴圈：LLM 在 search / read / 回呼間多次調用，找不到會換條件自我修正 | 高 | 私有資料多步推理、跨檔交叉比對；或當 semantic 答不好時的 fallback 層 |
| **Dynamic 多來源** | agent 自選資料源：內部 RAG / 指定單頁 / web search | 高 | 需要內外部資訊混合，web 常作 fallback |

選擇原則：**先問「連 RAG 都不必嗎」**——context window 裝得下整份文件就用 CAG，極簡又不遺漏；裝不下才進檢索光譜。進檢索後，**願意付出 latency 與 token 換正確率才往下走**，低延遲場景留在 semantic。超大資料集可混合：先用傳統搜尋（metadata / 檔名）找子集，只把子集餵 LLM。

## Hybrid retrieval 的四段

```
Query → [BM25 sparse top-K] + [Dense embeddings top-K]
      → Reciprocal Rank Fusion 合併
      → Cross-encoder reranker 重排 → 最終 top-N
```

- **sparse（BM25）抓精確詞、識別碼、罕見詞**；**dense embeddings 抓 paraphrase、語意**——兩者贏在對方輸的地方，所以該融合。BM25 不需要 DB，本機檔案就夠。
- **RRF** 免訓練、無參數可調（smoothing factor 取 60 即可）、跨檢索器通用，CP 值極高。融合前要把各 retriever 的 K 撐大，候選池夠大才有東西可融。
- **Cross-encoder reranker** 把 (query, document) 一起餵進模型直接打分（比 bi-encoder 慢但準），是「以時間換精準度」的關鍵層；候選池放大它的價值才出得來。
- 沒有絕對最佳組合——有時拿掉 BM25、純 dense + 拉大 top-K + reranker 反而更高，要靠自家資料測。

## Agentic RAG 的最小骨架

三個工具作用在檔案系統上即可，正是 coding agent（Claude Code / Cursor / Codex）共用的核心：`list` / `grep` / `read`。LLM 在迴圈中自主決定呼叫順序直到湊齊答案。Production 強化重點（與載體無關，換成 PostgreSQL / serverless 邏輯不變）：

- **error 用 return 不用 raise**：raise 會停掉整個 process；回傳人類可讀的 error string，LLM 才能收到並 self-correct 再試。
- **docstring 即 prompt**：tool 的 docstring 與型別會進 system prompt，加 domain knowledge 可導向 agent 搜對方向。
- **安全上限**：request limit 防無限迴圈、單檔讀取行數上限防灌爆 context。
- **路徑 sandbox**：把 agent 鎖在指定目錄內，禁止跳出讀任意檔。

## 跨三種形態的共識

1. **結構化輸出 + citation 是接進產品的基本盤**——前端能渲染答案並點擊跳原文。
2. **沒有評估指標就沒有優化依據**：用 NDCG（或等價指標）衡量每次改動（換 embedding、換 chunk 策略、換 reranker、調 K），憑感覺優化就是憑感覺退化。建 evaluation set（BEIR 風格 corpus / queries / qrels，可用 LLM 半自動生成）跟建檢索 pipeline 一樣重要。詳見 [[LLM-Evals-方法論]]。
3. **反對「丟給 Claude Code one-shot 出一套 RAG」**——要理解每一塊機制，才能針對自家資料調優。

## 相關

- [[LLM-Evals-方法論]] — NDCG / evaluation set 是 RAG 優化的前提
- [[Context-Engineering]] — RAG 作為 context engineering 的一個面向
