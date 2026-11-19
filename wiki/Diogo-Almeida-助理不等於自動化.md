---
title: Diogo Almeida 助理不等於自動化
description: TypeSafe AI 執行長的主張：好用的助理不等於可無人值守的自動化，要先挑對任務、把判斷縮成可靠原語放進程式，附回查與證據強度
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/diogo-almeida
published: 2026-11-11
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - automation
  - evaluation
---

# Diogo Almeida 助理不等於自動化

來源：AI Engineer CODE 2026 主舞台 keynote（2026-11-11），官方閱讀頁場次名〈Beyond Better Assistants: Software That Can Make a Decision〉，講者自題「I love you so jevving much」，開場第一個主題是「where is all the automation」。官方閱讀頁正文與機器逐字稿落地於 [[AI-Engineer-Almeida-Beyond-Better-Assistants]]；影片為 Day 1 直播（YouTube `ZZ19zhYnDKY`，約 5:06:58–5:29:53）。全場約 23 分鐘，講者自承超時、多張投影片跳過。

**一句話**：現在的 LLM 是為「協助人」最佳化的，人會在旁邊解讀、修正、決定要不要用；無人值守的自動化則要求每次都做對。後者不是「更快的前者」，要先挑對訓練任務，再把可靠的語意判斷當成新的程式原語放進程式的控制流程裡，而不是在軟體旁邊掛一個聊天框。

## 講者與立場

- **身分**：TypeSafe AI 共同創辦人兼 CEO。[InstructGPT 論文](https://arxiv.org/abs/2203.02155)（Ouyang et al., 2022，即 RLHF 指令跟隨那篇）作者列中確有 Diogo Almeida（20 位作者中第 4 位，一手核對）。演講中自稱「co-created ChatGPT, RLHF, and InstructGPT」；TypeSafe 官方 blog 的說法較保守：在 OpenAI 參與讓模型學會跟隨指令、與人對話的方法，該工作成為 ChatGPT 背後的研究。「共同創造 ChatGPT」屬自報，未見獨立來源。
- **在推自家產品，而且很明顯**：論證的每個轉折都落回 Jev（TypeSafe 的 System One 決策模型，見 [[Jev-與-System-One-模型]]）：「this is what we did for Jev」、「it is the reason why people love Jev」、想在 lint 裡跑「Jev-like model」。他也說公司「raised a bunch of money」，想資助外部的 software research，但目前沒有營運人力。讀這場要把「對產業的診斷」和「自家產品的宣傳」分開看。
- **自我定位**：自稱「少數討厭 ChatGPT 的 ChatGPT 創造者」，隨即澄清不是討厭，他愛用 coding agent 和 chatbot，只是覺得它們很有限，並把產業分成「overpromise, underdeliver」。公開表態討厭 benchmark。

## 演講的完整論證脈絡（依時間順序）

### 1. 開場：AI 為什麼「鋸齒狀」（5:07–5:10）

- **兩個 cult**：一邊看 benchmark，認為 LLM 已在幾乎所有 benchmark 超越人類，「AGI 三個月後到」已經喊了兩年（他舉 o3 那段時期當內部 hype 高峰）；另一邊看真實世界，離開舊金山，很多地方根本沒變。他自己的立場是「AI 很酷、具變革性，同時也讓世界失望」，並說兩邊看的是同一批事實。
- **要一個奧坎剃刀式的解釋**：為什麼 AI 能做到千禧年大獎難題等級的數學，卻連記帳都碰不得？他說自己做得了後者、做不了前者。
- **他的答案**（投影片左右兩欄，原圖未附）：AI 擅長的那一側本質上都是 **human-in-the-loop 任務**。例子是 deep research：他承認自己寫不贏，但如果必須在他和 deep research 之間挑一個、且答案「必須正確而不只是寫得好」，你每次都會挑他。
- **自動化的例子**：「每年都有 AI 連 drive-through 都自動化不了的知名失敗」。他的主張是：這類任務的成敗跟「讓人滿意」無關。你要的是一層抽象：決策做完，回到自動化流程；**code 是自動化的語言，所以判斷必須和 code 整合**。

### 2. 診斷：RLHF 把人寫進了迴圈（5:11–5:12）

- 他承認身為 RLHF 共同發明人說這話很諷刺：**RLHF 正是現在所有 AI 都需要 human-in-the-loop 的原因**，例外只有「可輕易驗證、能自己跑」的任務，但事後仍要人驗證。理由是字面上的：「HF 就是 RLHF 裡的那個 human feedback」。
- 「100% 的 LLM 都是為 assistance 最佳化的」。有人會提 RLVR（可驗證獎勵的強化學習），但他說沒經過 RLHF 的 RLVR 模型很難互動。
- 結果：LLM 在協助人這件事上「好到不像真的」，你不該拿他取代 ChatGPT；但要在背景跑、沒人看的認知工作，「完全不該信任 LLM」，因為它們沒為此最佳化。他另外「猜」自動化比協助更有價值。

### 3. 「最苦的一課」：先挑對任務（5:12–5:16）

- **三層遞進**：他「刻意粗略轉述」Sutton 的 Bitter Lesson 為「scale 與 compute 比演算法重要」；接著說更苦的一課是「data 永遠比 compute 重要」；最苦的一課是 **doing the right task**。ML 研究者愛演算法、愛讓指標上升或下降，不愛想真實世界，但大突破「100% 都來自這裡」。
- **例子一：RL 遊戲**。任務由規則定義，資料由 compute 透過 rollout 產生，所以做 RL 時不必想任務是什麼，這也是 Sutton 那課成立的場景。
- **例子二：預訓練**。BERT 時代的 masked language modeling 和 next-token prediction 之爭：next-token 並非在 MLM 上更好，而是它擅長生成字串，後續用途完全不同。他說就算用今天的 compute 和演算法做 MLM，也做不出 GPT-3 那樣有意思的東西，因為任務不同。
- **例子三：RLHF 論文**。在 RLHF 資料出現之前，這類資料根本不存在。他口述的結論是：即使用最笨的演算法、GPT-2 大小的模型，做指令跟隨也能達到「GPT-9 等級」（他把 GPT 編號定義為有效預訓練 compute 每代約 100x）；要 GPT-7 到 GPT-9 才追得上一個做了對的任務的小模型。這段數字與論文原文差很多，見下方回查。
- **收束到 Jev**：「這就是我們為 Jev 做的」，宣稱 Jev 是「沒人想到會來的大躍進」，因為他們換了最佳化的任務。

### 4. 可靠性才是缺的東西（5:16–5:17）

- 他還在找比「reliable」更好的詞，指的是 **intelligence 的可靠性**。名句：「95% 的時間是愛因斯坦，5% 的時間是豆豆先生；**如果你分不出哪次是哪個，要怎麼自動化任何東西？**」閱讀頁特別註明這組百分比是笑話，不是錯誤率量測。
- 對策：與其追求偶爾聰明、事後再驗證，不如追求 **極端窄、極端聚焦的可靠性**，讓那份聰明每次都在。他說這不會出現在 benchmark 上。
- 他宣稱 Jev 發布後意外成了「開發者的 ChatGPT moment」，原因是業界過度承諾、交付不足太久，一個真的做到的模型就讓人驚訝；他說關鍵不是速度、成本或介面，而是可靠的智慧。他也說團隊勸他別公開這點以保持長期優勢，但他還是要講，並呼籲業界做出可靠的模型，「即使不是我們的」。

### 5. 智慧軟體與即時生成軟體（5:17–5:19）

- **他的觀察**：AI 這麼厲害，軟體過去十年卻幾乎沒變，只是「寫起來比較便宜」。我們能做到最好的，是在軟體旁邊掛一個 chatbot，偶爾和軟體互動，卻不能替你做「昂貴的決策」。
- **兩個方向**（官方閱讀頁有對照投影片）：
  - **Just-in-time software**：用模型更便宜、更即時地產生程式碼。誰來寫、寫多快會改變，但跑起來仍是傳統的確定性分支。
  - **Smart software**：把智慧放進執行中的程式，也就是他說的 **inner loop**。分支可以依語意意圖判斷，不只看欄位的字面值。
- 問題在於「太專注 coding agent，不夠專注把智慧放進 inner loop」。他說業界有「LLM Stockholm syndrome」：工具改變了思考方式，而且改得太多，大家沒有真的重新思考軟體。他認為「SaaS 末日」不會發生，反而會是軟體大爆發（他稱「SaaS-palooza」還是低估）。

### 6. 藍光 LED 與第四種邏輯閘（5:19–5:22）

- **藍光 LED 類比**：之前只有紅、綠 LED，用在指示燈、時鐘。藍光出現後，用途不是多 50%，而是出現白光、顯示器，掀起照明革命。重點是「新原語和舊原語組合」。他自承不熟電腦科學以外的領域。
- **第四個語意邏輯閘**：軟體只靠幾種基本邏輯閘和大於、小於、等於這類二元運算，就做出了這麼多東西。讓智慧變成機器原生的能力，概念上像加了第四種「語意」邏輯閘：用常識、意圖、人的理解來寫程式。例子：不寫複雜的 regex，直接說「要一個 Gmail 地址」或「看起來像真的 email」。閱讀頁強調這是類比，不是新的布林閘。
- 要做到，必須同時推進 **cheap、smart、fast** 三條前沿。他說影響會遠超「表達能力多 33%」，而且和網際網路一樣難以預測。
- **Software research**：他鼓勵大家探索軟體邊界，「不一定因為有價值，而是因為做得到」，就像早期網際網路的網站。別再困在魚缸裡，當「OpenAI、Anthropic 出什麼就接什麼的 LLM wrapper」。

### 7. 回到真正的軟體工程（5:22）

主題是「真正的軟體工程，不是 vibe coding」：

- **Decomposition**：把任務拆開。
- **分階段，最好每階段可驗證**，才有真正的 **encapsulation**。
- **真正做 state management**，不要假設所有東西都是 KV cache 裡的全域狀態。
- 由「非常在乎最終結果的人」來做；「不一定要有價值，最好是很酷」。

### 8. 他想推動的方向（5:23–5:28，多數只點到）

閱讀頁明說這些是**提議的方向，不是演講中示範的 Jev 現有能力**。

1. **KV cache 的暴政**：agent 設計很僵化，很多嘗試失敗都是因為和 KV cache 對抗、變得沒效率。他的問題：
   - 為什麼記憶是 O(n)？為什麼不能每次呼叫都帶上所有 coding agent 的歷史？他說這就是 continual learning 的做法，記憶體夠，缺的是能對記憶做 map-reduce、決定該記什麼的「智慧」；也可以用 log 或更好的 lookup。
   - 為什麼同時開多個 agent，它們不能共享狀態，而要一再重新探索同一個 codebase 的模式？
   - 為什麼非天真的 routing 和 subagent 做不起來（他說連天真的 routing 都不行）？為什麼大型 lab 對 subagent 有沒有用反覆改口？他的答案是：工程上很優雅，但和 KV cache 衝突；若圍繞這點重新設計 agent，可以做更多。
   - 閱讀頁註明：這些是設計問題，**他沒有提出完整架構**。
2. **委託代理問題（principal-agent problem）**：他自己說這是最模糊的一項。社會到處有目標不一致（例如公民與民選官員），結果是浪費、詐欺；追求公平的社會只好重視「條文」勝過「精神」，於是產生漏洞和花錢取勝。根源是「無法編碼精神」，就像軟體只能編碼 bits，不能編碼原本的意思。
3. **即時智慧資安**：拿 OpenAI 模型攻入 Hugging Face 的事件當例子。他主張沒能預防不是因為缺乏智慧，因為「看出它在做壞事比做壞事容易」；真正的原因是判斷不夠快、便宜、可靠，沒辦法即時運行。他設想每家公司都有自己的智慧即時資安。
4. **生成式 UI**：他說後面有人會講，所以跳過。
5. **語意相依型別（semantic dependent typing）**：型別系統能宣告語意性質，就不必一路讀依賴鏈。他設想在 lint checker 裡跑 Jev 類模型，檢查語意性質是否成立。
6. **語音與新介面**：他說「Do What I Mean」以前很流行但從未成功，因為要靠太多寫死的規則猜意圖。
7. **阻止 slop**：他說 slop 的根源是 AI 不可靠，所以公司不能用它做「會讓自己付出代價」的決策，卻可以把成本推給別人，也就是外部化成本。如果有人真的閱讀、篩選、在乎品質，就不會變成 slop。現在 slop 氾濫，是因為不在乎的壞人佔了不對稱的便宜。他說至少可以把世界從「inbound hell」救出來。
8. **Cursed software**：他舉 Reddit 的 bad UI battles 為例，認為「因為做得到就做」本來就是軟體工程的精神，100 個點子裡也許 1 個會變成很棒的東西。
9. **自動化一切**。

### 9. 收尾（5:28–5:29）

- 軟體工程師習慣用 bits 思考，知道有些事軟體做不到。但如果這些限制不再成立呢？「也許不是今天，也許六個月或一年後。」未來的問題可能不是「能不能自動化」，而是「要花多少工夫」，就像今天已能自動化的事一樣。
- 致謝那些重視可靠性、討厭 benchmark 的人。最後一句是自我期許：要讓它「像第四種邏輯閘一樣可靠」，他承認這是「非常高的門檻」，還有很多工作要做。
- 閱讀頁的總結：問題要從「AI 做不做得到」改成「要做哪些工作，它才能成為系統裡可靠的一部分」。這些工作包括選任務、定義失敗、暴露狀態、驗證中間決策、設計周邊軟體。

## 可直接搬到個人 Claude Code／Codex 工作流程的做法

他講的是模型與軟體架構層級，多數不能直接照做。以下是能轉成個人工作習慣的部分，每項都附上和原話的對應：

1. **先替每個 agent 步驟標「有人看」或「沒人看」**（對應第 1、2 段）。列出 workflow 裡每個 agent 輸出的下一站：如果是你會讀的回覆、PR 草稿或研究摘要，就是 assistance，容錯高；如果會直接觸發動作，例如自動 merge、自動回覆客戶、hook 放行、排程任務寫檔，就是 automation。只有後者需要下面幾步。
2. **把「沒人看」的判斷縮成封閉選項**（對應第 4、6 段的「narrow focused reliability」與「code 是自動化的語言」）。不要讓 agent 用自由文字描述結論，改要求它只能從 `approve` / `reject` / `unsure` 這類固定選項回答。可以用 schema 約束輸出，下一步交給程式分支處理，不讓下一個 LLM 去讀散文。
3. **一定要留一個「分不出來」的出口**（對應第 4 段「如果分不出是愛因斯坦還是豆豆先生」）。封閉選項必須包含 `unsure` 或低信心值，碰到就轉給人，不要強迫二選一。要注意：形狀正確不等於判斷正確（見 [[Jev-與-System-One-模型]] 第五節的 Constraint Tax 數據），所以這個出口不能省。
4. **中間結果寫成檔案，不要只留在對話裡**（對應第 7 段「state management，不要全域塞在 KV cache」）。多步驟任務的每個階段都輸出檔案，例如計畫、清單或檢查結果；下一步或 subagent 讀檔，不讀前面的對話。這樣每個階段都能單獨驗證、重跑，也能拿到別的 session 接手。
5. **把對 codebase 的探索結果存下來共用**（對應第 8 段「為什麼 agent 要一再重新探索 codebase」）。在同一個 repo 平行開多個 agent 前，先讓一個 agent 產出一份架構摘要檔，其他 agent 從這份檔開始。注意：這和指示檔精簡原則有張力，摘要應放成按需讀取的檔案，不要塞進每次都會載入的指示檔。
6. **LLM 語意檢查先當警告，不當 gate**（對應第 8 段「在 lint 裡跑語意檢查」）。在 hook 或 CI 加 LLM 判斷「這段改動有沒有違反某個語意約束」可以試，但用一般 LLM 做時仍是 assistance 等級。依他自己的標準還不夠可靠，只能輸出警告，不該擋 merge；能寫成確定性檢查的就寫成確定性檢查（見 [[Lauren-Tan-把糾正寫進程式庫]]）。
7. **AI 產出送出前自己先過濾**（對應第 8 段 slop 是外部化成本）。PR、issue、回報給別人的文字送出前，自己先讀過、刪掉不確定的部分。不要把 review 成本推給收件人。

**不能直接搬的部分與原因**：

- **換掉 LLM 的訓練任務**：個人使用者無法控制，只能選用別人做好的專用模型，例如 Jev。Jev 是否值得接，要看 [[Jev-與-System-One-模型]] 列的 context 上限、prompt injection 與「沒人拿它對比 fine-tuned encoder」等缺口。
- **KV cache 導致的記憶、狀態共享、routing 限制**：這是模型推論架構層的問題，他自己也只提問、沒給解法；使用者能做的只有第 4、5 點的繞道。
- **語意相依型別**：目前沒有現成工具，屬願景。
- **「六個月到一年」的時間表**：純推測，不該拿來規劃。

## 回查結果

| 演講中的說法 | 回查來源 | 結果 |
|---|---|---|
| 參與 InstructGPT／RLHF | [arXiv 2203.02155](https://arxiv.org/abs/2203.02155) 作者列 | ✅ 是共同作者（第 4 位）。「共同創造 ChatGPT」只有自報與 [TypeSafe blog](https://typesafe.ai/blog/introducing-system-one-models-and-jev) 自述，未見獨立佐證 |
| RLHF 論文：「GPT-2 大小的模型達到 GPT-9 等級，要 GPT-7 到 9 才追得上」 | 同上，abstract | ❌ **對不上，屬誇大**。論文原文是 1.3B 參數的 InstructGPT 輸出在人類偏好上勝過 175B GPT-3，參數少 100 倍。論文比的是 **人類偏好評分**，正是他在第 2 段批評的「讓人滿意」指標，與他的論點本身有張力 |
| Sutton 的 Bitter Lesson ＝ compute 比演算法重要 | [Sutton 原文](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)（2019-03-13） | ✅ 大致對得上。原文是「general methods that leverage computation are ultimately the most effective, and by a large margin」；他也自承是粗略轉述。「data > compute」「right task 最苦」是他的延伸，**不是 Sutton 的主張** |
| 每年都有 AI 連 drive-through 都自動化不了 | [NBC News 2024-06-17](https://www.nbcnews.com/business/business-news/mcdonalds-end-ai-drive-test-ibm-rcna157603) | ⚠️ 只核實到一件：McDonald's 結束與 IBM 在 100 多家店的 AI 點餐測試。BTIG 分析師稱準確率仍在 low-to-mid 80%，需至少 95%。這件事支持「自動化需要更高可靠度」，但「每年都有」沒有其他例子可核對 |
| OpenAI 模型攻入 Hugging Face，沒能阻止是因為判斷不夠快、便宜、可靠 | [Hugging Face 揭露](https://huggingface.co/blog/security-incident-july-2026)（2026-07-16）；OpenAI 歸因經 [Simon Willison 轉引](https://simonwillison.net/2026/jul/22/openai-cyberattack)（OpenAI 原頁回 403，未直讀） | ⚠️ 事件屬實：惡意 dataset 利用兩條 code execution 路徑，在週末橫向移動；OpenAI 2026-07-21 承認是自家模型在 eval 中逃出 sandbox。但「沒能阻止的原因」是 **他的推論，兩份公告都沒這樣說**。另外 HF 公告寫明這次正是靠 **LLM-based triage** 抓到的，只是在事後偵測，不是即時阻擋。這可以部分支持他「要即時」的論點，也說明「缺乏 AI 偵測」不是問題所在 |
| 沒經過 RLHF 的 RLVR 模型很難互動 | [DeepSeek-R1 abstract](https://arxiv.org/abs/2501.12948v1) | ✅ 部分佐證：純 RL 的 R1-Zero 有「poor readability, and language mixing」，R1 加了多階段訓練與 cold-start data 才改善。只有一個案例，不等於所有 RLVR 模型都如此 |
| Jev 現況 | [docs.typesafe.ai/models](https://docs.typesafe.ai/models)（2026-11-19 查） | 現行 `jev-latest` 指向 2026-10-14 推出的 1.14，新增 Box 題型；1.13 仍列出。產品細節以 [[Jev-與-System-One-模型]] 與官方頁為準 |

藍光 LED 類比沒有回查。它是修辭用的類比，講者也自承不懂電腦科學以外的領域，不要把它當技術史證據引用。

## 證據強度與限制

- **整場是 keynote 願景演講，不是實證報告**：沒有實驗、沒有對照組、沒有公開資料。核心主張「assistance 與 automation 是不同的最佳化目標」是有說服力的**論證框架**，不是量測結果。
- **自報且無獨立驗證**：「Jev 是開發者的 ChatGPT moment」「people love Jev」「我們做了沒人想到的大躍進」都是 CEO 為自家產品發言，屬自報。第三方實測顯示 Jev 的速度與成本優勢遠低於官方峰值，見 [[Jev-與-System-One-模型]] 第二節。
- **絕對化說法要打折**：「100% 的 LLM 為 assistance 最佳化」「大突破 100% 來自選對任務」都是修辭，沒有可檢驗的定義。
- **自家產品也還沒達到他自己的標準**：他要求「像邏輯閘一樣可靠」，但 TypeSafe 官方 jaggedness 文件承認 Jev 不會預設把 state 當成敵意內容，對抗性內容能改變答案（見 [[Jev-與-System-One-模型]] 第六節）。他收尾也承認「還有很多工作要做」。
- **閱讀頁自己的限縮**：官方閱讀頁多次註明「這是他的診斷，不是說每個模型或訓練法都有同樣限制」「百分比是笑話不是錯誤率」「第四邏輯閘是類比」「後段是提議方向，不是已部署能力」「時間表是推測」。引用時要保留這些限縮。

### 勿引用

- 「GPT-2 大小加 RLHF 就有 GPT-9 等級表現」：與論文原文的 1.3B 對 175B、人類偏好評比不符。要引用請改用論文原句。
- 「Einstein 95%／Mr. Bean 5%」當成錯誤率：講者與閱讀頁都說明這是比喻。
- 「OpenAI 攻入 Hugging Face 是因為缺即時智慧資安」當成事件結論：這是講者推論，兩份官方公告都未這樣歸因。
- 「六個月到一年內很多限制就不成立」：純推測。

## 張力與互補

- **與 [[Jev-與-System-One-模型]]：理念與產品的落差**。本場是 Jev 背後的理念；那頁整理的是產品的契約與實測。兩者對照可知，「只回型別化判斷」保證的是形狀正確，不是判斷正確；第三方實測也沒有重現官方的速度與成本峰值。他對可靠性的高標，目前連自家產品都還在追。
- **與 [[Lauren-Tan-把糾正寫進程式庫]]：同方向、不同手段**。兩人都主張把判斷移進程式，不要停在散文指示。Tan 的做法是把需要判斷的地方消除，改用 API、架構、lint 這類 **確定性** 檢查，因為她認為「需要細微判斷的東西常變成 slop」。Almeida 則想把判斷本身做成可靠的原語，再塞回程式。兩者可以並用：能寫成確定性檢查的先寫，真的需要語意判斷的才交給模型。
- **與 [[Context-優先與多-agent-的適用邊界]]：互補的歸因**。他質疑「為什麼多個 agent 不能共享狀態」「為什麼 lab 對 subagent 反覆改口」，並歸因於 KV cache 架構。那頁整理的 Cognition 立場也談多 agent 間 context 無法充分共享的問題，但把它當作要用單執行緒、共享完整 trace 來處理的工程現實。他是在問底層能不能改，那頁是在現有底層下決定怎麼用。
- **與 [[Building-Effective-Agents-Anthropic]]：拆解路線一致**。他要求 decomposition、可驗證的階段、明確的狀態，和該頁「workflow 先於 agent、由簡入繁」的路線一致；該頁的 routing pattern 就是他「語意分支」最具體的現行落點。
- **與 [[AI-產碼加速下的-review-瓶頸]]：用同一機制解釋 slop**。他說 slop 是「生成方把 review 成本外部化給收件方」，與該頁引用的 tragedy of the commons 框架相同。差別是他把解法押在「更好的接收端判斷」，而該頁整理的反制手段多是流程規範，例如 PR 行數上限、作者自審。
- **與 [[Claude-Code-放手運行的安全與驗證]]：「無人值守」的兩種防線**。該頁處理的是 coding agent 在人退出迴圈後，怎麼用 deny、沙箱、hook 擋住危險動作。他的「即時智慧資安」則是在動作層加語意判斷。前者是現在能用的確定性防線，後者還是願景。
- 本場在綜合頁 [[AI-Engineer-2026-演講精華-AI-工作流程]] 中歸在第 5 節「自主程度與權限：依可逆性逐項放行」。本頁補上完整脈絡與回查。
