---
title: AI 產碼加速下的 review 瓶頸
description: 「瓶頸從寫碼移到 review」這個共識的認知與觀測互相矛盾，四條主流約束路線的定位、適用條件與各自的證據強度
created: 2026-08-06
updated: 2026-08-06
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - evaluation
---

產碼速度上去之後，業界處方分四條路線。但在選路線之前有個更前面的問題：**「瓶頸已經從寫碼移到 review」這個大家共用的前提，認知與觀測互相矛盾**——選錯瓶頸，所有投資都會落在錯的地方。

## 現況數字

| 數據 | 來源 | 強度 |
|---|---|---|
| 90% 技術人員用 AI；>80% 自認生產力提升；**30% 對 AI 產的碼幾乎不信任** | [DORA 2025 State of AI-assisted Software Development](https://dora.dev/research/2025/dora-report/) | **high**：大樣本一手問卷 |
| AI 採用同時關聯到 delivery throughput ↑ **與** delivery instability ↑（更多 change failure、rework、更長修復時間） | 同上 | **high**：相關性，非因果 |
| 高 AI 採用團隊 merge PR **+98%**，review 時間 **+91%**，PR 平均大小 **+154%** | [Faros AI](https://www.faros.ai/blog/ai-software-engineering)，10,000 名開發者 | **medium**：廠商研究、樣本大、方法未同儕審查 |
| 導入 coding agent 後 merged PR **+39%** | Cursor 與 U Chicago 經濟學家合作 | **low-medium**：廠商自家研究，利益方向有利於自己 |
| **85%** 同意「瓶頸已從寫碼移到 review」 | GitLab 2026 AI Accountability Report | **low**：主觀認知調查，非行為觀測 |
| **>90%** 團隊仍批次部署：半數批次含 2–10 個變更、1/4 含 11–50 個 | Octopus Deploy 進行中的原始研究 | **low-medium**：單一廠商、研究未完成 |

`updated` 時的數字快照；後續回查請以各來源最新版為準。

## 核心矛盾：認知與觀測對不上

85% 的人**相信**瓶頸在 review，但 >90% 的團隊**觀測到**變更 review 完還在排隊等部署。兩者不可能同時成立：如果 review 之後還有堆積，review 就不是約束點，而**加快 review 只會把壓力更快推給真正的瓶頸**。

Octopus 那方的論點是：code review 看起來像瓶頸，只因為它的佇列是可見的；下游佇列因為「行業一直都這樣」而隱形。原文的說法是「coding wasn't the bottleneck in the first place, and it's not code review now」。

**這個爭議有一個很便宜的自我檢驗**（不需要買工具、不需要問卷）：

> 數一下你的專案裡，**已經通過 review 但還沒部署給使用者**的變更有幾個。答案是 0 或 1，那你的瓶頸真的在 review；超過 1，瓶頸在下游。

⚠️ 強度限制：這個反論目前只有單一廠商一份進行中的研究支撐，**不足以推翻 DORA 的 instability 觀測**（後者是獨立的、更大的樣本）。兩者其實可以並存——AI 確實對 review 造成壓力（Faros 的 +91% 是實測），但壓力大不等於它是**約束點**。務實的讀法是：**先跑上面那個檢驗，再決定投哪條路線**，而不是預設瓶頸在 review。

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

## 證據強度總表

| 主張 | 強度 |
|---|---|
| AI 採用關聯 throughput↑ 與 instability↑ | **high**（DORA 大樣本） |
| verification tax 的機制（省下的時間轉去稽核） | **medium-high**（1,110 份質化回答，單一組織） |
| review 壓力確實增加（時間 +91%、PR 大小 +154%） | **medium**（單一廠商、樣本大） |
| 真正的瓶頸在部署批次而非 review | **low-medium**：單一廠商、進行中研究；**但其自我檢驗方法成本近乎零，值得先跑** |
| 各家 review 工具的相對抓 bug 率 | **勿引用**：全為廠商自評，互相矛盾且方法不公開 |
| false positive 率 5–10% / 15–30% | **low**：部落格彙整，未見一手方法 |

## 關聯

- [[用測試約束-AI-產碼]] — 本頁 B 路線的完整展開：AI 產測試的四種失效模式、mutation testing 與 property-based testing 的定位差異、以及防止 agent 繞過護欄的分層。本頁列出四條路線的地景，該頁是其中唯一有一手效果實證的那條。
- [[AI-自主工作流的實證檢驗]] — 本頁講「review 該怎麼安排」，該頁講「agent 自己驗自己為何不可信」：ImpossibleBench 測到越強的模型作弊率越高、Cursor 稽核發現約三分之二的成功不是推導出來的。本頁 DORA 建議第 4 條「投資測試自動化優於優化人工 review」若要成立，必須先解掉該頁記錄的「測試本身可被 agent 篡改」問題。
- [[長跑-Agent-的目標定義與計畫工具]] — 本頁 C 路線（約束前移）的可抄措辭層：EARS 驗收判準、機器可檢的停止條件、reward hacking 三道防線。
- [[設計品質的可量化檢測]] — 同構的方法論在設計領域的版本：把「好不好」拆成可機械檢測的訊號，並承認工具只能推到及格線、及格線之後是品味。本頁的 A 路線（LLM review）面對的是同一條界線。
