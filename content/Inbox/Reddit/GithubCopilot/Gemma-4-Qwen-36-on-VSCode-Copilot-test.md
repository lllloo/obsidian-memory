---
title: I am not switching yet. But I tested Gemma-4 and Qwen-3.6 on VScode Copilot today and the results are much better than I thought!
created: 2026-04-27
updated: 2026-04-27
source: https://www.reddit.com/r/GithubCopilot/comments/1ss583x/i_am_not_switching_yet_but_i_tested_gemma4_and/
published: 2026-04-22
tags:
  - reddit
  - github-copilot
  - ai-tools
  - local-llm
---

> **繁中摘要**：在 24GB VRAM GPU 上以 llama.cpp + LM Studio 跑 Gemma-4 26B（MOE）與 Qwen-3.6 35B（MOE），接到 VSCode Copilot 做 scraping 專案實戰。Gemma 在 60k context 後 instruction following 崩壞、進入 thinking loop；Qwen 3.6 35B 表現較穩。

---

## 原文重點

**動機：**

- Pro+ 也常觸發 weekly rate limit；下個月起會改 token-based billing，對重度使用者基本是斷線
- 早期測 token-based 模式：Sonnet 4.5 經 OpenRouter + VSCode Copilot custom model，兩個短 request 燒掉 $50
- 家裡有多張 24GB / 一張 32GB 卡，希望本地化

**模型選擇（限 24GB 卡可載入）：**

- 首選 dense 模型 Gemma-4 31B、Qwen-3.5 27B：太慢、KV cache 太重（dense 模型 KV cache 隨 density 增長）→ 排除
- 改測 MOE 版本：Gemma-4 26B、Qwen-3.6 35B
- Quantization：weights 4-bit
  - Gemma：額外開 8-bit KV cache quant
  - Qwen：因 SWA（Sliding Window Attention）大幅省 KV cache VRAM，無需 KV cache quant

**測試任務：**

- Scraping 專案 from scratch：抓網址 / 標題 / 描述、串 web service 取當前時間、aggregate 後 append 成 markdown
- 在常用的 VSCode Copilot 環境下跑，搭配多頁 custom instructions（同等對待 GPT 5.4 / Opus 4.x）

**Gemma-4 26B 結果：**

- 開頭 instruction following 偏弱，需重複關鍵指示，幾輪後跟上
- 自行解決 libcurl 不可用 → 改 shell 包 curl binary 的 hurdle
- 偽裝舊瀏覽器直連 Google 成功
- 約 60 個 agent 內部訊息後，**context 超過 ~60k 智能急跌**：陷入 thinking loop、嚴重 instruction following loss、6 次嘗試後仍卡住

**Qwen 3.6 35B 結果：**（原文截斷，下半段未取得）

- 表現比 Gemma 穩定，作者願意繼續測

## 社群討論亮點

- 有人疑問為何尚無「專為 coding 蒸餾」的 local 模型（多數仍是 general-purpose）
- 有用戶在 Cline 中跑 Qwen 3.6 配合 yarn scale 2.5x、超過 500k context 仍能維持可接受回應速度，意外於原本預期需「crawling」
- 觀望 Taalas HC1（目前支援 8B、未來可能 27B 單機可用）作為未來低成本 local 解
