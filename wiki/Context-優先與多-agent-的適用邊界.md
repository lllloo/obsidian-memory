---
title: Context 優先與多 agent 的適用邊界
description: 以 Anthropic、Cognition 與 MAST 證據界定多 agent 的效益與代價，建立 context 優先的實務決策判準
created: 2026-07-14
updated: 2026-07-17
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - agent-framework
  - context-engineering
---

# Context 優先與多 agent 的適用邊界

一個實務決策判準頁：面對「要不要為某任務建/找一個專用 agent、或堆多個 agent」時該怎麼想。核心命題——

> **能力來自 context 注入（prompt／`CLAUDE.md`／skill／memory），agent 的「數量與編排」是另一個維度的選擇，本身不提供知識。堆 agent 有可量測的實證代價與邊界。**

本頁把 vault 既有的 Anthropic 第一方論述，與**兩個非 Anthropic 的獨立/對立來源**（Cognition 實務立場、UC Berkeley MAST 失敗實證）並置，刻意平衡 [[Agent-Harness-Engineering-框架綜述]] 自陳的「來源高度集中 Anthropic」偏倚。

## 核心判準：知識問題，還是編排問題？

動念「要不要一個 agent」時先分類（**此二分框架為本頁綜合，非任一來源原文直述**；其組成零件各有下方一手佐證）：

- **知識/慣例不足**（agent 不懂某領域規範、缺專案脈絡）→ 這是 **context 問題**，解法是寫進 `CLAUDE.md`／做成 skill／補 prompt，任何 agent 都能吃到。**不需要新 agent**。
- **純編排需求**（要 context 隔離、要平行 fan-out、要限定工具/權限）→ 這才是 **agent 編排問題**，才考慮 subagent。而且多數編排需求，內建的通用 agent 臨時派一個就夠，未必要落成專用 agent。

## 佐證①：能力來自 context

- [[Building-Effective-Agents-Anthropic]]：agentic system 的基石是被 **retrieval／tools／memory 增強的 LLM**——能力來源是這些增強，不是「哪種 agent」。同頁主張「**先直接用 LLM API，許多模式幾行程式就能實作**」，反對為了能力去堆框架/抽象。
- [[Agent-Harness-Engineering-框架綜述]] 的 context engineering 節：context engineering 是「策展與維護最佳 token 集合的策略」——**agent 表現等於你餵進去的 context 品質**。
- **跨陣營共識**：Cognition 的 Walden Yan 亦言「At the core of reliability is Context Engineering」，並稱它「effectively the #1 job of engineers building AI agents」（[Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents)）。Anthropic 與 Cognition 在架構上對立，卻在「context engineering 是核心」上收斂——這條共識本身就是強訊號。

## 佐證②：subagent 提供的是「編排」，不是知識

- [[Agent-Harness-Engineering-框架綜述]]：long-horizon 三技術之一是 **sub-agent 隔離——用乾淨 context 深入工作、只回傳約 1,000–2,000 token 摘要**。價值是隔離，不是它更懂。
- [[多智能體研究系統-Anthropic]]：「**搜尋的本質是壓縮**」——subagent 各擁獨立 context 平行探索、濃縮回傳；`separation of concerns` 降低 path dependency。這是「平行 fan-out＋隔離」的一手描述，代價是多 agent 約 **15 倍 token**。

## 反面與邊界：堆 agent 的可量測代價

vault 外的獨立證據，界定「多 agent 何時反而更糟」：

- **Cognition 的單執行緒原則**（實務者經驗，Devin 團隊）：反對多 agent 的核心是「**決策分散、context 無法在 agent 間充分共享**」，導致相互衝突的結果。提出兩條 context engineering 原則——①「**Share context, and share full agent traces, not just individual messages**」；②「**Actions carry implicit decisions, and conflicting decisions carry bad results**」。最簡遵循法就是「**single-threaded linear agent**」。（強度：**實務者經驗值、非受控實證**；且立場**有演進**——作者一年後修正為「multi-agent 在**寫入保持單執行緒、額外 agent 貢獻智能而非行動**時才有效」，引用時勿當靜態教條；演進脈絡詳見 [[AI-自主工作流的實證檢驗]] 的多 agent 節。）
- **MAST 失敗 taxonomy**（UC Berkeley Sky Lab，[arXiv 2503.13657](https://arxiv.org/abs/2503.13657)）：分析 7 個 SOTA 開源多 agent 框架的 **1,642 條執行 traces**，失敗率 **41%–86.7%**；歸納 14 種失敗模式、3 類，其中**系統設計問題佔 44.2%**、其餘為 agent 間錯位與任務驗證。taxonomy 由 150 traces 建構、標註者一致性 kappa=0.88。（強度：**獨立學術 preprint（含 OpenReview）**、樣本限開源 MAS 框架與 2025-03 當時模型；是本主題目前最紮實的第三方失敗實證。）
- **協調成本非線性**：業界分析普遍指出協調失敗點隨 agent 數暴增（如 4 agent→6、10 agent→45 個潛在失敗點），結構不良的多 agent 可放大錯誤逾 [17 倍](https://towardsdatascience.com/why-your-multi-agent-system-is-failing-escaping-the-17x-error-trap-of-the-bag-of-agents/)。（強度：**二手業界分析/部落格**，數字為示意量級非嚴謹測量，僅作方向佐證。）

## 綜合洞察：Anthropic vs Cognition 不是矛盾，是適用域之分

表面上 [[多智能體研究系統-Anthropic]]（多 agent 內部評測**高 90.2%**）與 Cognition（別建多 agent）針鋒相對（多家報導以「architecture wars」框之，如 [CTOL](https://www.ctol.digital/news/ai-leaders-clash-agent-architecture-cognition-anthropic-strategies/)）。但兩者其實描述**不同任務類型**，可用一條判準統一：

> **多 agent 只在任務「可高度平行、讀重於寫、協調是確定性而非湧現」時才划算。**

- Anthropic 的成功案例正是**讀重、可平行的研究查詢**（subagent 各自搜尋、唯讀、無需彼此的寫入決策一致）——落在判準的甜蜜點。
- Cognition 警告的是**寫重、需決策一致的生成/coding**（多 agent 平行寫入 → 隱含決策衝突 → 結果不一致）——落在判準的雷區。
- MAST 的獨立實證把這條判準坐實：失敗集中於「系統設計」與「agent 間錯位」，正是寫重、需協調場景的失效模式。

**推論**：對 coding（寫重、需全域一致）這類任務，優先單執行緒 agent＋把慣例寫進 `CLAUDE.md`；只有明確可平行、唯讀的子工作（掃描、搜尋、審查）才拆 subagent。這也解釋了為何「為 Vue 開發建一個全包的多能 agent」是反模式——日常寫碼是寫重任務，隔離/平行幫不上，慣例入 `CLAUDE.md` 才對。

## 實務決策清單

1. 缺的是**知識/慣例** → 寫 `CLAUDE.md` 或 skill，不建 agent。
2. 缺的是**切版/既有專門流程** → 用既有的專門流程 skill（名稱依當下環境而定）。
3. 需要**隔離/平行/限權**的一次性任務（大範圍重構、掃全庫、獨立審查）→ 派內建通用 agent；反覆出現才落成專用 subagent。
4. 考慮**多 agent** 前，過一遍判準：可平行？讀重於寫？協調確定？三者不全中，優先單執行緒。

## 強度標註總表

| 主張 | 來源類型 | 強度 |
|---|---|---|
| 能力來自 context | Anthropic 第一方＋Cognition 實務，跨陣營共識 | 高（共識） |
| subagent＝隔離/壓縮/平行 | Anthropic 第一方描述 | 中高（架構描述） |
| 多 agent 失敗率 41–86.7% | UC Berkeley MAST，獨立 preprint | 中高（限開源框架/當時模型） |
| 單執行緒優先、寫入衝突 | Cognition 實務經驗、立場已演進 | 中（經驗值、非靜態） |
| 90.2% 多 agent 優勢 | Anthropic 內部評測 | 低（第一方、未複現） |
| 「知識 vs 編排」二分框架 | 本頁綜合 | 綜合判斷（零件有佐證） |

## 交叉引用

- 挑選清單引用：[[Agent-工作流-Pattern-藍本庫]]——該頁「多 agent 失效邊界」一條（誤配 peer input：過度採信不健全回饋或反過來忽略他 agent 輸出）是本頁 MAST 實證的濃縮版；要完整失敗分類與適用域判準讀本頁，要設計時的快速挑選讀該頁。
- 模式原型：[[Building-Effective-Agents-Anthropic]]——「由簡入繁、只在複雜度能實證改善時才加」是本頁判準的上游原則；本頁補上「加了複雜度（多 agent）實測會怎麼壞」的獨立證據。
- 方法對照：[[多智能體研究系統-Anthropic]]——該頁是「多 agent 划算」的成功案例，本頁界定它成立的**適用域邊界**（讀重、可平行）。
- 證據平衡：[[Agent-Harness-Engineering-框架綜述]]——該頁自陳「來源集中 Anthropic」，本頁引入 Cognition／MAST 兩個非 Anthropic 來源，是對那條證據限制的直接補救。
- 實證脈絡：[[AI-自主工作流的實證檢驗]]——同屬「vendor 敘事 vs 獨立實證」的檢驗路線；本頁的 MAST 失敗率可與該頁的長任務可靠度崩落並讀。
- 成本落地：[[LLM-方案定價與-coding-agent-比較]]——本頁「多 agent 約 15 倍 token」是相對成本，該頁給 coding agent 訂閱月費與 API 按量單價的絕對數字，合看「要不要堆 agent」與「這樣花多少錢」兩個決策軸。
