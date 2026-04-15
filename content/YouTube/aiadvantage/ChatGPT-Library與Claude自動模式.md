---
title: ChatGPT Library 與 Claude 自動模式
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-27
source: https://www.youtube.com/watch?v=kG0RkK69NyA
---

## ChatGPT Library（文件庫）

- 側邊欄新增 Library 頁籤，收集所有曾上傳或生成的檔案（截圖、Excel、Word 等）
- 僅收錄 **2025-03-25 之後**的檔案，不溯及既往
- 核心用途：
  - 直接在 Library 下載檔案，不需翻找舊對話
  - 選取檔案後直接開啟新對話，作為 context 使用
  - 在新對話輸入 `@` 可直接引用 Library 中的檔案
- 作者建議：將常用 context 檔案（如個人 DNA 檔案）存入，方便隨時調用
- 介面改善：Markdown 檔案現在完整渲染，不再是純文字
- 核心思維轉變：從「文字輸入 → 文字輸出」轉向「提供文件 context → 產出結構化輸出（Excel、Word、圖表等）」

## Google AI Studio 大改版

- 合併三個產品：
  - 原 **Google AI Studio**（開發者向 Gemini）
  - **Anti-Gravity**（agentic app builder）
  - **Firebase**（資料庫與帳號驗證）
- 主要亮點：內建 Firebase 讓**多人即時協作 app** 變得空前簡單（過去最難實作的場景）
- 流程示範：
  1. 點選預設 app 範例 → 即時看到多人互動版本
  2. 按 Remix → 建立自己的副本
  3. 在 chat 調整功能 → 按 Publish 上線（需設定 billing profile）
- 作者評價：多人 app 的複雜度（server 架構 + 資料庫）被完全抽象化

## Claude Code 自動模式（Auto Mode）

- 背景：過去有 `--dangerously-skip-permissions` 指令可讓 Claude Code 跳過所有確認，但曾造成刪除資料夾等事故
- Auto Mode 為輕量改良版：
  - 內建分類器判斷每個動作的危險等級
  - 高風險操作 → 仍詢問確認
  - 低風險操作 → 直接執行，不打斷流程
- Claude 遠端電腦操控（Remote Computer Use）：允許從手機遠端操控電腦，本質上與前週的 dispatch 功能相同，只是換了品牌名稱

## 其他快報

- **Midjourney V8**：Alpha 測試中，需先評分 300 張圖；prompt 遵循度弱（要求 Marvel 英雄卻給 DC），構圖偏軸，無明顯進步
- **Anthropic 用戶研究報告**：
  - 洞察：「AI 像金錢，讓你更像你自己」
  - 主要期待：個人成長、生活管理、時間自由（不只是工作效率）
  - 最大痛點：**不可靠性**（重複相同任務時偶爾失敗），需保留人工監督
- **Gamma Imagine**：Gamma（簡報工具）新增圖形設計功能；Lovable 同樣擴展為通用文件助理，雙方都在往超級 App 方向發展
- **GPT-5.4 Mini & Nano**：開發者用小模型，速度快、成本低，可作為 agentic 系統的子 agent
- **Figma AI Agents**：對應上週 Google Stitch 的競爭動作
- **Gemini 個人化智能**：Personal Intelligence 功能開始向免費帳號推廣
- **FAI MCP Server**：連接 FAI（集合所有圖像/影片生成模型的平台）與 Claude Co-work，半自動化圖像影片生成
