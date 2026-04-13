---
title: Claude Code + LightRAG = 勢不可擋
tags:
  - youtube
  - claude-code
  - rag
  - lightrag
  - ai
created: 2026-04-12
updated: 2026-04-12
published: 2026-04-01
source: https://youtu.be/QHlB-RJfx8w
---

介紹 Graph RAG 概念與 LightRAG 開源專案，說明為何 Naive RAG 已不夠用，以及如何將 LightRAG 整合進 Claude Code 工作流程。

## RAG 演進

- **Naive RAG**（2024 末）：文件 → chunk → embedding → vector DB → 查詢最相近向量。效果差，已過時
- **Graph RAG**：在 vector DB 基礎上額外建立 **knowledge graph**（entities + relationships）
  - 可回答跨文件的深層關聯問題，不只是「進階版 Ctrl+F」
  - LightRAG 同時做 hybrid search（vector + graph），成本是 Microsoft Graph RAG 的一小部分

## LightRAG 安裝

需要：
- OpenAI API key（embedding model）
- Docker Desktop

一行 prompt 給 Claude Code：
> Clone the LightRAG repo. Write the .env file configured for OpenAI with GPT-5 mini and text-embedding-3-large. Use all default local storage and start it with Docker Compose.

完成後在 `localhost:9621` 有 Web UI，可上傳文件、查看 knowledge graph、呼叫 API。

## Claude Code 整合

四個核心 skills（在免費 Chase AI 社群取得）：
- **query**：查詢 knowledge graph
- **upload**：上傳文件
- **explore**：瀏覽已存入的文件
- **status**：查看系統狀態

用自然語言觸發 skill，Claude Code 直接對本機 Docker 容器發 API 請求。

## 何時應使用 RAG

- 文件量達 **500–2,000 頁**時開始考慮
- 超過 100 萬 tokens 時幾乎一定要用
- 研究顯示：在大型文件情境下，RAG 比直接使用 LLM 便宜 **1,250 倍**（2025 年 7 月數據，現今差距或已縮小）
- LightRAG 可全本地（Ollama）或混合（OpenAI）部署，高度可客製化

## 後續

影片結尾預告 RAG Anything（隔日影片），可處理非文字文件（圖表、掃描 PDF）。
