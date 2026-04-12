---
title: Claude Code + Firecrawl = UNLIMITED Web Scraping
tags:
  - youtube
  - claude-code
  - firecrawl
  - web-scraping
  - ai
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/phuyYL0L7AA
---

Claude Code 內建的 web fetch 無法處理 JavaScript 渲染和反爬蟲保護，Firecrawl 提供 CLI + skills 解決這個問題。

## 為何需要 Firecrawl

Claude Code 原生 web fetch 的限制：
- 只讀取 HTML，無法處理 JavaScript 渲染的內容
- 遇到反爬蟲保護（如 Yellow Pages）直接拿到 403
- 大規模爬取時速度慢、token 耗費高

Firecrawl 將網頁資料以 **LLM 友好的 Markdown 格式**回傳，可設定 schema 只取需要的欄位。

## 八種 Actions

| Action | 說明 |
|--------|------|
| **scrape** | 給定 URL，抓取單頁內容 |
| **crawl** | 給定起始 URL，系統性爬取整站 |
| **search** | 不知道 URL，讓 Firecrawl 先找再抓 |
| **extract** | 指定 JSON schema 輸出結構化資料 |
| **agent** | 最強大，自動決定用哪種 action（耗最多 credits） |
| **browser_interact** | 最新功能，模擬真實瀏覽器操作（click/type/scroll） |

## 實測對比

| 測試 | 普通 Claude Code | Firecrawl |
|------|-----------------|-----------|
| SimilarWeb（JS 渲染）| 4.5 分鐘後卡住，幾乎無資料 | 42 秒，完整資料 |
| Yellow Pages（反爬蟲）| 持續 403 錯誤 | 53 秒，16 筆結果 |
| 4 個 Amazon 頁面 | ~5.5 分鐘 | 45 秒 |

## 費用

- **Free**：500 credits（一次性）
- Hobby / Standard / Growth 階層
- **開源版**：可自架，但失去：反爬蟲保護（Fire Engine）、agent/browser_interact 功能、需要 Docker

## 安裝

複製 Firecrawl 文件頁面內容，丟給 Claude Code 安裝 CLI + skills，一次驗證即可。

## 使用場景

- 競品分析、市場研究
- 批量抓取定價/評分資料
- 潛在客戶資料擴充
- 任何需要大規模、可靠爬取的任務
