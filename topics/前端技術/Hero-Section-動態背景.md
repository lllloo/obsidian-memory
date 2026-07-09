---
title: Hero Section 動態背景
created: 2026-04-20
updated: 2026-06-03
source: https://www.youtube.com/watch?v=jQxHo9PC19Q
tags:
  - design
  - frontend
---

## 核心概念

hero section 動態背景適合 landing page / 專案官網首屏，用低成本做出第一眼記憶點。重點不是炫技，而是讓背景用極慢、細微的動態拉開質感差距，同時不干擾文案閱讀。

素材準備順序：**Image → Video → Web formats**——先做靜態主視覺，再轉短循環影片，最後輸出 WebM / MP4 並準備 mobile poster。

分階段比一次到位穩定：不要期待一個 prompt 直接生成完整 hero section。先把靜態圖做好，再控制影片動態，最後才交給前端組版。

## 實作要點

- 影片動態要極慢極細微：`keep it static and have extremely slow and subtle motion`
- 壓縮碼率與長度，控制頁面載入負擔
- 優先輸出 WebM，保留 MP4 作 fallback
- 手機版改用靜態 poster，不載完整影片

## HTML 結構

```html
<video autoplay muted loop playsinline poster="/hero-poster.jpg">
  <source src="/hero.webm" type="video/webm">
  <source src="/hero.mp4" type="video/mp4">
</video>
```

