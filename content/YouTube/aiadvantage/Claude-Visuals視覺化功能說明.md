---
title: Claude Visuals 視覺化功能說明
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-19
source: https://www.youtube.com/watch?v=8QsdWYx2qmk
---

## 功能概覽

Claude 新增視覺化功能，介於純文字回覆與完整 Artifact 之間的中間層，可快速產生互動式 HTML 視覺內容，像是在對話中置入一塊白板。

- 免費帳號可用
- 速度接近生成文字
- 輸出是 HTML，不是獨立應用程式
- 與 Artifact 的差別：Artifact 更複雜、花更多時間；Visuals 是輕量快速版

## 觸發關鍵字

- `Show me`（最通用）
- `Draw a graph`
- `Create a visualization`

使用 `Show me` 會觸發 Claude 生成互動式 HTML 頁面，而不是純文字回覆。

## 使用範例

**複利計算機**
- 輸入：`Show me how compound interest works`
- 輸出：可調整各項數值的互動計算機

**抵押貸款流程圖**
- 輸入：`Show me a flowchart on how a mortgage works`
- 可追加指令客製化風格，例如 `Style the flowchart in a crazy way`

**產品比較視覺化**
- 先讓 Claude 做 web search 研究（例如：`Research different wireless headphones under $300`）
- 再輸入：`Show me by visualizing the comparison`
- 輸出：視覺化比較卡片，比純文字表格更直觀

## 分享與轉存

- 懸停圖表 → 三點選單
- `Copy to clipboard`：複製為截圖（非互動版）
- `Save as artifact`：轉為正式 Artifact，可取得可分享的網頁連結

## 注意事項

- 最佳效果需要 **Opus 模型**（Anthropic 官方推薦）
- 使用免費版 Sonnet 效果會較差
- Visuals 不能分享互動連結，僅能複製截圖或另存為 Artifact
