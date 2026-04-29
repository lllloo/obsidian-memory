---
title: The most valuable AI subscriptions/plans after Copilot nerf
created: 2026-04-29
updated: 2026-04-29
source: https://www.reddit.com/r/GithubCopilot/comments/1syqbgx/the_most_valuable_ai_subscriptionsplans_after/
published: 2026-04-29
tags:
  - reddit
  - github-copilot
  - ai-tools
---

> **繁中摘要**：在 Copilot 連串 nerf 後，OP 整理了當下五大 AI coding 訂閱方案 (Codex Pro 5x、MiniMax Starter、Gemini Pro、Opencode GO、Claude Pro Max 20x)，含價格、配額與適用情境；結論是 OpenAI Codex Pro 5x ($100/mo) CP 值最高，Claude Pro Max 20x ($200/mo) 已不如以往。

---

## 原文重點

OP 列出五大方案（依其評估排序）：

| 方案 | 月費 | 評語 |
|:-|:-|:-|
| **OpenAI Codex Pro 5x** | $100 | 配額極寬（5 月底前還有額外 boost），GPT-5.3-Codex Spark 有獨立配額；非跑 parallel agents 幾乎打不到上限。OP 認為當前最強 CP 值，搭 5.3-Codex high reasoning 「one-shot 多數任務」 |
| **MiniMax Starter** | $9 | 模型本身不算最聰明，但配額極大（約 5 小時 1500 次 request），tool calling 穩、速度快、相容性高。當作補位 workhorse |
| **Gemini Pro** | $19.99 | 推理略遜 GPT，但配額補位：Antigravity 內 3.0 Flash 無週上限（只限 5 小時視窗）；CLI / Code Assist 另有獨立 limits；附帶部分 Claude 存取 |
| **Opencode GO** | $10 | 可用 GLM 5.1、MiniMax、Kimi 等多家 open models；配額易燒完。OP 表示 GLM 5.1 推理近 Claude/GPT 等級，社群普遍說 100k context 後表現劣化，但 OP 在 150k context 仍有不錯結果 |
| **Claude Pro Max 20x** | $200 | 過去 CP 值很高，現在價值下降；只在預算充裕時推薦，且 limits 仍低於 Codex $100 方案 |

**免費補充：** Gemini CLI / Code Assist 有 free tier；NVIDIA NIM 與 Ollama 提供免費 cloud-hosted open-source models。

OP 另外 vibecoded 一個比較站 [vibecarats.com](https://vibecarats.com/)，crawler 用 MiniMax M2.7 驅動。

## 社群討論亮點

- **自架 vs 訂閱對立觀點**：有用戶選擇本機跑 Qwen3.6 處理日常 coding，認為中國開源模型「只比閉源差一點點」，$100/月「太誇張」
- **配額實況回饋**：另一用戶反映在 GPT-5.4 + Sonnet 4.6 + 偶爾 Opus 4.7 的混合用法下，Pro+ ($40/mo) 從未打到 limit，質疑 OP 對「高配額剛需」的描述
- **第三方聚合方案**：有人推薦 [nano-gpt.com](https://nano-gpt.com/subscription)（$8/mo），覆蓋市面上「幾乎所有模型」的聚合訂閱，作為更便宜的 multi-model 替代
- **Ollama Cloud** 被多人提及，但留言裡尚無實測數據可參考
