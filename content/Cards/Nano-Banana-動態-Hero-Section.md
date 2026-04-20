---
title: Nano Banana 動態 Hero Section 概念
created: 2026-04-20
updated: 2026-04-20
source: https://www.youtube.com/watch?v=jQxHo9PC19Q
tags:
  - design
  - front-end
---

## 核心概念

在網頁 hero section 放**動態影片背景**，是對抗 AI slop 外觀最有效的單一武器——視覺效果遠超 99% 的 AI 生成網站，實作成本卻低。

## 三個觀念

- **Image → Video → Code**：先用 Nano Banana Pro 生靜態圖 → 用 Kling / VO 生影片 → Claude Code 組網頁。分階段生成比一次到位穩定。
- **極慢細膩的動態**：prompt 原則「keep it static and have extremely slow and subtle motion」，避免浮誇干擾閱讀。
- **Mobile 用靜態圖替換影片**：不讓手機載完整影片，減流量、提載入速度。

## 設計原則

- 多次迭代，不期望一次成功
- 目標是 **wow factor，不是壓倒觀看者**——less is more
- 生成工具關閉 enhance，保持對 prompt 的控制

## 相關工具

- [Nano Banana Pro](https://nanobanana.ai/) — 圖片生成
- [Kling](https://klingai.com/) / [VO](https://deepmind.google/technologies/veo/) — 影片生成
- [21st.dev](https://21st.dev/) — 預建元件庫，搭配 Claude Code 加速組頁

## 靈感來源

Pinterest、Dribbble、MidJourney、[[Awwwards-找前端設計靈感|Awwwards]]
