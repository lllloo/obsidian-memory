---
title: Claude Code 加 RAG-Anything 無極限
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-02
source: https://www.youtube.com/watch?v=rJCgvnXgOiU
---

## 描述

介紹 RAG-Anything，解決傳統 RAG 只能處理純文字的限制，支援圖片、圖表、掃描 PDF 等非文字文件，直接整合至 LightRAG 系統。

## 重點摘要

- **解決的問題**：傳統 RAG 系統（包含昨日介紹的 LightRAG）只能處理文字文件，無法處理含圖片、圖表、掃描 PDF 的文件；RAG-Anything 解決了這個缺口
- **來源**：由開發 LightRAG 的同一團隊打造，可直接作為 LightRAG 的外掛層疊加使用
- **運作原理**：針對非文字文件，RAG-Anything 進行與 LightRAG 相同的知識圖譜建構流程，最終將兩個知識圖譜合併成一個統一的查詢入口
- **設置方式**：需在本機下載解析非文字文件的模型；非文字文件的匯入需透過腳本（無法用 LightRAG UI），適合用 Claude Code 來協助處理
- **缺點**：系統較重，需額外本機模型；非文字文件無法透過既有的 LightRAG 網頁介面直接匯入
- **前提條件**：本集假設已看過 LightRAG 集並完成基本設置，RAG-Anything 是其延伸
