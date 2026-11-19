---
title: Rajath Kotyal 規格先驗再交給 agent
description: AWS Kotyal 主張規格交給 agent 前先驗：LLM 譯成邏輯、SMT solver 抓矛盾與缺口、歧義交人決定，附 Kiro 對照與實作步驟
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-aws-specification-analyzer
published: 2026-11-11
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - testing
---

# Rajath Kotyal 規格先驗再交給 agent

來源：AI Engineer CODE 2026 演講〈Your Spec Has Bugs. Catch Them Before Your Agent Codes.〉的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-Kotyal-Your-Spec-Has-Bugs]]（Day 1 直播 `ZZ19zhYnDKY`，1:50:46–1:58:35，全場約 8 分鐘）。技術細節另讀 Kiro 官方部落格 [Requirements analysis: catching requirement bugs before they become code](https://kiro.dev/blog/deep-spec-analysis/)（2026-05-12）與[官方文件](https://kiro.dev/docs/specs/analyze-requirements/)。

**一句話**：規格本身就會有 bug（自相矛盾、一句兩義、沒涵蓋的狀態），換更強的模型寫 code 也修不好，因為模型無從得知作者本意。所以要在交給 coding agent **之前**先檢查規格：LLM 負責把自然語言翻成邏輯式，solver 負責檢查矛盾和缺漏，有歧義時由人決定。

## 講者與立場

Kotyal 自我介紹是 AWS automated reasoning group 成員，講的是他近期參與的「specification analyzer」專案。逐字稿把專案名辨識成「KO specification analyzer」，但演講沒有明說是哪個產品。對照 Kiro 官方部落格，兩邊的例子完全相同（backorder 兩條規則互相矛盾、「remove the record」有兩種讀法、閒置訂單沒有規則涵蓋），引用的研究數字一樣，三階段 pipeline 也一樣；部落格作者群（Stefan Zetzsche、Nadia Labai、Remi Delmas 等）也對得上演講結尾致謝的名字（逐字稿辨識成「Stefan, Nia and Delmos」）。因此可以合理推斷：演講內容就是 Kiro 的 **Requirements Analysis** 功能。這是推斷，演講本身沒提 Kiro。

**立場**：講的是自家產品功能，但語氣相當保守。他自己說「there's thin evidence right now for formalization and how it can be used in agents」，也明講除了使用者之外，沒有任何東西能判定規格對不對。

## 演講脈絡（依時間順序）

### 1. 開場例子：兩條各自合理、放在一起卻做不到的規則（1:51）

拿一般電商網站當例子：

- 規則 A：訂單送出且庫存不足時，訂單轉成 backorder。
- 規則 B：任何訂單都不得轉成 backorder。

兩句分開看都沒問題，但放在一起就不可能同時成立。LLM 讀到這種規格時，一定得自己挑一條，而作者從來沒做過這個決定。程式碼生成能力再強也解決不了，因為問題出在規格。

### 2. 為什麼值得做：三個數字（1:52）

他說根據公開研究：

- 提示不清楚時，生成程式碼的準確率下降 20–40%；
- 能跑的程式碼裡，60–90% 仍然是錯的；
- 部署後的 regression 多兩倍。

（三個數字的出處與失真處見下方「回查結果」，第三個說法和原論文對不上。）

### 3. bug 藏在哪：單句內和句與句之間（1:53）

- **單句內**：措辭有歧義、細節層級不對（太抽象，或直接寫成實作配方）。
- **句與句之間**：規則互相**矛盾**（conflict），或出現**缺口**（gap）。例如規則寫了已送出、已完成的訂單，卻沒有規則管閒置訂單。缺口不需要矛盾，也一樣會逼 agent 替作者做決定。

他拿這件事類比設計審查：工程師寫 design doc、畫流程圖，就是要在寫 code 前把流程定下來。他想做的是把這個「第一位審查者」自動化。

### 4. 三步 pipeline：refine → formalize → analyze（1:53–1:54）

1. **LLM refine**：先讓 LLM 自己清理措辭，清得乾淨就結束。
2. **LLM formalize**：清不乾淨，就把英文需求翻成 SMT-LIB 公式。
3. **SMT solver analyze**：交給 solver 判斷這組式子成不成立。成立就不動；如果發現兩句之間、或一句之內有兩種意思，就退回 LLM 重新處理那一句。

演講示範的是把「訂單送出且庫存不足 → backorder」寫成邏輯蘊含式。閱讀頁特別補了一句限制：solver 的精確性只作用在**已經形式化的那份需求**上，不能證明翻譯有抓到作者本意。LLM 可能把一句有歧義的話翻成一個完全一致的讀法，同時默默丟掉另一個同樣合理的讀法。

### 5. 用多次取樣抓歧義：sample → cluster → decide（1:55）

這是整場最有料的一段：

- 同一條需求讓 LLM 翻譯 **7 到 10 次**；
- 依**邏輯等價**把結果分群：字面不同但意思相同的歸同一群，字面相近但假設不同的分到不同群；
- 根據分群結果決定三種處置之一：**accept**（直接接受）、**ask**（請使用者釐清）、**abstain**（不實作這條）。

重點在於：重複翻譯的價值是讓**不同的假設浮出來**，不是靠多數決把生成文字變成事實。

### 6. 例子：「remove the record」（1:56）

「刪除這筆紀錄」到底是硬刪除，還是保留資料但對使用者隱藏？兩種實作都說得通，但資料保存、可否復原、日後查詢的後果完全不同。工具應該把選項擺出來讓人選，不該在 code 裡順手決定。演講同時重述了 conflict（規則一和規則三衝突）與 gap（沒有規則涵蓋閒置訂單）兩類發現。

### 7. 限制與結論（1:57–1:58）

- 規格對不對，沒有自動判定的 oracle，只有使用者能判斷。原因是隱含的領域知識：LLM 不知道很多領域常識，邏輯上完全一致的規格也可能描述的是錯的產品。
- 形式化用在 agent 上的證據目前還很薄，這個技術仍在起步階段。
- 收尾三點：**規格一定要先檢查再交給 agent**；**依邏輯等價把翻譯分群，看 LLM 有哪幾種讀法**；**LLM 翻譯、solver 檢查、人來決定**。人沒有答案時，就用 LLM judge 或乾脆不實作那一塊。

## Kiro 原文補上的細節（演講沒講到的部分）

8 分鐘的演講講不完，部落格多交代了以下細節（**廠商自述，未見獨立驗證**）：

- **四類需求 bug**：細節層級錯誤（太抽象，或寫成實作配方，例如「用 15 分鐘 TTL 的 JWT」）、歧義、不一致、不完整。
- **好規格的五個性質**：可測（testable）、不指定解法（solution-free）、無歧義、一致、完整。部落格說這些來自系統工程的長期實務，並引 INCOSE 的需求撰寫指南。
- **refinement 的做法**：從 user story 的成功狀態往回推，問達到成功需要哪些前提、什麼會阻止它、要有哪些錯誤路徑；同時檢查 EARS 句型是否用錯（錯誤情境要用 `IF … THEN`，`WHEN` 只用於正常情境）、有沒有模糊修飾語、有沒有混入實作語言。實例是一條「刪除物件」需求：原本 5 條驗收條件改寫了 3 條，再補 3 條遺漏的錯誤路徑（物件不存在、還有有效租約、使用者取消確認）。
- **形式模型分三部分**：schema（實體、屬性、事件、輸入、輸出，每個符號附自然語言說明以便回溯原文）；把每條 EARS 寫成 `antecedent => consequent` 的 assertion；以及 background assertions（例如時長非負這類隱含常識，靠多次取樣再用頻率門檻篩選）。
- **semantic entropy 的三段門檻**：熵低就採用多數群；熵高代表 LLM 很可能在亂翻，於是放棄這次翻譯，要求改寫需求；介於兩者之間時，對前兩大候選算 semantic diff，再轉成一個自然語言提問。門檻值可設定，但沒有公開具體數值。
- **邏輯分析能做的事**：找出 unsat 時回報造成矛盾的最小規則集（例如 {R2, R3}）；用 case split 找出條件式矛盾（已取消並退款的訂單被重新送出時，有庫存撞上 R1/R5，沒庫存撞上 R2/R3）；找完整性缺口（是否存在一個狀態，沒有任何規則會觸發）；另外產生「被接受／被拒絕的情境」，先用 LLM judge 篩掉不意外的，只把意外的拿去問使用者。
- **一律問二選一**：A 一律是「維持原樣」，B 一律是「改成某個具體方案」；也可以讓 LLM critic 代為選擇。回答完由 LLM 改寫受影響的需求。
- **部落格自承的弱點**：最大瓶頸是隱含領域知識（「訂單送出前不能取消」「已退款的款項不能再退一次」這類「暗物質」）。少了這些約束，solver 會在現實中根本不可能發生的情境裡回報問題，也就是誤報。

**產品現況**（2026-11-19 讀官方文件）：Kiro 產生 requirements 之後，chat 和編輯器的 Continue 選單都會出現 **Analyze Requirements**，與 Proceed to Design 並列；分析要跑「幾分鐘而非幾秒」，結果以釐清問題的形式陸續出現在 chat；目前只支援 feature spec，不支援 bugfix 等其他 spec 類型。支援範圍可能變動，以官方文件為準。

## 回查結果

| 說法 | 一手來源 | 核對結果 |
|---|---|---|
| 提示不清時 Pass@1 下降 20–40% | [Larbi et al. 2025, arXiv 2507.20439](https://arxiv.org/abs/2507.20439) | **對得上**。原文有「Task description issues lead to a 20–40% drop in Pass@1 in HumanEval and MBPP benchmarks」。條件：在 HumanEval／MBPP 上**人為把清楚的題目改壞**（改成歧義、矛盾、不完整），測 GPT-4 與 CodeLlama、DeepSeek-Coder、Qwen2.5 等 7 個模型。內文混用「percentage points」與「reduction」，絕對值還是相對值不明。另有細項：歧義約降 25–30%，矛盾最多降 40%。 |
| 能跑的程式碼 60–90% 仍是錯的 | 同上 | **對得上**。結論寫「60-90% of the code that compiles is semantically incorrect」。條件同上，只適用於被改壞的題目，不是一般 coding agent 的錯誤率。 |
| 部署後 regression 多兩倍 | [Yang et al. 2025, arXiv 2505.13360](https://arxiv.org/abs/2505.13360)（部落格引用的來源） | **對不上**。原文是「Under-specified prompts are 2x as likely to regress across **model or prompt changes**」，指換模型或改 prompt 時更容易退步，與部署無關，對象也是一般 LLM prompt，不是程式碼。演講把它講成「部署那段 code 時 regression 多兩倍」，屬於轉述失真。 |
| 形式化用在需求工程的證據很薄 | 部落格引 [Norheim et al. 2024, Design Science](https://www.cambridge.org/core/journals/design-science/article/challenges-in-applying-large-language-models-to-requirements-engineering-tasks/1FC7666F0A0B4E7091D2D4B2D46321B5) | **方向對得上**。這是一篇**文獻回顧**（作者明說不是系統性回顧），由 Airbus 產學合作資助。內文說 LLM 用於需求轉譯（含形式化）的應用「remains small」，生成類也「remain limited」，與演講的「thin evidence」一致。部落格說「AWS 自己的評估更樂觀」，但沒有公開數據。 |
| 專案就是 Kiro Requirements Analysis | [Kiro 部落格](https://kiro.dev/blog/deep-spec-analysis/)、[Kiro 文件](https://kiro.dev/docs/specs/analyze-requirements/) | **高度吻合**。例子、數字、pipeline、團隊名字都對得上，功能已正式上線。演講沒點名 Kiro，所以仍屬推斷。 |
| 「solver 回傳 valid 的 true/false」 | SMT 常識；部落格用語 | 演講口語簡化了。部落格的實際用法是做可滿足性（sat／unsat）查詢，並回報最小矛盾規則集，不只是一個布林值。不影響主旨。 |

貿易媒體（The New Stack）報導「AWS 在 60% 的軟體需求裡找到 bug」，本輪找不到 AWS 一手出處，列入勿引用。

## 搬到自己的 Claude Code／Codex 工作流程

Kiro 的完整 pipeline（多次形式化取樣、用 solver 判定邏輯等價、門檻設定）沒有公開實作，沒辦法原樣照搬。以下是能拆出來照做的部分，由輕到重排列：

1. **需求改寫成 EARS 句型**：正常情境寫 `WHEN <觸發> THE <系統> SHALL <可觀察行為>`，錯誤情境寫 `IF <條件> THEN THE <系統> SHALL <行為>`，持續狀態寫 `WHILE`，全域禁令寫 `THE <系統> SHALL NOT …`。每條都要寫得出輸入、輸出和條件（可測），也不准出現「用 X 技術」這類實作語言（不指定解法）。
2. **跑一輪 refinement prompt**：讓 agent 從 user story 的成功狀態往回推，逐條問「什麼會阻止它？錯誤路徑有沒有對應的驗收條件？」，順便抓出模糊修飾語（「大檔案」「很快」）。只補驗收條件，不寫 code。
3. **窮人版歧義偵測**：同一組驗收條件交給 **3–5 個彼此獨立的 subagent**（各開新 context，不讓它們看到彼此的輸出），每個都把每條驗收條件寫成具體的「輸入 → 預期輸出」測試案例，再比對各家的預期輸出。答案分歧的條件就是歧義候選。這是用**行為比對**取代 solver 的等價證明，只能抓到樣本測得到的分歧，無法保證沒有其他歧義。
4. **矛盾與缺口檢查（規則像狀態機時才做）**：請 agent 用 [`z3-solver`](https://pypi.org/project/z3-solver/)（Z3 的 Python 綁定）把每條規則寫成 `Implies(前提, 結果)`，再做三種查詢：每條規則的前提加上全部規則能不能同時成立（unsat 代表矛盾，再取 unsat core 找出是哪幾條）；是否存在一個狀態，所有非全域規則的前提都不成立（代表有缺口）；以及隨機抽幾個被接受或被拒絕的情境給人看。記得補上「已取消的訂單不能再送出」這類領域常識當背景約束，不然誤報會很多。
5. **把每個發現改寫成二選一問題**：A 維持原樣，B 改成某個具體寫法，由人來選。分歧太大、連兩個主要讀法都抓不出來的條件，就先不實作，退回重寫需求（對應演講的 abstain）。
6. 選完之後才進設計或實作。實作階段把這些驗收條件轉成 agent 改不到的測試。

**不划算的情況**：小改動、一次性腳本，或是需求只有兩三條時，第 3、4 步的成本高於收益。第 4 步只適合規則能寫成有限狀態與事件的需求（訂單、權限、狀態流轉），UI 手感或效能這類需求寫不成邏輯式。Kiro 文件也說分析要跑好幾分鐘，自己用多個 subagent 做只會更貴。

## 證據強度與限制

- **全場沒有任何對照實驗**：沒有「做了規格分析 vs. 沒做」的程式碼品質比較。動機用的數字全來自別人的論文，產品效果本身沒有數據。
- 20–40%、60–90% 兩個數字：**單一 preprint、未同儕審查**，基準是人為改壞的 HumanEval／MBPP 小題，不能外推成「真實專案的規格不清會讓 agent 錯六到九成」。
- 「AWS 內部評估顯示 LLM 形式化單條驗收條件表現不錯」：**廠商自述、未公開數據**。
- 機制描述（semantic entropy 分群、最小矛盾集、情境生成）：**廠商技術部落格一手描述，可信度高，但只是描述，不代表效果已被證明**。
- 演講只有約 8 分鐘，是 online 場次，深度主要靠部落格補足。

## 勿引用

| 主張 | 理由 |
|---|---|
| 「規格不清會讓部署後 regression 多兩倍」 | 原論文講的是換模型或改 prompt 時退步機率多兩倍，跟部署無關，演講轉述失真（2026-11-19 核對 arXiv 2505.13360 摘要） |
| 「AWS 在 60% 的軟體需求裡找到 bug」 | 只見於貿易媒體轉述，找不到 AWS 一手出處 |

## 與既有頁的關係與張力

- **呼應** [[AI-自主工作流的實證檢驗]] 的結論「規格越模糊，agent 越容易轉向讓測試通過」：Kotyal 把「把規格寫具體」從口號推進成可以自動檢查的流程。但他自己也說證據很薄，所以沒推翻該頁「spec-driven 流程可信、效果未經實證」的判斷，只是又多了一個沒有對照組的廠商實例。
- **延伸** [[長跑-Agent-的目標定義與計畫工具]] 記錄的 Kiro EARS 記法和 spec-kit `[NEEDS CLARIFICATION]` 標記：那兩者靠作者或 agent **自己意識到**歧義才會留下標記；Kotyal 的方法是讓多次翻譯之間的分歧**自動讓歧義浮現**，不依賴寫的人自覺。該頁提到的「checklist 勾了但標記還在」那種假完工，這套方法不會出現，因為分歧是算出來的，不是勾選出來的。
- **互補** [[Lauren-Tan-把糾正寫進程式庫]]：Tan 管的是 code 產出**之後**，把糾正寫成確定性檢查；Kotyal 管的是 code 產出**之前**，讓規格先通過邏輯檢查。兩人的共同點是：把能交給確定性工具（lint／型別／solver）的判斷交出去，人只處理真正需要判斷的部分。
- **與 [[OpenSpec]] 這類輕量規格工具的張力**：OpenSpec 主張規格就是一組 markdown 契約，不做形式驗證。Kotyal 的方法暗示，光有 markdown 契約時，矛盾和缺口會原封不動進到實作；但加上形式化的代價是要多跑好幾分鐘，還要先補齊隱含領域知識。兩邊都沒有效果數據可以分出高下。
