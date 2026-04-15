---
title: Cursor 真的偷了 Kimi 嗎
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-22
source: https://www.youtube.com/watch?v=QGnKTRtEH50
---

## Composer 2 是什麼

Cursor 推出了 Composer 2，一個僅在 Cursor 內使用的自訂模型，專門針對程式碼任務微調。Theo 是 Cursor 的投資人，但強調沒有受到任何報酬。

## 爭議起因：API 路徑洩漏模型名稱

有人在測試 Cursor API 時，發現新模型的名稱包含 `kimi-k2.5-rl-0317-s515-fast`，暗示 Composer 2 是基於 Moonshot AI 的 Kimi K2.5 所進行的 post-training。

## Cursor 的訓練策略

- Cursor 並非從頭預訓練，而是以 Kimi K2.5 為基礎，投入約 3 倍的額外算力做 post-training 和強化學習（RL）
- 訓練資料來自 Cursor 龐大的使用者 chat history（關閉 privacy mode 的用戶資料）
- 目標：讓模型在程式碼任務上達到 frontier 水準，同時大幅降低成本

## 成本與性能

- 定價：約 $0.50/M tokens in，$2.50/M tokens out（Opus 4.6 的 1/10）
- 速度：80–100 TPS（tokens per second），極快
- 性能：在 Terminal Bench 2 超越 Opus 4.5/4.6，設計能力亦不差

## 授權爭議

Kimi K2.5 採用修改版 MIT 授權，規定：若商業產品月活超過 1 億或月收入超過 200 萬美元，需在 UI 顯著標示「Kimi K2.5」。

Cursor 透過推理合作夥伴 Fireworks AI，主張 Fireworks 已符合授權揭露要求，因此 Cursor 本身不需在 UI 標示。Kimi 官方事後也承認此安排是「授權合規的商業合作」。

## Theo 的觀點

- Cursor 確實對 Kimi K2.5 做了大量工程投入（3 倍算力的 RL），Composer 2 已是完全不同的模型
- 但未主動揭露起點是 Kimi K2.5 的做法不在開源精神之內
- 長期影響：此先例可能讓中小型開源模型實驗室重新考慮是否繼續發布 open-weight 模型
- Cursor 最終只賺到比 Moonshot 更多的錢，而花在 post-training 上的算力費用可能已超過 Moonshot 的整體營收

## Anthropic 的補貼問題背景

Claude Code Max（$200/月）可消耗約 $5,000 的推論費用（25 倍補貼）。這迫使 Cursor 必須找到更便宜的推論方案，open-weight 模型是解法之一。
