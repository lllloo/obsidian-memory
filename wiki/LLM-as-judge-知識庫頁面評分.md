---
title: LLM-as-judge 知識庫頁面評分
description: 用 LLM 為 markdown 知識庫頁面打分的現成方案地景與方法學約束：promptfoo／DeepEval 兩條可用路徑、rubric 決定信度、self-preference bias 匿名化擋不住
created: 2026-07-21
updated: 2026-07-21
parent: "[[wiki/01.index]]"
tags:
  - evaluation
  - ai-agent
  - wiki
  - knowledge-graph
---

# LLM-as-judge 知識庫頁面評分

問題：能不能用 LLM 給 wiki 頁「打分數」，用來排序該修哪頁、或當品質 gate？本頁是 2026-07-21 一輪 deep-research（5 搜尋角度、每條主張 3 票對抗查證）的回存，聚焦**純 LLM-as-judge 路線**（機械指標如 markdownlint、連結數統計不在範圍內，僅作對照）。

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

## 三、證據空白：互聯知識庫層級的評分

「針對互聯知識庫（交叉引用品質、頁面間一致性、網絡結構健康度）而非單篇文件的 LLM 評分做法」，以及「其他 agent 記憶／LLM wiki 專案是否在做頁面品質評分」，本輪**沒有任何主張存活**。

**這是證據空白，不是已證實不存在**——16 條存活主張全落在工具與方法論兩塊，第三塊零產出，且本輪多個 verifier 的 WebSearch 預算明確用罄（有兩條 claim 記載 200/200）。

既有工具的形狀倒是印證了這個空白：promptfoo 的 `select-best` 比較同一 test row 內的多個輸出、DeepEval 的資料模型是 input→output 配對，**兩者都沒有「一組互相連結的文件」這個一等公民概念**。這與 [[LLM-Wiki-生態實作比較]] 掃到的生態現況一致：各實作都在解「怎麼寫、怎麼檢索」，沒人在解「怎麼衡量寫得好不好」。

重跑此塊應換詞彙：knowledge graph quality assessment、documentation coherence evaluation。

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

若要做，直接在 `vault-lint` 的語意層加一段帶 rubric 的評分 prompt，比接外部 harness 務實。這與 [[Agent-維護知識庫的已知失效模式]] 記錄的「無法驗證 agent 真的用了 wiki」是同一類問題：本 vault 的品質回饋迴路目前全靠人眼看 PR diff，沒有任何自動化的品質訊號。

**尚未解答的核心問題**：絕對分數（1–10）在 20 幾頁的小樣本上是否穩定到足以排序？本輪只證明「無 rubric 會與人類脫鉤」與「多候選排序極不穩」，**沒有任何來源直接比較「絕對評分 vs pairwise」在文件級評分上的排序穩定度**。可行的驗證是自己對同一頁重複評分數次量 test-retest 變異，而非再查文獻。

## 相關頁

- [[設計品質的可量化檢測]] — 反向對照：那頁刻意把判準押在非 LLM 的客觀量測（眼動模型、WCAG、CSS 統計）上，正是為了避開本頁探討的 self-preference bias
- [[AI-自主工作流的實證檢驗]] — 「驗證要用 agent 無法從內部滿足的判準」的原始論證；本頁的 self-preference 數據是該原則的實證支撐
- [[Agent-維護知識庫的已知失效模式]] — 本 vault 缺乏自動化品質訊號這個盲點的所在頁
- [[LLM-Wiki-生態實作比較]] — 生態現況：各實作都沒在解「怎麼衡量寫得好不好」
- [[多智能體研究系統-Anthropic]] — Anthropic 在生產系統中實際使用 LLM-as-judge 評測的做法
