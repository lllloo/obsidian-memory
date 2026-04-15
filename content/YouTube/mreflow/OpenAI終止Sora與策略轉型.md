---
title: OpenAI 終止 Sora 與策略轉型
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-24
source: https://www.youtube.com/watch?v=PKKN5be_my0
---

## Sora 正式終止

OpenAI 官方宣布關閉 Sora，範圍不只是 App：

- Sora mobile app 下架
- Sora 開發者 API 停止
- ChatGPT 內的影片生成功能一併移除

Sam Altman 承認公司「副業太多」：「不能因為分心於 side quests 而錯失這個時機。」

### 背景：Sora 每日虧損 $1M

Sora 團隊隸屬研究部門而非產品部門，compute 資源被頻繁從其他團隊調走。Sora 的 compute 成本極高，但使用需求主要是生成迷因影片。

### Disney 合作終止

OpenAI 與 Disney 的 $1B 投資合作包含：讓用戶生成含 200+ Disney IP 角色的影片（含 Star Wars、Toy Story 等），合約為期三年。Sora 停止後，Disney 立即退出，且據報導 OpenAI 並未提前通知 Disney，甚至在宣布前一週雙方仍在合作。

## OpenAI 當前策略

### 重心轉向
- 聚焦 coding、企業生產力工具、ChatGPT 核心平台
- 將 ChatGPT desktop app、Codex、Atlas 瀏覽器整合為單一 super app
- 「Spud」新模型完成 pre-training（全新訓練，非 fine-tune 或蒸餾），Sam Altman 稱數週內發布

### Compute 分配邏輯

以 Sora 為例說明為何 compute 應集中在核心業務：

- 企業客戶最需要：coding assistant、ChatGPT 聊天、圖片生成
- Kling、Veo 3.1、SeeDance 等競品在影片生成上已超越或不輸 Sora
- Google 有廣告收入支撐，可虧本補貼影片生成；OpenAI 沒有這個空間

### 已砍除或暫停的項目
- Sora（影片生成）
- Adult mode（對話式成人內容）
- N8N 競品（自動化工作流，幾乎無人使用）
- Atlas 瀏覽器（仍存在但幾乎無人使用）
- DALL-E 平台（已被 ChatGPT 圖片平台取代）
- Search GPT（整合進 ChatGPT）

## 模型命名模式說明

作者補充解釋各版本差異：

- **全新 pre-training**（如 Spud）：從頭訓練，耗時且昂貴
- **Post-training / Fine-tuning**：在現有模型上進行額外訓練，調整輸出方向
- **強化學習（RLHF 等）**：讓輸出更接近目標
- **Distillation**（mini/nano 版本）：讓大模型產生輸出，再用這些輸出訓練小模型，保留能力但減少參數
