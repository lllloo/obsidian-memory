---
title: AI 產碼加速下的 review 瓶頸
description: 「瓶頸從寫碼移到 review」這個共識的認知與觀測互相矛盾，四條主流約束路線的定位、適用條件與各自的證據強度
created: 2026-08-06
updated: 2026-08-14
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - evaluation
---

產碼速度上去之後，業界處方分四條路線。但在選路線之前有個更前面的問題：**「瓶頸已經從寫碼移到 review」這個大家共用的前提，認知與觀測互相矛盾**——選錯瓶頸，所有投資都會落在錯的地方。

> 人讀版是 `docs/architecture/` 的「AI 產碼的約束」三頁組，本頁對應第 1 頁 [`ai-constraints-1-bottleneck.html`](../docs/architecture/ai-constraints-1-bottleneck.html)（另兩頁由 [[用測試約束-AI-產碼]] 與 [[Uncle-Bob-的不讀碼約束閘門]] 承接）。該組是 2026-08-09 的快照，本頁維持完整密度與後續更新。

## 現況數字

| 數據 | 來源 | 強度 |
|---|---|---|
| 90% 技術人員用 AI；>80% 自認生產力提升；**30% 對 AI 產的碼幾乎不信任** | [DORA 2025 State of AI-assisted Software Development](https://dora.dev/research/2025/dora-report/) | **high**：大樣本一手問卷 |
| AI 採用同時關聯到 delivery throughput ↑ **與** delivery instability ↑（更多 change failure、rework、更長修復時間） | 同上 | **high**：相關性，非因果 |
| 高 AI 採用團隊 merge PR **+98%**，review 時間 **+91%**，PR 平均大小 **+154%** | [Faros AI](https://www.faros.ai/blog/ai-software-engineering)，10,000 名開發者 | **medium**：廠商研究、樣本大、方法未同儕審查 |
| 導入 coding agent 後 merged PR **+39%** | Cursor 與 U Chicago 經濟學家合作 | **low-medium**：廠商自家研究，利益方向有利於自己 |
| **85%** 同意「瓶頸已從寫碼移到 review」 | GitLab 2026 AI Accountability Report | **low**：主觀認知調查，非行為觀測 |
| **>90%** 團隊仍批次部署：半數批次含 2–10 個變更、1/4 含 11–50 個 | Octopus Deploy 進行中的原始研究 | **low-medium**：單一廠商、研究未完成 |
| OSS 專案導入 Copilot 後，生產力提升主要來自**經驗較淺**的貢獻者；負擔落在核心開發者身上——**多 review 6.5% 的碼，自己的原創產出掉 19%** | [arXiv 2510.10165](https://arxiv.org/abs/2510.10165) | **medium-high**：OSS 行為數據的計量分析，非自陳；preprint 未同儕審查 |

`updated` 時的數字快照；後續回查請以各來源最新版為準。

## 核心矛盾：認知與觀測對不上

85% 的人**相信**瓶頸在 review，但 >90% 的團隊**觀測到**變更 review 完還在排隊等部署。兩者不可能同時成立：如果 review 之後還有堆積，review 就不是約束點，而**加快 review 只會把壓力更快推給真正的瓶頸**。

Octopus 那方的論點是：code review 看起來像瓶頸，只因為它的佇列是可見的；下游佇列因為「行業一直都這樣」而隱形。原文的說法是「coding wasn't the bottleneck in the first place, and it's not code review now」。

**這個爭議有一個很便宜的自我檢驗**（不需要買工具、不需要問卷）：

> 數一下你的專案裡，**已經通過 review 但還沒部署給使用者**的變更有幾個。答案是 0 或 1，那你的瓶頸真的在 review；超過 1，瓶頸在下游。

**獨立印證**：2026-02 Thoughtworks 在 Deer Valley 主辦的 Future of Software Engineering 閉門工作坊（Agile Manifesto 25 週年，Martin Fowler 主辦，約 50 位資深實踐者，Chatham House Rule，[一手報告 PDF](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future%20_of_software_development_retreat_%20key_takeaways.pdf) 公開）得出同方向但更廣的結論：

> 「It is the same speed with more frustration, because the bottleneck has shifted from engineering capacity to everything else.」

該報告點名的「everything else」包含跨團隊依賴、架構審查與專案決策，並提出兩個延伸判斷：**code review 正在被拆解**（unbundled）成依風險分級的不同處理路徑（risk tiering），以及 **decision fatigue 才是新瓶頸**——當 agent 產出快過決策者能審核批准的速度，約束就從產能移到決策容量，原本作為協調節點的中階管理者變成核准瓶頸。

⚠️ 強度限制：批次那份仍是單一廠商進行中的研究；Thoughtworks 這份則是**閉門群體共識、非量測**（且 Chatham House Rule 下無具名歸屬）。兩者利益方向不同、獨立得出同結論，合起來足以支持「別預設瓶頸在 review」，但**仍不足以推翻 DORA 的 instability 觀測**（後者是獨立的、更大的樣本）。三者其實可以並存——AI 確實對 review 造成壓力（Faros 的 +91% 是實測），但壓力大不等於它是**約束點**。務實的讀法是：**先跑上面那個檢驗，再決定投哪條路線**。

## 四條路線

### A. AI code review 工具

CodeRabbit（跨 GitHub/GitLab/Bitbucket/Azure DevOps）、Greptile（全庫 context）、Cursor Bugbot（綁 Cursor 編輯器）、Qodo、Graphite（stacked diff 起家，2025-12 被 Cursor 收購）、SonarQube／Semgrep（確定性 SAST，非 LLM）。

**選型的真正判準是 signal-to-noise，不是抓 bug 率。** 二手 benchmark 給的 false positive 率：成熟工具 5–10%、較弱的 15–30%（**low**：部落格彙整，方法未公開）。廠商自家 benchmark 互相矛盾且無法交叉驗證（例如 Greptile 宣稱在 50 個 open-source PR 上比 CodeRabbit 多抓 50%+ bug）——**勿引用任何一家的自評數字**做選型依據。

同一方向有一條利益衝突較小的證據：Cognition 在[部分收回自己的反多 agent 立場](https://cognition.com/blog/multi-agents-working)時，把「獨立 context 的 code review agent」列為可行模式，宣稱平均每 PR 抓 2 個 bug、58% 為嚴重問題（**medium**：vendor 自陳，但方向不利於其原本論述）。詳見 [[AI-自主工作流的實證檢驗]] 的多 agent 一節。

### B. 用測試約束

把驗證責任交給機械判準，而非人的注意力。這條路線的失效模式與工具定位另立專頁：[[用測試約束-AI-產碼]]——**它是四條裡唯一有一手效果實證的**，但也是最容易做成「覆蓋率表演」的一條。

### C. 把約束前移

spec-driven development（[[OpenSpec]]、Spec Kit、Kiro、BMAD 等，採用度實據見 [[長跑-Agent-的目標定義與計畫工具]]）＋ 小批次 ＋ 把 AI 回饋給 author 而非 reviewer。

### D. 部署層安全網

feature flag 把 deploy 與 release 解耦、canary 縮小爆炸半徑、error budget 觸發自動 rollback。**如果上面那個「數一下積壓」的檢驗指向下游，這條才是你的路線**，買再多 review bot 都不會有幫助。

## DORA 對 review 流程的四條建議

一手來源、訊號最強的一組（出自 [Balancing AI tensions](https://dora.dev/insights/balancing-ai-tensions/)，基於 1,110 份 Google 工程師開放式回答的主題分析）：

1. **把 AI 回饋移到 author 端**——在寫作階段就攔，比事後丟給 reviewer 有效率得多。
2. **用 context-aware 的 review agent 自動執行組織標準**，人力介入前先過一輪。
3. **小批次**——強迫把大塊 AI 生成拆成可審、可測的單位。
4. **重新質疑非同步 review 本身**：「投資 robust test automation 的 ROI，可能高於優化人工 review。」

第 4 條是這批建議裡最反直覺的，也是 A 與 B 兩條路線的分水嶺：DORA 更傾向 B。原文還補了一句更根本的——傳統 code review 是一道 quality gate，在 AI 時代值得重新想「**這道 gate 的目的本身**，是否有其他技術能承擔它的一部分」。

## 這個問題的機制根源：verification tax

DORA 的質化分析給了一個比「速度變快」更有解釋力的框架：**寫作省下的時間被重新分配到稽核與驗證**。因為模型無法表達自己的不確定性、又會用高信心輸出幻覺，工程師被迫把每次互動都當成可能有詐。受訪工程師的原話：

> 「Reviewing \[another's\] code is so much harder than writing it. AI tools are increasing the rate at which people can churn out code that needs to be reviewed…」

這解釋了為何 throughput 與 instability 會同時上升，也解釋了為何**單純加快 review 不會解決問題**——review 的成本結構是認知性的，不是流程性的。DORA 對此的總結是：AI 是**放大器**，會放大高效組織的優勢，也會放大失能組織的問題；測試實踐薄弱的團隊，AI 只會幫他們更快產生技術債。

## 這場討論在哪裡發生

三類入口，用途不同——**工程解法的密度差很多**：

**業界資深群體的閉門共識**：上述 Thoughtworks Deer Valley 報告。四條「ready for broader industry conversation」的想法是 supervisory engineering middle loop、risk tiering 作為新的核心工程紀律、**TDD 作為最強形式的 prompt engineering**、以及把 developer experience 投資重新框成 agent experience。工程解法密度最高的一份。

**大型公開討論的學術彙整**：[arXiv 2603.27249](https://arxiv.org/abs/2603.27249)（Baltes、Cheong、Treude）對 Reddit 與 Hacker News 上 **15 個討論串、1,154 篇貼文**做質化編碼，建立 15 codes、3 個主題群（Review Friction／Quality Degradation／Forces and Consequences），把現象框成 **tragedy of the commons**——個人的生產力收益把成本外部化給 reviewer、maintainer 與整個社群。最高頻三碼是 structural-drivers（26.2%）、ai-limitations、slop-mitigations。從討論中萃取出的實際反制手段值得直接參考：**PR 行數上限**（有團隊訂 500 LOC，超過不審）、**要求作者自審後才能送 peer review**、**同步 walkthrough**（「can you walk me through it and explain some of your choices?」）、跨團隊雙重 review；問責規範「It's not AI's code, it's my code」被廣泛認同，有組織寫進年度考核。該研究對工具開發者的建議與 [[用測試約束-AI-產碼]] 同向：現有工具重生成、輕驗證，應改為提供不確定性指標、**主動標示對測試檔的改動**與 provenance。codebook、corpus 與標註資料皆公開。

**公開討論本身**：HN 的大型串（數百則留言等級）主軸幾乎全在抱怨、專業身分認同與社會後果，**工程解法密度低**——用途是確認議題規模，不是找做法。較對口的少數：[Ask HN: Do you have any evidence that agentic coding works?](https://news.ycombinator.com/item?id=46691243)（2026-01，461 分／455 則）、[There is an AI code review bubble](https://news.ycombinator.com/item?id=46766961)（2026-01，351 分／249 則）、[How we exploited CodeRabbit: RCE and write access on 1M repos](https://news.ycombinator.com/item?id=44953032)（2025-08，687 分／227 則，review 工具的供應鏈風險面）。

**具名立場**：Simon Willison 的 [agentic engineering anti-patterns](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/) 第一條是「Inflicting unreviewed code on collaborators —— Don't file pull requests with code you haven't reviewed yourself」；他另造 [vibe engineering](https://simonwillison.net/2025/Oct/7/vibe-engineering/) 一詞與 vibe coding 對立，界線正是**對產出是否保持完全問責**。

⚠️ **引用這些討論時的方法約束**：HN／Reddit 的留言樹用一般網頁擷取工具讀取時，容易錯置歸屬、甚至產生原串不存在的回覆。要引用原句，一律走 HN Algolia API（`hn.algolia.com/api/v1/`）取結構化資料，或直接開原串核對，不憑摘要轉述。

## 證據強度總表

| 主張 | 強度 |
|---|---|
| AI 採用關聯 throughput↑ 與 instability↑ | **high**（DORA 大樣本） |
| verification tax 的機制（省下的時間轉去稽核） | **medium-high**（1,110 份質化回答，單一組織） |
| review 壓力確實增加（時間 +91%、PR 大小 +154%） | **medium**（單一廠商、樣本大） |
| 瓶頸不在 review，而在下游（部署批次／跨團隊依賴／決策容量） | **medium**：兩個利益方向不同的獨立來源同向——Octopus 的批次觀測（廠商、進行中）與 Thoughtworks 的資深群體共識（閉門、非量測）；**且其自我檢驗方法成本近乎零，值得先跑** |
| 負擔從產出端轉移到核心開發者（多 review 6.5%、原創產出降 19%） | **medium-high**：OSS 行為數據計量分析、非自陳；preprint |
| AI slop 是 tragedy of the commons（個人收益、社群承擔成本） | **medium**：1,154 篇貼文的質化編碼，資料公開；為詮釋框架而非因果量測 |
| 各家 review 工具的相對抓 bug 率 | **勿引用**：全為廠商自評，互相矛盾且方法不公開 |
| false positive 率 5–10% / 15–30% | **low**：部落格彙整，未見一手方法 |

## 關聯

- [[用測試約束-AI-產碼]] — 本頁 B 路線的完整展開：AI 產測試的四種失效模式、mutation testing 與 property-based testing 的定位差異、以及防止 agent 繞過護欄的分層。本頁列出四條路線的地景，該頁是其中唯一有一手效果實證的那條。
- [[AI-自主工作流的實證檢驗]] — 本頁講「review 該怎麼安排」，該頁講「agent 自己驗自己為何不可信」：ImpossibleBench 測到越強的模型作弊率越高、Cursor 稽核發現約三分之二的成功不是推導出來的。本頁 DORA 建議第 4 條「投資測試自動化優於優化人工 review」若要成立，必須先解掉該頁記錄的「測試本身可被 agent 篡改」問題。
- [[長跑-Agent-的目標定義與計畫工具]] — 本頁 C 路線（約束前移）的可抄措辭層：EARS 驗收判準、機器可檢的停止條件、reward hacking 三道防線。
- [[不讀碼時該看哪些圖]] — 當人索性不讀 agent 產的碼時，圖能承擔的那部分：把架構邊界從「reviewer 要記得看」外移成 CI 上會 fail 的依賴規則。它與本頁 DORA 建議第 1 條（把 AI 回饋移到 author 端）同構，且明確劃出界線——**圖不替代 review**，它只接手「東西有沒有放對地方」這一段，行為對不對仍歸 B 路線。該頁另以第三方實證（ICSE 2020／ISSTA 2024）否定「掃程式碼自動生架構圖」這條看似省事的捷徑。
- [[設計品質的可量化檢測]] — 同構的方法論在設計領域的版本：把「好不好」拆成可機械檢測的訊號，並承認工具只能推到及格線、及格線之後是品味。本頁的 A 路線（LLM review）面對的是同一條界線。
