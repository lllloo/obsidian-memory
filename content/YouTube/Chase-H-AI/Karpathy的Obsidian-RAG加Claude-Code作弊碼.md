---
title: Karpathy 的 Obsidian RAG 加 Claude Code 作弊碼
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-04
source: https://www.youtube.com/watch?v=OSZdFnQmgRw
---

## 描述

介紹 Andrej Karpathy 分享的 Obsidian 知識庫系統，以 Obsidian 取代傳統 RAG（無需向量資料庫或 embedding），搭配 Claude Code 做知識查詢。

## 重點摘要

- **核心概念**：Karpathy 在 Twitter 發文說明，不需要向量資料庫、embedding 或複雜的 retrieval pipeline，只需善用 Obsidian 的檔案結構，就能達到與傳統 RAG 系統相同的效果
- **系統架構**：資料進入「raw」目錄（staging 區）→ 由 Claude Code 整理成 wiki 格式 → 存入 Obsidian vault；Obsidian 作為前端可視化，讓用戶直接看到文件組織
- **優勢**：極輕量、幾乎免費、適合個人或小型團隊；相比 LightRAG、RAG-Anything 等系統設置更簡單，不會被抽象化在黑箱中
- **運作方式**：大量文件（文章、論文、repo）匯入後，用 Claude Code 直接以自然語言提問，LLM 自行在檔案系統中查找連結關係
- **與傳統 RAG 的差異**：傳統 RAG 用 embedding 做向量搜尋，此系統依賴 LLM 的長上下文能力搭配結構化的 Obsidian 目錄直接讀取
- **適用族群**：個人操作者或小型團隊，需要處理大量文件但不想維護複雜 RAG 基礎設施的情境
