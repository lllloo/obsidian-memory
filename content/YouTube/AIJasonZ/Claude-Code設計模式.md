---
title: Claude Code 的設計模式
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-10-31
source: https://www.youtube.com/watch?v=vcJVnyhmLS4
parent: "[[01.index]]"
---

## 核心問題

用 AI agent 複製特定網站設計風格時，僅靠截圖通常只能達到 60-70% 的相似度，細節色彩、間距、字型常在轉換中流失。

## 高保真度設計的流程

### 第一步：取得高保真 CSS 上下文

- 不只給截圖，而是右鍵 Inspect → 複製整份 HTML/CSS 樣式
- 工具 **Visbug**（Chrome 擴充）可快速取得特定元素的精確顏色值
- 搭配截圖一起給 agent，先要求重建一個簡單頁面作為參考實作（`Motherduck.html`）

### 第二步：共同迭代參考頁面

- Agent 先生成初版，再根據具體差異（如背景色）回饋修正
- 目的是讓這個參考頁面成為後續所有頁面的設計基準

### 第三步：提取 style guide

提示詞範例：
```
幫我生成詳細 style guide 到 style-guide.md
必須包含：overview、color palette、typography、spacing、
component style、shadow animation、border radius 等
```

### 第四步：基於 style guide 設計新頁面

- 有了 style.md 後，要求 agent 設計新 UI 時自動套用此 guide
- 結合設計指令（如 `/design` command），可進一步提升細節品質

## 進階應用

- **Next.js 轉換**：將 HTML 原型移植為 Next.js，自動拆解為可重用 component，保持一致風格
- **投影片設計**：style guide 也能用於生成品牌一致的簡報（可匯出至 Tempest）
- **產品 Demo 動畫**：搭配 Framer Motion 生成互動式動畫，可嵌入網站或用於影片
- **其他設計工具**：複製 style guide 貼入 Google Stitch 等 AI 設計工具，可生成完整 UI 套件

## Superdesign Extension

作者開發的 Chrome 擴充，可自動：
1. 開啟任意網頁後輸入提示詞
2. 自動克隆該頁面並掃描所有 CSS
3. 生成高保真 style guide
4. 匯出含 component breakdown 的 production-ready React 專案
