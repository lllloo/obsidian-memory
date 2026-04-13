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

**影片描述**：Chase H 從底層解釋 RAG 的演進——從 Naive RAG 到 Graph RAG——並展示如何用一行 prompt 讓 Claude Code 自動安裝 LightRAG，再透過四個 skills 從 Claude Code 內部直接操作知識圖譜。

**重點摘要：**
- Naive RAG（2024 年末流行）已過時：文件切 chunk → embedding → vector DB → cosine similarity 查詢，本質上只是「進階 Ctrl+F」，無法處理跨文件的深層關聯問題。
- Graph RAG 的升級：在 vector DB 基礎上額外建立 knowledge graph（entities + relationships），讓查詢不只找最近的向量，還能沿著關係邊遍歷，回答「不同文件之間如何關聯」這類問題。
- LightRAG 的優勢：同時做 hybrid search（vector + graph），成本是 Microsoft Graph RAG 的一小部分，且持續更新維護，開源免費。
- 安裝極簡單：給 Claude Code 一行 prompt（Clone LightRAG repo、設定 OpenAI .env、用 Docker Compose 啟動），需要 OpenAI API key 和 Docker Desktop；也支援全本地（Ollama）部署。
- 安裝完成後可在 `localhost:9621` 使用 Web UI，可上傳文件、查看 knowledge graph、使用 retrieval tab 問答，同時提供完整 API 端點。
- Claude Code 整合靠四個 skills（可在免費 Chase AI 社群取得）：query、upload、explore、status；透過自然語言觸發，Claude Code 直接呼叫本機 Docker 容器 API。
- 何時開始用 RAG：約 500–2,000 頁文件時開始考慮；超過百萬 tokens 幾乎肯定要用；2025 年 7 月研究顯示大文件情境下 RAG 比直接 LLM 便宜 1,250 倍（現況差距可能縮小，但仍顯著）。
- 影片結尾預告隔日的 RAG Anything，解決 LightRAG 無法處理非文字文件（圖表、掃描 PDF）的缺陷。
