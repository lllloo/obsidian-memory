---
title: Claude Code 加 LightRAG 勢不可擋
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-01
source: https://www.youtube.com/watch?v=QHlB-RJfx8w
parent: "[[01.index]]"
---

## 為何 RAG 沒死

儘管 Opus 4.6 等模型的 context window 已大幅擴展，面對企業級文件庫時 RAG 仍不可或缺：

- 超過 ~100 萬 tokens（約 500–2000 頁文件）時，純靠 context window 成本過高
- 有研究（2025 年 7 月）顯示在極大文件量下，RAG 比直接丟給 LLM 便宜 **1250 倍**，速度也快得多
- 2024 末流行的「naive RAG」（Pinecone、Supabase 向量搜尋）已過時，現需 graph RAG

## RAG 基礎原理（Naive RAG）

```
文件 → chunk 切分 → embedding model → 向量（vector）
查詢 → embedding model → 查詢向量
查詢向量 vs 文件向量：cosine similarity → 取最近幾個 → 塞入 LLM context 作答
```

問題：每個向量互相獨立，無法理解文件之間的「關係」。

## Graph RAG 原理

在向量資料庫之外，額外建立**知識圖譜（knowledge graph）**：

- **Entity（實體）**：例如「Anthropic」、「Claude Code」
- **Edge（關係）**：例如「Anthropic created Claude Code」

查詢時不只找最近的向量，還會沿著知識圖譜**遍歷關係**，能回答跨文件的深層問題（例如：不同理論之間的關聯）。

LightRAG 同時做向量搜尋 + 知識圖譜，且成本只有 Microsoft GraphRAG 的一小部分。

## 安裝 LightRAG（一鍵 prompt）

前置需求：
- OpenAI API key（embedding model + 問答 LLM）
- Docker Desktop（需在安裝前啟動）

```
在 Claude Code 輸入：
Clone the LightRAG repo. Write the .env file configured for OpenAI 
with gpt-4o-mini and text-embedding-3-large. Use all default local 
storage and start it with Docker Compose.
[貼上 LightRAG GitHub URL]
```

Claude Code 會完成所有步驟，包括 clone、寫 .env、執行 Docker Compose。

## 使用 LightRAG Web UI

啟動後訪問 `http://localhost:9621`，功能：

- **Upload**：直接拖放文字文件、PDF（限文字類型）
- **Knowledge Graph**：可視化所有 entity 與 relationship，點擊 entity 查看屬性與來源
- **Retrieval**：在 UI 直接提問，右側可調參數
- 上傳時需等待（建立知識圖譜較耗時）；圖譜異常時點左上角 reset

## 接入 Claude Code（透過 Skills）

不用每次進 Web UI，透過 4 個 Skills 在 Claude Code 直接操作：

| Skill | 功能 |
|---|---|
| `lightrag:query` | 查詢知識圖譜，回傳 LLM 摘要（含原始 JSON 選項） |
| `lightrag:upload` | 上傳文件至 LightRAG |
| `lightrag:explore` | 瀏覽已上傳的文件清單 |
| `lightrag:status` | 查看 LightRAG 伺服器狀態 |

所有 Skills 原始碼可在 Chase AI 免費社群取得。

## 何時該導入 LightRAG

| 文件量 | 建議 |
|---|---|
| < 500 頁 | Claude Code 原生 agentic GP 足夠 |
| 500–2000 頁 | 灰色地帶，可嘗試 |
| > 2000 頁（~100 萬 tokens）| 強烈建議導入 LightRAG |

LightRAG 也支援完全本地化（embedding + LLM 全用 Ollama），或推送至 PostgreSQL/Neon 雲端主機。

## 延伸：非文字文件問題

LightRAG 只能處理文字文件；圖片、圖表、掃描 PDF 需搭配 **RAG-Anything**（同一團隊開發，下一支影片介紹）。
