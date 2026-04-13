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
status: done
source: https://youtu.be/rJCgvnXgOiU
---

RAG Anything 解決了大多數 RAG 系統只能處理純文字的問題，可處理 PDF 掃描件、圖片、圖表等非文字文件，並與 LightRAG 無縫整合。

## 核心概念

- **問題**：LightRAG 及一般 RAG 系統只能處理文字文件，無法處理圖表、掃描 PDF 等
- **解法**：RAG Anything 來自 LightRAG 同一個團隊，直接插入 LightRAG 系統
- **本地解析**：使用 MinerU（開源文件解析器）在本機執行，零成本

## 運作原理

1. **MinerU 解析**：將文件拆分為 header、text、chart、image、latex equation 等元件
2. **兩條路徑**：
   - 文字路徑：透過 PaddleOCR 轉為可讀文字
   - 圖片路徑：截圖處理
3. **送至 LLM**（如 GPT-4.5 mini）：產生 embeddings + entities/relationships
4. **合併**：RAG Anything 的 vector DB + knowledge graph 與 LightRAG 合併 → 統一查詢

## 安裝與使用

- 提供 oneshot prompt 讓 Claude Code 自動安裝
- 預設使用 GPT-4.5 nano + text-embedding-3-large
- 上傳非文字文件需透過 Python script（不能用 LightRAG UI），以 Claude Code skill 觸發即可
- 預設使用 CPU 執行 MinerU；如需加速可切換 GPU 版 PyTorch

## 重點摘要

- 查詢方式與 LightRAG 完全相同，差異只在上傳流程
- Skills 與 oneshot prompt 可在 Chase AI 免費社群取得
- 實際 Demo：成功查詢含長條圖的假 PDF（Novatech SaaS 收益分析）的月度數據
