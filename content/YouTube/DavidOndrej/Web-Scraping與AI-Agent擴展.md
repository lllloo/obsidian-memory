---
title: Web Scraping 與 AI Agent 100 倍擴展能力
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-02
source: https://www.youtube.com/watch?v=wk8joeKtXBA
---

## 概覽

- Web Scraping 結合 AI Agent = 可以自動找潛在客戶、追蹤競爭對手、搜尋職缺、監控房市的全自動機器人。
- 工具選擇：**Apify**（超過 4,000 個預建爬蟲 + Agent Skill 整合）。
- 單純的 AI 模型 Web Search 工具常被 Twitter、Reddit、LinkedIn 等平台封鎖，Apify 可繞過這些限制。

## Apify 核心概念

- **Actor**：Apify 平台上的無伺服器程式，接受 JSON 輸入 → 執行任務（如爬取網站）→ 輸出結構化資料。
- Actor 分兩類：Apify 官方開發 + 第三方開發者提供（近 16,000 個選項）。
- **Agent Skills**：告訴 AI Agent 如何使用 Apify 的指令集，安裝後 Agent 直接知道如何呼叫 API。

## 安裝 Apify Agent Skill

1. 前往 apify.com 建立帳號。
2. 前往 Apify 的 Agent Skills GitHub repo，複製安裝指令。
3. 在終端機執行（全域安裝）。
4. 選擇要安裝的 Skill（全選即可）。
5. 選擇目標 Agent（OpenCode、Claude Code、OpenClaw 等均支援）。
6. 建立 `.env` 檔案，加入 `APIFY_TOKEN=<你的token>`（從 Apify Console → Settings → API & Integrations 取得）。

## 案例一：找潛在客戶（Google Maps）

- **Prompt**：「Use Apify to scrape top 20 coffee shops in Austin, Texas from Google Maps. Get their names, ratings, review counts, and addresses. Save as a CSV.」
- **結果**：1 分 45 秒取得 20 家咖啡廳完整資料，儲存為 CSV。
- 費用：$0.09 美元。
- 手動執行：至少需 60-90 分鐘。

## 案例二：競爭對手分析（Trustpilot）

- **Prompt**：「I run a solar panel installation company in Poland. Use Apify to scrape 200 reviews across my top 10 competitors from Trustpilot. Identify patterns: what people love, what's making them leave. Create a single-page HTML report with actionable insights.」
- 執行過程：
  1. 先用 Google Maps Scraper 找出前 10 大競爭對手。
  2. 切換到 Trustpilot Scraper 取得評論（自動調整為爬取歐洲競爭對手）。
  3. 共收集 1,130 則評論，5 家公司。
- **結果**：600 行 HTML 報告，包含：
  - 評分分布（75% 五星，一星負評多）
  - 客戶最愛：客服品質、產品可靠性、安裝速度
  - 主要痛點：保固拖延戰術、海外客服（菲律賓/印度）、安裝指導不足、App Bug
  - 直接可執行的改善建議
- 費用：$0.20 美元。

## 案例三：Twitter 高互動 AI 推文分析

- **Prompt**：「Using Apify, scrape 50 highest engagement AI-related tweets from top AI influencers over the past 7 days. Build a web app where I can filter by engagement, see what formats are working, and save ideas to a swipe file. Fewer lines of code the better.」
- 結果：83 則推文，建立可過濾的互動式網頁應用。
- Twitter 是最難爬取的平台之一，Apify 的 Tweet Scraper V2 仍可處理。
- 費用：$0.04 美元。

## Apify 的 Schedule 功能

- 不需要設定 Cron Job，Apify Console 內建排程功能。
- 可設定每 10 分鐘、每天、每週定時自動執行 Actor。
- 適合：定期監控競爭對手、追蹤產業動態、自動更新潛在客戶名單。

## Agent Skill 的威力

- 不需要寫任何 Web Scraping 程式碼。
- 安裝 Skill 後，只需用自然語言告知 Agent 要爬取什麼，Agent 自動選擇合適的 Actor 並處理所有細節。
- 遇到問題時（如搜尋結果有限），Agent 自動調整策略（例如把範圍從波蘭擴展到整個歐洲）。

## 安全建議

- API Token 視同密碼，勿公開分享。
- 若上傳至 GitHub，先用 Agent 更新 `.gitignore` 確保 `.env` 不外洩：
  - 「Update the .gitignore to cover the 20 most likely things in our directory that should not leak to public.」
- 在 Apify 為每個 API key 設定花費上限（防止超支或洩漏後被濫用）。

## 使用場景總結

| 使用情境 | Apify Actor |
|---------|------------|
| 找本地商家潛在客戶 | Google Maps Scraper |
| 分析競爭對手評價 | Trustpilot / G2 Scraper |
| 追蹤社群媒體趨勢 | Twitter / Instagram Scraper |
| 監控競爭對手定價 | Website Content Crawler |
| 蒐集求職資訊 | LinkedIn Job Scraper |
