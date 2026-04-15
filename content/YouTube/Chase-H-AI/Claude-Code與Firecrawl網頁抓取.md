---
title: Claude Code 結合 Firecrawl 實現無限制網頁抓取
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-29
source: https://www.youtube.com/watch?v=phuyYL0L7AA
---

## 為何原生 web fetch 不夠用

Claude Code 預設的 web fetch 只能取得靜態 HTML，遇到以下情況會失敗：
- JavaScript 動態渲染的頁面（如 SimilarWeb 的流量統計）
- 具有反爬蟲保護的網站（如 Yellow Pages，持續回傳 403）
- 大規模抓取（逐頁耗時太長）

## Firecrawl 解決方案

Firecrawl 是開源的網頁抓取工具，現在提供 CLI 工具與技能，直接整合 Claude Code：

- 以 LLM 友善的 Markdown 格式回傳資料
- 支援自訂 schema，只取需要的欄位（如：商品名稱、價格、評分）
- 不會把大量 HTML 傾倒入 context window，節省 tokens

### 八種抓取動作

| 動作 | 說明 |
|------|------|
| `scrape` | 指定 URL 抓取單頁內容 |
| `crawl` | 給起始 URL，系統性爬完整站 |
| `search` | 不知道確切 URL，先搜尋再抓取 |
| `extract` | 輸出結構化 JSON |
| `agent` | 自動決定要 search/extract/map，最強但最貴 |
| `browser_interact` | 最新功能，啟動 Chromium 實際點擊、輸入、捲動 |

## 實測比較

**測試一：SimilarWeb 競爭分析**
- Claude Code（正常 web fetch）：卡住 5 分鐘，只取到 shell，完全失敗
- Firecrawl：42 秒，取回完整流量數據、國家分布、來源分析

**測試二：Yellow Pages 抓 Nashville 水電工名單**
- Claude Code：持續收到 403 被擋，改用搜尋繞路仍失敗
- Firecrawl：53 秒，16 筆業者資料（名稱、電話、年資、服務項目）

**測試三：Amazon 4 頁商品比較**
- Claude Code：約 5.5 分鐘
- Firecrawl：45 秒

## 費用結構

- 免費方案：500 credits（一次性）
- Hobby / Standard / Growth 付費方案依規模計費

## 安裝方式

1. 前往 Firecrawl 官網建立帳號
2. 在 Claude Code 中貼上安裝頁面 URL，說「幫我安裝 Firecrawl CLI 與技能」
3. 照提示完成認證

## 開源自架版限制

自架版失去：
- 專屬 Fire Engine 反爬蟲能力
- `agent` 與 `browser_interact` 功能
- 需自行搭建 Docker 環境
