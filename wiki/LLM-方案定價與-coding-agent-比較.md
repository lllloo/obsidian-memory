---
title: LLM 方案定價與 coding agent 比較
description: 主流 LLM 訂閱月費與 coding agent 三方案定價對照，依用途給經濟實惠推薦，含台幣概算與 2026-09 覆核
created: 2026-07-08
updated: 2026-09-02
parent: "[[wiki/01.index]]"
tags:
  - llm-pricing
  - coding-agent
  - claude-code
---

以 deep-research 多來源查證（對抗式驗證）彙整，聚焦「怎麼花錢用 LLM 最划算」，尤其是**寫程式**用途。價格為 **2026 年中（約 5–7 月）** 官方定價快照、**2026-09-02 覆核過一輪**（覆核結果見下方「2026-09-02 覆核」），變動極快，確切數字回官網查；台幣以 1 USD≈31 概算、未含匯差與稅費。

## 一、訂閱月費對照（主流廠）

| 方案 | 月費 (USD) | 約台幣/月 | 定位 |
|---|---|---|---|
| ChatGPT **Go** | $8 | ~NT$248 | 便宜入門 |
| Google **AI Plus** | $4.99 | ~NT$155 | 原 $7.99，2026-06-08 降價（中信心：聚合站，未見官方公告）；台灣 Google One 頁另標 NT$330／2TB，與美區數字對不上，區域差異待查 |
| xAI **X Premium**（含 Grok） | $8 | ~NT$248 | 綁 X/Twitter |
| Mistral **Pro** | $14.99 | ~NT$465 | 歐系替代 |
| **ChatGPT Plus** | $20 | ~NT$620 | 主流標配，含 Codex agent |
| **Claude Pro**（年繳 $17/月） | $20 | ~NT$620 | 含 Claude Code，coding 首選 |
| **Google Gemini AI Pro** | $19.99 | ~NT$620 | 含 **5TB** 儲存（原 2TB，2026 年內調升、價格未動）、Deep Research；台灣區 NT$650/月 |
| **Perplexity Pro** | $20 | ~NT$620 | 每週 200 次搜尋 |
| **Copilot Pro** | $19.99 | ~NT$620 | 綁 Microsoft Office |
| SuperGrok | $30 | ~NT$930 | Grok 進階 |
| **Max / Pro 高階層** | $100 / $200 | ~NT$3,100 / 6,200 | 重度～近乎無限 |
| SuperGrok Heavy | $300 | ~NT$9,300 | 最高階 |

**關鍵洞察**：入門付費層高度收斂在 **$20 一檔**，選誰主要看生態（coding 選 Claude、搜尋選 Perplexity/Gemini、Office 選 Copilot），不是看價差。省錢入門用 ChatGPT Go $8 或 Google AI Plus $4.99 即足；輕度使用者免費層就能撐。

## 二、Coding agent 三方比較（本 vault 重點）

三者都是「訂閱綁一個 coding agent」，但模型來源差異巨大——~~**OpenCode Go 只能用中國實驗室的開源模型，沒有 Claude/GPT**~~ **已被取代（2026-09-02）**：Go 的模型清單已納入 GPT 與 Grok 等閉源模型（仍無 Claude），新結論見下方「2026-09-02 覆核」。

| | **OpenCode Go** | **Claude Pro** | **ChatGPT Plus（Codex）** |
|---|---|---|---|
| 月費 | **$10**（首月 $5 的入手優惠已不見於官網） | **$20**（年繳 $17） | **$20** |
| 綁的 agent | OpenCode（開源，MIT） | Claude Code | Codex（web/CLI/IDE/iOS） |
| 能用的模型 | ~~**僅中國開源模型**：GLM、Kimi、Qwen、MiniMax、DeepSeek 等十餘個~~ **已被取代（2026-09-02）**：官網模型清單已納入 GPT 系列、Grok 與 Meta 系模型，不再只有中國實驗室，詳見下方覆核一節（版本輪替快，見 [官方模型清單](https://opencode.ai/go)） | Claude 自家 Sonnet / Opus / Haiku | GPT 系列 |
| 用量限制 | 按金額計：約 $12/5hr、$30/週、$60/月 | 滾動 5 小時視窗 + 週額度雙層 | 短視窗（數小時）+ 週額度雙層 |
| 省心度 | 要自己選模型/路由 | 開箱即用 | 開箱即用 |
| 模型天花板 | 開源 SOTA（略遜頂級閉源） | 頂級（Opus/Sonnet） | 頂級（GPT 旗艦） |

> 「用量限制」欄只描述**結構**（主流方案多為短視窗＋週額度雙層），不列具體則數——各家額度調整頻繁，實際數字回官網查。「模型天花板」一列則是廠商定位與 benchmark 排序的濃縮，讀時要打折：[[AI-自主工作流的實證檢驗]] 指出 benchmark 系統性高估實際可靠度、且越強的模型越容易在評測中作弊，故此欄可當選型起點、不可當品質保證。

**OpenCode 本體**是星數最多的開源終端 coding agent 之一，軟體免費、支援極廣的供應商清單（星數與供應商數變動快，回 [GitHub](https://github.com/anomalyco/opencode) 與官網查），可自帶 API key 或本機跑 Ollama（$0 邊際成本）；OpenCode Go 是其官方低價託管方案，用金額上限吸收模型成本。與 [[Claude-Code-記憶系統六層比較]] 同屬 coding agent 生態。

## 2026-09-02 覆核

以官方定價頁重查一輪，記錄與上方 7 月快照的差異。**未變**：Claude Pro $20（年繳 $17）與 Max 從 $100 起、ChatGPT Go $8 / Plus $20 / Pro $100・$200、OpenCode Go 的金額計用量結構。變動如下：

- **OpenCode Go 的模型清單不再限於中國開源模型**（官網一手，高信心）。2026-09-02 觀察到的 lineup 除 GLM、Kimi、Qwen、MiniMax、DeepSeek 外，另有 GPT 5.6 Luna、Grok 4.6、Hy4、LongCat、MiMo，以及 Meta 的 Muse Spark（限部分地區）。這推翻了上表原本「僅中國開源模型」的主張，連帶讓「模型天花板略遜頂級閉源」這條比 7 月時弱——但清單輪替極快，選型前務必回官網看當下版本，不要引用此處的具體型號。
- **OpenCode Go 首月 $5 優惠已不見於官網**，現為單一 $10/月（可另行 top up credit）。
- **Google AI Plus 由 $7.99 降至 $4.99**（中信心：來自聚合站摘要，我未取得官方公告一手佐證；台灣 Google One 頁面顯示的 AI Plus 為 NT$330／2TB，與美區數字對不起來，是區域差異或某一邊過時，未判定）。
- **Google AI Pro 的附帶儲存由 2TB 升至 5TB**，月費未動（台灣區頁面一手確認 5TB／NT$650）。
- **ChatGPT 訂閱價格未動**，但 Go 層在 8 月加入無限文字對話、Business 新增 Premium 層（約 $100/席年繳、$125 月繳）——皆為聚合站摘要，中信心，未見官方頁一手佐證。

**對推薦的影響**：主推薦不變（寫程式仍首選 Claude Pro，跑量仍是 OpenCode Go CP 值最高）。唯一該調的是「Go 只能用開源模型、所以只適合跑量」這個前提已鬆動，併用玩法的必要性略降。

## 三、依用途的經濟實惠推薦

- **寫程式（要品質最穩、最省心）** → **Claude Pro $20**（綁 Claude Code）。
- **寫程式（預算優先、能接受開源模型）** → **OpenCode Go $10**，CP 值最高；複雜任務品質不如頂級閉源模型。
- **寫程式（已在 OpenAI 生態）** → **ChatGPT Plus $20**，Codex + 聊天一魚兩吃。
- **併用玩法** → OpenCode Go（跑量）+ Claude Pro（硬任務攻堅），約 $30/月涵蓋「便宜跑量 + 頂級攻堅」。
- **一般聊天/寫作** → 任一 $20 訂閱即足，省錢用 ChatGPT Go $8 或 Google AI Plus $4.99。
- **大量自動化（API 按量、成本敏感）** → 走 API 用經濟型模型：GPT-5-nano、Gemini Flash-Lite、grok-4-fast、DeepSeek，每百萬 token 輸入可低至 $0.05–0.25，比旗艦便宜 20–100 倍。

## 注意事項

- **時效**：LLM 定價與方案迭代極快（模型名單、額度、價格每月都可能變），OpenCode Go 模型清單尤其常換——下手前看一次官網當下版本。
- **信心分級**：訂閱與旗艦定價多有官方一手佐證（高）；經濟型/開源模型部分倚賴聚合站（中）。研究中多筆過時數字（如某些免費層模型代號、舊 DeepSeek 促銷價、MiniMax 最便宜宣稱）已在對抗驗證被否決、排除。
- **台灣在地**：實際結帳可能加課 5% 營業稅、Apple/Google 內購加成與匯差，帳單略高於換算值。

**官方查價**：[claude.com/pricing](https://claude.com/pricing)、[chatgpt.com/pricing](https://chatgpt.com/pricing)、[opencode.ai/go](https://opencode.ai/go)、[ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing)。

## 關聯

- [[Claude-Code-記憶系統六層比較]] ——同屬 coding agent 生態；該頁比較 Claude Code 等記憶方案，本頁比較其訂閱定價與競品，合看能同時掌握「選哪個 agent」與「選哪套記憶方案」兩個決策軸
- [[Context-優先與多-agent-的適用邊界]] ——該頁的「多 agent 約 15 倍 token」是相對成本判準，本頁提供訂閱月費與 API 按量單價的絕對數字，兩頁合成「要不要堆 agent／這樣花多少錢」的完整成本決策
- [[AI-自主工作流的實證檢驗]] ——該頁 token 經濟性一節承認多 agent 的成本倍率，本頁把倍率換算成實際可付的訂閱與 API 價格
