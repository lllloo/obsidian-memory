---
title: Prasanna Sankar 雲端 agent 的瓶頸一路移到開工
description: Vorflux 的 Sankar 依序拆解雲端 agent 從環境到 merge 的六個瓶頸，再談人成為專案經理後改由常駐 Autobot 自己開工，附回查
created: 2026-11-19
updated: 2026-11-19
source: https://www.ai.engineer/talks/TlOAhw9t5DA-merge-is-bottleneck
published: 2026-11-10
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - automation
---

# Prasanna Sankar 雲端 agent 的瓶頸一路移到開工

來源：AI Engineer 演講〈Merge Is the Bottleneck〉的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-Sankar-Merge-Is-the-Bottleneck]]（YouTube `TlOAhw9t5DA`，約 20 分鐘，2026-11-10 上傳）。本頁按逐字稿順序整理；閱讀頁是主辦方改寫版，兩者有出入處會標明。回查日 2026-11-19。

**一句話**：要讓 agent 跑幾個小時，人得先離開筆電，所以要依序拆掉「環境、規劃、拆工、測試、review、merge」六個卡點，讓雲端 session 一路做到合併；拆完之後人能平行開 20–30 件事，新瓶頸變成「誰記得開工、誰追進度」，答案是給常駐 agent 一個目標、一個負責人、一個預算和一個頻道，讓它從客戶通話、告警裡自己找事做。

**標題和內容的落差**：題目叫「Merge Is the Bottleneck」，但 merge 只是六個瓶頸的最後一個，講了大約半分鐘。整場真正的論點是「瓶頸會一直移動」，後半場（約 9:00 之後）都在講 merge 之後的新瓶頸：專案管理與開工。閱讀頁開頭的「把開發者時間算到 merge 為止」是主辦方的提煉，逐字稿沒有這句原話。

## 講者與立場

- Prasanna Sankar，Rippling 共同創辦人，Inc42 報導他 2016 年與 Parker Conrad 共同創辦 Rippling、任 CTO 到 2020 年。演講自述：18 歲是印度排名第一的競程選手、TopCoder 第一、Google Code Jam 與 ACM ICPC 兩度世界決賽；在 Microsoft 待一年後覺得大團隊限制了個人槓桿，受 Paul Graham 文章影響，約 2009 年到矽谷創業，三次 YC founder。
- 現在的公司是 [Vorflux](https://vorflux.com/)，產品就是本場講的雲端 coding agent（1.0）與常駐 Autobot（2.0）。**整場是自家產品的發展史與功能介紹**，例子全是 Vorflux 內部或客戶情境，數字沒有一個有外部量測。
- 他的方法論是「profiling」：觀察人（包括他自己）把時間花在哪裡，哪裡卡人就往那裡砸 token。結尾用 Tesla 自駕類比：一次一個 intervention 地找出模型在哪些情境出錯。

## 演講脈絡（依順序）

### 1. 起點：Opus 4.5 讓 agent 能自己跑幾分鐘（0:05–3:32）

- 他把 Opus 4.5 當轉折點（他說「差不多一年前」）：軟體開發從 IDE 自動完成，變成 agent 自己跑幾分鐘，所以可以完全跳過 IDE、搬進終端機。他判斷這幾分鐘只會越來越長。
- 同時，模型開始在程式競賽拿滿分、在純推理上超過他。但贏競賽的 harness 不是原版的 Claude Code 或 Codex，而是**在推論階段花多得多的算力**。他想要的就是這種版本：多花一點 token，換到更多智力、省下人的時間。
- 推論：agent 一旦能跑幾小時，就該放在雲端，不該放在你的機器上。

### 2. 瓶頸一：雲端環境要能重現 localhost（3:32–5:10）

- 他說多數雲端 agent「run blind」：頂多跑起正在改的那一個服務。但人在 localhost 測，是因為有一堆其他相依服務；雲端要像 localhost 一樣完整，人才搬得過去。
- Vorflux 的做法：onboarding 時開一批 subagent，在一台空白 EC2 上把整個開發環境架起來：接好 port、處理機器 secret、處理登入驗證、準備 seed data。**先花 token 把使用者搬上雲**，他認為這是多數雲端 agent 漏掉的一步。

### 3. 瓶頸二：規劃階段的來回（5:10–6:18）

- 他 profiling 自己和使用者的時間，發現大量時間花在規劃。當時的 planning agent 在規劃階段花的 token 不多，一兩分鐘就回來，然後人跟它來回討論好幾輪。
- 「人的時間花在哪，我就把 token 丟到哪」：Vorflux 在規劃階段加大推論算力，平行開多個探索 subagent 一起做設計與架構，產出更詳細的「plan of plans」，再濃縮成摘要給人看。
- 閱讀頁把這畫成「同一份詳細計畫有兩個讀者」：人讀摘要；build subagent 讀完整計畫與相依圖。

### 4. 瓶頸三：拆工與編排（6:18–6:41）

- 人通常會把大任務拆成小任務，再一個個辛苦地合進去。Vorflux 預設由 subagent 來做：計畫附一張**相依圖**，subagent 各自做互不相依的部分，前置條件沒完成的部分就等。

### 5. 瓶頸四：測試不能還要拉回本機（6:41–7:45）

- 如果每個雲端 session 最後都要你把分支拉回 localhost 測，人就離不開筆電。
- Vorflux 在雲端機器上跑瀏覽器測試與端對端測試，產出能「向使用者證明東西會動」的東西。他個人最喜歡看**影片**證明新功能真的會動。
- 另一個是**每個功能一個 staging 連結**：app 本來就跑在那台機器上，他可以自己點、走影片沒走的路徑。閱讀頁的區分很清楚：影片回答「測試實際測了什麼」，staging 連結回答「我換個操作會怎樣」。

### 6. 瓶頸五：code review（7:45–8:00）

- 他說很多人會叫多個模型幫忙 review，Vorflux 把這件事做進 harness，而且可以自訂。**常見配置是 Claude 寫、GPT 審**；也可以讓多個 reviewer subagent 從不同角度看同一個變更。
- 注意：這是他描述「很多人這樣做」與產品可設定，不是他給出任何「交叉審比較有效」的數據。

### 7. 瓶頸六：merge（8:00–8:34）

- 節奏快的團隊、人和 agent 平行開很多 PR 時，審完的 PR 可能在等的時候 base 就動了，需要 rebase。Vorflux 做了一個 merge queue：**持續把待合的 PR rebase 到 master 保持可合併，並自己把 PR 合進去**。
- 六個瓶頸都拆掉之後，才真的能跑「好幾小時的雲端 agent」。這是 Vorflux 1.0，他說約兩個月前推出。

### 8. 新瓶頸：人變成專案經理（9:00–10:50）

- 他的經驗值：桌面上的 coding agent 大概能平行 3–5 件事，長時間跑的雲端 agent 能到 20–30 件。槓桿變大了，但瓶頸從「寫程式」移到「專案管理」：確認東西真的合進去、真的有用，確認腦中想做的事真的有開工。他說自己的「context window」有限，超過 **10 件平行**就非常吃力。
- 他引模型趨勢佐證方向：近幾個月的模型進步來自 orchestration，主 agent 當指揮、重活丟給 subagent，因為新的 context window 能給更多「智力預算」。依同樣設計就能做一個專案經理：開 session、追進度、把東西合進去。這就是 Vorflux 2.0 的 Autobot，他稱為「24/7 的員工」，朝一個目標工作。

### 9. 更前面的瓶頸：開工本身（10:50–12:58）

- 他觀察到很多「增量意圖」其實已經存在：客戶通話結束時列了幾個 to-do，那些就是意圖，不需要人一個個複製貼上去開工。「注意到、記住、開工」這三步可以自動化。
- 「多數團隊把 agent 當 task queue，而 task queue 只能跑得跟餵它的人一樣快。」佇列裡大多數東西不需要你：意圖已經在 codebase、告警或通話逐字稿裡，不需要天才來開工。這類事需要的是一個**負責人**，以及能讓分散的負責人一起把平行 session 合進去的**多人協作**空間。
- 他把方向說成兩個轉變：從 single player 到 multiplayer、從被動（reactive）到主動（proactive）。
- **工作分兩類**：真正從 0 到 1 的創造性工作，客戶自己都說不出要什麼，需要品味與判斷，這部分仍由人做（他說他喜歡做這個）；另一類是 n+1 的增量工作（逐字稿辨識成「end to end plus one」），意圖已經充分存在於公司收到的訊號裡，這類交給 Autobot。

### 10. 失敗模式：叫 agent「修掉所有告警」（12:58–14:17）

他列出大家「燒到手指」的經驗（以 Sentry 為例）：

- PR 洪水：開出的 PR 多到沒人有時間合。
- 一次一個地 ping 你一整天，很吵。
- 常常只是把告警**靜音**，根本原因沒修。
- agent 為一件沒人要它做的事跑好幾小時，token 帳單爆掉。
- 黑箱：你不敢把重要的事交給它。

他的解法是「新人比喻」：對一個還不完全信任的新人，你先給重要且明確的事、預期他早期常回報、做得好就多給、做不好就少給；他在預算內工作、你看得到他在做什麼。「沒有人雇一個人然後說：把所有事都解決。」閱讀頁把它濃縮成：交出常駐任務前，先講清楚**觸發訊號、結果歸誰、追這件事的預算**。

### 11. Autobot 的組成與內建 bot（14:17–15:36）

- 「1.0 把你開的工做完；2.0 替你開工。」一個 Autobot 有一個**目標**、一個**家頻道**，接上你的 **webhook** 自己開始工作。
- 他說大家想像不出這種 bot 該長什麼樣，所以 Vorflux 做了一個**有主見的 bot 目錄**，放公司內部用起來有效的幾個，讓使用者從那裡改。最常用的幾個：
  - **On-call**：分類 Sentry 與 PagerDuty 告警，先調查再找工程師，工程師可以從 bot 已查到的東西開始。
  - **CI**：持續加速 build。變慢給它一個具體問題，修好且測過的改動給團隊一個可 review 的東西。
  - **專案經理**：一個專案放一個頻道，每天回報進度與卡點，有東西要 review 時 tag 對的人。他說他們用得很多。

### 12. 案例：一次 Slack 沒回覆變成客戶追蹤（15:36–16:50）

- 對一個友善客戶推 beta 時，bot 有 bug，在 Slack 沒回應。以前他會截圖再 tag Vorflux 去修。
- 這次通話結束後，看客戶通話的 Autobot 讀逐字稿找到他的 to-do，**用時間戳去對錄下的螢幕分享**，拿到他原本要自己截圖的畫面脈絡。
- 核准鏈：Autobot 先問他要不要修 → 他同意 → bot tag 負責的工程師並帶回 PR → 工程師核准 → 合併、部署 → bot 關掉項目並起草給客戶的「已修好」訊息 → 他核准措辭 → 送出。
- 他說未來例行工作會像「approve、approve、approve」，bot 會學到自己多有把握，像員工一樣越來越好。閱讀頁補了一句比較節制的話：這個例子裡每一次核准都有作用，bot 省下的是人記住下一個交接點的負擔。

### 13. 為什麼是現在、怎麼省錢（16:50–17:39）

- 最新一輪模型訓練聚焦 orchestration：主 agent 規劃與追蹤，重活交給 subagent。他認為多數 frontier 模型都能解好定義清楚的任務，產出難分高下；再上一層是「經理」，也就是開 session、追 session 的 agent。
- 成本：多數團隊直接帶自己的 Claude Code 或 Codex 訂閱；API 用量大的團隊可以把**規格清楚的工作派給開源模型**，frontier 模型留給判斷與溝通。
- 「我們做的是一個在你設的限制內決定下一步做什麼、而且說明理由的 agent。」

### 14. 願景與收尾（17:39–19:54）

- 把「每人槓桿最大化」推到底，就是一間「靠迴圈運作」的公司：客戶通話結束、產品就變好；告警響起、已經有人知道原因；CI 變慢、一個測過的修正已在等 review。人花時間在 0 到 1，和打造下一個迴圈。
- 北極星是「零員工公司」：北極星指方向，不代表會抵達；10 個人撐起很大的生意，四捨五入就是零。他也承認：還很早，Autobot 會出錯，有些責任還不能交出去。
- 結尾是創業論：他認為我們可能正處於超級智慧起飛期，競爭極激烈，贏的是每人槓桿很高、各自擁有很多決定權的小團隊；傳統大公司跟不上。「擁有 0 到 1，在這場搶地盤中盡量拿下地盤。」

## 可以搬到個人 Claude Code／Codex 工作流程的做法

這場的六個瓶頸是「團隊加雲端產品」的版本。個人能搬的是**找瓶頸的方法**和其中幾個具體做法，平台本身不能搬。

1. **先 profiling 自己，不要先加工具**。連續幾天，每次被 agent 拉回來就記一筆：卡在哪一步（來回改計畫、要自己跑起來測、看 diff、rebase、想不起來還有什麼沒開工）。最常出現的那一項才是你的瓶頸。這和 [[Claude-Code-放手運行的安全與驗證]] 收尾建議的「觀察你還在哪一步被拉回迴圈」是同一招。
2. **規劃多花 token、人只讀摘要**。在 plan mode 明確要求：「用多個 Explore subagent 平行調查 A、B、C 三塊，產出完整計畫，每個任務標 depends-on；另外給我 10 行以內的摘要。」Claude Code 官方文件確認 Explore 與 Plan 是唯讀的內建 subagent，可以平行開。完整計畫存成檔案，下一步讓 subagent 照相依圖做。
3. **照相依圖分派**。沒有相依的任務各自開 subagent 或 worktree；有前置條件的等前面合進去再開。不要一開始就全部平行，否則會撞進 [[平行-agent-產出的合併與-review]] 講的衝突與 rebase 問題。
4. **讓 agent 能在自己的環境把整個 app 跑起來**。本機就是寫一支一鍵啟動腳本（相依服務、seed data、測試帳號）；用 Claude Code 雲端 session 或 Codex cloud 時，把同樣的東西寫進環境的 setup script。secret 不要寫進 repo。
5. **完成要附證據**。要求 agent 用 Playwright 之類跑過主要流程，附截圖或錄影；有 preview 部署就附連結讓你自己點。只有「測試通過」四個字不算。
6. **換一家模型做 review**。用 Claude 寫、Codex 審（或反過來），各給一個角度（正確性、安全、跟需求對不對得上）。但演講沒有證明交叉審比同模型審更好，當成多一道便宜的檢查，不是品質保證。
7. **merge queue 個人多半不需要**。同時開的 PR 只有幾個時，一次合一個、其餘 rebase 後重跑測試就夠。團隊真的需要時，GitHub merge queue 的做法和 Vorflux 描述的不同：它不 rebase 你的分支，而是把 base 加上排在前面的 PR 組成暫時分支跑 CI，失敗就踢出佇列（見回查）。
8. **常駐或排程 agent 先寫三件事再開**：觸發訊號是什麼、結果歸誰（誰要看、誰核准）、預算與停止條件（每天多少、連續失敗幾次停）。範圍從窄開始：例如告警 bot 先只「調查並回報」，不開 PR；表現穩了才放寬。這就是演講的新人比喻。

**不能直接搬的**：

- 20–30 個平行 session 加專案經理 bot：需要 Vorflux 這類平台；個人能盯的量遠低於此（見下方張力）。
- 從客戶通話逐字稿加螢幕錄影自動抓 to-do：需要會議錄影、逐字稿管線和 Slack 整合，個人開發者通常沒有這個訊號來源。
- 規格清楚的工作派給開源模型：要自己架或接 API，對用訂閱的個人來說省不到錢。

## 回查結果（2026-11-19）

| 主張 | 結果 | 來源 |
|---|---|---|
| Rippling 共同創辦人；Vorflux 募資約 1,500 萬美元 | **成立**：Inc42 報導 2026-07-16 種子輪 1,500 萬美元，投資方含 Y Combinator、Peak XV 等；Sankar 2016 年共同創辦 Rippling、任 CTO 到 2020 年。該報導寫 YC 領投，其他報導寫 Peak XV 領投，領投方說法不一 | [Inc42](https://inc42.com/buzz/former-rippling-cofounder-prasanna-sankar-raises-15-mn-for-vorflux-after-0xppl-shutdown/) |
| Vorflux 在最新一期 YC | **成立**：YC 公司頁標示 Fall 2026 批次，創辦人列 Prasanna S | [YC 公司頁](https://www.ycombinator.com/companies/vorflux) |
| 競程戰績（印度第一、TopCoder 第一、Code Jam 與 ICPC 世界決賽） | **部分佐證**：只找到二手資料稱他曾是 TopCoder 印度排名第一；Code Jam 與 ICPC 世界決賽未找到一手紀錄，**未核實** | 搜尋結果（Latka 個人頁、SingleStore 部落格），非一手 |
| Opus 4.5 是約一年前的轉折 | **時間對得上**：Anthropic 公告日 2025-11-24。「從此 agent 能自己跑幾分鐘」是他的主觀感受 | [Anthropic 公告](https://www.anthropic.com/news/claude-opus-4-5) |
| Autobot 有目標、預算、Slack 家頻道，有現成 bot 目錄；可每個角色選模型、帶 Claude／Codex 方案 | **成立**（產品頁）：官網寫「A goal and tools」「A budget（每日花費、每個任務指定模型）」「A home in Slack」，自建 Autobot 要設角色、Slack 頻道、觸發條件與**每週**預算；目錄有 on-call（Bolt）、CI（Sage）、PR 安全審查等；Harness 設定可分 Plan／Build／Review 各用一家模型並帶 Claude 或 Codex 方案 | [vorflux.com](https://vorflux.com/) |
| Vorflux 的 merge queue 持續 rebase 並自動合併 | **未核實**：官網首頁只看得到 PR review 與「merge risk 評分」，沒有 merge queue；文件頁是前端動態載入，抓不到內容 | [vorflux.com](https://vorflux.com/) |
| （對照）GitHub merge queue 的機制 | 官方文件：不需要作者更新分支；每個排隊的 PR 和最新 base 及排在前面的 PR 組成 `merge_group` 暫時分支跑 CI，失敗就移出佇列並重建後面的暫時分支 | [GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) |
| （對照）Claude Code 能平行開唯讀探索 subagent、subagent 可指定不同模型 | **成立**：Explore、Plan 為內建唯讀 subagent，plan mode 會委派給 Plan；文件示範平行用多個 subagent 調查不同模組；subagent 可設 `model` 欄位；預設有同時執行數上限 | [Claude Code subagents 文件](https://code.claude.com/docs/en/sub-agents) |

## 證據強度與限制

| 主張 | 強度 |
|---|---|
| 桌面 3–5 件平行、雲端 20–30 件、超過 10 件就難以追蹤 | 講者個人經驗值，**自報**，沒有量測方法 |
| 規劃階段是人時間的主要去處 | 他自己 profiling 自己與使用者的結果，**自報**，沒給比例或樣本 |
| 「修掉所有告警」會造成 PR 洪水、只靜音不修根因、token 爆掉 | 他說是「大家燒到手的經驗」，**軼聞**，沒有具體案例或數字 |
| 客戶通話 → 修復 → 部署 → 回覆客戶 | **單一案例**，自家產品、自家客戶 |
| 多數 frontier 模型在定義清楚的任務上產出難分高下 | 講者**意見**，沒有引用評測 |
| 最新模型訓練聚焦 orchestration | 講者**意見**，沒有引用模型廠商的說法 |
| 規格清楚的工作派給開源模型能省很多錢 | 方向合理，但**沒給任何成本或品質數字** |

整體限制：

- **廠商立場**：題目講瓶頸，內容是 Vorflux 1.0 到 2.0 的產品路線，每個瓶頸的解法都是自家功能。
- **沒有任何結果指標**：題目是 merge，卻沒給 merge 時間、PR 量、revert 率、Autobot 開的 PR 被接受的比例。對照同屆 [[Walden-Yan-軟體工廠與給-agent-長期-job]] 至少給了 PR 數與工程師數（同樣自報）。
- **merge queue 只講「持續 rebase」**：沒提 rebase 後要重跑測試、沒提語意衝突。文字上能合不代表行為沒壞。

### 勿引用

- 「把開發者時間算到 merge 為止」當作 Sankar 的原話：這是官方閱讀頁的提煉，逐字稿裡沒有這句。可以引用為「閱讀頁對本場的摘要」。
- 「Sankar 主張用 Claude 寫、GPT 審」：原話是「很多人常常」這樣做，Vorflux 讓它可設定；他沒有說這是他推薦的配置，也沒有效果數據。
- Code Jam 與 ICPC 世界決賽：本輪未找到一手紀錄，引用前要再查。

## 與既有頁的關係與張力

- **和 Walden Yan 幾乎同一條路線**：[[Walden-Yan-軟體工廠與給-agent-長期-job]] 也是雲端 VM 跑完整環境、用影片當證據、從「給任務」轉到「給長期 job」，而且演講後也推出常駐 bot 產品。差別是環境怎麼來：Yan 用 Docker Compose 加 mock、每小時重建 VM snapshot；Sankar 在 onboarding 時用 subagent 把真實環境搬上一台 EC2。工作怎麼來也不同：Yan 的 job 是「把一個量測指標往上推」，Sankar 的 Autobot 是「從通話、告警這些訊號抓出已存在的意圖」。兩者都是廠商自報，可以互相佐證方向，不能互相佐證數字。
- **和 Lauren Tan 的順序相反**：[[Lauren-Tan-把糾正寫進程式庫]] 主張先穩內圈（程式庫、lint、驗證）再自動化外圈，否則只是更快產出更多 slop。Sankar 幾乎只講外圈。他自己列的失敗模式「只把告警靜音、沒修根因」正是 Tan 那套要擋的東西；照 Tan 的順序，Autobot 應該排在 repo 有足夠確定性檢查之後。
- **平行上限和既有經驗值一致**：[[多-agent-的人類監督與介入]] 記錄 Kilo Code 訪談的 foreground 2–4 個、Morph 部落格「超過約 8 個就改由 lead agent 協調、人只管 lead」。Sankar 的「超過 10 件就變專案管理，所以讓主 agent 當經理」是同一個轉折點的另一個經驗值，也是同樣的解法。該頁也提醒核准閘門會退化成橡皮圖章，正好對應 Sankar 樂觀描述的「approve、approve、approve」。
- **merge 這一段比較淺**：[[Patrick-Debois-多人多-agent-同時合進同一-main]] 把同一個問題講得深很多：每合一個 PR 其他都要 rebase 重測、要用 speculative merge train、要比對意圖。[[平行-agent-產出的合併與-review]] 也記錄了文字無衝突不代表語意正確。Sankar 只說「持續 rebase、自己合」，沒碰這些。
- **subagent 給更多智力預算的說法有條件**：[[Context-優先與多-agent-的適用邊界]] 整理的證據是多 agent 在可平行的「知識問題」上有效，在需要一致決策的「編排問題」上容易出錯。Sankar 的「新 context window 等於更多智力預算」只講了好處；他把 build 交給 subagent 的前提是相依圖切得乾淨。
- **「瓶頸移到 review／merge」本身有爭議**：[[AI-產碼加速下的-review-瓶頸]] 記錄大家共用的「瓶頸已移到 review」前提，認知調查與行為觀測對不上。Sankar 的 profiling 是另一個未量測的認知來源。
- **反方提醒**：[[Diogo-Almeida-助理不等於自動化]] 主張現在的 LLM 是為「人在旁邊修正」最佳化的，無人值守要每次都做對。Sankar 的 Autobot 用核准鏈和新人比喻來處理這點，但核准鏈越長，越接近「助理」而不是「自動化」。
