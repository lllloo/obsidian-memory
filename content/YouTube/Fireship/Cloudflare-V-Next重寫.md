---
title: Cloudflare 用 Vite 重寫 Next.js：V-Next 解析
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-02
source: https://www.youtube.com/watch?v=abbeIUOCzmw
---

## 背景：Vercel vs Cloudflare

- Next.js 最大弱點：部署目標有限，在 Vercel 之外的平台（Cloudflare、Netlify 等）運作不穩定
- 現有解法 **OpenNext**：對 `next build` 輸出重新封裝以適應其他平台，但脆弱且容易出錯

## Cloudflare 的解法：V-Next

- 直接以 **Vite** 從頭重寫 Next.js API，而非在現有輸出上做處理
- 使用 AI 開發：**1 天**完成基本 SSR、middleware、server actions、streaming；**第 3 天**部署至 Cloudflare Workers 並完成 client hydration；整週花費約 **$1,100 AI tokens**
- API 覆蓋率達 **94%** 的 Next.js API
- 底層使用 **Rolldown**（Rust 基礎的 bundler），提升效能

## 效能比較

- Cloudflare 自家 benchmark：V-Next production 建置時間比 Next.js 快 **4.4 倍**，client bundle 小 **57%**
- 測試者在實際網站上測出 **5x** 更快的建置速度
- 主要原因：Vite + Rolldown 的架構優勢

## Vercel 的反應

- Vercel CTO 稱之為「slop fork」
- Vercel 創辦人 Guillermo Rauch 發佈 Cloudflare to Vercel 遷移指南，並揭露安全漏洞

## 遷移方式

- Cloudflare 提供 agent skill，安裝後可輔助遷移至 V-Next
- 主要需注意的相容性問題：
  - `package.json` 加入 `"type": "module"`（所有 JS 視為 ES modules）
  - 含 JSX 的 `.js` 檔改為 `.jsx` 副檔名（Vite 要求）

## 評價

> 關於 bleeding edge 軟體，永遠記住：流血的人是你自己。
