---
title: Pretext 解決瀏覽器文字測量效能瓶頸
tags:
  - youtube
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-02
source: https://www.youtube.com/watch?v=vd14EElCRvs
---

## 問題：瀏覽器文字測量的效能瓶頸

每當瀏覽器需要知道文字的高度或換行位置，就必須觸發 **layout reflow**，計算頁面上所有元素的位置與幾何形狀，是瀏覽器最昂貴的操作之一。

這使得建立文字密集 UI（如虛擬列表、Masonry 版面）變得極為困難——你需要預先知道每個元素的高度，才能計算捲動高度並決定哪些元素應該渲染。

## 解法：Pretext

**Pretext** 是由 Cheng Lou（前 React 核心成員、Midjourney 工程師）開發的 TypeScript 函式庫，完全繞過瀏覽器文字渲染流程：

**取得寬度：**
- 使用 **Canvas API**（位於 DOM 之外），直接取得任意字型字串的像素寬度，不觸發 reflow

**取得高度：**
- 自行撰寫演算法，處理各瀏覽器、各語言的換行規則
- 用 AI agent 反覆撰寫換行邏輯 → 對真實瀏覽器測試 → 比對結果 → 迭代，持續數週直到演算法穩健

## API 使用方式

```typescript
// 1. 準備文字：分割為片段並快取每段寬度
const prepared = pretext.prepare(text, { font, fontSize });

// 2. 計算版面：取得總高度與行數，完全不碰 DOM
const { height, lineCount } = pretext.layout(prepared, { width });
```

## 應用範例：影片字幕 ASCII 渲染

利用 Pretext 知道每個字元精確位置的特性：

1. `prepare` 將 script 分割並快取每段像素寬度
2. 在迴圈中對每列呼叫 `layout_next_line`，確定每個字元落在哪個欄位
3. 建立字元格網，每格對應一個字元
4. 將影片畫到同等大小的離屏 canvas，讀取原始像素資料
5. 依像素亮度決定對應格子是否顯示字元 → 影片由字母組成

## 意義

Pretext 證明瀏覽器不必再主導文字測量。對需要精準文字位置的 UI（虛擬列表、Masonry、程式碼編輯器等）來說，是重要的底層基礎建設。
