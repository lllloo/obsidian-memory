---
title: LLM 方案定價與 coding agent 比較
description: 主流 LLM 訂閱月費與 coding agent 三方案定價對照，依用途給經濟實惠推薦，含台幣概算、2026-09 覆核與第三方工具可用性
created: 2026-07-08
updated: 2026-09-09
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

## 2026-09-09 補記：訂閱額度能否給第三方工具用

使用者問「是不是只有 Codex 能把訂閱額度給第三方用」，答案是**三大家裡目前只有 OpenAI 明確允許，Anthropic 與 Google 都已明文禁止**。這條直接影響「併用玩法」：想用 OpenCode／OpenClaw 這類第三方 harness 吃訂閱額度，現在只剩 ChatGPT 一條路。

| 訂閱 | 給第三方 harness（OpenCode／OpenClaw 等）用 | 現況與依據 |
|---|---|---|
| ChatGPT Plus／Pro（Codex） | **允許** | 官方推「Sign in with ChatGPT」供第三方工具登入，另有「Codex for Open Source」計畫點名支援 OpenCode、Cline、pi、OpenClaw；額度受 Codex 本身用量上限約束。**強度**：部落格與計畫聲明，非契約條款，報導本身也如此提醒（[Manifest](https://manifest.build/blog/chatgpt-plus-tokens-third-party-harnesses/)、[explainx](https://explainx.ai/blog/openclaw-chatgpt-plus-pro-openai-anthropic-subscription-2026)、[OpenClaw OAuth 文件](https://docs.openclaw.ai/concepts/oauth)） |
| Claude Pro／Max／Team | **禁止** | 2026-01-09 伺服器端先擋掉 OpenCode／Cline 的 OAuth；02-19 條款新增「Free/Pro/Max 的 OAuth token 不得用於第三方工具或 Agent SDK」；04-04 起訂閱額度正式不涵蓋第三方工具。要用得開 extra usage 按量計費或改 API key。**強度**：多家科技媒體轉述，條款原文本頁未直接核對（[DEV](https://dev.to/mcrolly/anthropic-kills-claude-subscription-access-for-third-party-tools-like-openclaw-what-it-means-for-3ipc)、[MLQ](https://mlq.ai/news/anthropic-ends-paid-access-for-claude-in-third-party-tools-like-openclaw/)、[Shareuhack](https://www.shareuhack.com/en/posts/opencode-anthropic-legal-controversy-2026)） |
| Google AI Pro／Ultra（Gemini CLI OAuth；入口已由 agy 接手，見下節） | **禁止** | 2026-02 列為違反條款、03-25 起偵測強制執行，有付費 Ultra 用戶因此被停權；Gemini CLI 對 AI Pro／Ultra 的 Google 登入路徑已移除。**強度**：官方 gemini-cli 討論串為一手，其餘為媒體轉述（[gemini-cli #22970](https://github.com/google-gemini/gemini-cli/discussions/22970)、[Trending Topics](https://www.trendingtopics.eu/google-blocks-paying-ai-subscribers-using-third-party-openclaw-tool/)、[Syntackle](https://syntackle.com/blog/google-gemini-ai-subscription-with-opencode/)） |

## 2026-09-09 補記：Gemini CLI 退場，入口改為 Antigravity CLI（agy）

上表 Google 那列的「Gemini CLI」已非現行入口。Google 於 I/O 2026 宣布退休開源的 Gemini CLI，**2026-06-18 起對個人／免費層停止服務**，改由 **Antigravity CLI**（指令名 `agy`）接手——閉源 Go 單一 binary，主打多 agent 工作流，企業授權另有緩衝期。禁止第三方 harness 借用訂閱額度的政策未因換入口而改變：Google 池的唯一入口仍是官方 CLI 本身。（強度：科技媒體轉述為主，Google 官方公告原文未逐字核對——[The Register](https://www.theregister.com/ai-ml/2026/05/20/bye-bye-gemini-cli-google-nudges-devs-toward-antigravity/5243605)、[OSTechNix](https://ostechnix.com/google-is-replacing-gemini-cli-with-google-antigravity/)。）

agy 本身內建 subagent、`/schedule` 排程、`/boost` 三層編排，並可在同一份額度下切換 Gemini、Claude Sonnet／Opus 與 GPT-OSS 等模型（2026-09-09 於本機 v1.1.25 以 `agy models` 實測列出）。headless 模式 `agy -p` 在 pipe 下輸出正常（同日實測）——社群 issue #76 回報的 non-TTY 空輸出在此版本未重現，故專為繞過該 bug 的橋接工具未必需要。

## 2026-09-09 補記：agy 生態的主流用法是「被派工」，不是「當調度中心」

盤點 GitHub 上 agy 相關專案（按 star 排序）後的一致訊號：**熱度最高的都是「從別的 agent 委派給 agy」**，把它當便宜快手用——[antigravity-for-claude-code](https://github.com/yuting0624/antigravity-for-claude-code)（319★）、[agy-staff](https://github.com/keli-wen/agy-staff)（123★，是這批裡少數明確支援 Codex 而非只支援 Claude Code 的）、[claude-antigravity-agents](https://github.com/markfulton/claude-antigravity-agents)（120★）。反之，把 agy 或其他 harness 當統一調度中心的專案，星數天花板約在 300 上下，且不少已數月未動。

**判讀**：真正的高星集中在**跨 harness 的技能庫**而非調度層——[wshobson/agents](https://github.com/wshobson/agents)（39.5k★，同一份 Markdown 供 Claude Code／Codex／Cursor／OpenCode／Copilot／Antigravity 消費）、[conductor](https://github.com/gemini-cli-extensions/conductor)（3.7k★，SDD）、[google/mantis](https://github.com/google/mantis)（1.1k★，安全 review）。這與 [[pi-workflow-編排-harness-與本-vault-分野]] 的定性一致：**編排職能持續被 harness 自身吸收，獨立編排層長不大**；決定「做什麼」的技能層才是生態實際累積的地方。（強度：GitHub star 與 push 日期為 2026-09-09 一手查得，但關鍵字檢索不可能窮盡；「主流用法」是分布觀察，非抽樣調查。）

**選型含意**：若目標只是消耗閒置的 Google 池額度，直接開官方 `agy` 即可，委派層、MCP bridge 與外部排程器多為不必要的中介——agy 自帶排程，worker 端本身就有「規律」能力。

**對推薦的影響**：OpenCode Go 是 OpenCode 自家託管方案、本來就不借別家訂閱，「跑量選 OpenCode Go」不受影響。但「Claude Pro 綁第三方 harness」這條路已關，Claude 訂閱只能在 Claude Code／官方 app 內用；想在 OpenCode 裡跑 Claude 得走 API 按量。GitHub Copilot、xAI 等其他家未查。

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
