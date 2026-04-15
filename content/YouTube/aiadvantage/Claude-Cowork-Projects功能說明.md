---
title: Claude Cowork Projects 功能說明
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-26
source: https://www.youtube.com/watch?v=zvCOmAzwa3Y
---

## 什麼是 Claude Cowork Projects

Claude Cowork 是比 ChatGPT 或一般 Claude 更高一層的應用，能實際執行任務：存取電腦資料夾、遠端控制瀏覽器、連接各種工具。Projects 功能讓你在 Cowork 裡組織不同任務，就像 ChatGPT 或 Claude 的 Projects，但搭配了 agentic 能力。

## 為何需要 Projects

使用 AI 的核心關鍵是提供正確的 context。不同生活領域（個人目標、工作、副業）需要不同 context，Projects 讓你預先建立這些 context 包，進入即可直接工作，不必每次重新說明。

作者的使用策略：
- `Eigor's clone` — 個人常用 project，包含身份、價值觀等 Markdown 文件
- 工作 project — 聚焦教育與社群建立任務
- 一次性 projects — 針對特定短期目標開一個新的

## 建立與設定流程

1. 點擊 Projects 旁的 `+`，可以從頭新建或 **import** 既有 project
2. 建立後，Cowork 會在你的裝置上自動產生對應資料夾結構（以前都混在 Claude 根資料夾裡）
3. 介面結構：
   - 上方：Instructions 欄位（建議放基本說明）
   - 檔案區：上傳 Markdown 文件作為 context（優先選 Markdown 而非 PDF）
   - 排程任務清單：顯示此 project 下所有排程
   - 自訂 Memories：僅針對此 project 學習，不混入整個帳戶

## 與 Claude chat interface 的連動

Cowork project 會自動參照 Claude chat interface 裡同名 project 的檔案與 memories，兩邊動態同步，不需要重複上傳。

## 實際應用範例：個人化新聞摘要

在 Eigor's clone project 內執行：`Create a personalized news brief for me`

- Cowork 自動使用 project 內的個人 context
- 搭配 web search 工具抓取最新消息
- 可遠端控制瀏覽器（需安裝 Claude 擴充）
- 完成後一鍵排程：點上方箭頭 → `Schedule` → 設定每個工作日 8am 自動執行

## 排程任務

- 建立後會自動優化 prompt，點進排程任務可見更詳細的版本
- 可手動編輯加入偏好的新聞來源
- 所有輸出都會保留在同一個 project 內，方便查找

## 費用

需要 Claude Plus（約 $20/月）。
