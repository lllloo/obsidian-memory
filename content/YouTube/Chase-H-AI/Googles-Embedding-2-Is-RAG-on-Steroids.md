---
title: Google's Embedding 2 Is RAG on Steroids (But Everyone is Getting it Wrong)
tags:
  - youtube
  - claude-code
  - rag
  - embedding
  - ai-tools
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/gmbW_lXXIkc
---

Google 發布首個原生多模態 embedding 模型 Gemini Embedding 2，可直接將影片、圖片、音訊嵌入向量資料庫。但大多數人對其使用方式有根本性的誤解。

## 核心誤解

能把影片嵌入向量資料庫 ≠ 能在向量資料庫中「分析」影片

標準 naive RAG 架構配合 Embedding 2 只會回傳影片片段，而非文字分析。這是因為 LLM 無法直接讀取 MP4 檔案來生成答案。

## RAG 架構深度解析

### 文字 RAG 的運作方式
1. 文字文件 → Embedding 模型 → 向量（1526 維數字）
2. 問題也轉換為向量
3. 比較相似度，取出最近的向量
4. 配對的文字文件作為 context 傳給 LLM → 生成回答

### 影片 RAG 的問題
- 影片嵌入後也變成向量
- 取出後配對的是 MP4 檔案
- LLM 無法直接分析 MP4 → 只能回傳影片片段，無法生成文字分析

## 正確的多模態 RAG 架構

在影片入庫時，先讓 Gemini（例如 Gemini 3.1 Flash）分析影片並生成文字描述/逐字稿，**與影片一起配對存入向量資料庫**。

當查詢觸發該向量時，LLM 同時取得：
- 影片片段（媒體預覽）
- 文字描述/逐字稿（可被 LLM 分析）

## 影片分塊（Chunking）問題

影片的分塊目前尚無完善解決方案。簡易做法：每 2 分鐘切一段，30 秒重疊，類似文字分塊的傳統方式。

## 實作資源

- GitHub repo 提供完整架構（含 Claude Code blueprint）
- 技術棧：Python 3.1+、FFmpeg、Supabase CLI（向量資料庫）、Gemini API
- 兩種啟動方式：clone repo 後指向 Claude Code，或直接複製 blueprint prompt 貼進 Claude Code

## Gemini Embedding 2 限制

- 影片最長 120 秒/段
- 文字最多 8,192 tokens
