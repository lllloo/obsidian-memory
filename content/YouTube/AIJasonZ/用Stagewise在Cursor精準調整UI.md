---
title: 用 Stagewise 在 Cursor 精準調整 UI
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-05-22
source: https://www.youtube.com/watch?v=2RlBb4C_XwI
---

## Stagewise 解決的問題

Cursor 通常能讓 UI 達到 80%，但最後 10~20% 的細部調整很難精準溝通，例如對齊、間距、特定元素的視覺修正。Stagewise 讓你直接在瀏覽器中選取 UI 元素，並將元素資訊自動傳入 Cursor。

## 安裝與設定

1. 在 Cursor Extension 搜尋 `stagewise` 並安裝
2. 開啟任何 web 專案，按 `Cmd+Shift+P` 搜尋 `stagewise`
3. 選擇 **Auto Setup Stagewise Toolbar**，Cursor 會自動偵測框架（Next.js / React）並完成設定
4. 執行專案後，畫面底部會出現浮動工具列

## 使用方式

1. 點開浮動工具列
2. 在瀏覽器畫面中選取想修改的 UI 元素（可多選）
3. 輸入修改指令，例如：「make all buttons border radius larger」
4. Stagewise 會將選取元素的 div 路徑、class 資訊連同指令一起送進 Cursor

## 關鍵優點

- **全域修改**：因為傳入了具體的 class 資訊，修改會套用到所有相同的元素，而不只是單一個
- **支援複雜佈局調整**：可同時選取多個元素，描述它們之間的排列關係
- 網站上有更多進階範例，如將元素轉為 accordion、修改 table label 顏色等
