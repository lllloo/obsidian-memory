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

## JavaScript 與框架

- [[SPA-內部跳轉為何要用-router-而非原生-a-href]] — SPA 路由與原生連結的差異

## 動效實作

- [[Hero-Section-動態背景]] — 首屏動態背景素材流程
- [[GSAP-與-Lenis-捲動動畫分工]] — scroll animation 與 smooth scroll 分工
