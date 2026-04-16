---
title: Claude Code 加 RAG-Anything 無極限
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-02
source: https://www.youtube.com/watch?v=rJCgvnXgOiU
parent: "[[01.index]]"
---

## 解決的問題

傳統 RAG（包含 LightRAG）只能處理純文字文件。現實中大量文件包含：掃描 PDF、圖片、圖表、LaTeX 公式等非文字內容。

**RAG-Anything** 由 LightRAG 同一團隊開發，作為 LightRAG 的包裝層（wrapper），最終將兩者的知識圖譜合併為單一查詢入口。

## RAG-Anything 運作原理

### 第一步：文件解析（MinerU，本地執行、開源、免費）

MinerU 是文件解析工具，不理解內容，只識別結構：

```
掃描 PDF / 非文字文件
    ↓ MinerU 分析
┌─────────────────────────────────────┐
│ 標題 header  │  文字 text  │ 圖表 chart │
│ 圖片 image  │  LaTeX 公式  │ ...        │
└─────────────────────────────────────┘
```

內部使用 PaddleOCR 等專門模型提取各類型內容的文字。**無法轉為文字的（圖片、圖表）→ 截圖處理**。

### 第二步：兩條路徑分別處理

| 路徑 | 內容類型 | 處理方式 |
|---|---|---|
| 文字路徑 | 識別出的所有文字 | 發送給 GPT-4o-mini，提取 entities + relationships + embeddings |
| 圖片路徑 | 截圖形式的圖表/圖片 | 以視覺方式發送給 GPT-4o-mini，同樣提取 entities + relationships + embeddings |

分開處理而非全部截圖的原因：**節省成本與時間**（想像 10,000 張截圖全部 OCR 的開銷）。

### 第三步：合併

```
文字路徑 → 向量資料庫A + 知識圖譜A
圖片路徑 → 向量資料庫B + 知識圖譜B
    ↓ 合併（以 entities 配對）
RAG-Anything 的統一向量資料庫 + 知識圖譜
    ↓ 再與 LightRAG 合併
最終：一個向量資料庫 + 一個知識圖譜
```

對使用者完全透明，查詢方式與純 LightRAG 完全相同。

## 安裝（一鍵 Claude Code prompt）

前置：已完成 LightRAG 安裝並在 LightRAG 目錄下執行。

```
在 Claude Code（LightRAG 目錄）輸入：
[安裝 prompt，可在 Chase AI 免費社群搜尋 "rag anything" 找到]
```

Prompt 會做三件事：
1. 更新 storage path（對接已有的 LightRAG Docker 實例）
2. 更新模型至 `gpt-4o-mini`（nano）+ `text-embedding-3-large`
3. 修復 GitHub repo 範例腳本中的 embedding double-wrap bug

下載時間較長（需下載 MinerU 及其依賴）。

> 預設使用 CPU 執行 MinerU；若想加速，告訴 Claude Code「讓 MinerU 在 GPU 上跑」，它會自動處理 PyTorch 版本切換。

## 上傳非文字文件（兩條路徑注意事項）

| 文件類型 | 上傳方式 |
|---|---|
| 純文字、普通 PDF | LightRAG Web UI 拖放，或 `lightrag:upload` skill |
| 非文字文件（掃描 PDF、圖表等）| 使用 `rag-anything:upload` skill（背後跑 Python script）|

上傳非文字文件後，需重啟 Docker container（skill 會自動執行此步驟）。

```
# 使用方式
Claude Code，使用 rag-anything skill 上傳 [文件路徑或資料夾]
```

## 查詢方式（與 LightRAG 完全相同）

```
Claude Code，用 lightrag:query skill 查詢 Novatech Inc. 
1 月到 9 月的月營收趨勢
```

實際測試：成功從含有條形圖的掃描 PDF 中提取各月份數字（January 4.6M, February 4.9M...），LightRAG 單獨無法做到。

## 調整查詢參數

LightRAG Web UI Retrieval 頁籤右側有多個調整參數。也可以直接告訴 Claude Code 調整，它了解各參數的最佳實踐。
