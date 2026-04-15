---
title: OpenAI Codex App 實測：打造 3D 動畫 Landing Page
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-06
source: https://www.youtube.com/watch?v=sC4JpJlD3aQ
---

## 重點摘要

- 目標：用 OpenAI Codex App 從零打造含 3D 車型動畫的產品 Landing Page
- 使用 Tripo 3D（AI 3D 物件生成工具）生成 3D 模型，匯出 GLB 檔後整合進 Next.js 專案
- Codex App 內建 skill creator，可設定客製化 3D 動畫工作流，這是多數 AI agent 不具備的功能
- 利用 Codex 多 agent 功能把建置任務分拆到不同 worktrees 平行執行，大幅加速開發
- 加入 GSAP scroll-triggered 動畫，並將一般元件換成 Aceternity UI（含 tilt-on-hover 等 micro-interactions）
- 使用 React Three Fiber 的 post-processing 套件為 3D 模型加上微光效果

## 相關工具

- Tripo 3D：3D 模型生成
- Aceternity UI：含 micro-interactions 的 UI 元件庫
- Post Processing（pmndrs/postprocessing）：React Three Fiber 後製效果
