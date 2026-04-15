---
title: 測試首個擴散推理 LLM Mercury 2
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-24
source: https://www.youtube.com/watch?v=HNihdU8LMig
---

## 什麼是 Mercury 2

- Mercury 2 是第一個結合擴散模型（Diffusion Model）與推理能力的大型語言模型
- 一般 LLM 像打字機，逐一生成 token；擴散 LLM 先生成「雜訊」再逐步精煉，像編輯而非打字機
- 支援並行處理多個 token，速度比同類模型快約 5 倍

## 速度對比

- Mercury 2 每秒約生成 1,000 個 token
- 相較 Claude Haiku（專為速度設計）快約 5 倍
- 相較 OpenAI 速度優化模型也有明顯優勢

## 實測示範

### 跳棋遊戲
- 一個 prompt 即生成可在瀏覽器中運行的跳棋遊戲，程式碼幾乎即時生成

### 西洋棋（高推理等級）
- 高推理等級下生成約 600 行程式碼，遊戲可正常運行
- 追加 prompt 修改規則，同樣快速重寫並立即生效

### 速度測試：Mercury 2 vs Claude Haiku 4.5（含 Extended Thinking）

- 使用相同 prompt，Mercury 2 啟動後幾乎立即完成（約 250 行程式碼）
- Haiku 4.5（含 Extended Thinking）明顯花費更長時間
- 兩者程式碼量相近，Mercury 2 速度壓倒性優勢

## 定位與適用情境

Mercury 2 對標的是速度優化型模型（Haiku、GPT-Mini 等），而非 Opus/Sonnet 這類旗艦模型。

**最適合的場景：**
- **API 開發**：在 AI 驅動的 App 中作為後端推理引擎（速度快，延遲低）
- **客服 App / 語音 App**：需要接近即時回應，但也需要推理品質
- **AI Agent 建置**：agent 通常需要速度與推理雙重保障
- **搜尋功能**：需快速推理的搜尋回應

## 定價

- 輸入：每百萬 token $0.25
- 輸出：每百萬 token $0.75
- 定價具競爭力，適合高用量應用

## 試用方式

- Playground：直接測試 prompt，可調整推理等級與網路搜尋
- API：提供開發者整合
- 說明連結放在影片描述中
