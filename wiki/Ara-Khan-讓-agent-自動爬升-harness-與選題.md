---
title: Ara Khan 讓 agent 自動爬升 harness 與選題
description: Cline 讓監督 agent 跑 eval、改 harness 再重跑的實驗與選題建議，附 PR、prompt 回查與數字強度
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-cline-rsi
published:
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - evaluation
  - ai-agent
---

# Ara Khan 讓 agent 自動爬升 harness 與選題

來源：AI Engineer CODE 2026 線上場〈Pick Problems That Survive When AI Solves Coding〉的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-Khan-Pick-Problems-That-Survive]]。實驗細節另核對 Cline 官方 blog〈[Recursive Self Improvement for Coding Agents](https://cline.bot/blog/recursive-self-improvement-for-coding-agents)〉（2026-07-24，Ara Khan 署名）、作者公開的 [hill-climb prompt](https://gist.github.com/arafatkatze/fe7d3743315c80d5e3e8ab1bdef39903)、[成本與 trace 說明](https://gist.github.com/arafatkatze/8ef2e3d452703fc2978715b40dff97fe)，以及 [cline/cline#12465](https://github.com/cline/cline/pull/12465)。

**一句話**：只要能做出「判斷自己有沒有變好」的量測，就能讓一個監督 agent 反覆跑 eval、讀失敗、改 harness、再跑一次；工程師應該靠近這種改進迴圈（推論、資料、post-training、硬體等），避開下一版模型一出就被抹掉的題目。

## 講者與立場

Ara Khan 自稱 Cline 的 founding engineer。演講的核心案例是他用 Cline 自家 harness 跑的實驗，對應的 blog 結尾直接推銷 Cline 是「跑 Kimi K3 最好的 harness」和付費方案 ClinePass。所以 benchmark 數字有推銷自家產品的動機，下文的強度標註要一起看。演講本身的後半段是職涯建議，不賣產品。

官方閱讀頁的編者把話講得比講者保守：它把標題的「遞迴自我改進」和實際展示的 harness 實驗分開，說兩者之間「留有相當距離」，並說實際能帶走的東西比標題窄。

## 演講脈絡（按順序）

### 1. 三個目標與焦慮來源（開場）

他先列三個目標：看懂 frontier lab 的路線圖、在模型快速進步下想清楚未來幾年的職涯、以及「escaping the permanent underclass」（他說聽起來像玩笑，但有人真的在擔心收入全集中到少數 GPU 廠和模型公司）。背景是：以前拿 side project 放 GitHub 證明能力，現在任何 frontier coding agent 都能一次寫出來，「proof of work」失效了。

### 2. 先丟出案例：Kimi K3 在 Cline 上只拿 77.5%

Cline 每次新模型發布都會 hill climb，想把該模型在自家 harness 上的分數推到最高。Kimi K3 在 Cline 上跑 Terminal-Bench 2.1 拿 77.5%，但他說模型發布文件宣稱可到 85% 以上（blog 寫的 vendor 數字是 88.3%，見回查）。差距代表 harness 有改進空間，而手動 hill climb 有大量重複的苦工，於是他們把這件事自動化。這段先當伏筆，後面才講細節。

### 3. RSI 的定義與他的歷史敘事

遞迴自我改進（RSI）：AI 系統幫忙造出更強的下一代，下一代再重複這個過程。他承認這聽起來像空想，接著用時間線說明怎麼走到這裡：

- 2021 年某家 lab 的路線圖寫要做能用對話建立、編輯、解釋軟體的通用助手，像工程師同事一樣寫函式、找 bug、設計 API（逐字稿把出處辨識成「topics road map」，原文出處本頁未查到）。
- 2022 ChatGPT；2023–2024 chat model 能呼叫簡單函式；2024 年某代 Sonnet 讓 agent 能真的用讀檔、改檔、搜尋、列目錄這類工具。
- 2024 AutoGen 這類多 agent 對話，他評為「janky」、大多是確定性的流程拼接。
- 2025 agent 越來越好、越快、越便宜；2026 開始問「agent 能不能改進自己」。

這段是他的敘事框架，不是論證的證據。

### 4. 評估從「答對問題」變成「環境真的能用」

單輪問答（例：貓有幾根腳趾）可以直接判對錯。但「幫我設定這個 MCP」要上網查設定、下載、改檔、接資料庫、跑 bash，最後 agent 說「我做好了」只是很弱的證據，要用測試確認環境真的能動。

他們用 Terminal-Bench（終端環境的 agent benchmark）。他列出的評估組成：

- 每題在獨立 sandbox 裡跑；Terminal-Bench 2.1 有 89 題，就開 89 個平行容器，互不影響。
- 獨立 grader 記錄 turn 數、token、延遲、tool call 數、整條 trajectory。
- 另外檢查有沒有 reward hacking：有沒有作弊、有沒有上網查答案。

拿到總分後要看失敗的種類，例如讀檔工具壞了；推論太慢，agent 還在推進卻耗完約 45 分鐘的題目時限；agent 原地打轉。把失敗分桶（例如 10 個某種 tool call、20 個推論問題），再針對 harness 改。閱讀頁的整理是：一旦分好類，harness 就從包著模型的黑盒變成「一組可修的機制」。他說手動做很耗時，但這是他們學會怎麼改進模型表現的方式。

### 5. 在評估迴圈外面再包一個 agent

做法：GPT-5.6 Sol 當主導（監督）agent，Kimi K3 是被評估的模型。監督 agent 的循環是：跑 eval → 看分數與失敗 → 找出哪裡出錯 → 改 Cline harness → 再跑 eval。他提醒這很容易出軌：一輪 eval 大約一小時，接著要讀回饋、判斷自己有沒有正確解讀、確認改動是真改進而不是 reward hacking。

結果（演講說跑了 17 小時，同一段又說「13 小時後回來看」；blog 寫約 17 小時）：監督 agent 自己找到並分桶了 loop detection、背景程序跑太久、file index 等問題，自主完成整個 hill climb。他強調「我們」其實是指 GPT-5.6 Sol，他本人沒介入。逐字稿說 baseline 是「27%」，與投影片的 77.5% 不符，應是辨識錯誤。

投影片（閱讀頁附圖）的四個改動與數字：

| 步驟 | 投影片標註 |
|---|---|
| Baseline | 69/89（77.5%） |
| Bounded provider retries | 診斷切片 13/14 |
| Progress-aware loop detection | 診斷切片 4/4 |
| File-index request liveness | 診斷切片 1/1 |
| Safe background-process guidance | 診斷切片 2/2 |
| Frozen full stack | 77/89（86.5%） |
| Best run | 79/89（88.8%） |
| 其他確認輪 | 76/89、78/89；重複平均 77.5/89（87.1%） |

投影片自己加的但書：中間階梯高度是示意，各改動在 89 題上的貢獻**沒有分離**；retry 的歸因部分模糊；背景程序是「guidance」不是強制；兩次中斷的執行已揭露並排除；max reasoning 支援保留但不計分。

閱讀頁的評語：這證明自動化流程**能找到有用的 harness 改動**，但不證明每一步造成了圖上的提升幅度，也不該只報最佳那一輪。

### 6. 外層迴圈 vs 任務中途自改

他區分兩件事：監督 agent 在多題之間改 harness（外層），和 agent 在任務中途即時改自己。後者他個人認為更難，因為會過度針對眼前的問題。改動要能在更廣的題目上站得住，要能用「適用範圍廣」來說服人，否則所謂自我改進只是對單一任務的過擬合。

### 7. 同樣的結構往下延伸到整個 stack

既然模型能改 harness，就能改別的。他的例子：

- **推論 kernel**：OpenAI 的貼文說 GPT-5.6 Sol 自主重寫並最佳化自家 production kernel，與其他 kernel 改進合計讓端到端服務成本降 20%，另有 15% 的 token 生成效率提升（回查見下）。他推論對 frontier lab 來說這是數十億美元等級的節省。
- **kernel 競賽**：某家辦 kernel 撰寫比賽的公司（逐字稿為「core auto」），冠軍說自己從沒手寫過 GPU operator，全靠 LLM 與 agent。本頁未查到出處。
- **其他層**：pre-training（以 Nemotron 的 AI 篩選資料為例）、post-training（以 Constitutional AI 為例）、推論、eval 生成（Cline 自己的例子）。他說從電力、網路請求、模型推論到回應，整條管線每一段都能最佳化。

閱讀頁特別註明：他的主張不是單一 agent 已經掌握所有層，而是每一層都能露出可量測的目標和回饋迴圈。

### 8. 人的一次糾正就是一筆能力缺口

例子：要 agent 幫資料庫加一個欄位、填值、前面加 cache。它都做了，但 cache 的設法不對，你說「改成這個 TTL」，問題解決、你繼續過日子。他的觀點是：每一次人對 agent 的糾正，都標出模型能力邊界上的一個「delta」。與其只告訴 agent 答案就算了，不如把情境存成可重現的任務，它就能變成 eval 或訓練訊號。post-training 做的就是找困難的長任務、讓模型慢慢爬升。結論是「任何有可驗證迴圈的東西都能被最佳化」，而且不限於軟體。

### 9. 實體世界的例子

- 一段機器人自己在打字、想「解決機器人學」的影片，他拿來比喻：若機器人能解讀結果並持續改進，就是某種超級智慧機器人。這段是想像，不是實驗。
- 他送女友的一個小裝置（有鏡頭、喇叭、麥克風，內含 agent）回應很慢。他把裝置接上電腦，讓 coding agent 自動對它下測試、問它「你現在看到什麼」，量端到端延遲，拆出每個高延遲或演算法不對的情境。再給 coding agent 一把 OpenRouter key，讓它在韌體、tool call、推論模型、語音辨識模型之間自動實驗，一夜之後裝置「被深度最佳化」。他**沒給任何量測數字**，閱讀頁也明說沒有證明特定的加速幅度。

### 10. 迴圈相連：這是預測，不是 benchmark 結果

推論更便宜 → 同樣預算能跑更多實驗 → 資料和模型更好 → 下一輪實驗又更便宜。他說「parts of the loop are already weird」，我們已經很接近 RSI 迴圈的部分環節。閱讀頁強調不能把小型 harness 實驗和這個總體經濟預測混為一談：他的職涯建議源自「收益會集中到模型與基礎設施提供者」的擔憂，而不是已證明的智慧爆發時程表。

### 11. 職涯建議：靠近改進迴圈

- 「please move closer to the RSI loop」。他認為做營建 agent、某某 agent 這類垂直應用是「見樹不見林」，很多題目「只差一次模型發布就會被完全抹掉」，而且整天說「Claude 幫我做這個」也不怎麼有智識上的刺激。
- 建議方向：模型還不足的端到端管線，例如推論、post-training、實體互動、硬體、網路、資料管線。他觀察到做資料管線和實體硬體的公司都在募資。
- 他引用一張 Anthropic 某人的投影片（逐字稿為「Sasha」，本頁未查到出處）：假設你只剩一到五年能對世界做出貢獻，偏好有野心、目標明確、快速的合作；把給自己的時程大幅壓縮。
- 但也要權衡：題目太有野心時，是否該等下一代 frontier 模型出來再做，而不是現在硬做繁複的 workaround。
- 選題準則：**受益於規模、但不會單靠規模就被解掉**的題目；最好本身就是改進管線的一部分。
- 如果你發現日常工作 Claude 一次就做完、自己只是個「proxy」，值得退一步想：哪裡是你真正有貢獻、經得起時間的題目。

他在結尾承認時程可能太悲觀或太樂觀，歡迎反駁。

## 回查結果（2026-11-19）

| 項目 | 結果 |
|---|---|
| Cline 官方 blog | 存在，2026-07-24 發布，Ara Khan 署名。細節比演講多：baseline 一次完整 run 69/89、花 $79；共五個實驗（見下）；combined 77/89、$65；確認輪 79/89、$49.8。說他們每次新模型都會手動 hill climb：1 月花了約兩週人工把 Opus 4.5 從 47% 拉到 57%（2 月發布的 hill climbing playbook 由 4 位工程師合寫），這次換成一個 prompt 跑約 17 小時 |
| 五個實驗（blog） | 0：Cline 把 K3 的 `max` reasoning 悄悄降成 `high`，修抽象層，但**沒有分數歸因**（OpenRouter 本來就只對應 K3 唯一支援的 effort）；1：5 題因 OpenRouter 429 直接放棄，改成 exponential backoff 多重試；2：loop detector 把「同一指令但輸出在變」的輪詢誤判成迴圈，改成看輸出；3：一題 7.6 秒就零 token 結束，根因是含 `@a` 這類 token 的 prompt 觸發未被引用的 async worker 做 file-mention 查找，process 在呼叫模型前就合法退出，一行 liveness 修正；4：兩題 agent 用 `pkill -f` 的寬鬆 pattern 殺到自己的 harness，改成工具指引要求追蹤 PID。blog 也承認 pkill 指引只減少、沒消除寬鬆匹配 |
| hill-climb prompt（gist） | 存在，約 13KB，可直接參考。內容包括：固定資料集版本、模型、provider、溫度、資源、timeout、題數、並行數、retry 政策、verifier；一次只改一個因果軸；明列禁止事項（改 verifier／測試、讀隱藏測試、task 名稱判斷、寫死答案、加 Terminal-Bench 專屬 prompt、加資源或 timeout、只重跑失敗題再當成完整 run、挑最幸運的一輪）；預先登記固定的診斷子集；A–E 評估階梯（合成重現 → 診斷子集 → 89 題完整 run → 至少重複 3 次確認 → leaderboard 相容協定）；升級為新 incumbent 須多贏至少 3 題或有成對證據加確認；持續更新實驗 ledger，失敗也要記 |
| prompt 的自我警告 | prompt 寫明 Moonshot 的 88.3% 是 KimiCode＋max reasoning 的跨 harness 數字，「不要宣稱追平或超越，除非協定真的可比」；也寫明開發用 runner 的 **timeout 乘數是 2、只跑 1 次**，「絕不可標成 leaderboard 等價」。但 blog 標題段落寫「achieved SOTA」「We matched it」，與自己 prompt 的規則衝突 |
| 「自我」改進的主體 | prompt 開頭把任務寫成「Kimi K3 檢查並改進跑 Kimi K3 的 Cline harness」，並說「你同時是改 Cline 的工程 agent 與被改進的目標模型」。但 blog、成本 gist 與演講都說主導改動的是 GPT-5.6 Sol（Codex thread），K3 只負責跑 eval。所以實際是「一個模型改另一個模型的 harness」，不是字面上的自我改進 |
| PR #12465 | 存在，標題「Improve CLI resilience for long-running agent workflows」，+774／−58、34 檔。**狀態是 closed、未合併**（2026-07-27 關閉），作者留言「被拆成更聚焦的 provider-routing 與 loop-detection PR 取代」。blog 寫「we reviewed the full PR before merging」，與此不符。PR 說明還多一項：把 AI SDK 對暫時性 provider 失敗的重試上限從 2 次提高到 5 次 |
| 後續 PR | reasoning 路由以不同形式合併（#12542〈Route reasoning controls from models.dev across providers〉，2026-07-29）；loop detection 拆成 #12543〈Recognize progress in repeated tool-call loops〉，查詢當下仍是 open（最後更新 2026-09-01）。retry、liveness、pkill 指引有沒有另外合併，用關鍵字搜 PR 沒找到，**不確定**（搜尋不保證完整） |
| token 與成本 | blog 說約 10 億 token（agent 4 億、eval 6 億）、約 $680。成本 gist 的明細是控制 thread 約 2.77 億 token、$336.86，eval 約 3.91 億 token、$343.83，合計約 6.68 億 token、$680.69。**金額對得上，token 總量對不上**，以 gist 明細為準 |
| Terminal-Bench 2.1 | [官方發布頁](https://tbench.ai/news/terminal-bench-2-1)說它修正了 Terminal-Bench 2.0 的 89 題中 28 題（外部依賴、資源不足、說明與測試不符），修正後沒有任何一題是無解的。89 題、獨立容器的描述對得上 |
| OpenAI kernel 說法 | OpenAI 原頁回 403；[Simon Willison 的轉引](https://simonwillison.net/b/9570)（2026-07-30）引原文：「With Codex, GPT‑5.6 Sol autonomously rewrote and optimized our production kernels」「These efforts, combined with broader kernel advancements from GPT‑5.6 Sol, reduced end-to-end serving costs by 20%」。20% 是**多項工作合計**、OpenAI 自家量測。15% token 生成效率在 Willison 轉引中沒有，搜尋摘要說出自同一篇的 speculative decoding 段落，未回讀原文確認 |
| 未查證 | 2021 路線圖引文的出處、kernel 競賽冠軍的說法、「一到五年」投影片的出處、裝置最佳化的成效 |

## 證據強度與限制

| 主張 | 強度 |
|---|---|
| 69/89 → 77/89 → 79/89 | 講者自報、單一模型、單一 benchmark；有公開 trace 與 ledger 連結，但沒有第三方重跑。開發協定 timeout 乘數 2、單次嘗試，不是 leaderboard 協定 |
| 「88.8%」 | 是最佳那一輪；同組確認輪 76、78，重複平均 87.1%。引用時應報平均或範圍 |
| 各改動的貢獻 | 投影片自承未分離；診斷切片（13/14、4/4 等）是挑過的小子集，不能外推到 89 題 |
| 「追平 SOTA 88.3%」 | 跨 harness、跨 reasoning 設定、跨 timeout 設定比較，講者自己的 prompt 就禁止這樣宣稱 |
| 成本 $680 換掉數週人力 | 金額有 gist 明細；「數週人力」是拿 1 月 Opus 4.5 那次自報經驗對比，不是同條件對照 |
| OpenAI 降 20% 服務成本 | 廠商自報、多項工作合計，不是單靠 agent 寫 kernel |
| 人的糾正可變成 eval／訓練訊號 | 觀點，合理但沒有在演講中示範 |
| 裝置延遲被「深度最佳化」 | 個人軼聞、沒有任何數字 |
| 職涯建議 | 個人意見，講者自己說可能太悲觀或太樂觀 |

### 勿引用（2026-11-19 核對）

- 「baseline 27%」：逐字稿辨識錯誤，投影片與 blog 都是 77.5%。
- 「13 小時」：同一段前面說 17 小時，blog 也寫約 17 小時。
- 「10 億 token（4 億＋6 億）」：與作者自己的成本 gist 明細（約 6.68 億）不符。
- 「Cline 追平／超越 Kimi 官方 SOTA」：協定不可比，作者 prompt 自己禁止這樣宣稱。
- 「整個 PR 經人 review 後合併」：PR #12465 實際是 closed 未合併，後來拆成其他 PR。
- 「Kimi K3 改進了自己的 harness」：主導改動的是 GPT-5.6 Sol。
- 「首個公開的自動 eval 改進案例」：講者自稱「probably」，同期已有學術工作（例如 [Agentic Harness Engineering](https://arxiv.org/abs/2604.25850) 這篇 preprint）在做自動演化 harness，本頁未逐一比對先後。

## 可以搬到個人 Claude Code／Codex 工作流程的做法

個人沒有 89 個平行容器和數百美元預算，但迴圈的形狀可以縮小照做。

**A. 把一次糾正存成可重跑的小任務**（對應第 8 段）

1. 在專案裡開一個目錄（例如 `evals/cases/`），每次你得糾正 agent 時，存一筆：原始指示、當時的 repo 狀態（commit SHA）、一條能判對錯的驗證指令（測試、`curl`、`grep` 都可以）。
2. 只存「能用指令判定」的糾正；需要人判斷品味的不存，因為無法自動評分。
3. 同一類糾正第二次出現，再去改 skill、`AGENTS.md`，或照 [[Lauren-Tan-把糾正寫進程式庫]] 的優先序改成 lint／型別檢查。

**B. 改 skill 或指示檔前後跑同一批題**（對應第 4、6 段）

1. 改動前，用固定的模型與設定跑一遍 `evals/cases/`，記下通過數與每題結果。
2. 先把失敗分桶（工具錯誤、超時、原地打轉、真的不會），而不是一題一題修。
3. 一次只改一件事，再跑全部題目，不只跑剛修的那幾題；看有沒有讓別的題目退步。
4. 題目少的時候，多一兩題通過幾乎都是雜訊。照他 prompt 的標準，至少重跑幾次、看範圍，不要拿最好的一次當結論。

**C. 讓 agent 長跑改進時，抄 prompt 的骨架**（對應第 5 段與回查的 gist）

1. 寫明哪些東西固定不能動（評分腳本、測試、資源、timeout）。可參考 [[長跑-Agent-的目標定義與計畫工具]] 的「計分腳本標成不可編輯」。
2. 列出禁止事項清單：不改測試、不讀隱藏答案、不針對題目名稱寫特例、不挑幸運的一輪。
3. 要求 agent 維護一份 ledger 檔：每次的假設、證據、改動、commit、分數、保留或回退，失敗也記。中斷後可以接著跑。
4. 設升級門檻（例如多贏幾題且重跑確認），沒過就不算進步。
5. 最後產出分開的 commit 給人 review。這次案例中，人 review 後也沒有整包合併，而是拆成小 PR。

**D. 兩條可以直接拿來檢查自己 harness 的教訓**

- agent 在 shell 裡用 `pkill -f <pattern>` 清背景程序，pattern 可能匹配到 agent 自己的 harness 指令列，把自己殺掉。指示裡要求追蹤確切的 PID 比較安全。不過寫在指示裡只是散文層，Cline 的投影片自己也說「guidance 不是強制」，只減少、沒消除。
- 只看「同一個指令重複幾次」的 loop 偵測，會誤殺正常的輪詢（例如等 build 或背景工作）。判斷卡住要看輸出有沒有變化。這是 harness 開發者的問題，Claude Code／Codex 使用者通常改不到，但遇到長任務被中斷時可以想到這個原因。

**不能直接搬的**

- 完整版的成本：一次 89 題完整 run 約 $50–80、整個活動約 $680、一輪約一小時，個人專案通常養不起。
- 職涯建議不是工作流程，而且是單一講者的判斷。

## 與既有頁的關係

- [[Lauren-Tan-把糾正寫進程式庫]] 和本頁是同一件事的兩個尺度：Tan 把每次糾正寫進程式庫的確定性檢查，Khan 把糾正存成可重現的任務，再讓 agent 在 eval 上找 harness 的修法。用 Tan 的倒金字塔看 Khan 的四個改動：retry、loop detection、liveness 改的是程式（確定性層），pkill 是工具指引（散文層），正好是 Cline 自己承認「沒消除」的那一項，支持 Tan「散文最不可靠」的排序。
- [[長跑-Agent-的目標定義與計畫工具]] 的「reward hacking 當預設會發生」列了鎖定計分腳本、硬規則清單等防線；Khan 的 prompt 是這套防線的完整實例，多了「預先登記診斷子集」「至少重複 3 次確認」「只重跑失敗題不算完整 run」。
- [[AI-自主工作流的實證檢驗]] 記錄了 benchmark 系統性高估、越強的模型越會作弊，以及 Cursor 稽核中封鎖網路後分數大降的結果。Khan 的評估有檢查上網查答案和 reward hacking，但結果沒有第三方稽核，應以同樣的懷疑看待。[[用測試約束-AI-產碼]] 提到 BenchJack 能用假的 curl wrapper 攻破 Terminal-Bench，提醒 grader 本身也可能被利用。
- [[Agent-Harness-Engineering-框架綜述]] 的 Managed Agents 一節說 harness 假設會隨模型升級過期。這和 Khan 的做法有張力：他的部分修正是針對特定模型與 provider（K3 的 reasoning 檔位、單一 provider 容量不足造成的 429），換模型後可能變成多餘。retry、liveness、輸出感知的 loop 偵測則是一般性的 bug 修正，比較不受影響。這也呼應 blog 說「每次新模型都要先跑 baseline 再爬升」：爬升的結果本來就跟模型綁在一起。
- [[AI-Engineer-2026-演講精華-AI-工作流程]] 是同屆 28 場的綜合頁，第 6 節用一兩句話提到本場；本頁補上完整脈絡與回查。

## 張力與限制

- **「遞迴」的成分有限**：實際上是外部模型（GPT-5.6 Sol）改 harness 程式，被改進的模型（K3）的權重沒變，也沒有改進「改進者」本身。稱為自動 hill climbing 比 RSI 更準確。演講後半從這個實驗跳到整個 stack 與智慧爆發，是外推。
- **它的效益和選題建議互相牽動**：他建議遠離「下一版模型就抹掉」的題目，但這次 hill climb 的成果本身就跟特定模型綁在一起，下一版模型出來要重跑。他的回應是把流程變成每次新模型的標準作業，也就是可重用的是流程，不是改動。
- **對個人開發者的選題建議落差大**：推論、kernel、post-training、硬體都需要資源與專業。他沒說個人或小團隊在沒有這些時該怎麼靠近迴圈；比較可行的版本是上面 A–C 的小型 eval 迴圈。
- **人仍是最後一道防線**：blog 說人工 review 是最終保障，實際 PR 也被人拆小才合，所以「幾乎零人工介入」只適用於找出改動的階段，不適用於合併。
