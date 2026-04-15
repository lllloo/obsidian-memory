---
title: OpenAI 在說謊
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-26
source: https://www.youtube.com/watch?v=l-gfVIm0Xn8
---

## 事件起因：OpenAI 發布「如何用 GPT-5.4 設計精美前端」文章

OpenAI 發布了一篇文章，聲稱透過正確引導，可以用 GPT-5.4 做出「production-ready」的前端設計，並提供了幾個範例。Theo 認為這些範例全是「卡片海」（card slop），並認為這篇文章是對用戶的誤導。

## GPT-5.4 前端設計問題：卡片成癮

- GPT-5.4 的所有設計輸出幾乎都是同一個版型：大量卡片、相同布局
- OpenAI 在他們自己的設計 skill 中寫了 13 次「no cards」，模型仍然一直輸出卡片
- 與 Kimi K2.5、Opus 4.6、Gemini 3.1 比較，GPT 的設計多樣性和品質均居末

## 各模型前端設計能力排行（Theo 觀點）

| 模型 | 設計品質 | 多樣性 | 備注 |
|------|---------|--------|------|
| Opus 4.6（含設計 skill）| 最佳 | 中等（約 10 種版型）| 偶爾亂加 pill 標籤 |
| Gemini 3.1 Pro | 良好 | 最高（約 15 種）| 需要多次嘗試才穩定 |
| Kimi K2.5 | 良好 | 中等 | 開源模型，效果超乎預期 |
| GPT-5.4 | 最差 | 最低（約 4 種版型）| 全是卡片，幾乎無法使用 |

## 為什麼 GPT 模型前端設計能力差

Theo 的推測：

1. **訓練資料問題**：OpenAI 購買的 UI 訓練資料版本較舊，Anthropic 和 Google 可能購買了更新的資料集
2. **RL 模板過少**：強化學習的參考「好設計」樣本數量太少（約 4 種），且這些樣本本身就有過多卡片
3. **新技術適應慢**：GPT 在新版 Tailwind、Svelte、Convex 等也有類似問題，說明訓練資料更新較慢

## 設計 Skill 的重要性

Anthropic 的 Claude frontend 設計 skill（`frontend-design`）：

- 核心規則：避免通用 AI 設計風格（Inter/Roboto/Aerial 字體、紫色漸層白底、可預測的布局）
- 強調：品牌優先、排版選擇獨特字體、避免 pill 標籤叢集
- 這個 skill 對 GPT-5.4 效果有限，用在 Opus/Gemini 才能真正發揮

## Theo 的建議

- 前端設計任務：優先用 Opus 4.6（最穩定）或 Gemini 3.1 Pro（多樣性更高）
- GPT-5.4 適合：底層邏輯、工具使用、複雜推理——不適合 UI 設計
- OpenAI 這篇文章應該下架，它讓不知情的用戶誤以為是自己 prompt 技巧不好，實際上是模型能力本身的限制
