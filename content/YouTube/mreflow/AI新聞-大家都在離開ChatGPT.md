---
title: AI 新聞：大家都在離開 ChatGPT
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-06
source: https://www.youtube.com/watch?v=JH2ak7kS43E
---

## GPT 5.3 Instant

- 3 月 3 日發布；本質是微調與 RLHF 調整，非全新模型
- 重點：減少不必要的拒絕、降低過度防衛性的前言，直接回答問題
- OpenAI 自稱「less cringe」；可在 API 以 `gpt-5.3-chat-latest` 取用

## GPT 5.4

- 兩天後（3 月 5 日）發布，是真正的能力升級
- 主要改進：
  - 首個內建電腦使用（computer use）能力的模型，無需切換至獨立 computer use 模型
  - 更好的視覺理解與推理
  - coding 小幅優於 GPT 5.3 Codeex
  - 新增 **Tool Search**：按需查找工具定義，避免將所有工具定義預填入 prompt（節省大量 token）
  - 網路搜尋強化：可跨多輪搜尋整合資訊，處理「大海撈針」型問題
  - **1M token context window**（僅 API）
- 可用方案：Plus、Team、Pro（免費和 $8/月 Go 方案不含）
- 取代 GPT 5.2 thinking 模型

## GPT 5.4 Mini / Nano

- 輕量版，速度更快、成本更低；電腦使用能力接近完整版
- 適合 agent 背景任務（token 用量大，需控成本）
- 定位：多模型規模系統中，輕模型承接日常任務，重模型處理複雜問題

## Box AI（贊助）

- 企業內容管理平台，整合 AI 分析散落的各類檔案
- 跨檔案類型做摘要、比較、抽取、分析；模型無關（model agnostic）

## Gemini 3.1 Flash-Lite

- 設計目標：極快、極低成本；適合 API 輕量應用
- 實際案例：作者用於 YouTube 縮圖描述工具，幾乎即時產出

## NotebookLM 電影風影片摘要

- 整合 Gemini 3、Flux Pro、VO3，生成含動態動畫的影片（vs. 舊版靜態投影片）
- 目前限 Ultra 方案（$250/月）

## Google Canvas in AI Mode

- Google AI Mode 新增 Canvas，可在搜尋頁面直接生成/預覽 HTML/JS 程式碼
- 可在美國地區免費使用

## Anthropic vs. Pentagon 完整事件線

**背景**：Anthropic 設下兩條紅線：不得用於監控美國公民、不得用於全自主武器。

| 時間 | 事件 |
|------|------|
| 前幾週 | Anthropic 被 Pentagon 宣布為 supply chain risk，拒絕紅線限制 |
| 2026/02/28 | OpenAI 宣布與 Pentagon 簽約，聲稱相同兩條紅線 + 第三條（不得大規模國內監控） |
| 同日 | Anthropic 被 Trump 宣布列入黑名單 |
| 當週末 | ChatGPT 解安裝量暴增 **295%** |
| 後續 | Claude 躍升 App Store 下載第一名 |
| 持續中 | Anthropic 年化營收接近 **200 億美元**（上年倍增） |

**OpenAI 的矛盾**：
- 公開聲稱與 Anthropic 相同的紅線
- 內部備忘錄：「國防部不希望 OpenAI 對軍事行動的好壞表達意見」
- Sam Altman 仍公開支持取消對 Anthropic 的 supply chain risk 指定

**Anthropic 內部備忘錄外洩**（Information 報導）：
- 「真正的原因：我們沒有捐款給 Trump，沒有給予獨裁者式讚美，支持 AI 監管，堅守紅線」
- Dario 事後表示這是激動時刻的備忘錄，非正式立場

**後續走向**：
- Pentagon 正式發出 supply chain risk 通知（3 月 5 日）
- Anthropic 聲明將在法院挑戰此指定
- Anthropic 同時仍在進行和解談判

## 用戶流向 Claude

- TechCrunch 報導並指導如何從 ChatGPT 切換至 Claude
- Claude 推出「從其他 AI 提供商匯入記憶」功能（隱指 OpenAI）
- Claude 記憶功能從付費方案擴展至**免費方案**
- Ramp 企業支出數據：企業端 Anthropic 支出已超越 OpenAI（去年 OpenAI 遠領先）

## Qwen 3.5

- Alibaba 開放權重模型，四種大小（800M / 2B / 4B / 9B）
- 9B 以下版本可在 iPhone 離線本地執行

## Grok 4.20 Beta 2

- 改進：指令遵循、減少幻覺、科學文本品質、圖片搜尋觸發精準度

## Microsoft Phi-4-reasoning-vision

- 15B 參數開放權重多模態推理模型，擅長數學、科學推理及 UI 理解

## OpenAI Codex App for Windows

- 原本僅限 Mac，現開放 Windows；介面極簡（類 ChatGPT），適合不熟悉 VS Code/Cursor 的入門者

## Meta AI Glasses 隱私爭議

- 若未關閉分享設定，錄影內容傳至人工標注（可見到浴室、信用卡等敏感畫面）
- 英國 ICO 調查中；美國紐澤西、加州已提起訴訟

## Be Inaudible Spectre I

- 新型設備：發出干擾訊號讓周圍錄音設備無法錄製清晰音訊
- 定價約 $1,000；實際使用可能干擾合法設備（AirPods 通話等）

## Uber × Rivian 自駕計畫

- 投資 12.5 億美元，部署 10,000 輛 Rivian R2 自駕計程車競爭市場
