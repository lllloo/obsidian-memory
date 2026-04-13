---
title: Claude Code 加 LightRAG 勢不可擋
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-01
source: https://www.youtube.com/watch?v=QHlB-RJfx8w
---

## 描述

說明 2026 年 RAG 的現況與適用場景，並示範如何用 LightRAG 建立 graph RAG 系統接入 Claude Code，處理大規模文件庫。

## 重點摘要

- **為何 RAG 沒死**：儘管 Opus 4.6 等模型的上下文視窗已大幅提升，面對企業級或大型文件庫（500～1000+ 份文件）時，RAG 系統在成本與速度上仍優於純靠 context window
- **RAG 演進**：2024 末到 2025 初流行的「naive RAG」（Pinecone、Supabase 等向量搜尋）已過時，現需使用更進階的 graph RAG
- **基本原理回顧**：文件不直接存入資料庫，而是先 chunk 再向量化，檢索時比對 embedding 相似度後，將結果塞入 LLM context 作答
- **LightRAG 優勢**：開源、持續更新，能與 Microsoft 等更複雜的 graph RAG 系統競爭，但成本只是一小部分
- **實作目標**：建立可透過 API 讓 Claude Code 查詢的 LightRAG 服務，處理大量文件並保留知識圖譜關係
- **適用場景**：需要 AI 處理大量企業文件、知識庫、多文件問答的情境
