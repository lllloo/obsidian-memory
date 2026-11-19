---
title: Saloni Gandhi 與 Ziwei Guo 先驗證 judge 再讓 agent 自改
description: LinkedIn 用 judge、根因反思與 GEPA 改使用者理解 agent 的 prompt；重點是 judge 與診斷本身要先對人校準
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/talks/yH7_SIIgI-Y-agent-that-fixes-its-own-mistakes
published: 2026-11-10
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - evaluation
---

# Saloni Gandhi 與 Ziwei Guo 先驗證 judge 再讓 agent 自改

來源：AI Engineer 演講〈An Agent That Fixes Its Own Mistakes〉（YouTube `yH7_SIIgI-Y`，2026-11-10 上傳）的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-Gandhi-Guo-Agent-That-Fixes-Its-Own-Mistakes]]。方法部分另核對 [GEPA 論文](https://arxiv.org/abs/2507.19457)、[gepa-ai/gepa](https://github.com/gepa-ai/gepa)、[DSPy GEPA 文件](https://dspy.ai/current/api/optimizers/GEPA/overview/)。

**一句話**：LinkedIn 把「跑 agent → judge 評分 → 找根因 → 提 prompt 修改 → 同 rubric 評估 → held-out 比較 → 人審後上線」做成一條定期跑的流程，而且已經有第一個由 GEPA 產生的 prompt PR 上線。但整場最有價值的部分在後半：他們拿約 180–200 筆人工審查去對 judge，發現 judge 最常在「低分」這一側出錯，而低分正是送進改進迴圈的樣本；負責找根因的第二層 judge 還會把錯怪到沒問題的 rubric 上。結論是：評估器沒先校準就讓迴圈自動改，可能把正確的元件改壞。

## 講者與立場

Ziwei Guo（前半，系統設計）與 Saloni Gandhi（後半，成果與教訓）都是 LinkedIn 的工程師；演講沒有交代兩人的職稱，本頁不補。演講是公司內部專案的經驗分享，**沒有推銷可購買的產品**，GEPA 是開源方法、不是 LinkedIn 的東西。不過「已經上線」「一致率提升」都是公司自報，沒有公開資料或程式碼。

標題用的是 recursive self-improvement（RSI），但他們自己說目前只改 prompt、底層模型不動，做改動的是外部的「improvement engine」而不是 agent 自己。官方閱讀頁的標題敘述也比較保守，只寫「How an edit earns its place in the next run」。把它讀成「一個有 judge 和人審的 prompt 最佳化流程」比讀成「自我改進的 agent」準確。

## 演講脈絡（按順序）

### 1. RSI 的定義：從 production trace 學（0:01–1:41）

Guo 的定義：在 AI 系統外圍建一個迴圈，從 production trace 和日常開發中發現的問題學習。目標系統是 LinkedIn 的 career agent（幫會員達成職涯目標），這次具體只做其中的「user understanding」部分。流程是：記錄 production trace → 用 evaluation engine（例如 LLM judge）檢查 trace、找問題、給回饋 → 依回饋持續改系統。

他特別強調一點，之後整場都在呼應：**評估必須客觀、而且要和使用者回饋對齊**，因為評估決定了瓶頸在哪、下一步改哪裡。

### 2. 可以改的是 harness，不是模型（2:12–3:52）

他把 agent harness（包在模型外面的軟體，他也稱作 orchestrator）拆成四個可改的元件：

- planning 與邏輯：決定執行路徑。
- context 與 memory：保存、管理 session 狀態。
- tool interface：存取內外部 API 與資料集。
- artifact storage：存輸出與生成 log。

上面還有一層評估邏輯。base model 的最佳化**不在範圍內**，先做 harness。

### 3. 最佳化的階梯（3:52–5:01）

他把「讓 optimizer 能改什麼」排成難度遞增的階梯：

1. 改 prompt（最簡單、最直接）。
2. 改 structured context 的組織方式。
3. 自動設計整個 workflow。
4. 改 harness 程式碼本身。
5. 改 optimizer 自己的程式碼。

目前**只做到第 1 階**，其他是未來方向。

### 4. 七個步驟（5:01–9:05）

| 步驟 | 做什麼 |
|---|---|
| 1 | 對 query 跑 agent，保存輸出與 trace（agent 的完整軌跡） |
| 2 | 用 judge 評分，說明哪裡好、哪裡不好 |
| 3 | Agent reflection（他們也叫 root causing）：依 judge 輸出找低分原因，可能是 agent、模型、prompt、tool，**也可能是 judge 或 rubric 本身錯了** |
| 4 | 依根因產生 edit proposal；目前只有 prompt，未來可能是 workflow、harness 程式碼、optimizer 程式碼 |
| 5 | 用**同一個 judge、同一套 rubric** 評估各個候選修改 |
| 6 | 把有希望的修改併進 prompt |
| 7 | 在 **held-out set** 上比較新舊版本，確認新版真的比較好 |

通過第 7 步的版本成為新 baseline，之後依固定節奏再跑一輪。閱讀頁補充的關鍵：只看低分，optimizer 沒有理由改某一句特定指示；所以就算只能改 prompt，第 3 步的診斷也必要。

### 5. 被改的 agent 長什麼樣（9:05–12:26）

輸入只有 member ID。agent 用它抓搜尋紀錄、profile、地點、偏好等資料，經過多步 agentic 綜合後輸出一組描述會員的欄位。以「偏好職稱」這個欄位為例，輸出包含：

- 職稱清單（例如 network manager、account manager）。
- confidence。
- citation：指向支持推論的會員資料，例如這些職稱在已存搜尋中很常出現。
- reasoning：例如「明確陳述的偏好決定主要職稱，已存搜尋支持相鄰職稱」。

閱讀頁的整理是：這些欄位讓審查者能回頭檢查推論。

### 6. 第一層 judge（L1）（12:26–14:11）

L1 依產品定義的 rubric 在 **15 個任務維度**上評分，分數 1–3（1 差、2 普通、3 很好）。例子中某會員整體得 2.31，底下每個欄位（例如 goal summary、preferred job title）各有分數和 notes 說明理由。欄位層級的 notes 讓下一步有具體的主張可以查。

### 7. Reflection 的四個小步驟（14:11–18:30）

1. **分群**：把失敗的 row 依低分的維度分組。只用既有分數，不呼叫 LLM。
2. **L2 judge 診斷**：在每一群裡逐筆給自由文字的根因說明與 cause tag（prompt、agent、harness、程式碼、judge、rubric 等）。同一個症狀（例如偏好職稱低分）在不同會員身上可能原因不同。
3. **合併近似重複**：自由文字難以計數。例子：一筆說「會員 profile 資料缺漏」，另一筆說「profile 沒反映完整瀏覽紀錄」，其實是同一件事：現有資料撐不起 agent 的結論。合併成 canonical issue label 後才能看出合計頻率。
4. **依頻率排名**：不需要 LLM。產出給工程師看的 scorecard，同時把根因存起來，下一輪 L2 診斷時當 context 用（投影片上那條往回指的箭頭）。

### 8. 產生修改與 GEPA（18:30–20:15）

依 judge 的證據與 reflection 結果，用 GEPA（逐字稿辨識成 JPA）提出新 prompt，以 mini-batch 的方式在抽樣 trace 上跑；選出候選 prompt 進 validation set；通過的就更新 prompt、進 production、成為下一輪 baseline。

### 9. 三個工作重點（20:15–22:37）

- **品質**：大量人工標註來改進 L1 與 L2；研究 agent 與 judge 的變異（LLM 不確定性）；依標註與變異分析回頭更新 judge 與 reflection。
- **自動化**：把七步包成 workflow，依需要每週、每兩週或每月觸發，持續提出 prompt 修改。
- **上 production**：目前有 human in the loop；他們說品質夠好之後會逐步減少人工、提高自動化程度（這是意圖，沒有時程）。

### 10. 兩個成果（Gandhi 接手，23:16–25:09）

Gandhi 的開場論點：**評估器的品質和最佳化系統的品質一樣重要**。

1. 第一個經 GEPA 與這個迴圈最佳化的 PR 已上 production，上線前經過人審與量化量測。她稱這是讓 RSI 脫離實驗性質的里程碑。
2. 在使用者理解 judge 上投入大量人工標註，分析 judge 與人不一致的地方，因此找到 rubric 與 reflection 系統的反覆弱點並針對修正，提升可靠度、降低評估變異。她的說法：要讓系統自動改 agent 之前，必須先確定驅動改動的回饋本身值得信任。

### 11. L1 和人對不對得上（25:09–28:18）

分析約 180–200 筆人工審查：

- **依 L1 分數分組的完全一致率**：1 分約 55%、2 分約 57%、3 分約 80%。judge 認得出好輸出，卻分不清不同程度的差輸出，而且很多最低分是**太嚴**。閱讀頁點出要害：送進 reflection 的正是這些低分樣本。
- **依欄位分組**：偏好職稱屬於一致率最低的一群（沒給數字）；領域／專長約 47%；工作型態約 50%。她的結論是各維度評估品質不一致（逐字稿講成「was uniform」，依上下文應為口誤），某些維度需要更清楚的定義、證據處理規則與評分指引。

標註中反覆出現的失效型態：

- **偏好職稱**：judge 因為回傳的職稱「說得通」就接受，沒發現 agent 漏掉了重要的意圖訊號。她的說法是 judge 在評「合理性」而不是「完整性」。只看輸出的審查者看不出漏了什麼，要回頭看輸入才看得到。
- **專長欄位**：domain（software engineering）、role（machine learning engineer）、skill（machine learning）的界線不清；rubric 也沒有一致的**部分給分**規則，輸出對錯混雜時不知道怎麼給分。
- **格式與推論**：judge 會因無害的格式差異扣分；對「能不能從會員目前的工作推論出偏好」做出不一致的假設。
- **太嚴的分布**：37 筆被判定太嚴的評分中，31 筆是 1 分的輸出，表示分數邊界要重新校準。

她的總結：很多不一致**不是模型錯誤，而是 rubric 與評估政策本身的模糊**。

### 12. 改 rubric 與 L2 的問題（28:18–31:21）

rubric 的修正：

- 格式差異不再算語意失敗（例：「full-time」只因大小寫就被扣分）。
- 加職稱正規化指引；釐清兼職／多份工作、推論年資、推論地理位置的處理方式。
- 重新校準「低分」與「部分正確」的分界。

結果：與人的一致率從約 57% 升到 64%，mean error 從 96 降到 74（逐字稿數字；量表與定義沒說，閱讀頁也只寫「scale 未說明」）。她強調改善不是靠換模型，而是把「正確的評估長什麼樣」寫得更明確。

接著對 L2（反思／找根因）做同樣的人工審查：

- **找根因比找失敗難得多**。L2 把問題歸給底層模型時人比較常同意；歸給其他原因、尤其是 rubric 時，一致率低很多。
- 原本的 cause tag 清單**沒有「L1 判錯了」這個選項**。於是遇到 rubric 合理、只是 L1 套錯的情況，L2 只能退而怪 rubric。
- L2 有時直接沿用 L1 的理由，沒有自己對照 agent 輸出驗證。一次錯判就會看起來像兩個評估者都同意的發現。
- 風險：reflection 能產出聽起來很有說服力的解釋，卻診斷錯元件；拿它去產 prompt 修改，會改到原本正常的地方。所以改進 L2 成為下一個優先事項。

### 13. 衡量影響的兩個層次（31:21–33:38）

- **流程可靠度**：L1 改善讓分數更穩、更貼近人；L2 改善讓根因診斷更準；用 **majority voting** 降低單次 LLM 判斷的影響，用 held-out 評估確認改善能遷移。她提到「採用門檻」與「信賴區間」有改善，但**沒給數值、也沒說往哪個方向變**。
- **採用規模**（提議中的指標）：能可靠由 RSI 產生並驗證的 prompt 修改比例、下游回應品質、維護 agent 的工程師省下的時間。她明說終極目標不是最大化自動 prompt 修改的數量，而是在對改動有信心的前提下，讓 agent 品質有可量測的進步。

### 14. 推廣到其他團隊（33:38–36:40）

能力的層次依序是：base agent → agent evaluation → agentic reflection（系統化找根因）→ RSI 迴圈。各層互相依賴，沒有可靠的診斷就建不出可信的迴圈。現況是多數團隊有 agent，但評估參差：有人有客製化流程、有人靠一次性分析或手看輸出，只有少數有可重複使用的穩定評估。所以她把「先升級評估基礎設施」當成擴大 RSI 的前提，並提議共用基礎設施的五個面向：

1. **標準化評估**：可重用的框架、指標，以及能用人類回饋校準的 judge。
2. **自動化回饋**：持續收 trace、偵測反覆失敗、做根因分析。
3. **自動化最佳化**：prompt 最佳化與 reflection，以可重複的方式產生並測試候選修改，取代臨時改動。
4. **驗證與信任**：held-out 評估加回歸測試。
5. **自助採用**：元件化，讓團隊不用自己從頭建整條管線。

### 15. 收尾：改的是斜率（36:40–38:50）

RSI 有兩個元件：target agent（被改的對象，這裡是使用者理解 agent）與 improvement engine（評估、找根因、提修改）。如果把 agent 表現看成時間的函數，目標不是某一刻的高度，而是**一階導數**，讓改進曲線更陡。最後一句：改進流程最重要的是能信任自己做的改動。

## 回查結果（2026-11-19）

| 項目 | 結果 |
|---|---|
| GEPA 論文 | [arXiv 2507.19457](https://arxiv.org/abs/2507.19457)，〈GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning〉，Agrawal、Khattab、Zaharia 等 17 位作者，2025-07 提交、2026-02 修訂，頁面標註被 ICLR 2026 接受為 Oral。論文自報：六個任務平均比 GRPO 高 6%、最高 20%，rollout 少最多 35 倍；比 MIPROv2 高 10% 以上。這些是論文作者在自選任務上的結果，不是 LinkedIn 的數字 |
| gepa 開源專案 | [gepa-ai/gepa](https://github.com/gepa-ai/gepa) 存在，MIT 授權，描述「Optimize prompts, code, and more with AI-powered Reflective Optimization」，查詢當下約 7.5k stars、最近一次 push 為 2026-11 上旬，仍在維護 |
| DSPy 裡的 GEPA | [官方文件](https://dspy.ai/current/api/optimizers/GEPA/overview/)有 `dspy.GEPA`。metric 可以回傳分數加文字 feedback（`dspy.Prediction(score=..., feedback=...)`）；只回傳分數也行，但 GEPA 拿到的訊號比較少。從 `trainset` 抽 mini-batch 做 rollout 與反思；在 minibatch 上有改善的候選才拿去 `valset` 評估；保留一組在至少一個驗證樣本上最好的 Pareto 前緣候選。這和演講「mini-batch 抽樣 trace → 候選進 validation」的描述對得上，也說明 L1 的欄位 notes 為什麼重要：它就是 GEPA 需要的文字 feedback |
| LinkedIn 一手資料 | 搜尋沒找到 LinkedIn 官方 blog 或論文描述這個 RSI 專案，演講是唯一一手來源（搜尋不保證完整）。另有一篇 [arXiv 2602.07333](https://arxiv.org/abs/2602.07333) 在 LinkedIn 產品上用 RL 產生會員的文字表示，但作者不同，也沒提到這個 agent，**不確定**和本演講是否同一系統 |
| 第三方報導 | [StartupHub](https://www.startuphub.ai/ai-news/artificial-intelligence/2026/linkedin-s-self-improving-agent-still-needs-humans)（2026-11-11）只引用 YouTube 演講、沒有新的一手資料，主軸是「迴圈跑得起來，但 judge 還不值得信任」，並批評目前範圍稱不上強義的 RSI。它建議在信任這類迴圈前預算約 200 筆人工標註，這是報導者的推論，不是 LinkedIn 說的 |
| held-out 的必要性 | 與演講同方向的獨立研究：[The Winner's Curse in LLM Self-Improvement Loops](https://arxiv.org/abs/2610.09239)（2026-10 preprint，未同儕審查）。摘要說「比較好就保留」的步驟是在量測雜訊下做選擇；用 16 題的選擇集時，選擇集分數比 held-out 高 13–20 個百分點，256 題時高 1–5 點；GEPA 與 MIPROv2 的選擇集增益也高估了 held-out 增益；測過的接受規則整輪下來沒有勝過貪婪接受。LinkedIn 沒有公開 held-out set 的大小，所以無法判斷他們落在哪個區間 |

## 證據強度與限制

| 主張 | 強度 |
|---|---|
| 第一個 GEPA 產生的 PR 上 production | 公司自報、單一案例；沒說改了什麼、改善多少 |
| L1 一致率 55%／57%／80%、欄位 47%／50% | 自報；約 180–200 筆人工審查，切成三個分數組或多個欄位後每組樣本更少；沒說審查者人數、彼此一致率，「完全一致」的定義也沒說 |
| 37 筆太嚴中 31 筆為 1 分 | 自報；分母（全部 1 分有幾筆）沒給 |
| 一致率 57% → 64% | 自報；沒說是否在同一批資料上量（若用同一批審查資料改 rubric 再量，會高估）；與第 11 段「2 分約 57%」的數字相同，不確定是否同一個量 |
| mean error 96 → 74 | 只出現在逐字稿，量表與定義未說明，閱讀頁也不給數值 |
| 採用門檻與信賴區間改善 | 沒有數值、沒有方向，等於無法引用 |
| L2 歸因給模型時人較常同意 | 自報、只有相對描述，沒有數字 |
| 共用基礎設施五面向、改斜率 | 提議與願景，尚未實作或量測 |

### 勿引用（2026-11-19 核對）

- 「LinkedIn 的 agent 會自己修正自己的錯」：改 prompt 的是外部的 GEPA 流程，上線還要人審，模型不動。
- 「judge 和人的一致率只有 55%」：這只是 L1 打 1 分那一組；3 分那組約 80%。要引用就連分組一起引。
- 「改 rubric 後 mean error 從 96 降到 74」：量表與定義不明，只能說「下降」。
- 「信賴區間／採用門檻有改善」：原文沒給數值與方向。

## 可以搬到個人 Claude Code／Codex 工作流程的做法

個人沒有 15 維產品 rubric 和 200 筆人工標註，但這場最能用的是「先懷疑評分者」的那半場，不需要 GEPA 也能做。

**A. 用 LLM 評自己的 agent 產出前，先拿手標資料對一次**

適用：你用 LLM 評 commit message、PR 描述、skill 輸出、wiki 頁品質之類。

1. 先手標 20–30 筆，同一套分數（例如 1–3）。
2. 讓 judge 評同一批，**依 judge 給的分數分組**算和你一致的比例，不要只看整體一致率。LinkedIn 的教訓是錯誤集中在低分側，而低分正是你要拿去修的那些。
3. 再依欄位或維度分組看。一致率特別低的維度，先改 rubric 的定義（什麼算 1、什麼算 2、要看哪些證據），不要先改被評的 agent。
4. rubric 寫明：格式差異不扣分、正規化規則（大小寫、同義詞）、部分正確怎麼給分、什麼情況下可以接受推論。
5. 改完 rubric 後用**另一批**沒參與調整的手標資料再量，避免拿同一批資料自我驗證。

**B. 找根因時，把「評分者錯了」列成選項**

1. 診斷 prompt 的原因清單至少包含：輸入缺證據、prompt／指示缺漏、工具錯誤、模型能力不足、**rubric 錯了**、**judge 套錯了 rubric**。後兩個要分開。
2. 要求診斷者先自己對照原始輸入與 agent 輸出下判斷，再看 judge 的理由，不能直接沿用。可以的話用不同的 subagent 或不同模型家族跑診斷。
3. 把自由文字根因合併成少數 canonical label 再計數，先修出現最多次的。label 清單存檔，下次診斷時當 context 餵回去。

**C. 改 skill／指示檔時，選擇與驗證用不同的題**

1. 把案例分兩堆：一堆用來試改法，一堆只在最後比新舊版本時用。
2. 用同一個 judge、同一套 rubric 比較候選改法。
3. 案例少時（十幾筆），選擇集上的進步很可能是雜訊，上面那篇 Winner's Curse preprint 量到 16 題時選擇集會高估 13–20 個百分點。至少重跑幾次或多數決，再看 held-out。
4. 最後仍由人看 diff 決定要不要合，這也是 LinkedIn 目前的做法。

**D. 想真的用 GEPA 的話**

- 目標是 DSPy 程式時，直接用 `dspy.GEPA`，metric 回傳分數＋文字 feedback；feedback 越具體，GEPA 越有依據去改指示。
- 不是 DSPy 時，可以看 `gepa-ai/gepa` 套件，它的定位是最佳化任意文字元件。要先有可重複跑的評估集與 metric，這通常才是難的部分。
- 這是本頁依官方文件推得的用法，LinkedIn 沒公開他們怎麼接 GEPA。

**不能直接搬的**

- 15 個維度的產品 rubric、每週固定排程的整條管線、幾百筆人工審查：成本與資料量是團隊等級。個人規模做到 A、B、C 的小版本就有大部分價值。
- 「逐步減少人工審查」：他們自己也還沒做到，目前沒有證據說可以放掉人審。

## 與既有頁的關係

- [[Ara-Khan-讓-agent-自動爬升-harness-與選題]] 是同一個「RSI」標籤下的對照案例：Khan 讓監督 agent 直接改 harness 程式碼，用 benchmark 測試的通過與否當訊號，評分本身是確定性的；LinkedIn 只改 prompt，但評分是 LLM judge，於是花了大半場在驗證評分者。兩者共同的教訓是改動要在選題以外的資料上站得住（Khan 講過擬合，LinkedIn 用 held-out）。兩邊的「自我改進」也都不是字面意思，實際上都是一個系統去改另一個系統。
- [[LLM-as-judge-知識庫頁面評分]] 記錄了「拿掉 rubric 的 judge 看起來很穩，卻穩定地量錯」；LinkedIn 的資料從實務面補強這點：rubric 模糊時，不一致集中在低分與特定欄位，修 rubric 比修模型有效。該頁的建議「judge 換模型家族」可以直接套到 L2 不該沿用 L1 理由這個問題上。
- [[Lauren-Tan-把糾正寫進程式庫]] 主張把糾正變成確定性檢查；LinkedIn 的案例落在另一端，被改的對象是無法用確定性測試判對錯的推論輸出（偏好職稱），只能靠 judge，所以代價就是要持續校準 judge。兩者互補：能寫成確定性檢查的先寫，寫不成的才走 judge 迴圈。
- [[長跑-Agent-的目標定義與計畫工具]] 的「計分腳本標成不可編輯」是在防 agent 改評分；LinkedIn 碰到的是另一種失效：評分者沒被竄改，自己就是錯的。改進迴圈的防線因此要兩種都有：評分不能被改，也要定期對人校準。
- [[AI-自主工作流的實證檢驗]] 記錄 benchmark 與自評普遍高估；本頁的 L1 太嚴、L2 誤歸因是反方向的錯（低估、歸錯因），提醒評估器的偏差不一定都朝「太樂觀」。
