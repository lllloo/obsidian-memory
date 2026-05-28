---
title: Nano Banana 動態 Hero Section 概念
created: 2026-04-20
updated: 2026-04-25
source: https://www.youtube.com/watch?v=jQxHo9PC19Q
tags:
  - design
  - frontend
---

## 核心概念

在網頁 hero section 放**動態影片背景**，通常是很有效的差異化手段：能快速拉開與常見 AI 模板的距離，而且不一定要先做超複雜的互動工程。

## 三個觀念

- **Image → Video → Code**：先用 Nano Banana 生靜態圖 → 用 Kling / Veo 生影片 → Claude Code 組網頁。分階段生成比一次到位穩定。
- **極慢細膩的動態**：prompt 原則「keep it static and have extremely slow and subtle motion」，避免浮誇干擾閱讀。
- **Mobile 用靜態圖替換影片**：不讓手機載完整影片，減流量、提載入速度。

## 設計原則

- 多次迭代，不期望一次成功
- 目標是 **wow factor，不是壓倒觀看者**——less is more
- 若生成工具的 enhancement 類選項讓結果太花，可先關掉或調低，保留對 prompt 的控制

## 相關工具

- [Nano Banana](https://ai.google.dev/gemini-api/docs/image-generation?hl=zh-tw) — 圖片生成
- [Kling](https://kling.ai/) / [Veo](https://deepmind.google/models/veo/) — 影片生成
- [21st.dev](https://21st.dev/) — 預建元件庫，搭配 Claude Code 加速組頁

## 靈感來源

Pinterest、Dribbble、Midjourney、[[bookmark-Awwwards-前端設計靈感站|Awwwards]]