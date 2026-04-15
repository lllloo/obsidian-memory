---
title: Gemini 3 Pro 全面實測：推理、編程、多模態能力展示
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-11-18
source: https://www.youtube.com/watch?v=GviLqGdp2go
---

## 模型概況

- Gemini 3 Pro 是 Gemini 3 系列的首款模型，為 thinking 型推理模型
- 在基準測試中大幅領先 Claude 與 OpenAI 的模型
- 擁有 1 百萬 token 上下文視窗（多數模型為 256K）
- 免費帳號也可使用（需手動切換到 thinking 模式）
- 付費帳號可使用 Pro 版（思考時間更長）

## 互動式儀表板建立

### 銀河視覺化器
- 自行設計 prompt 展示模型能力，生成 659 行程式碼
- 可用滑鼠縮放、移動探索銀河，有「分析特定星系區域」的 AI 功能
- 「Add Gemini Feature」按鈕自動建議新功能並加入

### 房地產抵押貸款分析儀表板
- 一個 prompt 生成含空置率、利率等互動式滑桿的分析工具
- 調整假設值時即時更新報告（含財務摘要與問題分析）
- 可直接分享（無需發布）

### 24 個月營收預測試算表
- 互動式試算表，修改假設值即時更新數字，數學計算正確
- 「Add Gemini Feature」按鈕生成不同情境的 CFO 報告

## 寫作測試

- Prompt：500 字 SEO 部落格文章，禁用 M dash
- 結果：文字自然流暢，適合非技術讀者，成功避免 M dash
- 缺點：字數為 576 字（AI 模型普遍無法精確控制字數）

## 視覺推理（多模態）

- 測試立方體數量（圖像）→ 正確答案 9，Gemini 3 Pro 答對（思考約 10 秒）
- 測試金字塔頂視圖（顏色辨識）→ 正確答案 C，Gemini 3 Pro 答對
- 之前測試中多數模型均答錯這兩題

## Coding：Neon Swarm 遊戲

- Prompt 由 Gemini 自行生成，首次嘗試出現 bug（要求 API 金鑰）
- 第二次重試：多條生命、Wave 系統、計分板均正常
- 建議在 Google AI Studio 中進行更複雜的遊戲開發

## 多媒體分析能力

- 上傳無聲截圖影片 → 正確辨識介面內容、通知、名稱
- 上傳匹克球比賽影片 → 分析技巧並提出改進建議

## 個人化設定

- **Personal Context**（Settings → Personal Context）：從歷史對話學習個人習慣
- **Custom Instructions**：設定全帳號層級的指令
- **Connected Apps**：連接 Gmail、Google Drive、YouTube 歷史紀錄等，個人化回應

## Google Search AI Mode

- 使用 Gemini 3 Pro，但目前仍有準確度問題（如飯店篩選顯示錯誤價格）
- Gemini Agent Mode（Ultra 方案）正在持續測試中，未來會有專屬影片介紹
