---
title: 前端設計
created: 2026-03-25
updated: 2026-04-21
tags:
  - frontend
  - design
  - moc
---

AI 時代前端設計相關筆記總索引。涵蓋工作流方法論、設計工具、動效實作、CSS 切版規則。

## 工作流方法論

- [[Claude-Code-前端設計工作流]] — AI 設計七層級、工具速查、陷阱（整合 4 篇 YouTube）
- [[Stitch]] — Google Stitch MOC（視覺設計生成工具）

## 設計系統與動效

- [[DESIGN.md-規格]] — DESIGN.md 格式、9 區段、awesome-design-md 品牌範例庫
- [[動效與互動]] — Hero 動態背景、GSAP + Lenis 捲動動畫分工

## CSS 切版原則

- [[避免魔術數字]] — 固定 px 寬度的使用原則，應改用語意化寫法
- [[有-Border-的容器-Padding-規則]] — 有 border 的容器，padding 應放到子元件

## Pencil 設計稿整合

- [[Pencil-讀取規則]] — 遞迴讀取所有節點，讀 ref 必須確認 descendants override
