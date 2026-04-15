---
title: Orchids：突破限制的 AI 應用建構工具完整示範
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-30
source: https://www.youtube.com/watch?v=Bt_3mkp7ho4
---

## 現有 AI 建構工具的問題

- 大多數 builder 只專注單一類型（Web 或 Mobile），跨越邊界就會遇到限制
- 被平台的 stack 和模板綁定，客製化困難
- 使用平台自有模型，token 費用被加成（markup），試驗成本高

## Orchids 的核心差異

**可建構的類型（同一個工作區）：**
- Web app、Mobile app、Chrome extension、Slack bot、Python script、AI agent

**自帶 AI 訂閱/API keys：**
- 支援 OpenAI、Anthropic、GitHub Copilot 等 API key
- 或直接連結 ChatGPT Plus、Claude Pro 等現有訂閱
- Orchids **不加成 token 費用**——付原廠價格，或使用已訂閱的額度

## 實際示範：10 分鐘建立咖啡品牌 Landing Page

描述需求：Morning Ritual 永續咖啡烘焙品牌，包含影片 hero、豆源故事、產品目錄、沖泡指南、大宗詢問表單，配色使用暖土色系（terracotta、cream、forest green）。

- 約 45 秒生成完整 HTML/CSS 結構
- 包含影片 hero、split layout 故事區、三個產品卡片、沖泡指南、聯絡表單
- 直接從 Orchids 部署，不需 Netlify 或 GitHub，約 30 秒上線

## 社群案例

- Bloomberg Terminal（即時市場數據和圖表）
- 建築物識別 mobile app（相機指向即識別）
- 實體機器手臂控制介面（OpenClaw）
- 自動加入會議並將筆記傳送至 Slack 的 bot
- 可玩的 CS:GO clone
- Tetris

## 費用邏輯

傳統 AI builder 對 token 加成 30%：用 $50 OpenAI credits 實際付 $65。Orchids 直通原廠價格，降低試驗成本，讓用戶不再猶豫「這個 idea 值不值得嘗試」。

## 適用對象

- 獨立開發者快速建立 MVP
- 新創團隊迭代產品
- 已有 ChatGPT Plus/Claude Pro 訂閱的用戶
- 想用企業協議的企業團隊

**不適用：** 只想要拖拉操作、不想看程式碼的用戶。
