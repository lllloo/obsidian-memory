---
title: Gemini 3.1 動畫提示技巧
tags:
  - youtube
  - gemini
  - animation
created: 2026-04-14
updated: 2026-04-14
published: 2026-02-25
source: https://www.youtube.com/watch?v=kcOowmrVI7k
---

## 核心問題

直接用 Gemini 3.1 Pro 生成動畫，結果往往像 PowerPoint 投影片，差距在於缺乏結構化的 prompt 規劃。

## 關鍵概念：Scene-based Prompt

好動畫的 prompt 需要拆解為場景式結構，讓模型專注實作、不需同時做空間規劃：

每個場景需包含：
- **Timing**：時間長度
- **State**：各元素在該時間點的 UI 狀態
- **Effects**：關鍵效果關鍵字（如 3D perspective rotation、fading with stagger delay）
- **Action**：元素動作描述

## 為什麼要分離規劃與建構

動畫需要大量空間思考，模型不擅長同時規劃時序與實作。把兩件事分開：
1. 先用 scene-based prompt 做規劃，產出帶有時序與 UI state 的結構化 prompt
2. 再把此 prompt 給模型實作

這樣可得到 2-3 倍更好的結果。

## 使用 Super Design 的流程

1. 用 Chrome extension 複製目標 UI 為 HTML
2. 貼入 Super Design 取得 pixel-perfect 複製
3. 選取 UI → Skill Library → Animation → Product Release Demo
4. Skill 會主動問動畫細節（初始狀態、Tab 出現方式、cursor 外觀等）
5. 生成場景規劃 → 確認後開始建構

核心觀念可用於 Claude Code、Cursor 等任何 coding agent，Super Design 只是讓流程更順暢。
