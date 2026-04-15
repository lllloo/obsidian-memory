---
title: Google Stitch 設計工具介紹
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-04-05
source: https://www.youtube.com/watch?v=EfnIdEPF8MU
---

## Google Stitch 是什麼

Google Stitch 是 Google 推出的 AI 設計工具，用自然語言 prompt 快速產生 app/網站 UI 設計稿，並可直接匯出到 AI Studio 轉成可運行的程式碼。

## 三種設計模式

- **Ideate（構思）**：從問題出發，AI 生成解決方案的 UI。支援 Mobile App 或 Web App 類型
- **Redesign**：上傳現有截圖，用 Nana Banana Pro 模型重新設計
- **直接編輯（Direct Edit）**：對已有設計直接點擊修改元素或用 AI prompt 調整

## 使用流程

1. 選擇模式（Ideate / Redesign）
2. 選 Mobile App 或 Web App
3. 可選用設計系統（色票、字型、按鈕樣式）
4. 輸入 prompt（建議先用 Gemini 生成精緻 prompt 再貼入）
5. 可上傳參考截圖或輸入網站 URL 做為靈感來源

## 模型選擇：Flash vs Thinking

- **Flash 模型**：速度快，適合快速原型（從 prompt 到結果 60 秒內）
- **Thinking 模型**：品質更高，適合需要精緻輸出的最終設計

## 主要功能

- **設計系統**：統一色調、字型、按鈕樣式，在整個設計中重複使用
- **Canvas 操作**：可拖移元件、增加頁面
- **Direct Edit**：直接點擊文字/元素快速修改，不需輸入 prompt
- **Prototype 預覽**：點擊即可預覽 app 在手機/平板/桌面的互動效果
- **Variations**：一次生成多個設計版本做比較

## 工作流程：Stitch → AI Studio

1. 在 Stitch 完成設計稿
2. 匯出到 **Google AI Studio**（Google 的 vibe coding 平台）
3. AI Studio 自動生成對應程式碼，幾乎完全還原設計
4. 在 AI Studio 可繼續調整：加 user login、新增頁面、加深色/淺色主題、加入 Gemini AI 功能
5. 按 Publish 直接部署到雲端

## Google LIA 音樂模型

影片中也順帶介紹 Google 的 AI 音樂生成模型 **LIA**，可透過 Art List 平台使用：
- LIA 3 Pro：生成最長 3 分鐘的歌曲
- LIA 3：生成最長 30 秒
- 支援自動填詞、自訂曲風、節奏、主題
- 可用「Enhance Prompt」功能自動優化描述

## 適用場景

- 快速製作 SaaS dashboard / 內部工具原型
- 個人 app 概念驗證
- 重新設計現有產品 UI
