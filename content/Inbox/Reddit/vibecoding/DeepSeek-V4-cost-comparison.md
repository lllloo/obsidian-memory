---
title: its not just me is it? deepseek v4 is INSANELY cheap
created: 2026-04-29
updated: 2026-04-29
source: https://www.reddit.com/r/vibecoding/comments/1sxx9dl/its_not_just_me_is_it_deepseek_v4_is_insanely/
published: 2026-04-28
tags:
  - reddit
  - vibecoding
  - ai-tools
  - deepseek
---

> **繁中摘要**：開發者實測 DeepSeek V4 在 vibecoding 工作流上的 API 成本，約一天用量燒掉 4400 萬 Pro tokens + 1400 萬 Flash tokens 僅花 $1.57（剩 $3.41 / $4.98）；但留言提供同 prompt 對照，指出 V4 Pro 解題路徑混亂、V4 Flash 失敗，廉價的代價是品質與耗時。重點是 5/5 前的 promo 價窗 + Pro 經常因 capacity 不可用。

---

## 原文重點

- 觸發背景：Codex 限額（GPT-5.5/5.4 都被 rate limit 擋住）後改用 DeepSeek V4 替代。
- 用量約一天：
  - Pro：44M tokens
  - Flash：14M tokens
  - 餘額從 $4.98 → $3.41（總耗 ~$1.57）
- 品質主觀評估：
  - Flash 「very capable alone」
  - Pro 「fantastic」，但仍不及 Opus / Codex 高檔模式
  - 比 K2.6、M2.7（同價位段）依然便宜很多

## 社群討論亮點

- 同 prompt 對照（top comment, score 23）：
  - Codex 5.4 mini：30 秒完成、修改精準
  - DeepSeek V4 Flash：5 分鐘後失敗
  - DeepSeek V4 Pro：40 分鐘完成，結果 OK 但解題路徑混亂
  - 結論：以工作工具評估時，便宜未必划算（時間成本 + 不可預測性）
- 官方策略提醒（score 6）：DeepSeek 全線降價活動到 **5/5** 為止，是促銷而非常態價格。
- 容量問題（score 2）：V4 Pro 經常因 capacity issue 無法使用，沒有自架 GPU cluster 的人會卡關。
