---
title: GSAP 與 Lenis — 捲動動畫的分工
created: 2026-04-20
updated: 2026-06-03
source: https://www.youtube.com/watch?v=sdxJEd7nqiQ
tags:
  - frontend
  - design
---

## 核心觀念

網頁捲動動畫分成**兩個層次**，各用不同 library：

- **GSAP**：控制「**捲動時發生什麼**」——元素淡入、視差、pin 住、時間軸編排
- **Lenis**：控制「**捲動本身的手感**」——平滑捲動（smooth scroll）library

這張卡只處理 scroll animation，不處理 hero section 背景影片。首屏動態素材看 [[Hero-Section-動態背景]]。

## 使用時機

適合 portfolio、產品 landing page、storytelling 長頁面，尤其是捲動手感本身就是體驗一部分的網站。

## 為什麼要搭配使用

單靠原生 scroll + GSAP 可以做出動畫，但在講究整體 scroll feel 的專案裡，底層捲動手感容易和動畫觸發混在一起。把 Lenis 墊在底層讓捲動慣性變順暢後，GSAP 的動畫觸發時機通常也更自然——拆成兩層，責任比較清楚。

## 記憶要點

> 把「**做什麼**」和「**怎麼捲**」拆成兩層，是高水準前端網站的常見做法。

## 相關連結

- [GSAP](https://gsap.com/) — 動畫引擎（ScrollTrigger 是其 plugin）
- [Lenis](https://lenis.darkroomengineering.com/) — darkroomengineering 出品的 smooth scroll library
