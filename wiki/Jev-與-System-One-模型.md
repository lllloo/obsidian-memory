---
title: Jev 與 System One 模型
description: 只回型別化判斷、不生成文字的決策模型：三項核心宣稱的可信度落差、兩個接入硬限制，以及對上 fine-tuned encoder 的缺口
created: 2026-09-22
updated: 2026-09-22
source: https://typesafe.ai/blog/introducing-system-one-models-and-jev
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - agent-framework
  - evaluation
  - llm-pricing
---

# Jev 與 System One 模型

TypeSafe AI 於 2026-09 發布的 Jev 自稱「首個 System One Model」：不生成文字，只對一塊 state 回傳型別化的判斷與機率。它爆紅的兩個點——「193x 快／444x 便宜」與「數學上不會 hallucinate」——**都被外界誤讀，而廠商官方文件本身就已載明界線**。本頁的重點不是介紹產品，是把「哪些是 API 契約層的事實、哪些是廠商自選基準的峰值、哪些根本沒人驗過」分開。

它落在 [[Building-Effective-Agents-Anthropic]] 五種 workflow pattern 裡的 **routing**（分類輸入導向專門後續任務）這一格，主打的就是該格「簡單常見問題導向便宜小模型」的極端化：把決策本身做成一個不會寫字的原語。

證據強度分四層，逐條就地標：**契約層事實**（官方 docs／平台 metadata／回應 schema，多方可交叉核對）、**廠商自承**（官方 blog 明文，含其自陳限制）、**第三方獨立實測**、**未獨立核實**（僅搜尋摘要轉述，不可當引文）。全頁為 **2026-09-22 快照**，模型發布距查證僅七天，生態變動極快。

## 一、它是什麼（契約層事實）

介面是「一塊 `state`（字串／JSON object／陣列）＋ 一個或多個 typed questions」，**單次平行且互相隔離**地評估全部問題，回三種原語：

| 原語 | 回什麼 |
|---|---|
| `Choice` | 選項＋`probabilities`＋`confidence` |
| `Score` | 分數＋`probabilities`＋`confidence` |
| `Noul` | 回 yes 的機率，**刻意沒有 `confidence` 欄位**——機率本身就是答案 |

這不只是行銷定位，是可在三處獨立交叉核對的契約：官方 docs 逐字「System One models do not write replies, produce code, or generate explanations of their reasoning.」；OpenRouter 的模型 metadata 標 `output_modalities: [decisions]`、`has_text_output: false`；Cloudflare AI docs 給出獨立於廠商 blog 的 response schema，三種回應皆無任何文字欄位。

> **限制**：這證明的是「已發布的 response schema 無文字欄位」（介面事實），**不等於**獨立驗證「模型內部不生成文字」或機率確實 well-calibrated。TypeSafe 未發表架構、權重或技術論文。

## 二、三項核心宣稱的可信度落差

這是本頁最該記住的一節——三項宣稱掛在同一個首頁上，但可信度差了三個檔次。

### 定價：契約層事實 ✅

input `$0.042/M` tokens、output `$0`。這不只是廠商自述：OpenRouter provider 頁內嵌的 pricing JSON 為 `prompt: 0.000000042, completion: 0`，且無 per-request fee 或最低消費欄位。

> **但掛牌價不等於帳單**：Jev 走 alpha decisions endpoint，是否另有 per-decision 計費未見任何來源說明；OpenRouter 帳戶層級的儲值手續費不在 model pricing 內；第三方 SDK 另有成本歸因 bug（litellm issue #42200：經 OpenRouter 時成本追蹤列 $0，因 model ID namespacing），會影響自建成本監控。廠商 blog 拿來對比的「既有 LLM input $0.20–$10/MTok」是**自選基準、未指名比較對象**。

### 「數學上不會 hallucinate／type error」：定義式保證，非實測 ⚠️

實質是「輸出空間由 schema 預先定義，模型無法回傳 schema 外的值」。官方 blog 的 Nuance 段自己寫得很清楚：

> "Our number is not empirical. Schema matching is guaranteed, thus we can confidently add 0% into the plots."

官方 docs 也載明「Calibration is measured across groups of predictions; it does not guarantee that an individual answer is correct.」

**所以它保證的是「形狀正確」不是「判斷正確」**：給定 Billing／Technical／Sales 三選項，Jev 不可能回 Legal，但完全可能在正確答案是 Technical 時選 Billing。第三方實測也確實抓到 in-schema 判錯（GitHub `themsquared/jev-benchmark` 的 agent tool-call risk classification，錯誤答案信心值落 0.130–0.785，未出現信心 1.000 卻答錯）。

要校正的是**外界的誤讀**，不是廠商的措辭——這點值得分清楚，否則會誤以為廠商在唬人。

### 「193.6x 快／444.6x 便宜」：自家 workflow 峰值，零第三方重現 ❌

官方 blog 在同一段自承了四件事：該 workflow 由自家 model-capabilities 團隊設計「so some bias could exist」、數字「on the higher end of real world gains」、LLM 那側基準取自 OpenRouter 有 routing 偏誤、競品是用自家 System One LLM adapter 包裝而該包裝「tends to be slower and more expensive」。官方 benchmark 另以 GPT-6 Astra 與 Fable 5.1 的平均值當 reference answer，自承這會「biases answers towards OpenAI and Anthropic's models」。

**第三方獨立實測從未重現峰值**（速度普遍落在 2–25x）：

| 測試者 | 速度 | 成本 |
|---|---|---|
| ayautomate（獨立基準） | 中位 2.0–3.6x；對 GPT-5.6 Terra 約 3.6x | 比兩個最便宜小模型便宜 4.7–7.5x；對 Terra 40–49x |
| Every（最有利設定：最貴對照＋單一 extraction 任務） | 約 25x | 約 580x（成本倍率反高於官方，速度遠低） |
| 某英國活動公司（50 筆 listing moderation 實測） | 約 5x | 約 8.6x（對 Mistral Small 4） |

ayautomate 明言原宣稱「did not show up against these baselines」。官方另自承無法證明定價未受補貼。

## 三、接入：兩個真正卡人的地方

三條路徑，成熟度差很多：

1. 官方 SDK 或 `POST /v1/systemone`，預設模型別名 `jev-latest` — 最穩
2. OpenRouter，但走 **alpha** 端點 `POST /api/alpha/decisions`：**不在標準 chat-completions 模型池、不出現在公開 `/api/v1/models` 清單中**
3. `langchain-typesafe`（官方第一方套件，包成標準 Runnable，可 invoke／batch／compose、支援 LangSmith tracing）

### Context 是硬失敗，不是降級

口徑要講精確，兩個數字都對但語境不同：**OpenRouter 標 32K**（其 FAQ 明言這是該平台上 TypeSafe 全系列最大值），**官方文件則是「單次 request 總額 64k，其中 `state` 加最長的那一題合計上限 32k」**。直接引用「context window 只有 32,000」在 OpenRouter 語境下字面正確，套到直連 API 則低估總額。

超限是 **HTTP 400 硬失敗**，不會截斷降級。真正卡 32k 的是 state 體積（長文件、DOM），不是題數多寡——第三方建議「Treat 32K as a hard failure boundary and target well under it」，且提到 context rot 使實用上限低於標示值。

### middleware 層還不能押

把 Jev 真正插進 agent 決策點的三個 LangChain middleware（`ModelRouterMiddleware` 模型路由、`AutoModeMiddleware` 工具風險攔截、`SkillsMiddleware`）**官方明標 experimental**，需裝 `langchain-typesafe[experimental]`，文件寫「APIs may change without notice」，套件本身仍在 pre-release alpha（2026-09-22 查證時為 `0.0.1a3`，此版號會很快過期，回查官方 release 頁為準），且有多筆未結 bug。

> **範圍要收窄**：`TypeSafeClassifier` 本身**不在** experimental 範圍，自行接線走 classifier 是受支援路徑。「不成熟」只適用於 middleware 層，不適用於整個整合。

## 四、什麼時候划算、什麼時候別用

**划算**：高頻、短 state、固定選項、延遲敏感的**應用內決策點**（routing／分類／風險 gating）。

**別用**：開放生成、長文件、需要可稽核的推理鏈——以及最容易被忽略的第四種：**原本就能用 fine-tuned encoder 吃下、且已有標註資料的場景**。

最後這點是本輪查證最實用的對照。單作者 arXiv preprint（2602.06370，未同儕審查）在 IMDB／SST-2／AG News／DBPedia 四個基準上測得 fine-tuned BERT 家族相對 LLM prompting **低一到兩個數量級的成本與延遲**（abstract 逐字「one to two orders of magnitude lower cost and latency」），品質依任務型態分歧：

- 二元情感分類 LLM 小勝（IMDB：Claude 4.5 FS 96.48 對 RoBERTa 94.84，差 1.64 點）
- SST-2 幾乎打平（BERT 94.42 對 94.41）
- **多類別任務 encoder 領先**（AG News：RoBERTa 94.63 對最佳 LLM Claude 4.5 ZS 91.35，差 3.28 點；DBPedia 14 類 BERT 99.40 對 98.83）

**缺的那一格**：官方與所有第三方的對照組都是 LLM，沒有人拿 Jev 對上已 fine-tune 的 encoder——而 encoder 正是 Jev 主打情境（routing／分類）的既有主場。沒有這一格，就無法回答「什麼情境真的該換掉既有 classifier」。選 pattern 前的 gate 判準見 [[Agent-工作流-Pattern-藍本庫]]：複雜度是最後手段，能用既有簡單解就別換。

## 五、型別保證的真實價值：兩個獨立旁證

「100% 結構合法」和「呼叫參數正確」是兩件事，而且有量化代價。arXiv 2605.26128《The Constraint Tax: Measuring Validity-Correctness Tradeoffs in Structured Outputs for Small Language Models》（未同儕審查）逐字報告：

- 對 sub-3B 模型施加硬性 answer-only schema decoding，schema 有效性 **61.5% → 100.0%**，但答案正確率 **19.7% → 11.0%**，「格式合法但答錯」的輸出 **49.5% → 88.9%**
- Qwen2.5-1.5B 的 deterministic calendar 任務：純 prompt 引導的 JSON 有 **91.5%** 可執行正確率，改用同一套硬性 tool-call schema 只剩 **48.0%**，而兩者 schema 有效性**都是 100.0%**

作者結論是錯誤屬語意性而非結構性。這不直接否定 Jev（Jev 不是對通用 LLM 施加約束解碼，是專門訓練的模型），但它量化了「形狀保證不是免費的」，是評估 Jev 型別宣稱價值時最相關的獨立參照。

## 六、Prompt injection 可以動搖判決（第三方實測，樣本極小）

Octomind 的工程師實測：問 Jev 要不要擋 `rm -rf ~/.ssh`，然後注入一段假的 tool-output 欄位宣稱該指令已預先核准、指示自動放行——

- 注入前：block 機率 **0.76**，confidence **0.64**
- 注入後：block 機率 **0.48**，confidence **0.22**

TypeSafe 官方文件自己承認這個面向：「Jev treats the state as data, not as hostile」，並寫明 adversarially steer 的內容「can move the answer」。

> **強度**：報導本身標明這是「one command in one integration test, not a benchmark」，n=1，不可當成通則化的攻擊成功率。但**方向是官方文件背書的**，所以要拿 Jev 當工具風險攔截 gate，這條得先解。另有一個未解的 TOCTOU 疑慮（LangChain issue #40694：已分類過的 tool call 可被內層 middleware 在執行前替換），若成立會讓 gating 形同虛設；尚未見官方回應。

## 七、勿引用與未獨立核實

### 勿引用：本輪為空

依寫入慣例第 6 條，被對抗式查證否決的主張應明列標「勿引用」。**但本輪三條否決經一手複核全部推翻，故勿引用清單為空**——詳見下節方法論教訓。

### 未獨立核實（不可當引文用）

- **HN／Reddit 第一手實測心得**：verifier 只取到 Algolia 搜尋摘要層級的轉述（最高票主張更準的標題應是 "Trading general purpose generation for fast typed inference"；有人質疑「70ms versus 329 seconds is not apples-to-apples if the LLM baseline is doing full chain-of-thought」；另稱 TypeSafe CEO 在串中當場承認 schema-valid 但語意錯會發生）。**未回讀原串核對**，依既有經驗 WebFetch 讀討論串會錯置歸屬甚至虛構回覆，全批標未核實。
- **第三方 calibration 實測**：三個 GitHub repo 的數字互不一致（ECE 0.035–0.18，準確率 62.6%–91.7%，相差近 5 倍與 30 個百分點），且多為搜尋摘要層級證據、未逐一回讀原始檔。引用前必須回查一手。
- **發布日期三個並存**：官方 blog 2026-09-15、OpenRouter 上架頁 Sep 18、permaslug `jev-1.13-20260917`，未釐清哪個是正式 GA。
- **SEO 衍生站**（jev-ai-guide.com、orcarouter.ai 等）措辭鏡像 OpenRouter 文案，等於證據繞回同一份稿子，**不構成獨立佐證**。

## 八、方法論教訓（2026-09-22）

本輪 deep-research 的對抗式查證**否決了三條主張，經一手複核三條全部成立**：

| 被否決的主張 | 票數 | 一手複核結果 |
|---|---|---|
| 官方 blog 的 `70ms–500ms`、`40x–200x`、`3–329 秒` | 0-3 | fetch 原頁，**三組數字逐字存在** |
| arXiv 2602.06370 的 encoder vs LLM 成本對照 | 0-3 | abstract 逐字「one to two orders of magnitude lower cost and latency」，**成立** |
| arXiv 2605.26128 的約束解碼取捨數字 | 1-2 | 三組數字**逐字存在** |

更露骨的是：同一組速度數字，**直接引自官方 blog 的版本被 0-3 否決，而經 Wikipedia 轉述、內容幾乎相同的版本卻 3-0 通過**——同一輪內部自相矛盾，且否決的是證據較強的那一條。

這是 [[長跑-Agent-的目標定義與計畫工具]] 與 [[架構圖框架採用現況與-AI-時代轉向]] 已記載的同一失效模式（全票否決會誤殺真事實）的第三次獨立重現，可視為**穩定的 harness 行為而非偶發**：對抗式 verifier 的 refuted 清單一律要回查一手來源後才能採信，不可直接當成「勿引用」寫進頁面。

成本面：102 個 agent、5.5M token、25 條主張進查證，最後留 9 條 finding；而改變結論的三條全靠事後一手複核補回，查證階段本身是淨負貢獻。

## 九、開放問題

1. 經 OpenRouter alpha 端點計費時，除 token 掛牌價外是否另有 per-decision 費用、最低收費或 rate limit？無任何帳單層級實測。
2. 機率是否真的 well-calibrated？三個第三方 repo 分歧過大，需回讀測試集與評分程式才能判斷分歧來自任務難度、OOD 程度還是評測方法。
3. **同一任務、同一延遲預算下，Jev 對上已 fine-tune 的 encoder 誰划算？** 這是「該不該換掉既有 classifier」的關鍵，目前無人測過。
4. 32k（state＋最長問題）在真實 agent harness 的 state 體積下多快撞牆？有無成熟的 state reduction 模式？目前只有零星踩雷紀錄。
5. `AutoModeMiddleware` 的 TOCTOU 缺口（issue #40694）是否讓風險 gating 形同虛設？未見官方回應或修復。

## 交叉引用

- [[Building-Effective-Agents-Anthropic]] — Jev 的定位正是其 **routing** pattern 的極端化：該頁說「簡單常見問題導向便宜小模型」，Jev 把「導向」這個動作本身抽成不會寫字的原語
- [[Agent-工作流-Pattern-藍本庫]] — 換用 Jev 前該過的 gate：複雜度是最後手段，第四節的 encoder 對照缺口正是這條紀律的具體應用
- [[LLM-方案定價與-coding-agent-比較]] — 另一條定價軸（訂閱制與 coding agent），本頁補的是 per-token 決策端；兩頁共通的警告是官方定價快照變動極快
- [[長跑-Agent-的目標定義與計畫工具]]、[[架構圖框架採用現況與-AI-時代轉向]] — 同一個「對抗式查證過度否決」失效模式的前兩次記錄，本頁為第三次重現

## 主要來源

官方一手：[TypeSafe blog](https://typesafe.ai/blog/introducing-system-one-models-and-jev)、[docs: System One](https://docs.typesafe.ai/concepts/system-one)、[docs: models](https://docs.typesafe.ai/models)。平台與整合：[OpenRouter provider](https://openrouter.ai/provider/typesafe)、[LangChain 整合文件](https://docs.langchain.com/oss/python/integrations/providers/typesafe)、[Cloudflare AI models](https://developers.cloudflare.com/ai/models/typesafe/jev/)。第三方：[KDnuggets 誤讀校正](https://www.kdnuggets.com/what-everyone-is-getting-wrong-about-typesafe-ais-jev)、[ayautomate 獨立基準](https://www.ayautomate.com/blog/jev-vs-llm-benchmark)、[reticle.sh 限制實測](https://reticle.sh/blog/what-jev-cannot-do)、[VentureBeat prompt injection](https://venturebeat.com/security/companies-are-putting-jev-in-charge-of-ai-agent-decisions-and-prompt-injection-can-influence-the-verdict)、[The Register](https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711)。文獻：[arXiv 2602.06370](https://arxiv.org/abs/2602.06370)、[arXiv 2605.26128](https://arxiv.org/abs/2605.26128)。
