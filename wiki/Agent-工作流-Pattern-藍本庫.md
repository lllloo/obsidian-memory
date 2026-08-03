---
title: Agent 工作流 Pattern 藍本庫
description: 設計 agent skill 時的 pattern 挑選清單：每項附定義、適用、失效條件、出處與強度，並收錄選用決策樹與被查證否決的組合宣稱
created: 2026-07-17
updated: 2026-07-30
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - agent-framework
  - context-engineering
---

# Agent 工作流 Pattern 藍本庫

設計新 agent skill／自動化工作流時的**挑選清單**：把散在多個出處的編排 pattern 收成統一格式（名稱／定義／適用／失效／出處／強度），供設計時挑選組合。與 [[Building-Effective-Agents-Anthropic]] 的分工是：那頁是**單一來源的完整轉述**，本頁是**跨來源的挑選視角**，補上 Anthropic 五項之外的 pattern（CSIRO 論文級 catalogue、OpenAI 的多 agent 編排二分、ReAct／Reflexion／Self-Refine 的原始出處）與各自的失效邊界。

**本頁只涵蓋領域一（agent 工作流編排）。** 知識管理流程方法論與軟體開發概念型流程屬同一藍本庫構想的另兩塊，**第一輪未蒐集**；第二輪已覆蓋三個角落、成果回存至他頁，其餘仍待補（見文末〈未解與待補〉）——讀者勿把本頁當完整藍本庫。（2026-07-17 deep-research 回存；該輪 119 條抽出主張中僅 25 條進查證，領域二三的主張全數被預算砍掉。）

## 先讀：三層強度標註

本頁所有條目依此分層，**不可齊平閱讀**：

| 強度 | 適用對象 | 意義 |
|---|---|---|
| **強** | 同儕審查論文：ReAct（ICLR 2023）、Reflexion（NeurIPS 2023）、Self-Refine（NeurIPS 2023）、CSIRO catalogue（JSS Vol 220, 2025）、MAST（NeurIPS 2025 Datasets & Benchmarks track，見 [OpenReview](https://openreview.net/forum?id=fAjbYBmonr)） | 有對照或系統性方法支撐 |
| **強（僅限描述性）／中（規範性）** | vendor 工程指南：Anthropic《Building Effective Agents》、OpenAI《A Practical Guide to Building Agents》 | pattern **定義為何**屬 first-party、強度最高；**該不該這樣做**（單 agent 優先、簡單優先）是 lab 工程經驗值、非對照實驗 |
| **弱** | 軼事觀察與社群口語 pattern | 田野觀察，不可當實測門檻 |

**來源同源性警告**：LangGraph 官方 pattern 頁雖是獨立 primary source，但 LangChain 自承該教學係照 Anthropic 那篇重建，**不構成獨立印證**。領域一詞彙真正的獨立源頭只有 CSIRO catalogue 與各 pattern 原始論文——統計上的「多來源一致」在此處部分是回音而非收斂。

## 第一層：選用 gate（在挑 pattern 之前先過）

- **複雜度為最後手段**（Anthropic，3-0）：預設用單次優化過的 LLM call（配 retrieval 與 in-context examples），只在簡單方案**可證明不足**時才加多步 agentic 系統。原文三處重述，其中「adding complexity _only_ when it demonstrably improves outcomes」。注意這條是**實證性而非教條性**——它預設了你有評估基礎設施；沒有評測就沒有「demonstrably」，這條 gate 會退化成口號。（強度：規範性建議＝中）
- **先極大化單 agent、必要才多 agent**（OpenAI，3-0，Anthropic 獨立同向佐證）：分家由**可量測的複雜度**而非概念切分的美感決定。（強度：規範性建議＝中，但兩家獨立收斂提高可信度）這條 gate 的深度版見 [[Context-優先與多-agent-的適用邊界]]——該頁以 Cognition 的單執行緒原則與 MAST 失敗實證，給出「可平行／讀重於寫／協調確定」三條比「可量測複雜度」更可操作的分家判準。

## 第二層：workflow / agent 分野

判準是**執行路徑能否事先決定**：workflow 經預定義程式路徑編排、提供可預測性與一致性；agent 由 LLM 動態自行導引流程與工具用法，適用於步驟數難以預測、無法硬編碼固定路徑的開放式問題。（3-0）

**但這實為 spectrum 而非二元。** 可操作的測試是：**branches 與 stop conditions 在執行前是否靜態可知**。這條測試比「感覺上像 workflow 還是 agent」可靠得多，設計時應優先用它。

## 第三層：pattern catalogue（兩套互補詞彙）

### A. Anthropic 骨架

五種 workflow pattern——prompt chaining、routing、parallelization（含 **sectioning** 與 **voting** 兩變體）、orchestrator-workers、evaluator-optimizer——加上 autonomous agents，另有 **augmented LLM**（LLM＋retrieval／tools／memory）作為**先於五者呈現的獨立基礎元件**，藍本庫應單獨收錄為第六元素、不可折進五項內。各項的完整適用時機見 [[Building-Effective-Agents-Anthropic]]，此處不重述。

**這是骨架，不是完整分類法。** 原文明言「These building blocks aren't prescriptive」「common patterns... we've seen in production」。直接後果：**ReAct、plan-act-reflect、human-in-the-loop、adversarial verification、loop-until-dry 都不在這五項內**，須另行溯源（見下）。可寫「權威骨架」，不可寫「權威完整分類法」。

**最實用的一條 disambiguation**：**orchestrator-worker 與 parallelization 的分界是「子任務能否事先定義」**——能預先切好的獨立子任務走 parallelization（為速度）；切不出來、須由 orchestrator 依具體輸入動態決定的才走 orchestrator-worker（典型例：跨多檔改程式碼）。設計時最常混淆的就是這兩者。（3-0）

### B. CSIRO Data61 的 18-pattern catalogue

一個**與 Anthropic 詞彙體系獨立**的論文級藍本庫：以 systematic literature review 產出 18 個 foundation model-based agent 架構 pattern，每個均附 **context、forces、trade-offs**——正是藍本庫想要的目標格式。（強度：**強**，已發表於 Journal of Systems and Software Vol 220, art. 112278, 2025，DOI `10.1016/j.jss.2024.112278`。研究過程中一度誤標為未同儕審查的 preprint，已更正上修。）

其中兩組已確認的細分特別有設計價值：

**Reflection 拆三個備選**（同一設計關切下的替代方案，2-1）：

| Pattern | 回饋來源 | overhead |
|---|---|---|
| **Self-Reflection** | agent 自評自修 | 低 |
| **Cross-Reflection** | 換用不同 agent／foundation model 提供回饋 | 中 |
| **Human Reflection** | 收人類回饋 | 高 |

三者**共用 generate→feedback→refine 骨架，差別只在回饋來源（reflective entity）**，構成一條清晰的 overhead 光譜。這個「骨架相同、只換回饋來源」的洞察，是設計時最省力的變化軸——先定骨架，再依成本挑回饋來源。

**多 agent 分工拆三個 cooperation pattern**（3-0）：

- **Voting-based**：提交投票達成共識，以保 fairness、accountability、collective intelligence。
- **Role-based**：指派各色角色、依角色定案，以利分工、容錯、擴展性、可歸責。
- **Debate-based**：跨多 agent 提供並接收回饋直至達成共識。

**catalogue 的時效限制**：其 SLR 語料截止於 2024 年中，不涵蓋其後命名的 pattern（Anthropic 那篇 2024-12 才發布）。故 CSIRO catalogue **不能單獨當完整清單**，須與 Anthropic 並列使用。

> **編纂者詮釋警告**：把 CSIRO 詞彙映射到 Anthropic 詞彙（Voting↔parallelization-voting、Debate↔對抗式驗證、Role-based↔orchestrator-worker）**論文本身沒說**，是研究者自加的。其中 Role-based↔orchestrator-worker 最鬆——前者涵蓋任何角色切分（如 ChatDev 的固定流水線），後者特指中央 LLM **動態**拆解；Debate↔對抗式驗證也不完全，debate 以**達成共識**為目標，非以反駁為目的。使用映射時請帶著這個折扣。

### C. OpenAI 的多 agent 編排二分

以 **graph edge 語意**區分兩個具名 pattern（3-0）：

- **Manager pattern（agents as tools）**：中央 manager LLM 透過 **tool call** 調度專職 agent 並綜合結果。適用於「只希望單一 agent 掌控 workflow 執行並接觸使用者」。**這是 Anthropic orchestrator-worker 的 OpenAI 對應物**（此對應較紮實：結構近同，且有獨立二手來源獨立命名為 Manager/Orchestrator Pattern）。
- **Decentralized pattern**：**handoff** 單向轉移控制權並移交最新對話狀態，接手 agent 立即開始執行。適用於 triage 類「專職 agent 完全接管、原 agent 不需再參與」；**不適用於需中央綜合（synthesis）者**；可選配反向 handoff 交還控制權。

### D. 有論文出處的 loop 類 pattern

- **ReAct**（Yao et al., ICLR 2023，**強**）：LLM 以**交錯（interleaved）方式**生成 reasoning trace 與 task-specific action——reasoning 負責誘導、追蹤、更新 action plan 並處理例外，action 負責對接外部知識庫或環境取額外資訊。**但「interleaving 帶來 synergy 是效能主因」的因果宣稱已遭正式反駁**，應列為失效條件、不得寫入適用時機。provenance 數字（ALFWorld +34%、WebShop +10%，僅用一到兩個 in-context example）是 **PaLM-540B 世代**結果，且 ALFWorld 的 +34% 是 best-of-6 對 best-of-8（平均對平均僅 +20%）——**絕不可當當前 SOTA 複述**，只能當出身證明。
- **Reflexion**（NeurIPS 2023，**強**）：plan-act-reflect／self-reflection loop 的**主要論文級出處之一**（非唯一）。不更新權重，改以語言回饋強化 language agent——agent 對任務回饋訊號進行口語化反思（verbal reflection），存進 **episodic memory buffer**，供後續 trial 改善決策。回饋可為 **scalar 或 free-form language**，來源可為 **external（環境／編譯器／測試）或 internally simulated（自評）**，在 sequential decision-making、coding、language reasoning 三類任務皆優於 baseline。**前提是「存在可取得的回饋訊號」**——沒有回饋訊號時這個 pattern 不成立。
- **Self-Refine**（NeurIPS 2023，**強**）：evaluator-optimizer／reflect 類的具名 pattern——**同一個 LLM** 依序扮演 generator、feedback provider、refiner 三種角色的迭代循環，不需 supervised training data、額外訓練或 RL，屬 **test-time** 方法，跨 7 類異質任務實證。

## 第四層：失效邊界與可檢核判準

這層在設計時最實用——它告訴你 pattern 什麼時候會壞。

- **單 agent 的典型失效**：陷入無盡執行迴圈（ReAct 重複產生相同 thought 與 action，無法產生新 thought 以脫離）。這正是 `loop-until-dry` 一類設計的失效邊界。但要注意證據強度：[[AI-自主工作流的實證檢驗]] 把「agent 無限迴圈燒 token」列為開放問題——目前只有軼事性工程部落格，缺系統性測量，故此失效可當設計提醒、不可當已量化風險。
- **多 agent 的典型失效**（3-0）：受無關對話（extraneous dialogue）干擾推理與工具選用；且 agent 會**誤配 peer input——過度採信不健全回饋、或反過來忽略他 agent 輸出，雙向皆會失效**。（出處但書：此條所引的 arXiv 2404.11584 是**轉述 AgentVerse**、非原始發現；原始出處應追 AgentVerse 或 MAST FM-2.5／2.6。）
- **何時該拆多 agent，兩條可檢核判準**（OpenAI，3-0）：(1) **Complex logic**——prompt 含大量 if-then-else 條件分支、prompt template 難以擴展時，按邏輯區段拆分；(2) **Tool overload**——關鍵**不是工具數量而是相似／重疊程度**，且**應先嘗試改善工具命名與描述，無效才拆 agent**。（附帶的「15／10 個工具」門檻是**軼事觀察、強度弱**，原文措辭為「Some implementations... while others struggle...」，是田野觀察而非實測 cutoff，勿寫成硬門檻。）
- **Human-in-the-loop 的兩個具名觸發條件**（OpenAI，3-0）：**超出失敗門檻**（對 retry／action 設上限，超過即升級給人）與**高風險動作**（敏感、不可逆、高賭注——原文舉例：取消訂單、授權大額退款、付款）。配套 **tool safeguards**：依唯讀 vs 寫入、可逆性、所需帳號權限、財務影響四個示例性因素給每個工具 low/medium/high 風險評級，用以觸發執行前暫停或升級。

## 可組合性：本輪最弱的一欄

必須誠實標記：**「pattern 之間怎麼組合」這一欄本輪幾乎沒拿到有效證據。** 唯一針對組合性的主張（evaluator-optimizer 與 HITL 互為同位替換）遭 **0-3 全票否決**。僅存的組合性依據只有兩條間接材料：Anthropic 的「These building blocks aren't prescriptive. They're common patterns that developers can shape and combine」，與 CSIRO catalogue 的 Related Patterns 欄位。

設計時的實務含意：**可組合性目前只能靠自己試，不要引用不存在的權威**。

## 勿引用（對抗查證中被否決的主張）

依寫入慣例第 6 條明列，不無聲丟棄：

1. **「evaluator-optimizer 適用條件為『成功標準明確但需迭代』，且可與 HITL 同位替換」（0-3）**——最值得記的一條：直覺上非常吸引人，但未通過查證，**不得寫進可組合性欄位**。
2. 「單 agent 適用窄工具／明確流程、多 agent 適用多重人格觀點」（0-3，出自 arXiv 2404.11584）。
3. 「多 agent 分 vertical／horizontal，vertical 特有失效為 leader 未傳關鍵資訊」（0-3，同上來源）。
4. 「迭代回饋與人類驗證對複雜問題不可或缺」（0-3，同上來源）。
5. 「ReAct 靠 Wikipedia API 克服 CoT 幻覺，界定『需外部事實錨定時才划算』」（1-2）。

> 前四條中有三條出自同一來源（arXiv 2404.11584），該來源**僅在「失效條件」一項存活**——引用它時要特別小心。

## 未解與待補

- **`loop-until-dry` 至今無正式出處**。20 條存活主張中無一為其提供定義來源，唯一相關的只有其失效條件（單 agent 無盡迴圈、MAST FM-1.5「Unaware of termination conditions」）。目前定位：**社群實務、無論文出處、強度弱**，保留但標明。
- **領域二（知識管理流程方法論）與領域三（軟體開發概念型流程）已跑第二輪，但仍只覆蓋三個角落**：成果分別回存至 [[第二大腦方法論比較]] 的「流程方法論的證據強度盤點」（GTD 五步、spacing effect、retrieval practice 爭議）與 [[AI-自主工作流的實證檢驗]] 的 spec-driven 節（Kiro 三階段閘門）。PARA、Zettelkasten、CODE、Evergreen notes、MOC、Shape Up、TDD、ADR、event storming、pre-mortem 等仍零存活主張。**2026-07-30 領域三再進一塊**：[[長跑-Agent-的目標定義與計畫工具]] 收下「長跑 agent 的目標定義與收斂控制」——目標分層、驗收判準記法、機器可檢的停止條件、防範圍膨脹的舉證責任反轉，逐條標強度且明列 9 條勿引用。注意它與本頁是**不同領域**：本頁是 agent 之間怎麼編排，該頁是給 agent 的目標怎麼寫。
- **這不是主題的問題，是工具的結構限制**：兩輪 deep-research 分別抽出 119／135 條主張，但**皆只有 25 條進入查證**——截至 2026-07 兩輪觀察均為此數，研判是該 harness 當時的固定上限（隨版本可變，非恆值），與主題無關。故「窮舉一個 pattern 藍本庫」與 deep-research 在結構上互斥：它適合把**少數幾條主張查到極深**，不適合把**大量 pattern 掃得很廣**。要補齊廣度應改用一個 pattern 派一個 subagent 的輕量掃描（見 `mini-research` skill），把多票對抗查證這個乘數換成覆蓋率。

## 交叉引用

- 骨架原文：[[Building-Effective-Agents-Anthropic]]——本頁的 Anthropic 五項不重述其適用時機，僅補「這是骨架非完整分類法」的邊界與跨來源對照。
- 綜述定位：[[Agent-Harness-Engineering-框架綜述]]——本頁是該綜述的**挑選視角切片**：綜述講 harness 工程的時間線與框架演進，本頁只回答「設計時該挑哪個 pattern、它什麼時候會壞」。
- 失效實證的深度版：[[Context-優先與多-agent-的適用邊界]]——本頁「多 agent 誤配 peer input」的失效條目，該頁以 MAST 的 1,642 traces 實證給出更完整的失敗分類與適用域判準；兩頁的 MAST 引用應保持一致。
- orchestrator-worker 的生產級落地：[[多智能體研究系統-Anthropic]]——本頁把 orchestrator-worker 與 parallelization 的分界定在「子任務能否事先定義」，該系統正是「不能事先定義」側的實例（lead 動態拆解、平行 subagent、綜合結果）。
- 評測基礎設施的必要性：[[AI-自主工作流的實證檢驗]]——本頁第一層 gate 的「demonstrably improves outcomes」預設了評估基礎設施，該頁給出「驗證迴路必要但不充分」（測試本身可被 agent 篡改）的獨立證據，是這條 gate 的現實折扣。
- evaluator-optimizer 的領域落地：[[設計品質的可量化檢測]]——本頁 evaluator-optimizer 的可組合性欄位是空的，該頁提供了一個實際跑起來的閉環（自動化檢測當 evaluator）作為參考實例。
- 同構想的另兩塊（人類流程側）：[[第二大腦方法論比較]] 的「流程方法論的證據強度盤點」與 [[AI-自主工作流的實證檢驗]] 的 spec-driven 節——同一次「概念流程藍本庫」構想下的知識管理與軟體開發側，同樣逐條標強度、同樣覆蓋不全。三處合起來才是藍本庫的現況。
- 編排層 prior art：[[pi-workflow-編排-harness-與本-vault-分野]]——該頁用 workflows／agents 二分定位 pi-workflow，與本頁第二層的「branches 與 stop conditions 是否靜態可知」測試是同一判準的兩種表述。
