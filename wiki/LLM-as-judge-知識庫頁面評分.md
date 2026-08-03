---
title: LLM-as-judge 知識庫頁面評分
description: LLM-as-judge 給 wiki 頁評分的方案與方法學約束：rubric 決定信度、bias 匿名化擋不住、本 vault 實測分辨力不足
created: 2026-07-21
updated: 2026-08-03
parent: "[[wiki/01.index]]"
tags:
  - evaluation
  - ai-agent
  - wiki
  - knowledge-graph
---

# LLM-as-judge 知識庫頁面評分

問題：能不能用 LLM 給 wiki 頁「打分數」，用來排序該修哪頁、或當品質 gate？本頁是 2026-07-21 兩輪 deep-research（各 5 搜尋角度、每條主張 3 票對抗查證）的回存：第一輪查工具面與方法論面，第二輪換詞彙補查「互聯知識庫層級」。聚焦**純 LLM-as-judge 路線**（機械指標如 markdownlint、連結數統計不在範圍內，僅作對照）。

**核心結論：沒有任何現成方案是為「互聯 markdown 知識庫」設計的。** 能用的兩個都是 LLM eval harness，要把頁面 shoehorn 成 test case 才跑得動；真正可搬的不是工具，是三條設計約束（rubric 必須寫、judge 換模型家族、不要一次丟多頁排名）。

## 一、現成工具：兩條路，都是硬塞

### promptfoo — 最接近可用

*（強度：官方文件直讀，主張 3-0 通過查證；但三條較強版本的細節主張 0-3 遭否決，設定檔照抄前須回官方文件現場確認）*

- 內建 `llm-rubric` 斷言，官方定位為「general-purpose grader，依自訂 criteria 評估輸出」，歸在 output-based 而非 context-based——`context-recall`／`context-relevance`／`faithfulness` 才是 RAG 專用，故 **`llm-rubric` 結構上不需檢索 context**，可用於單份文件評分。
- 評分模型可三層覆寫：CLI `--grader`、`test`／`defaultTest` 的 `options.provider`、assertion 層的 `provider:`，優先序為 assertion > test > defaultTest。**這讓「judge ≠ 撰寫者」在設定層即可達成**，是它相對其他 harness 的實質優勢。
- 另有 `select-best`，官方定義為「比較同一 TestCase row 內的多個輸出，選出最符合指定 criterion 的一個」。

限制（全部來自官方文件的結構，不是猜測）：

1. `llm-rubric` 原生輸出是 `{reason, score 0.0–1.0, pass}`，要 1–10 分需自訂 `rubricPrompt`。
2. promptfoo 評的是 test case（prompt + provider + vars）的**輸出**，對既有 markdown 檔評分要靠 `file://` 變數或 passthrough provider 把檔案內容灌進去——可行，但不是一等公民用法。
3. `select-best` 是 n 選一的 winner selection，**不回傳排序、不給每項分數**；要排 21 頁得自己編排多輪比較，且它比較的是「同一 row 內的多個輸出」，與「21 份彼此獨立的文件」形狀不同。
4. **陷阱**：預設 grader 依 API key 決定（有 Anthropic key 就落回 Claude 家族）。不明確設定 grader，開箱路徑反而會踩到同家族自評——正是下節要防的事。

**精確度提醒**：三層覆寫中只有 assertion 層是裸 `provider:`，`test` 與 `defaultTest` 必須寫成 `options.provider`，照字面抄會設錯。

### DeepEval G-Eval — 另一條，官方自承不穩

*（強度：官方文件直讀，3-0 通過；「不決定性」為廠商自承對己不利的宣稱，可信度高，但無 test-retest 變異數或人類一致性數字支撐）*

- G-Eval 需要 `name` + (`criteria` 或 `evaluation_steps`) + `evaluation_params`，criteria 明文可為任意自訂條件。官方 use case 中 Coherence／Tonality／PII 都**只用 `ACTUAL_OUTPUT`**，文件並說「coherence doesn't rely on an expected output」——這確實是文件級評分而非 RAG 評估。
- 官方文件逐字寫：「Although GEval is great it many ways as a custom, task-specific metric, it is **NOT deterministic**. If you're looking for more fine-grained, deterministic control over your metric scores, you should be using the DAGMetric instead.」

三項必須隨附的限定：

1. 同一頁也給了三個穩定化槓桿——用固定 `evaluation_steps` 取代自由文字 criteria、加 `rubrics` 分數帶、`strict_mode` 二元化。所以文件說的是「**原生**絕對評分不穩」，不是「絕對評分無法穩定」。
2. DAGMetric 並非決定性逃生口：每個判斷節點仍由 LLM 下判，決定性的只是給定路徑後的分數聚合。
3. 資料模型上 `LLMTestCase.input` 為必填，評一份 wiki 頁得塞占位字串到 `input` 再從 `evaluation_params` 排除——可行但是 shoehorn。

### 其餘工具：本輪無存活證據

Ragas、OpenAI Evals、LangSmith evaluators、Vale 的 LLM 擴充、Obsidian 生態外掛在本輪都**沒有存活的主張**。這是「未查到支撐」而非「已證實不適用」——本輪多個 verifier 的 WebSearch 預算耗盡，覆蓋不完整。

## 二、方法論：三條有數字的約束

### 1. rubric 是絕對評分的命脈——但失效方式反直覺

*（強度：單一 preprint、未同儕審查；任務錯配明顯——「1–5 評指令回應且有參考答案」，非長篇 markdown 文件評分，更非繁中語料。arXiv 2506.13639，Yamauchi/Yano/Oyamada，NEC，2025-06）*

BIGGEN-Bench，Krippendorff α（括號內為與人類相關）：

| 設定 | GPT-4o | LLaMA-3.1-70B |
|---|---|---|
| 給評分準則＋參考答案 | 0.908 (0.666) | 0.806 (0.641) |
| 移除評分準則 | 0.909 (0.591) | 0.807 (0.555) |
| 移除參考答案 | 0.921 (0.638) | 0.824 (0.581) |
| 兩者皆移除 | 0.896 (**0.487**) | 0.758 (**0.346**) |

論文自述評分準則的影響大於參考答案，且弱模型退化更嚴重。

**最該記住的是失效的形狀，不是數字**：退化的是「與人類的一致性」，**不是自我一致性**——全移除後 Krippendorff α 幾乎不動（0.908→0.896），論文明說 consistency 未受實質影響。也就是說，**沒有 rubric 的 judge 會看起來很穩定，卻穩定地量錯東西**。這直接否定「分數重跑幾次都差不多，所以可信」這個檢查方式。

限定：崩幅是 BIGGEN-Bench 專屬，第二個 benchmark（EvalBiasBench）同樣的全移除只從 0.865 掉到 0.811，說「崩到」對後者是誇大。論文未指明所用相關係數種類（Pearson 或 Spearman）。評分模型為 GPT-4o-2024-08-06 與 LLaMA-3.1-70B，已屬舊世代，但發現屬方法論層次。

### 2. self-preference bias：匿名化擋不住

*（強度：方向為多來源收斂、信心高；所有量化值皆 2023–2024 世代模型，對 2026 年前沿 judge 無直接數據）*

對本 vault 最直接相關的一題：讓維護 wiki 的同一個模型評自己寫的頁，偏誤有多嚴重？

**存在性**（arXiv 2404.13076，Panickssery/Bowman/Feng，COLM 2024）定義為「LLM evaluator 給自己的輸出打的分高於他人，而人類標註者認為兩者品質相當」——**有人類基線**，排除了「自評高只是因為真的比較好」這個簡單反駁。

**機制不是看到署名**：2404.13076 用 fine-tuning 建立 self-recognition 能力與 self-preference 強度的關聯（example-level Kendall tau：GPT-3.5 on XSUM 0.41→0.74）；Wataoka et al.（arXiv 2410.21819）則歸因於 perplexity／熟悉度，「regardless of whether the outputs were self-generated」。

**匿名化實測擋不住**：CALM（arXiv 2410.02736）Appendix C 明載評分時「without prior knowledge of the authorship」，Table 5 六個模型中**五個仍自評較高**（self/other 分與 error rate）：

| 模型 | 自評 | 他評 | error rate |
|---|---|---|---|
| Qwen2 | 7.64 | 6.58 | 16.1% |
| Claude-3.5 | 7.04 | 6.55 | 7.48% |
| GPT-4o | 7.01 | 6.89 | 1.74% |
| GPT-4-Turbo | 6.98 | 6.90 | 1.16% |
| GLM-4 | 7.73 | 7.64 | 1.18% |
| ChatGPT | 5.21 | 5.72 | （反例） |

**推論：blind rubric 沒有方法學依據，換 judge 模型才有。** 兩種機制都不需要看到署名。CALM 論文自身建議「Avoid using the same model to generate and judge answers」。但文獻同時指出換模型**只能緩解、無法根除**；arXiv 2604.22891（2026-04，20 個 LLM）以多維度分解降低 SPB 平均 31.5%，同樣是緩解而非消除。

**嚴重程度分歧很大，不可一概而論**：最常被引的 Wataoka GPT-4 = 0.520 出自 Chatbot Arena 33k 對話的 **pairwise 偏好**，不是文件級絕對評分；其對照組全是 2023 年小型開源模型（oasst-pythia-12b 等），「低偏誤」很可能只是「當 judge 能力不足」，所以「挑一個低偏誤模型」這個推論不成立——真正會拿來用的 judge 都在高端。對照 CALM，前沿模型的自評加成其實很小（GPT-4o +0.12、GPT-4-Turbo +0.08，error rate 1–2%），大效應集中在 Qwen2（+1.06）與 Claude-3.5（+0.49）。

**一個對 wiki 場景特別不利的細節**：Chen et al.（arXiv 2504.03846，與 2404.13076 共同作者 Shi Feng）主張在**可驗證任務**上部分自我偏好是「合理的」（強模型輸出真的較好），殘餘的有害偏誤集中在**自己出錯時仍給高分**。wiki 頁品質多半不可驗證，「合理偏好」的辯護不適用，而「看不出自己的錯」正是要防的失效模式。

反例一則：extractive QA 場景（短 span 答案、幾無文體特徵）觀察不到 self-preference——與長文 markdown 評分不類比。

這與 [[AI-自主工作流的實證檢驗]] 的結論同構：驗證要用 agent 無法從內部滿足的判準。LLM-as-judge 恰恰是「從內部滿足」的那一類，所以 [[設計品質的可量化檢測]] 才刻意把四項檢測全押在眼動模型、WCAG、CSS 統計這些非 LLM 的客觀量測上，只保留一項行為結果的 LLM 判斷。本頁探討的路線在方法學上比那頁弱一階，取捨要自覺。

### 3. 別一次丟多頁排名

*（強度：單一 preprint、單一資料集 439 樣本、2024-10 世代模型；3–4 選項的結果只有圖無逐模型表格，屬圖層讀數。arXiv 2410.02736，CALM）*

CALM 定義 Robustness Rate `RR = (1/|D|) Σ 𝕀(y_i = ŷ_i)`，即注入偏誤擾動前後判決一致的比例；position bias 的擾動就是重排候選順序，故 **RR < 0.5 字面上就是過半判決會因順序翻轉**。

pairwise RR（Table 7）：Claude-3.5 0.832、GPT-4-Turbo 0.818、GLM-4 0.781、GPT-4o 0.776、Qwen2 0.760、ChatGPT 0.566。而**評 3–4 個候選時多數模型掉到 0.5 以下**（正文與 Figure 6(a)）。

**注意這支持的是「兩兩比較 > 多候選一次排序」，不等於「pairwise > 絕對評分」**——後者本輪**沒有任何存活證據**。CALM 擾動的是「同一問題的多個候選答案」順序，不是多份獨立文件，外推到「一次排 21 頁 wiki」是合理但未經測量的推論。

### 附帶可搬：CALM 的 12 類偏誤清單

*（強度：分類法與指標定義不隨模型世代腐化；逐模型 RR 數值已過時，不可當現況引用。應以 preprint 引用，peer-review 狀態未確認）*

position、verbosity、compassion-fade、bandwagon、distraction、fallacy-oversight、authority、sentiment、diversity、chain-of-thought、**self-enhancement**、refinement-aware。其中 self-enhancement 正是本 vault 場景關心的那一類。

移植限制：部分偏誤（compassion-fade、bandwagon、diversity、sentiment）在 wiki 頁評分場景沒有明顯對應物；RR 定義在「判決一致」上，移植到絕對分數需改成「分數落在 ±k 內」之類，論文未做。

## 三、互聯知識庫層級的評估（2026-07-21 第二輪補查）

第一輪這塊零產出，換七組詞彙（knowledge graph quality assessment、cross-document consistency、Wikipedia ORES、ontology quality evaluation 等）重跑後**確實找到成熟文獻**——但它長在兩個離本 vault 有距離的傳統裡，且共同的問題是**可攜性斷崖**：所有指標都為大語料設計，n≈22 時退化或數學上未定義。

> **本節整體強度警訊**：第二輪 12 條主張的 verifier **全部回報 WebSearch 預算耗盡（200/200），沒有任何一條做過對抗式反面搜尋**，只做了主要來源逐字核對。對「某論文說了什麼」影響小，對「這是最好的做法／這領域沒有更新做法」則完全未覆蓋——故本節刻意不含後者這類主張。

### 傳統一：Linked Data 品質評估——有正式的互聯層詞彙

*（強度：同儕審查，Semantic Web Journal 7(1):63–93, 2016；但取得的是 author version，引用請用 SWJ 頁碼）*

Zaveri 等人的系統性回顧整理出 **18 個品質維度、69 個指標**，分析 30 個方法與 12 個工具，其中 **Interlinking 是一等公民維度**，定義為「同一概念的實體彼此連結的程度，無論在單一或多個資料源之間」。其 I1 指標明列網絡結構量測：interlinking degree（hub 數）、clustering coefficient（密度）、centrality、open sameAs chains。

四個可對映到 wikilink 檢查的指標（metric ID 皆經原文逐字核對）：

| 指標 | 原文定義 | markdown 對應 |
|---|---|---|
| A5 | 所有出站連結可解引用 | 出站 wikilink 目標存在 |
| I3 | 偵測所有本地入連／反向連結 | 反向連結存在 |
| A3 | 死連結（HTTP-GET 回 404） | 死連結 |
| CM4 | 已互連實例／總實例 | 非孤立頁比例（補數即孤立率） |

**但這對本 vault 的邊際貢獻幾乎為零**：`vault-lint` 機械層現有的死連結、孤立頁、雙向 wikilink 三項檢查，已分別等同 A3、CM4、A5+I3。文獻給的是**命名與正當性，不是新檢查項**。

必須帶的折扣：A5 與 I3 分屬 Availability 與 Interlinking 兩個**不同**維度，把它們併成「連結健康」是本頁的歸併框架而非論文自身框架；全部指標為 RDF/triple 層級，對 markdown wikilink 只是類比；A5+I3 的**合取**才近似「雙向性」，單獨任一個都不是。另有一處投票不一致值得記：同輪兩條敘述同一內容的主張被 0-3 否決，合理解讀是否決票針對「可直接搬到小 wiki」的可攜性宣稱而非事實本身——**引用該框架時引用其維度／指標定義，不要引用「可直接搬」的結論**。

### 傳統二：Wikipedia 文章品質評估——證明了「不能搬」

*（強度：官方 production model card，兩次獨立 fetch 數字一致；權重和 0.998）*

Wikimedia 生產環境的 language-agnostic 文章品質模型只用 6 個結構特徵：

| 特徵 | 權重 |
|---|---|
| page length | 0.395 |
| references | 0.181 |
| sections | 0.123 |
| **wikilinks** | **0.115** |
| media | 0.114 |
| categories | 0.070 |

連結相關特徵僅約 11.5% 權重，且那個 wikilinks 特徵**只是密度**（`sqrt(# wikilinks) / normalized-page-length`），不含雙向性、語意或指向正確性。精確性提醒：若把 references(0.181) 與 categories(0.070) 也算成連結類結構，合計約 36%，**不宜簡化成「連結不重要」**。

**最關鍵的是它為什麼搬不動**：這是無截距線性回歸映射到 0–1，各特徵以「**該 wiki 前 5% 文章**」為分母正規化。官方明載這使分數是相對於所在 wiki 族群分布的相對值——「在英文維基得 0.5 分的文章，若在簡明英文維基會得高得多的分數」。**22 頁的前 5% 只有 1 頁，校準步驟在此規模下數學上未定義。** model card 另自承不適用於 Wikipedia 以外專案，且「不評估行文品質，一篇塞滿假詞的長文章會被評為高品質」。

特徵空間本身倒是分類完整（*強度：ACM Computing Surveys 同儕審查系統性回顧，Moás & Lopes, FEUP, 2023*）：149 篇研究收集到 **321 個相異特徵**，分為 Content、Style、Readability、History、Network、Popularity 六族，Network 定義為「利用文章間連結量測影響力」。可攜限制同樣嚴重：History（版本史、多編者）與 Popularity（瀏覽量）在單人 vault 結構上不存在，Network 族是為百萬級語料設計的 centrality／PageRank 類量測，n=22 時統計基礎崩壞。**唯一可能有意義的是 Content／Style／Readability 三族**（單篇層級、不需大語料校準），但具體哪些特徵在繁中 22 頁上算得出來且有意義，未查（補充資料 Full Feature List.pdf 未取得）。

*（強度：MediaWiki 官方文件，廠商自承限制，2-1 通過）* ORES 的 articlequality 模型官方逐字說「不評估行文品質或語氣問題」，特徵為「有幾節？有沒有 infobox？幾個 references？references 有沒有用 cite 模板？」，唯一的缺陷偵測是 `citation needed`／`who?` 等**人工模板的計數**。兩個保留：ORES 已掛 deprecation banner（服務層遷往 Lift Wing），應寫成「ORES/Lift Wing articlequality」；且同輪多條宣稱該清單「完全不含 wikilink 結構特徵」的主張被 **0-3 否決**（language-agnostic 模型明確含 wikilinks 特徵）——**不可擴張成「Wikipedia 品質模型完全不看連結」**。

### 跨文件矛盾偵測：現成 benchmark 全是「單篇內部」

*（強度：ContraDoc 為 NAACL 2024 主會；WikiContradiction 為 IEEE BigData 2021。3-0）*

這是本輪最乾淨的否定答案：**現有 benchmark 沒有一個做跨文件矛盾**。

- **ContraDoc**（arXiv 2311.09182）自述為「第一個研究長文件**自我**矛盾的人工標註資料集」，全文以單一 document 為單位。
- **WikiContradiction**（arXiv 2111.08543，含 Wikimedia 作者）任務嚴格限單篇文章內，**把跨文章列為 future work**。

也就是說，本 vault 的跨頁一致性問題**沒有現成 benchmark 直接覆蓋**。

**唯一可搬的具體技巧**來自 WikiContradiction 的 future work：透過 `Contradicts others` 模板收集互相矛盾的文章**對**，「把每一對文章合併成一篇長文」，**藉此把跨文件問題轉成單文件問題**。這是最直接可搬的做法——但**論文本身沒驗證過**，且成本是 O(n²) 頁對（22 頁約 231 對）。

其架構模式也值得記（*2-1*）：先用 SNLI/MNLI 預訓練 pairwise 矛盾（繞開自我矛盾標註稀缺），再對所有句對打分、取 **top-K 最高矛盾機率句對**聚合成文件層級判定。產出的**不只是分數，還包含定位到具體句對的證據**——這個「分數＋定位」的形狀比單純打分對 lint 更有用。折扣：PCNN 需監督訓練、句對評分 O(n²)，論文未證明在小語料或繁中上可行；「可搬架構」是本頁的編輯性框架而非論文主張。

**LLM 做矛盾偵測不是即插即用的能力**（*2-1，且有明顯時效問題*）：ContraDoc 作者自評，即使表現最好、整體可超越人類標註者的 GPT-4 **仍「unreliable」**，在需要細微語境的矛盾上失敗。2025 年的後續工作（ContraGen 需多 agent 框架、HealthContradict 需 fine-tune、MMKC-Bench 發現模型偏好內部參數知識勝過外部證據）**一律靠專用 pipeline 或 fine-tune 而非直接 prompt**。

時效保留必須帶：這是 **2023 年對 2023 世代模型**的評測，至今約 2.5 年，**不可改述為「當前前沿模型不可靠」**。方向上則保守——ContraDoc 是**較簡單**的設定（整份文件在同一 context 內），跨頁分別檢索只會更難。這也直接折扣了「把頁面串接成單一 context 就能沿用」這條外推：ContraDoc 量到的失敗模式正是 nuance/context，串接長 context 後只會加重。

這與 [[Agent-維護知識庫的已知失效模式]] 第 3 條記錄的 CLAIRE AUROC 75.1% 相互印證：**自動矛盾偵測本質不可靠**，是跨兩篇獨立論文的收斂結論，非單一來源。

> **一則查核警訊的澄清**：第二輪 verifier 回報「54.7%／AUROC 75.1% 在查核的論文中不存在，來源不明」。**此為查錯論文**——它查的是 WikiContradiction 與 ContraDoc，而本 vault 該數字的出處是 [arXiv:2509.23233](https://arxiv.org/html/2509.23233)（CLAIRE），不在其查核範圍。既有頁面的引用**不受影響**，此處記錄以防日後被這條誤報推翻。

### 仍未答：agent 知識庫專案的內建評分

**第三題連續兩輪零產出，且第二輪明確記錄：證據鏈中沒有任何一次對目標 repo 的讀取。**

點名未讀的專案：nvk、Hermes 的 `llm-wiki` skill、llm-wiki-kit、wiki-garden、Wuphf、ai-memory、DiffMem、nashsu/llm_wiki、Cline Memory Bank、Letta MemFS、Mem0、ReMe、Basic Memory。

兩輪都敗在同一處：**預算耗在前面的塊，搜尋 agent 沒有真的去讀 repo**。這仍是「未查到」而非「已排除」。若要重跑，唯一沒試過的方法是**不派搜尋、直接 clone／讀 README 與原始碼**。

**2026-08-03 拍板不重跑**：下方 07-22 的階段 0 實測已推翻重跑的前提——本 vault 頁面方差太小，就算查到別的專案有內建評分，也不改變這裡的任何決定。此題**維持「未查到」狀態存查，不再排程重跑**。

既有工具的形狀仍印證這個空白：promptfoo 的 `select-best` 比較同一 test row 內的多個輸出、DeepEval 是 input→output 配對，**兩者都沒有「一組互相連結的文件」這個一等公民概念**；與 [[LLM-Wiki-生態實作比較]] 掃到的生態現況一致——各實作都在解「怎麼寫、怎麼檢索」，沒人在解「怎麼衡量寫得好不好」。

## 勿引用（本輪查證否決）

- ~~「rubric 只寫 Score 1 與 Score 5 的描述即得最高人類相關，中間 2/3/4 的描述貢獻近乎為零」~~——**0-3 否決**。若成立會是最實用的 rubric 設計指引，但未通過查證，不應寫進實作方案。
- ~~「多次取樣取平均優於 greedy decoding，mean 聚合最佳」~~——**1-2 否決**。同上。
- ~~promptfoo 三條較強版本的工具細節~~（`llm-rubric` 可直接評任意內容的強版本、固定 JSON 輸出格式、context-* 與非 context 指標的分界線）——**0-3 否決**，較保守的版本才存活。
- CALM 的「Most models rated their outputs more favorably, even when answer sources were anonymized」經中性重抓未命中，**判定為摘述而非原文，不可當逐字引用**；其實質由 Table 5 + Appendix C 支撐。
- arXiv 2404.13076 的「self-recognition 與 self-preference 呈線性相關」**沒有給相關係數或 p 值**，只有跨 fine-tuning checkpoint 的圖示；可引用的是 example-level Kendall tau。該主張為 2-1 分裂通過，作者自己在 Limitations 寫明只能「provide evidence towards the causal hypothesis without fully validating it」，且 fine-tuning 實驗只用 GPT-3.5 與 Llama-2-7b-chat、單一任務（摘要）、兩個資料集——**不可當已確立的通則**。

## 對本 vault 的判讀（2026-07-21）

**未拍板落地，僅記錄判讀。**

以 21 頁的規模，接 promptfoo 或 DeepEval 的管線成本大於價值——兩者都要 shoehorn，且這個實作摩擦只在文件層面推斷、未實測。真正可搬的是三條設計約束：

1. **rubric 必須明文寫出**，否則 judge 會穩定地量錯東西（且看不出來）。
2. **judge 換模型家族**，不要讓維護 wiki 的模型評自己的頁；blind rubric 沒有方法學依據。
3. **不要一次丟多頁讓模型排序**，要比就兩兩比。

曾考慮直接在 `vault-lint` 語意層加一段帶 rubric 的評分 prompt（比接外部 harness 務實）——但 2026-07-22 的實測（見下）證明這方向對本 vault 不划算，未採用。這與 [[Agent-維護知識庫的已知失效模式]] 記錄的「無法驗證 agent 真的用了 wiki」是同一類問題：本 vault 的品質回饋迴路目前全靠人眼看 PR diff，沒有任何自動化的品質訊號。

第二輪補上第四條，且是**否定性的省事結論**：

4. **互聯層級的既有指標對本 vault 幾乎沒有邊際貢獻**——Zaveri 框架的 A5/I3/A3/CM4 已等同 `vault-lint` 現有的雙向 wikilink、死連結、孤立頁三項檢查；Wikipedia 的品質模型因百分位正規化在 n=22 時未定義。**文獻能給的是命名與正當性，不是新檢查項**。這反而是好消息：機械層不必再擴。

真正還缺的是**跨頁一致性**（同一事實在多頁被重述時是否矛盾），而這塊現有 benchmark 全是單篇內部矛盾、沒有直接覆蓋。唯一具體可搬的是 WikiContradiction 未經驗證的 merge-pair 技巧（把矛盾頁對合併成長文，轉成單文件問題），成本 O(n²)、22 頁約 231 對。

### 2026-07-22 實測：建了評分 skill、階段 0 判定不適用、已刪除

*（強度：n=3 單次實測、非統計，但方向明確且與 vault 結構一致）*

依上述三條約束建了一個唯讀評分 skill（`vault-page-score`，五面向各三檔 `0/1/2`、每檔附頁內原文、同模型 subagent、一頁一 agent），並跑了信度驗證的**階段 0（分辨力）**：手挑「明顯好／中間／明顯弱」三頁各評一次，看檔次能否拉開。

**結果沒拉開**：三頁 15 格中 14 格頂到 2，只有「明顯弱」那頁在「強度標註」面向掉到 1。判定分辨力不足，未進階段 1，**skill 隨即刪除**。

兩個成因都成立，且都指向「這個 vault 不適合做頁面評分」而非「rubric 沒寫好」：

1. **天花板效應**：三檔制對這個 vault 太粗。22 頁全由同一套寫入慣例產出、又都過了多輪 lint，**本來就都不差**，想在「都不差」裡排高低，`0/1/2` 解析度不夠。
2. **ground truth 站不住**：事後看，我判為「明顯弱」的頁（早期概念頁、篇幅短）其實交叉引用密集、時間抗性好，**根本沒弱到哪去**——那唯一掉檔的一格可能正是 rubric 抓對了唯一真實差異，而我以為的「好／弱」落差不存在。

**根本結論**：LLM-as-judge 評分要有用，前提是頁面之間有足夠品質變異可排序；而本 vault 的寫入慣例＋lint **刻意消除了那種變異**。這正是本頁前述放棄條件（「結果與直覺高度一致就該放棄」）的近親——不是工具壞，是**對一個已被持續維護、方差很小的 vault，評分的邊際價值本來就低**。品質回饋迴路維持現狀：人眼看 PR diff。

**尚未解答的核心問題**：

- ~~絕對分數在 20 幾頁小樣本上是否穩定到足以排序？~~ 2026-07-22 實測**部分回答**：問題不在分數穩不穩，而在 vault 方差太小、天花板效應下根本排不出有意義的高低。test-retest（階段 1）未跑，因階段 0 已中止。
- merge-pair 技巧在 22 頁上的實際可行度——需實測而非文獻能回答。
- ~~第三題（agent 知識庫專案的內建評分）連續兩輪未觸及，需一輪純 repo 直讀。~~ 2026-08-03 拍板**不重跑**：方差太小這個前提已由 07-22 實測確立，答案不影響決定；維持「未查到」存查。

## 相關頁

- [[設計品質的可量化檢測]] — 反向對照：那頁刻意把判準押在非 LLM 的客觀量測（眼動模型、WCAG、CSS 統計）上，正是為了避開本頁探討的 self-preference bias
- [[AI-自主工作流的實證檢驗]] — 「驗證要用 agent 無法從內部滿足的判準」的原始論證；本頁的 self-preference 數據是該原則的實證支撐
- [[Agent-維護知識庫的已知失效模式]] — 本 vault 缺乏自動化品質訊號這個盲點的所在頁
- [[LLM-Wiki-生態實作比較]] — 生態現況：各實作都沒在解「怎麼衡量寫得好不好」
- [[多智能體研究系統-Anthropic]] — Anthropic 在生產系統中實際使用 LLM-as-judge 評測的做法
