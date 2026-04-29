---
title: "OpenAI listens to feedback: 1M context coming to GPT-5.5 in Codex"
created: 2026-04-29
updated: 2026-04-29
source: https://www.reddit.com/r/codex/comments/1sxduiu/openai_listens_to_feedback_1m_context_coming_to/
published: 2026-04-27
tags:
  - reddit
  - codex
  - ai-tools
---

> **繁中摘要**：OpenAI 在 GitHub issue 上確認 GPT-5.5 in Codex 將支援 **1M context**，呼應社群對 5.5 推出時被 cap 在 400K 的反彈；社群同時提醒長 context 可能伴隨 IQ 下降與 usage multiplier 提升。

---

## 原文重點

- 來源：[openai/codex GitHub issue #19464](https://github.com/openai/codex/issues/19464#issuecomment-4329299628)
- OpenAI 官方在留言中確認 **GPT-5.5 in Codex 即將支援 1M context window**
- 此前 GPT-5.5 在 Codex 中被 cap 在 400K（見 [[Codex-GPT-55-context-window-cap]]），與 API 版本支援 1M 有落差
- 此調整是回應社群對 5.5 context cap 與 GPT-5.4 時期 `model_context_window` 旋鈕被拿掉的不滿

## 社群討論亮點

- **Usage multiplier 待觀察**：top comment 推測大 context 模式可能比照 Fast mode，套用 **2x** 用量倍數
- **長 context 品質下降**：實作經驗在 100K~200K tokens 後模型開始「變笨」、輸出 unaligned，1M 可用但實用區間可能更窄
- **品質與容量的取捨**：多位使用者表示如果 1M context 是以「降低 IQ」為代價就寧可不要，呼應大模型 long-context 一致的退化曲線
- 社群普遍預期此變更只是時間問題，但效果是否真的優於現行 400K + auto-compact 仍存疑
