---
title: CLI-Anything Just Brought Claude Code Into The Future
tags:
  - youtube
  - claude-code
  - cli
  - ai-tools
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/Uzd2ckXnsg0
---

介紹開源工具 CLI Anything，可將任何開源軟體自動轉換為 CLI 工具，讓 Claude Code 能直接透過終端機控制原本需要 GUI 操作的軟體。

## 為什麼 CLI 優於 MCP

Claude Code 本身就住在終端機裡，CLI 工具也在終端機裡，沒有中間人、沒有額外開銷，溝通效率最高。這是目前 agentic coding 的演進方向。

## CLI Anything 是什麼

由香港大學數據與智慧實驗室（Data and Intelligence Lab, HKUST）開發，也是 LightRAG、RAG Anything、Nanobot 等工具的製作團隊。

**核心能力**：指向任何開源軟體的程式碼，自動生成對應的 CLI 工具，讓 AI agent 可以透過結構化 CLI 控制該軟體。

## 七步自動化流程

1. 分析程式碼
2. 設計輸出格式
3. 實作
4. 計畫
5. 撰寫測試
6. 文件化
7. 發佈

之後還可以繼續迭代改善 CLI。

## 已支援的大型開源專案

- Blender（28 個測試）
- Inkscape
- Audacity
- draw.io（示範用）

## 安裝與使用

### 前置需求
- Python 3.1+
- 目標軟體已安裝

### 步驟
1. 在 Claude Code 安裝 CLI Anything plugin：`/plugin` → 安裝
2. Clone 目標軟體的 GitHub repo
3. 執行 `cli-anything <repo路徑>`（約 20 分鐘）
4. 看到「all success criteria are met」即完成

### 示範效果
指向 draw.io repo 後，只需一句 prompt 即可讓 Claude Code 建立複雜的 SaaS 後端架構圖，包含視覺樣式與陰影效果。

## 適用場景

- 你有某個開源工具的完整程式碼存取權
- 該工具原本需要 GUI 操作
- 想讓 Claude Code 自動化這個工具的使用

這是 AI coding agents 的未來方向：任何軟體都能變成 agent 可控的工具。
