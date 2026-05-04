---
title: OpenAI has been quietly classifying user type base on codex activity
created: 2026-05-04
updated: 2026-05-04
source: https://www.reddit.com/r/codex/comments/1t0bsv3/openai_has_been_quietly_classifying_user_type/
published: 2026-04-30
tags:
  - reddit
  - codex
  - ai-tools
---

> **繁中摘要**：OpenAI 在 ChatGPT 後端會替帳號打 `coding_power_user` / `professional_user` 等 user segment 標籤，可在 chatgpt.com 用 DevTools Network tab 過濾 `user_segments` 看到自己的 flag；用途偏廣告 / 分群投放，不是公開 badge。

---

## 原文重點

- **檢查方法（可重現）**：
  1. 進 [chatgpt.com](http://chatgpt.com)
  2. 按 `F12` 打開 DevTools，切到 **Network** tab
  3. filter 搜尋 `user_segments`
  4. 看到的 JSON 內含布林 flag 如 `coding_power_user: true/false`、`professional_user: true/false`
- **觀察**：作者推測自己被標 `coding_power_user` 是因「狂用 gsd flow」觸發。
- **未知觸發條件**：OpenAI 沒公開分群規則，社群推測與訂閱等級、地區、累計使用量、特定 feature 使用習慣有關。

## 社群討論亮點

- **不是 badge，是廣告分群桶**：最高評論判斷 `user_segments` 用途偏 ad targeting / cohort 投放，不是 user-facing 榮譽標籤。
- **訂閱等級可能有關**：有 $100 Pro 用戶拿到 `professional_user` 但沒 `coding_power_user`；亦有人懷疑 `coding_power_user` 與 $200 plan 或地區（US）綁定。
- **使用量重不一定有 flag**：有人重度使用仍 `false/false`，顯示分群不是線性看 usage；可能涉及行為類型（gsd flow / 特定 prompt pattern）而非總量。
