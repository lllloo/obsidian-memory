---
title: Claude Code + RAG-Anything = 無極限
tags:
  - youtube
  - claude-code
  - rag
  - ai
created: 2026-04-12
updated: 2026-04-12
published: 2026-04-02
source: https://youtu.be/rJCgvnXgOiU
---

**影片描述**：RAG Anything 解決了幾乎所有 RAG 系統（包括 LightRAG）的共同弱點——只能處理純文字。同一個 LightRAG 團隊開發，可直接疊加在現有 LightRAG 系統上，處理掃描 PDF、圖表、圖片等非文字文件。

**重點摘要：**
- 核心問題：LightRAG 和大多數 RAG 系統無法處理非文字文件（掃描 PDF、圖表、圖片、LaTeX 方程式），RAG Anything 專門解決這個問題。
- 解析引擎 MinerU：開源文件解析器，在本機免費執行，將文件拆解為 header、text、chart、image、latex 等元件，再分兩條路徑處理——文字路徑（PaddleOCR 轉可讀文字）和圖片路徑（截圖處理）。
- 處理流程：MinerU 解析後，兩條路徑分別送至 GPT-4.5 nano（或其他 LLM），產生 embeddings 和 entities/relationships，分別建立各自的 vector DB 和 knowledge graph，再合併成一套統一的知識庫。
- 與 LightRAG 整合：RAG Anything 最終的 vector DB + knowledge graph 會與現有 LightRAG 的合併，形成「rag everything」，查詢方式與原本完全相同。
- 安裝方式：提供 oneshot prompt 給 Claude Code 自動安裝（需在 LightRAG 目錄執行），系統比 LightRAG 稍重，需下載 MinerU 及其相依套件；預設使用 GPT-4.5 nano + text-embedding-3-large。
- 重要限制：上傳非文字文件必須透過 Python script，不能用 LightRAG Web UI；以 Claude Code skill 觸發即可，對用戶而言操作無感。
- 設計哲學：先在本機以 MinerU 解析，再用 LLM 處理，避免把大量截圖全部丟給 GPT 處理（昂貴且慢），是一種「先低成本分類再精準處理」的架構。
- 實際 Demo：成功查詢含長條圖的假 PDF（Novatech SaaS 收益分析），可正確回答月度收益數據問題。
