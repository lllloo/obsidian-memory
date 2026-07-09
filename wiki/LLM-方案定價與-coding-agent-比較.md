---
title: LLM 方案定價與 coding agent 比較
description: 2026 年中主流 LLM 訂閱月費與 coding agent 三方案定價對照，依用途給經濟實惠推薦，含台幣概算
created: 2026-07-08
updated: 2026-07-09
parent: "[[wiki/01.index]]"
tags:
  - llm-pricing
  - coding-agent
  - claude-code
---

以 deep-research 多來源查證（對抗式驗證）彙整，聚焦「怎麼花錢用 LLM 最划算」，尤其是**寫程式**用途。價格為 **2026 年中（約 5–7 月）** 官方定價快照，變動極快，確切數字回官網查；台幣以 1 USD≈31 概算、未含匯差與稅費。

## 一、訂閱月費對照（主流廠）

| 方案 | 月費 (USD) | 約台幣/月 | 定位 |
|---|---|---|---|
| ChatGPT **Go** | $8 | ~NT$248 | 便宜入門 |
| Google **AI Plus** | $7.99* | ~NT$248 | *傳後續降至 $4.99 |
| xAI **X Premium**（含 Grok） | $8 | ~NT$248 | 綁 X/Twitter |
| Mistral **Pro** | $14.99 | ~NT$465 | 歐系替代 |
| **ChatGPT Plus** | $20 | ~NT$620 | 主流標配，含 Codex agent |
| **Claude Pro**（年繳 $17/月） | $20 | ~NT$620 | 含 Claude Code，coding 首選 |
| **Google Gemini AI Pro** | $19.99 | ~NT$620 | 含 2TB 儲存、Deep Research |
| **Perplexity Pro** | $20 | ~NT$620 | 每週 200 次搜尋 |
| **Copilot Pro** | $19.99 | ~NT$620 | 綁 Microsoft Office |
| SuperGrok | $30 | ~NT$930 | Grok 進階 |
| **Max / Pro 高階層** | $100 / $200 | ~NT$3,100 / 6,200 | 重度～近乎無限 |
| SuperGrok Heavy | $300 | ~NT$9,300 | 最高階 |

**關鍵洞察**：入門付費層高度收斂在 **$20 一檔**，選誰主要看生態（coding 選 Claude、搜尋選 Perplexity/Gemini、Office 選 Copilot），不是看價差。省錢入門用 ChatGPT Go $8 或 Google AI Plus $7.99 即足；輕度使用者免費層就能撐。

## 二、Coding agent 三方比較（本 vault 重點）

三者都是「訂閱綁一個 coding agent」，但模型來源差異巨大——**OpenCode Go 只能用中國實驗室的開源模型，沒有 Claude/GPT**。

| | **OpenCode Go** | **Claude Pro** | **ChatGPT Plus（Codex）** |
|---|---|---|---|
| 月費 | 首月 $5，之後 **$10** | **$20**（年繳 $17） | **$20** |
| 綁的 agent | OpenCode（開源，MIT） | Claude Code | Codex（web/CLI/IDE/iOS） |
| 能用的模型 | **僅中國開源模型**：GLM、Kimi、Qwen、MiniMax、DeepSeek 等十餘個（版本輪替快，見 [官方模型清單](https://opencode.ai/go)） | Claude 自家 Sonnet / Opus / Haiku | GPT 系列 |
| 用量限制 | 按金額計：約 $12/5hr、$30/週、$60/月 | 滾動 5 小時視窗（Pro 每視窗上百則） | 約 160 則/3hr、數千則 Thinking/週 |
| 省心度 | 要自己選模型/路由 | 開箱即用 | 開箱即用 |
| 模型天花板 | 開源 SOTA（略遜頂級閉源） | 頂級（Opus/Sonnet） | 頂級（GPT 旗艦） |

**OpenCode 本體**是最多星（16 萬+）的開源終端 coding agent，軟體免費、支援 75+ 供應商，可自帶 API key 或本機跑 Ollama（$0 邊際成本）；OpenCode Go 是其官方低價託管方案，用金額上限吸收模型成本。與 [[Claude-Code-記憶系統六層比較]] 同屬 coding agent 生態。

## 三、依用途的經濟實惠推薦

- **寫程式（要品質最穩、最省心）** → **Claude Pro $20**（綁 Claude Code）。
- **寫程式（預算優先、能接受開源模型）** → **OpenCode Go $10**，CP 值最高；複雜任務品質不如頂級閉源模型。
- **寫程式（已在 OpenAI 生態）** → **ChatGPT Plus $20**，Codex + 聊天一魚兩吃。
- **併用玩法** → OpenCode Go（跑量）+ Claude Pro（硬任務攻堅），約 $30/月涵蓋「便宜跑量 + 頂級攻堅」。
- **一般聊天/寫作** → 任一 $20 訂閱即足，省錢用 ChatGPT Go $8 或 Gemini AI Plus $7.99。
- **大量自動化（API 按量、成本敏感）** → 走 API 用經濟型模型：GPT-5-nano、Gemini Flash-Lite、grok-4-fast、DeepSeek，每百萬 token 輸入可低至 $0.05–0.25，比旗艦便宜 20–100 倍。

## 注意事項

- **時效**：LLM 定價與方案迭代極快（模型名單、額度、價格每月都可能變），OpenCode Go 模型清單尤其常換——下手前看一次官網當下版本。
- **信心分級**：訂閱與旗艦定價多有官方一手佐證（高）；經濟型/開源模型部分倚賴聚合站（中）。研究中多筆過時數字（如某些免費層模型代號、舊 DeepSeek 促銷價、MiniMax 最便宜宣稱）已在對抗驗證被否決、排除。
- **台灣在地**：實際結帳可能加課 5% 營業稅、Apple/Google 內購加成與匯差，帳單略高於換算值。

**官方查價**：[claude.com/pricing](https://claude.com/pricing)、[chatgpt.com/pricing](https://chatgpt.com/pricing)、[opencode.ai/go](https://opencode.ai/go)、[ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing)。
