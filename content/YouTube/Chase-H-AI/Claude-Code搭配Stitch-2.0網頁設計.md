---
title: Claude Code 搭配 Stitch 2.0 進行網頁設計
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-19
source: https://www.youtube.com/watch?v=qqcpiDXPCvY
parent: "[[01.index]]"
---

## 為何需要 Stitch

Claude Code 在 agentic coding 上表現卓越，但前端設計是其弱點。Stitch 2.0 是 Google 推出的免費設計工具，由 Gemini 3.1 驅動，可彌補這個缺口。Figma 股價因此下跌近 8%。

Stitch 的核心價值：
- 提供無限畫布，可快速看到多個 prototype
- 可一次生成 2-3-4 個設計變體並比較
- 完全免費
- 最終可將設計匯出為程式碼交給 Claude Code

## 使用流程

**步驟一：找靈感**

在以下平台尋找喜歡的設計截圖或 URL：
- Dribbble（三個 B）
- godly.website
- Pinterest（搜尋 landing page design 效果佳）

**步驟二：在 Stitch 生成設計**

1. 前往 Stitch（Google 搜尋「Google Stitch」）
2. 選擇 Web App
3. 選擇模型：Gemini 3.1 Pro（推薦）或 3.0 Flash
4. 上傳截圖或貼入網址作為靈感
5. 給出提示，例如：「Create a landing page for my AI agency in the style of the screenshot」

**設計系統（Design System）**

Stitch 會自動產生設計系統文件，包含：
- 主色、副色、中性色
- 字體、按鈕、搜尋列等元件規範
- 創意方向（如何避免 AI slop 的具體說明）

不需要額外要求，Stitch 自動生成。

**步驟三：迭代**

- 右鍵 → Regenerate：重新生成
- 右鍵 → Variants：選擇 layout、color scheme、images 等維度的變體
- 點鉛筆圖示可針對個別元件編輯
- Live mode：Stitch 即時觀看你的螢幕，可用語音或文字直接對話修改

## 整合 Claude Code

達到 80-90% 滿意度後：
1. 點選設計 → More → Export → Code to Clipboard
2. 切換到 Claude Code
3. 提示：「Create a landing page for [用途]. Here's the front-end code: [貼上]」
4. Claude Code 約 60 秒完成前端頁面

完成後可用 GitHub + Vercel 免費部署（詳見其他網頁部署影片）。

## 關鍵結論

- 純用 Claude Code 做前端設計仍有不足，Stitch 是有效的免費補充工具
- 在 Stitch 消耗的 token 為零（在 Claude Code 外完成）
- 核心工作流程：靈感截圖 → Stitch 設計 → 匯出程式碼 → Claude Code 實作
