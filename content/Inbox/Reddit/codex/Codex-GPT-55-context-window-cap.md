---
title: The 1 Million context rugpull by Codex and OpenAI. New max is (258k).
created: 2026-04-28
updated: 2026-04-28
source: https://www.reddit.com/r/codex/comments/1swqdt9/the_1_million_context_rugpull_by_codex_and_openai/
published: 2026-04-27
tags:
  - reddit
  - codex
  - ai-tools
---

> **繁中摘要**：Codex 上 GPT-5.5 的 context window 被鎖在 400K（實務最高約 258K），即使同一模型在 API 上支援 1M。原本 GPT-5.4 可用 `model_context_window` 推到 1M + auto-compact at 512K 的彈性已不存在；OpenAI 另發了一份 harness engineering 文件作為對應 workaround。

---

## 原文重點

- 對應討論：[openai/codex issue #19464 留言](https://github.com/openai/codex/issues/19464#issuecomment-4323216312)
- 抱怨內容（由留言補充）：
  - GPT-5.5 在 Codex 中被 cap 在 **400K context window**，但同一模型的 API 版本支援 **1M**。
  - GPT-5.4 時期，使用者可以透過 `model_context_window` 把 context 拉到 1M、設定 auto-compact at 512K，對大型 repo 與長 session 友好。
  - 5.5 之後此調整旋鈕「等同被拿掉」。
  - OpenAI launch page 標示 GPT-5.5 in Codex = 400K，但實測 model catalog 行為更接近 258K。

## 社群討論亮點

- 多數高分留言認為長 context 本身是 anti-pattern：benchmark 上長 context 退化明顯，過某個點之後反而變笨；此次降 cap 不一定是壞事。
- **官方對應 workaround**：把 [OpenAI 釋出的 harness engineering 文](https://openai.com/index/harness-engineering/) 直接貼進 Codex，並下指令「follow this and update my project」，留言回報效果良好。可作為 long context 縮窗後的補強做法。
- 部分留言質疑 "rugpull" 用詞過重，因為官方文件本來就標 400K，但對既有靠 1M 設定跑大 repo 的人衝擊真實存在。
