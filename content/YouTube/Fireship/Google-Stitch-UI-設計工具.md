---
title: Google Stitch UI/UX 設計工具全面更新
tags:
  - youtube
created: 2026-04-14
updated: 2026-04-14
published: 2026-03-19
source: https://www.youtube.com/watch?v=qaB5HF4ax9M
---

## 什麼是 Google Stitch

Google Stitch 是一個**無限畫布的 AI 驅動 UI/UX 設計工具**，允許用戶以「vibe」（感覺描述）取代傳統線框圖作為設計起點：

- 描述產品感覺、目標用戶
- 提供截圖或現有網站 URL
- 語音直接下指令

工具會生成完整設計，並可一鍵轉為互動式 prototype，模擬完整使用者流程。

## 主要新功能

### 互動元件
- 產生的 UI 不是靜態圖片，每個元素都是可獨立修改的互動元件
- 支援響應式預覽，可在瀏覽器內切換裝置尺寸

### 設計系統擷取
- 輸入任意網站 URL，Stitch 會分析並生成對應的 **Design System**
- 可匯出為設計檔案（design markdown 格式），跨專案複用
- 該設計檔可直接整合進 Claude、OpenAI 等 coding model，實現**跨專案 AI 設計一致性**

### Gemini 語音互動
- 不需打字，直接對 Gemini 說話描述需求
- Gemini 會追問細節（版面類型、風格感覺）後生成設計

### Figma 整合
- 可將 Stitch 產出匯出至 Figma 繼續手動編輯

## 對設計生態的衝擊

- **Tailwind CSS**：儘管使用率創新高，Tailwind 因 AI 工具崛起被迫裁員，目前靠捐款維持運營
  - 背景：Tailwind 解決的是「實作速度」問題，而非設計問題，AI 工具直接跳過了這個需求
- **Figma**：Google Stitch 被視為直接競爭對手，定位為「Figma 殺手」

## 核心價值

設計 → 互動 prototype → 匯出設計系統 → 整合 AI coding model 的完整流程，讓沒有設計背景的開發者也能產出一致風格的 UI，是 2026 年 vibe coding 工作流的重要一環。
