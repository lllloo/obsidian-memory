---
title: Agent 維護知識庫的已知失效模式
description: 長期由 agent 自主維護的 markdown 知識庫會怎麼壞：機制成立的三種退化、判定不適用的類比、無法驗證的盲點，逐條標證據強度
created: 2026-07-21
updated: 2026-07-21
parent: "[[wiki/01.index]]"
tags:
  - wiki
  - ai-agent
  - memory
  - knowledge-graph
---

# Agent 維護知識庫的已知失效模式

本 vault 走的是「agent 全權維護、無硬守門、事後 diff review」路線（見 [`CLAUDE.md`](../CLAUDE.md) 與 [`SYSTEM-DESIGN.md`](../schema/SYSTEM-DESIGN.md)）。這個選擇有對立論述與已知失效模式，依寫入慣例第 6 條**應明列而非丟棄**。本頁收攏 2026-07-21 一輪四路平行搜尋的結果，逐條標**證據強度與場景差距**——多數來源的實驗場景與「23 頁個人 vault」差距很大，方向可借鏡、速率不可直接套用。

與 [[LLM-Wiki-生態實作比較]] 的分工：那頁比各實作**怎麼做**，本頁記這條路線**怎麼壞**。

## 機制上成立的失效模式

### 1. 迭代重寫必然累積失真（Broken Telephone）

模型反覆處理自己的輸出時，每輪都是一次有損重編碼，失真隨鏈長累積。作者結論是**退化不可避免，但可用 prompt 策略減緩**。

**強度：同儕審查**（[LLM as a Broken Telephone, ACL 2025 長文](https://aclanthology.org/2025.acl-long.371.pdf) / [arXiv:2502.20258](https://arxiv.org/abs/2502.20258)，三資料集各 150 篇，指標含 BLEU/ROUGE/BERTScore 與 FActScore）。本輪唯一經同儕審查的直接證據。

**場景差距（重要）**：其迭代載體是**翻譯往返鏈、每輪強制全文重生成**；本 vault 的 wiki 頁多為**局部編輯**且每輪有 `raw/` 原文可回錨，重寫壓力小得多。**方向成立，速率不可套用**（每輪衰減曲線未取得，PDF 文字層抽取失敗）。

**對本 vault 的推論**：真正危險的不是「改很多次」，是**不回讀 `raw/` 就直接改 wiki 頁**——那才是無錨點的迭代鏈。

### 2. 壓縮改寫系統性丟掉限定語境

LLM 壓縮**不是均勻丟資訊，而是偏食脈絡類事實**（caveat、適用條件、限定詞）。壓縮後 context facts 佔比 25% → 9%，產物是「事實正確但決策含意相反」的摘要。

實測：naive 壓縮決策翻轉率 **33.0%**，對照「重讀原文」的雜訊底線 11.0%，超出兩倍以上。把被刪的脈絡事實補回可救回 37% 的翻轉案例（隨機補其他事實僅 16–19%）。**緩解實測**：只改 prompt（要求保留 decision-relevant 限定詞）即 33.0% → **21.3%**——純 prompt 級介入就吃掉最大一塊改善。

**強度：preprint、非同儕審查**（[When Summaries Distort Decisions, arXiv:2606.29251](https://arxiv.org/html/2606.29251)，S&P 100 財報 MD&A n=300／法說 n=297），但對照設計紮實且有商用系統部署驗證。

**場景差距**：量測的是金融下游決策翻轉，wiki 無等價指標。但**機制**（壓縮偏食脈絡）與「摘要頁／綜合頁改寫」高度同構，類比成立。

**對本 vault 的推論**：寫入慣例第 6 條的強度標註方向正確，但目前只綁 deep-research 產出。可擴大為通則——**改寫時限定詞（適用條件、反例、版本前提）優先於結論保留**。零基礎設施成本。

### 3. 真實 wiki 的矛盾以數值為大宗，且自動偵測不可靠

Wikipedia Vital Articles 955 條標註事實的實測：**約 3.3% 的事實與語料內他處矛盾**。類型分布：

| 類型 | 佔比 |
|---|---|
| 數值不一致（含 off-by-one 23.0%） | **54.7%** |
| 邏輯矛盾 | 17.5% |
| 定義差異 | 10.6% |
| 時間衝突 | 7.9% |
| 具名實體不一致 | 6.0% |
| 分類錯配 | 2.1% |
| 空間錯誤 | 1.2% |

同篇的 agentic 偵測系統 CLAIRE **AUROC 僅 75.1%**（小勝 NLI pipeline 72.2%、retrieve-and-verify 73.0%），作者自承仍有大量改進空間。

**強度：preprint，但屬人類維護的真實 wiki 實測、非模擬**（[arXiv:2509.23233](https://arxiv.org/html/2509.23233)）。

**場景差距**：Wikipedia 是多人協作、規模大數個量級，23 頁 vault 的矛盾絕對數必然低。但**類型分布**是關於「文字知識庫的矛盾長什麼樣」的通則，判斷可遷移。

**兩個推論**：其一，**lint 語意層目前找的邏輯矛盾只佔 17.5%**，而佔 54.7% 的數值／日期不一致沒有專門規則——投報比最高的補強方向。其二，**自動矛盾偵測本質不可靠**（約四分之一判斷是錯的），本 vault「語意項一律自主修補」等於在 75% 準確率的偵測器上直接執行寫入；不必改回只報告，但修補動作應在 diff 中可辨識。

### 4. 「事後看 diff」這條防線本身會鬆動

automation bias：人把自動化輸出當認知捷徑，產生 commission error（接受錯誤輸出）與 omission error（沒發現 AI 漏掉的）。文獻另指出**提供解釋會提高接受度但通常不改善判斷準確度**，有效的是提高實際驗證投入。

**強度：綜述級文獻**（涵蓋同儕審查研究；[automation bias review](https://www.researchgate.net/publication/392771285_Exploring_automation_bias_in_human-AI_collaboration_a_review_and_implications_for_explainable_AI)、[MIT SMR](https://sloanreview.mit.edu/article/ai-explainability-how-to-avoid-rubber-stamping-recommendations/)、[Bias in the Loop, HDSR 8.2](https://hdsr.mitpress.mit.edu/pub/nrcn4h7d/release/2)）。**註**：常被引用的「跟隨錯誤建議比率高出 26%」一數取自搜尋摘要、未讀原始系統性回顧全文，**當方向性而非精確值**。

**場景差距**：研究場景為醫療／招募等即時決策，不是事後讀 diff；共通的是「人審查機器輸出」的結構，不共通的是時間壓力與責任歸屬，遷移性評為中等。

**對本 vault 的推論**：拿掉所有硬守門後唯一防線是使用者事後看 GitHub diff，而其失效模式**不是「不看」，是「看了但看不出」**——當 diff 是流暢繁中散文、風格與既有頁一致時，被無聲刪掉的限定詞最難察覺，而那正是第 2 條實測的主要失真形態。**緩解方向是改變 diff 的可審性而非增加審查量**（例如 commit message 列出本輪改寫／刪除了哪些既有主張，把 omission 轉成 commission），文獻亦顯示增加 review 次數不等於增加 review 品質。

## 判定為不適用的類比

- **model collapse ——【勿引用】**。它講的是**用合成資料遞迴訓練導致模型權重層的分布崩塌**（尾部消失、方差塌陷，如 [arXiv:2509.04796](https://arxiv.org/html/2509.04796v1)）。本 vault 沒有任何訓練環節，模型權重不因 wiki 內容改變；唯一共同點只是「遞迴吃自己輸出」這個表層描述。**用它論證 wiki 退化會讓論點站在不成立的基礎上**；機制上真正類比得上的是上面第 1、2 條。

## 無法驗證的盲點

**沒有機制能證明 agent 真的在行動前搜尋過知識庫、真的用了取回的內容、真的因此改變了行為。** 這是 [Wuphf 第三方 review](https://zby.github.io/commonplace/agent-memory-systems/reviews/wuphf/) 對該專案的批評，明指找不到 with/without-memory 的 ablation——**本 vault 同樣暴露**，我們沒有任何機制驗證這批 wiki 頁真的改善了回答品質。

目前無解法，記為已知盲點而非假裝不存在。相關但方法論最嚴謹的一篇是 [Progressive Disclosure for LLM-Maintained Wiki KBs, arXiv:2607.04576](https://arxiv.org/pdf/2607.04576)（**預註冊 ablation**，題目與本 vault 幾乎完全對口），但其 PDF 文字層抽取失敗、**未取得任何數字**，只取到方向性描述（progressive disclosure＋prompt caching 降成本、觀察到 drift/contradiction/orphan/bloat、建議週期性 garbage collection）。**值得日後專門讀原文**。

## 對立論述（Wuphf Show HN 串）

[Show HN 討論串](https://news.ycombinator.com/item?id=47899844)（260 分）是對「全 LLM 維護 markdown wiki」最集中的公開批評。以下歸屬**經 HN Algolia API 抓原始留言逐則核實**——初次以 WebFetch 讀取時，摘要模型錯置引言歸屬**並虛構了一段作者回覆**，該虛構內容已剔除。這本身是可操作的教訓：**二手摘要讀討論串不可靠，具名歸屬必須回原文核對**。

| 批評 | 提出者 | 性質 |
|---|---|---|
| 「agent 未經人眼寫的內容衰減最快；六個月後有自信但錯誤的條目，lint 分不出來」 | Abby_101 | **半 firsthand**（"my own LLM features"），無數據、無可驗證產物 |
| 「壞條目被其他 agent 引用，最後整個知識庫都是自信的胡說」 | ryanshrott | 個人經驗值；其提出的「投票制」緩解措辭為 "Some teams use…"，**屬轉述非自身實測** |
| 「Everyone is writing. Nobody is reading.」 | simsla | **純推測**，一句格言、無經驗陳述 |
| 「怎麼阻止 LLM 寫太多？我建過幾套類似系統，都太容易讓 LLM 一直記錄到整個系統變成一團亂、越大越沒用」 | johntash | **本串最紮實的 firsthand**（實際建過多套、實際失敗），但他補充那是幾年前的實驗、新模型或許不同，屬**過期經驗**；他自己也未提出解法 |
| 「Karpathy 的設定依賴一個 LLM 必須手動保持同步的 index.md，而 LLM 不擅長這件事，staleness 會跨 session 累積」 | jermolene（TiddlyWiki 原作者） | **具名資深實作者的設計判斷**，非實證量測 |
| 自 2026-02 起實跑 LLM-writes-a-wiki，正面經驗（環境設定知識的回存與重用） | 0123456789ABCDE | firsthand **成功案例**，列出以免單邊呈現 |

**判讀**：批評有力度但**證據薄**——全串無人提出可驗證的量化證據，也無人做過對照。串中唯一收斂的建議是「draft freely, promote on approval」，但那是 Wuphf 這類**多 agent 團隊**場景的解法（多 agent 互相污染）；本 vault 是單使用者＋單 agent，capture 與 promote 之間沒有第三方，加 promotion gate 大概率只是把「事後看 diff」改名成「事前看 draft」，同時違反零守門設計。**故不因此串採用 promotion gate。**

真正該吸收的是兩條不需守門即可處理、也不與設計衝突的：**寫太多**（johntash）與**物化索引漂移**（jermolene）。後者值得特別記——本 vault 的 `wiki/01.index.md` 正是手動維護的物化索引，而 Obsidian Bases（`.base`）就是 jermolene 所說的計算式視圖，vault 已在 `feeds/youtube/` 用了。23 頁尚不急，是為 100+ 頁預備的方向。

## 不可引用的數字（附理由）

被查證否決但仍記錄，防日後誤引：

- **「向量搜尋讓 recall 從 58.2% 提升到 71.4%」**（nashsu/llm_wiki）——單一 repo 自報、無公開方法論、無獨立驗證，baseline 是自家關鍵字搜尋。**勿外推。**
- **「LLM wiki 超過 5–10 萬 token 就失效」**——多篇 2026 部落格互相轉述，**未找到原始實測來源**。不可當事實引用；但它指向的問題（index 頁隨頁數線性膨脹）是真的，值得自行觀察。
- **Agent Drift 的「漂移中位數第 73 次互動出現」**（[arXiv:2601.04170](https://arxiv.org/html/2601.04170)）——**全來自模擬**、preprint、未同儕審查，且各項數據整齊得可疑（所有緩解 p<0.001、效果單調遞增）。**尤其別把「73 次互動」寫進任何頁面。**
- **Knowledge Compounding 的「−84.6%」**（[arXiv:2604.11243](https://arxiv.org/abs/2604.11243)）——**僅 n=4 查詢**、單一系統、30 天數字為**推估非實測**。其理論框架另有價值（見 [`SYSTEM-DESIGN.md`](../schema/SYSTEM-DESIGN.md)「為何有效」），**但數字勿引**。
- **[Silent Failure in LLM Agent Systems, arXiv:2606.08162](https://arxiv.org/pdf/2606.08162)**——單作者、無實驗的立場論文，「熵原理」是隱喻不是量測。概念貼切但**無證據價值**。

## 關聯

- 實作面對照：[[LLM-Wiki-生態實作比較]]——那頁比各實作怎麼做、哪些設計已收斂，本頁是同一批來源的失效面；兩頁共用 Wuphf 與 HN 串的證據基礎
- 記憶系統定位：[[Claude-Code-記憶系統六層比較]]——本頁的失效模式限於 Level 5（自組織知識庫）路線，向量／自動抽取路線的失效模式另見 [[Mem0]]
- 同構的抽取污染：[[Mem0]]——其「LLM 每次寫入抽取原子事實」在長時 agent 上自我放大污染，與本頁第 1、2 條同屬「反覆重編碼」家族，是本 vault 不採自動抽取的反面對照
- 工具清單：[[Memory-Atlas]]——本頁記這條路線怎麼壞，該頁是同一家族的中立工具目錄（含授權與自建難度），兩頁同為 2026-07-21 同一輪搜尋的產物
- 空氣數字的既有清單：[[AI-自主工作流的實證檢驗]]——該頁已列必須停止引用的數字，本頁末節是同一紀律在 agent 記憶領域的延伸
