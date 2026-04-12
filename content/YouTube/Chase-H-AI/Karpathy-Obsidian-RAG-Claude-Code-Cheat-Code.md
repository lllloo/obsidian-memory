---
title: "Karpathy's Obsidian RAG + Claude Code = CHEAT CODE"
tags:
  - youtube
  - claude-code
  - obsidian
  - rag
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/OSZdFnQmgRw
---

Chase H 拆解 Andrej Karpathy 分享的 Obsidian 知識庫系統：無需向量資料庫、無需 embeddings，卻能達到類似 RAG 的效果。

## 核心概念

Karpathy 的系統用 Obsidian + Claude Code 建立個人知識庫，解決「大量文件問答」的問題，但比傳統 RAG 輕量許多。

關鍵洞見：LLM 自然地維護 index 文件與摘要，讓文件網絡易於導航，不需要複雜的 retrieval 機制。

## 檔案結構

```
vault/
├── raw/          # 暫存區：放入所有原始資料（文章、PDF 等）
├── wiki/         # 主知識庫
│   ├── master-index.md   # 所有 wiki 的目錄
│   ├── AI-Agents/
│   │   └── index.md
│   ├── RAG-Systems/
│   │   └── index.md
│   └── Content-Creation/
│       └── index.md
└── CLAUDE.md     # 知識庫規則與導航方式
```

## 運作流程

1. **資料進入 raw/**：透過 Obsidian Web Clipper 或 Claude Code 自動爬取
2. **Claude Code 建立 wiki**：將 raw/ 資料轉化為結構化 wiki 文件，包含 wikilinks 互連
3. **Q&A 查詢**：Claude Code 先查 master-index → 找對應 wiki → 讀取相關文件

## 設定步驟

### 1. 安裝 Obsidian
到 obsidian.md 免費下載，指定一個資料夾為 vault。

### 2. 建立檔案結構
在 Claude Code 中貼上提示，讓它自動建立 raw/ 和 wiki/ 資料夾結構。

### 3. 設定 CLAUDE.md
說明知識庫規則：如何遍歷文件、如何格式化 wiki 文件。

### 4. 安裝 Obsidian Web Clipper
Chrome 擴充功能，可一鍵將網頁轉為 Markdown 送入 raw/。
- 設定：Options → Note Location 改為 `raw`

### 5. 安裝 Local Images Plus 插件
解決 Web Clipper 不支援圖片的問題，自動下載並儲存圖片至本地。

## 資料注入方式

| 方式 | 適用情境 |
|------|---------|
| Obsidian Web Clipper | 手動選擇要收藏的網頁 |
| Claude Code 自動研究 | 告訴 Claude 主題，讓它自行搜尋並建立 wiki |

## Obsidian vs 真正的 RAG

| | Obsidian 系統 | LightRAG / 傳統 RAG |
|-|--------------|---------------------|
| 設定難度 | 低 | 高 |
| 成本 | 幾乎免費 | 需要 embedding API |
| 透明度 | 高（可直接看所有文件）| 黑盒 |
| 可擴展性 | 數百到數千份文件 | 數萬到數百萬份 |
| 適用對象 | 個人、小團隊 | 企業、大規模應用 |

## 建議

先用 Obsidian 系統。如果明顯超出規模（成千上萬份文件且查詢慢），再遷移到 LightRAG。不要過早優化。

> 「People want to sit here and argue this back and forth. Just try it.」— Chase H
