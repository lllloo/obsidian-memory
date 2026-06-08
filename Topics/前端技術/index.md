---
title: 前端技術
description: CSS 排版陷阱、scrollbar/flexbox/padding 等常見 bug、SPA 路由判斷，以及切版時反推魔術數字的檢查習慣
created: 2026-04-25
updated: 2026-06-03
tags:
  - frontend
---

前端技術實作：CSS 技巧、常見 bug、best practices、框架路由判斷與動效實作。

## CSS 技巧與陷阱

- [[sr-only-導致-body-scrollbar-的-bug]] — sr-only 導致 body scrollbar 的 bug
- [[Flexbox-min-width-auto-陷阱]] — 子元素 `min-width: auto` 導致 `flex-1` 不收縮
- [[有-Border-的容器-Padding-規則]] — `border` 容器 padding 必須放子元件，不放外層
- [[切版的反推魔術數字]] — 看到 `w-[XXX]px` 先問是否反推結果
- [[scroll-相關的-css]] — 隱藏／佔位穩定／客製 scrollbar 的常用招式
- [[Img-相關-css]] — object-fit／background-size 的 cover vs contain、aspect-ratio
- [[CSS-換行]] — overflow-wrap／word-break／white-space 差異、單行與多行省略號
- [[最後一行移除下邊框]] — 三欄佈局用 nth-last-child + nth-child(3n) 去除多餘分隔線

## JavaScript 與框架

- [[SPA-內部跳轉為何要用-router-而非原生-a-href]] — SPA 路由與原生連結的差異
- [[複製文字到剪貼簿]] — navigator.clipboard.writeText 用法與 HTTPS／使用者手勢限制
- [[前端檔案下載]] — a download 同源限制與 AJAX Blob 下載（CORS／記憶體釋放）
- [[input-限制數字與小數位]] — input 事件即時 regex 格式化 vs pattern／type=number 取捨

## 動效實作

- [[Hero-Section-動態背景]] — 首屏動態背景素材流程
- [[GSAP-與-Lenis-捲動動畫分工]] — scroll animation 與 smooth scroll 分工

## 瀏覽器相容性與坑

- [[Safari-Canvas-Size-上限]] — Safari canvas 超總面積靜默清空，html2canvas 截圖全白
- [[拿不到-Content-Disposition]] — CORS Expose-Headers／CDN 過濾導致前端讀不到下載檔名標頭
