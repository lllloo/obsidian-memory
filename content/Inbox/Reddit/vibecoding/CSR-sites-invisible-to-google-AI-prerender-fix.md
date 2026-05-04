---
title: "Vibe-coded CSR sites are invisible to Google and AI crawlers — prerender fix"
created: 2026-05-04
updated: 2026-05-04
source: https://www.reddit.com/r/vibecoding/comments/1sysz4m/so_apparently_all_our_vibe_coded_sites_are/
published: 2026-04-29
tags:
  - reddit
  - vibecoding
  - workflow
  - best-practices
---

> **繁中摘要**：React/Vite 等 CSR 預設讓 AI bot（GPTBot / ClaudeBot / PerplexityBot）看到空 `<div id="root">` 直接離開，內容不會進訓練也不會被 chatgpt 引用；用 SSR / SSG / prerender 即可修，原作者把 Vite SPA 遷到 TanStack Start 約 10 分鐘解決。

---

## 原文重點

### 為什麼 CSR 對 AI bot 是空的

- **CSR**：browser 收空 HTML，JS 執行後填內容。React / Vite / Lovable 的預設。Crawler 看到 `<div id="root"></div>` + scripts 就走人。
- **Google**：可以 render JS 但分兩階段（先抓 HTML，後續才可能 render），中途容易失敗，schema 即使對也救不了第一輪空 HTML。
- **AI bot 更糟**：GPTBot / ClaudeBot / PerplexityBot **完全不執行 JS**。Vercel 分析半 billion 次 GPTBot crawl，零次 JS 執行——只抓原始 HTML，看到空就走，內容不會進訓練、不會被 ChatGPT 引用。

### 三個修法

- **A. Prerender**：build 時把每頁產成靜態 HTML。最簡單，Lovable 最近加了這功能。
- **B. SSR**：server 每次請求都產完整 HTML 回傳。
- **C. SSG / static site generators**：Astro、TanStack Start、Next（適當設定）。

### 實際操作（作者做法）

請 Claude Code 把 Vite SPA 遷移到 **TanStack Start**——同樣 React、同樣設計、同樣速度，但每頁都是 prerendered HTML，部署在 Cloudflare Pages，全程 10 分鐘。

### 自我驗證

1. 右鍵 → 檢視原始碼（view page source）。看到內容文字 → OK；只看到 `<div id="root"></div>` + `<script>` → 對 AI bot 隱形。
2. 跑 [Google Rich Results Test](https://search.google.com/test/rich-results) 確認 schema。

## 社群討論亮點

- 多數頂讚回應在嘲諷「這是 SSR/ISR 的舊知識，Next.js 早就在做」，技術上正確：CSR vs SSR/SSG 不是新議題，但對 vibecoder 而言是常被忽略的 production 缺陷。
- 補充：別期待 Google 自動發現你的站，要交 `sitemap.xml`。
- 結論不變：**view source 看不到內容文字 = 對 AI/Google 隱形**，這個 1 分鐘檢查值得每個 vibe-coded landing 跑一次。
