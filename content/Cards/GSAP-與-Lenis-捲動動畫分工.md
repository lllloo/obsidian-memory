---
title: GSAP 與 Lenis — 捲動動畫的分工
created: 2026-04-20
updated: 2026-04-20
source: https://www.youtube.com/watch?v=sdxJEd7nqiQ
tags:
  - front-end
  - design
---

## 核心觀念

網頁捲動動畫分成**兩個層次**，各用不同 library：

- **GSAP**：控制「**捲動時發生什麼**」——元素淡入、視差、pin 住、時間軸編排
- **Lenis**：控制「**捲動本身的手感**」——平滑捲動（smooth scroll）library

## 為什麼要搭配使用

兩者**互補**：Lenis 讓底層捲動慣性變順暢後，GSAP 的動畫觸發時機也更自然；單用 GSAP 在原生 scroll 上會覺得動畫生硬。

## 記憶要點

> 把「**做什麼**」和「**怎麼捲**」拆成兩層，是高水準前端網站的常見做法。

## 相關連結

- [GSAP](https://gsap.com/) — 動畫引擎（ScrollTrigger 是其 plugin）
- [Lenis](https://lenis.darkroom.engineering/) — Studio Freight 出品的 smooth scroll library
