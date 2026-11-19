---
title: Galletta 與 Felisola Caso 可信任財務分析 harness 五原則
description: Monzo 兩位資料人用婚禮付款規劃示範財務分析 harness 的五原則：共識、一致、證據、問責、驗證，附 repo 核對與可搬做法
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/talks/ATMcd9tkhhc-stop-chatting-spreadsheets
published: 2026-11-09
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - evaluation
  - skill
  - testing
---

# Galletta 與 Felisola Caso 可信任財務分析 harness 五原則

原料：[[AI-Engineer-Galletta-Felisola-Caso-Stop-Chatting-With-Spreadsheets]]，包含官方閱讀頁與官方機器逐字稿。影片 `ATMcd9tkhhc` 在 2026-11-09 上傳，是一場約 1 小時 50 分鐘的 workshop。工作坊 repo 是 [francescogalletta/aienyc-harness-workshop](https://github.com/francescogalletta/aienyc-harness-workshop)，2026-11-19 核對過 README、`workshop/BUILD_YOUR_OWN.md`、`SPEC.md`，以及 gate、number check、reviewer 的原始碼與 prompt。

**一句話**：用 agent 做財務分析，瓶頸已經不在速度，而在你敢不敢照結果動用自己的錢。要讓人信任，不能只是把 trace、unit test、eval 這些元件堆上去，而要照五條原則設計 harness：先對齊領域語意，再把算術固定成有測試的程式碼，讓每個數字都能追回來源，只在真正需要人判斷的地方設閘門，最後加入能改變計畫的外部檢查。關鍵規則要寫進後端程式強制執行，不能只寫在 skill 裡的文字指示。

## 講者與立場

- **Francesco Galletta**：官方講者頁寫他在 Monzo 帶 financial crime 的 analytics engineering，並共同主導資料部門的 AI 策略。他是 BI analyst 出身，委內瑞拉人，在英國住了約七年後搬到馬德里。
- **Felippe Felisola Caso**：官方講者頁寫他是 Monzo 的 Lead Analytics Engineer，待過 Nubank 和 Loft。他負責內部 AI 生產力工具，也參與開發員工從 Slack 呼叫的內部 agent「Agent Chip」。
- **立場**：兩人明說這場是以個人身分講，**不代表 Monzo**。工作坊 repo 是 Galletta 的個人 repo，採 MIT 授權，沒有推銷任何產品。唯一的「廣告」是預告隔天另一場 Monzo 分享〈A Bank Built Its Own Coding Agent. It Took Off〉（官方講者頁有這場，影片 `adfw3xJBx1o`）。Monzo 的 AI 導入「效果很好」是**自報**，沒有給任何數字。
- **形式**：這是 workshop，聽眾一邊跟著跑 repo 的 UI，一邊聽講。講者自己說 UI「不是好設計」「有些地方過度工程」，強調重點是讓人**感受**一個為信任而設計的 harness，不是拿出一個產品。

## 演講脈絡（依時間順序）

### 1. 問題設定：瓶頸是信任，不是速度（0:00–11:57）

- 財務分析交給背景 agent 跑很快，但如果主人事後還要把整段工作重建一遍才敢動手，速度就沒有省下什麼。他們用「trust」當主軸，判斷一個 AI 專案的標準是能不能帶來具體的業務效益：「我們不想 token maxing。」
- trace、unit test、planning、eval、loop、graph 這些都只是**元件**，不是設計原則。這場要談的是原則，不談特定技術。
- 五原則會一層疊一層：**Shared domain**（你和模型講的是同一件事）→ **Consistency**（數字來自正確的地方）→ **Evidence**（拿得出收據）→ **Accountability**（就算跑一百個 agent，後果仍由你承擔）→ **Verification**（從另一個角度檢查）。
- 他們說這不是唯一正解，只是在幾個用例上對他們有效。

### 2. 範例：婚禮能不能準時付款（11:57–20:38）

- Galletta 自己正在籌備婚禮，他和未婚妻算帳時就對不上：她手上的是晚餐單價，他算的是晚餐之外還有兩項跟人數連動的費用。用晚餐單價乘以賓客數，只會正確算出帳單的一部分。這說明一個看起來合理的數字，可能在回答錯的問題。
- repo 分成四個部分：起步指南、婚禮範例、harness 本體，以及存放自己作品的 `my/` 資料夾。參加者可以開空白工作區問自己的財務問題，也可以載入預先跑好的婚禮計畫。
- Felisola Caso 的比喻：這有點像「拿一張桌子教你怎麼做桌子」。他們認為現在難的不是 build，而是知道要用什麼方式處理問題；不懂原則就叫 Claude「幫我做一間百萬美元公司」，只是把結果交給運氣。

### 3. Shared domain：先面談，再出計畫（20:38–30:43）

- Galletta 在空白工作區用語音口述：要付三筆款，第一筆 6,000，第二筆金額未知，第三筆付清餘額；DJ 是固定成本，晚餐按座位計價，出席人數不確定。他真正要問的不是總額，而是**每個截止日前要付多少、到時候手上有多少現金**。
- 接著他刻意講得很亂：沒有存款、媽媽**可能**給 5,000、每人**大約** 150、花 500、還要買西裝。**限定詞和數字一樣重要**：如果把「可能」的禮金當成現金，算術一個都沒錯，付款也會看起來付得起。
- harness 的 interview 指示規定它要問到什麼程度才能提出計畫，避免一開始就進入「yes man 模式」。模型認得一個詞，不代表它知道你在這個詞裡包含了哪些東西；除非你很有錢、有專門為你訓練的模型，否則你的定義不會和大多數人一樣。
- 他們說，打造 harness 時大部分時間都花在這段來回對齊上。harness 設計得好，會帶著你得出好計畫；設計成「我說什麼你都說好」，結果就會不穩定。

### 4. 接受計畫：每個決策都有自己的位置（30:43–36:41）

- 範例計畫是大約十分鐘討論後的結果。問題被拆成一個個決策點，畫成圖。這是 interview 指示裡規定的**產出形狀**，所以使用者最後拿到的是一個個可以重新打開的決策，而不是一大段對話。
- 點開某一步，可以看到每項資訊的來源：使用者講的、agent 提議的、還沒決定的。例子是 agent 根據 Galletta 用的某個詞推斷了他的意思，而這個推斷被標了出來。
- **長對話問題**：講者請聽眾舉手，問誰在超過十輪的對話裡想過「乾脆從頭來」，很多人都舉了手。他們認為這是現行 harness 的設計後果：所有東西都塞在一條線性對話裡。把討論掛在節點上，就能單獨重談一個問題，計畫的其他部分仍然留在畫面上。

### 5. Consistency：同樣的計算要能重跑（36:41–45:23）

- Galletta 遇過聊天回覆把公式排版得很漂亮，結果卻錯到他心算就看得出來，而排版讓他差點信了。
- **聽眾質疑**：如果程式碼也是模型寫的，到底改善了什麼？回答是：把實作**存下來**之後，方法就能脫離對話、被檢查和測試。預測可以用可信 repo 的現成函式庫；自訂計算可以拆成小函式，再做 unit test 和 end to end 測試。每個問題都讓 agent 重寫一次程式碼，第一百次執行時可能已經換了實作，名稱卻沒變。
- **月結預算的經驗**：Galletta 每月結算預算時，讓 agent 自己決定怎麼分類帳目、怎麼加總、怎麼處理退款。前三次都對，第四次錯了，對帳花掉的時間和錢比自己做還多。後來他改用腳本：「寫一次，每次需要就跑。」模型仍可以選工具，但 harness 要嚴格規定它不能靠 token 做算術。
- Felisola Caso 補充，這也是他們選擇**自建 harness**、不只把原則寫成 skill 掛在 Codex 或 Claude Code 上的原因：只寫指示，最後還是在拜託 agent「make no mistakes」。在 Monzo 他們做的是讓非確定性和需要控制的確定性行為混合使用。
- **聽眾追問**：「這個 harness 是 vibe-coded 的吧，production 版呢？」講者沒有正面回答，改為預告隔天的 Monzo 場次，只說抽象層、方法這些實作細節會不同，但「確定性與非確定性混合」的原則一樣。
- 另一個反駁是「模型越來越會自己呼叫工具，等一等就好」。他們的回應是：模型會在執行當下臨時寫新的程式，第一百次可能又發明一個不需要重新發明的版本。

### 6. 建出計算節點、跑測試、試著弄壞它（45:23–56:04）

- 接受計畫後，UI 會問「要不要幫你建程式碼」。他們也提到別處實作的一個做法：**記錄程式碼版本**。函式名稱沒變但版本變了，就要提示使用者，因為舊公式算出的結果不能說明新公式會怎麼算。
- 練習：點第一步，打開 Code 和 Tests，再按 Run tests now。測試在本機執行，沒有模型思考的等待時間。Galletta 說：不要靠你自己記得跑測試，也不要讓 agent 臨時把東西黏起來，元件之間應該本來就接得起來。
- **build-your-own 指南**：他們稱之為「instructions for instructions」，像 IKEA 說明書。指南只規定每個元件的目的，例如「蒐集足夠資訊才能提出計畫」，怎麼實作由你決定。Galletta 說因為 IP 考量，有些部分不便多講。
- **聽眾問：這和 spec-driven development 有何不同**？Felisola Caso 的回答有兩點：
  1. coding agent 的程式碼是達成目的的手段，最後產出一個產品；分析型 harness 則是陪人解決一個會一直變動的問題。婚禮的 spec 會不斷改，每次都把整份 spec 交給 agent 重新解讀，等於又回到依賴非確定性。harness 把 spec 拆成**有立場的分段工作流程**，每個決策和計算各有自己的流程。
  2. 資料工作的經驗是，metric 和 dimension 的定義一直在變，「這個數字對嗎？」這種對話永遠存在。前提、來源資料和脈絡都會變，harness 要預期這些變動，不能每次都重新下 prompt。
  - 他們也承認，`my/` 資料夾裡存的東西本質上就是 spec，原則和 SDD 相同，差別只在呈現方式是分段工作流程，不是一份文件。
- **改輸入和改定義是兩回事**：新的賓客估計可以直接丟進現有計算；改變一個指標「算什麼」則可能需要新程式碼。練習是把乘法改成加總，存檔會成功，但分析會被 harness 擋下，得不到結論。

### 7. Evidence：追回數字，也追回產生它的方法（56:04–1:06:41）

- 例子：賓客數是 Galletta 給的，但未婚妻剛多邀了三個人沒告訴他。程式完全正確，用的卻是過時的人數。Evidence 讓你從總額倒推到輸入，再追問是誰提供的、當時知道什麼。
- **三種資訊看起來一樣確定，harness 要把它們分開**：
  - **Interpretation（詮釋）**：把聊天裡沒有結構的一句話變成預算項目，需要詮釋說話者的意思。
  - **Assumption（假設）**：agent 推斷或從記憶拿出的值，要一直標成「這是 agent 提供的」。
  - **Recorded fact（紀錄事實）**：銀行對帳單上的交易金額是事實，地位和「未來支出的估計」不同。
  - 他把這比作資料標註，認為建立 curated data set 的紀律在這裡同樣適用。
- **master file 事件**：每家公司都有一個大家共用、存在共享硬碟的 master file。有人照常填入熟悉的數字，看起來一切正常，但檔案已經被改過，連帶改了「合理數值範圍」的假設，而那個人沒有理由知道。輸入一樣，結果全錯。所以追溯不能只追輸入，**還要追轉換輸入的流程和它的變更**。harness 建出來的確定性程式碼也一樣。
- 業界其他財務分析實作可以追溯到資料集層級，例如是哪個 connector 或供應商回報了某支股票在某個時間點的價格。
- **簡報事件**：Galletta 做過一個幫他做簡報的 harness，會蒐集文件、挑重點。修改時他舉了一個例子說明要怎麼改，模型卻把這個例子當成內容，寫進整份簡報。高層問那個數字和假設從哪來，他答不出來。一個「怎麼修改」的指示，變成了一個關於業務的主張。現場聽眾也說，他和 agent 的每次對話幾乎都在問「這個數字哪來的」。

### 8. Accountability：把人的決定放在錢真正取決於它的地方（1:06:41–1:20:34）

- 「Agents face no real-world consequences. You do.」講者說這句話他很喜歡，但不知道出自誰。他說他領薪水有一部分是因為要對結果負責，不是因為坐在電腦前打字。
- **兩個極端都不行**：一邊是全黑箱，結果是「隨機機器說沒問題」；另一邊是每次改動都按 Enter 核准，或每個 PR 逐行看。現場問「誰想回到沒有 auto mode、每個改動都按 Enter 的時代」，有人說自己還在這樣做。講者追問：一百次核准裡，有幾次真的攔到東西？
- 一位聽眾的做法：先 review 任務，讓 agent 去做，再 review 結果。講者說這正是刻意的設計：**review 任務，而不是 review 每一個改動**。
- **主要原則：少量、高訊號的閘門**。例子是只在功能測試通過時才看 PR，在那之前可以粗略一點。程式碼的部分不需要問人，因為測試結果本身就是收據。財務上的對應做法是：數值有幾種可能時，讓系統跑三個情境，再並排交給人選。他們也拿 Claude Code 能調整人參與程度的功能來類比，說財務 harness 也可以這樣引導使用者。
- 範例計畫只有一個人工檢查點：看過所有情境後，決定每月存多少。**沒有任何錢被轉出**。另一個值得打開的假設是：預期有一筆 20,000 的入帳，和第三筆付款同一天。同一天不代表付款到期時錢已經在帳上。（repo README 的範例資料是：家人在 2027-05-29 給 20,000，婚禮在 2027-06-12，第三筆付款在婚禮前 14 天到期，算起來正好也是 2027-05-29。）
- **分支再併回的決策樹**：做完決定之後，你仍然可能想到新的事情需要修正。他說自己用手機口述時，中間講了一句不相干的話，整段分析就毀了，因為「沒辦法只拿掉那一句、其他保持原樣」。所以 harness 不只要有核准閘門，也要有安全修正方向的機制。
- 練習：對賓客數 chip 說「不會少於 150 人」，這是一個下限，會改變哪些出席情境合理，也會透過每席成本改變各情境的花費。歷史紀錄會區分「使用者放行的假設」和「使用者修正過的假設」。
- **側問題**：講者問 Claude Code 的 `/btw` 好不好用。一位聽眾說「有時有用、有時沒用」，又說側問題最後還是會變成 session 的一部分（回查結果見下）。Galletta 說他常為了一個笨問題另開一個新聊天，因為怕污染主分析，而在聊天裡寫「這是笨問題，別拿去做別的」根本沒用。harness 的分支對話就是讓題外話有自己的位置，結論要不要併回主計畫，是另一個獨立的選擇。

### 9. Verification：給 reviewer 外部參照，並讓它能改計畫（1:20:34–1:33:23）

- **反面情境**：有人把錯推給 reviewer，說「但 Francesco review 過了」。他們聊到 vibe coding 讓「確保正確」的負擔落到 reviewer 身上，很打擊士氣。Verification 是多加回饋迴路來消除盲點，但**不轉移問責**。
- **財務團隊的專家其實不會檢查每一格**：他們看幾個能估出總額量級的格子，感覺不對就說「行銷怎麼可能花這麼多」。這個落差告訴分析者該去哪裡查，責任仍在分析者身上。另一個例子是那則廣為流傳的推文：「馬斯克的錢可以給全世界每人一百萬美元，還有剩。」讀起來好像說得通，再想一下就知道不對。以約 80 億人估算，需要約 8,000 兆美元（這是本頁自己的估算，演講沒有給數字）。
- **Golden examples 的極限**：golden example 反映的是作者挑的案例，會有選擇偏誤。Galletta 當 BI analyst 時，query 看起來沒問題，數字也合理，自己怎麼查都沒發現錯；把 dashboard 給另一個團隊的利害關係人看，對方立刻說不對。他不必懂 SQL，只是大概知道公司那年賣了多少。容忍度也由使用者決定：誤差 5% 看起來合理，卻可能大到改變團隊的決策。
- **Thin slicing**：逐字稿寫成「thing slicing」，推斷是心理學的 thin-slicing。專家用片段經驗快速判斷事情對不對勁，而模型擁有的是「所有人經驗的平均」，它覺得「大概沒問題」的範圍可能和你的完全不同。他說這正好是 shared domain 的反方向：shared domain 是把你的語言翻譯進模型的訓練分布，verification 則是由你的經驗回頭檢查模型。
- **設計**：由另一個 agent 審查計畫和假設，提出帶 tag 的 challenge。使用者在分支裡處理，可以「Use this」，讓它併回主幹並改變計畫，也可以「Dismiss」。決策也可以附一則帶外部參照的 note。重點是 **review 要有路徑回到分析裡**。他們說，如果只是做成 LLM-as-judge，每一步都由另一個 agent 給意見，Galletta 最後拿到的儲蓄計畫可能還是跟一開始一模一樣。

### 10. Q&A：什麼時候值得自建 harness（1:33:23–1:43:55）

- **要建幾個 harness？** Felisola Caso 說沒有明確答案，光譜兩端是「全部用 Claude Code／Codex 加 skill 解決」和「每件小事都從頭建」。判斷依據有三個：同樣的失敗是否反覆出現、有多少使用者會碰到、錯了代價多大。偶爾做、低風險的事，多引導 agent 幾輪就好；50 個 credit analyst 用同一套工具支撐公司關鍵決策（這是假設情境），就有強烈理由控制變異。
- **反例**：如果目的是大量產出社群影片，evidence、verification、accountability 都沒那麼重要。這五原則是針對財務的高風險場景。
- **不要一直磨斧頭**：先試 skill 或 command，觀察使用者還得手動做什麼。如果一再需要開新 session、從另一個聊天複製文字、重新解釋背景，「重複了三到五次的那串動作」就是該做成軟體的候選。他婚禮的兩個結果：用 web search 找馬德里的前五名攝影師比較，效果很好，什麼都不用建；但用語音規劃財務時，一趟約一小時的車程裡同一段對話重來了三次，這就是 harness 值得做的地方。他也自嘲用最貴的 Claude 方案，還「把 Anthropic 用到赤字」。
- **聽眾問怎麼和主管溝通**（只要一提到 AI，大家就期待 100%、甚至「200%」正確）？Felisola Caso 的回答是從可量測的結果出發：驗證一個新 dashboard 要來回幾次，就去數次數；使用者因為數字看起來不對而開內部 ticket，就去追蹤這些 ticket。這些是**提議的評估方式**，不是已經公布的成果。重點是對齊 AI 要推動的結果，而不是爭論 AI 本身的可信度。

### 11. Q&A：skill 可以呼叫 Python，但誰保證它真的會呼叫（1:43:55–結尾）

- **聽眾**：我已經有一個 skill 會問問題，再用 Python 腳本算數，為什麼還要 UI 和資料庫？
- **Felisola Caso**：腳本能做可重複的算術，但要不要呼叫、怎麼理解周邊指示，還是模型在決定。他把 prompt-based 的做法形容成「請照做、不要出錯、拜託拜託」。agent 可能 99% 的時候會照指示做（這是他的口頭估計，不是量測），問題在剩下的 1% 和邊界情況。skill 發給其他使用者後，對方 user 層的 `CLAUDE.md` 可能和你的指示衝突。Monzo 內部有一個 agent extension 的共享貢獻機制，review 時常看到大家為每種不支援的情況加一段文字，連「使用者這樣做時要回什麼」都寫進去。每多一條，模型就多一條要詮釋的指示。後端程式碼可以直接決定哪些操作可用，並強制條件成立。**把規則搬進 harness 的理由，是使用者需要它在每一次執行都成立。**
- **Galletta 的收尾**：會計其實充滿創意和詮釋。例如現金流看起來怪怪的，可能是有人把營收晚了一個月入帳；看出這種可能，和「日期確定後把帳加總」是兩種不同的工作。財務問題是「必須 100% 可靠執行的部分」和「字裡行間大量詮釋」的混合。模型會變強，但信任仍然要靠掙來；講到錢時，1% 的錯誤可能就是很多錢。閱讀頁特別註明，這個 1% 是在說明小錯的代價，**不是** harness 的實測失敗率。
- **最後一題：UI 上哪裡看得到信任？** 答案是沒有單一位置。對總額有疑問的人，可以追輸入的來源、看執行過的程式碼和測試；擔心能不能準時付款的人，可以打開那筆 20,000 入帳的 challenge。不同使用者在意的驗證點不同，介面的價值在於讓「即將做決定的人」能追下去他自己的那個疑問。

## 回查結果（2026-11-19）

| 項目 | 結果 | 依據 |
|---|---|---|
| 工作坊 repo 存在、內容對得上演講 | **成立**。repo 為 MIT 授權，2026-10-09 建立，最後 push 在 2026-10-21，查詢當下約 4 顆星。README 依五原則逐步帶練習，`workshop/BUILD_YOUR_OWN.md` 就是演講說的「IKEA 說明書」，`examples/wedding/` 有 6 個計算模組，每個都有 `spec.json`、`module.py`、`tests.py`、`golden.json` | [repo](https://github.com/francescogalletta/aienyc-harness-workshop)、[BUILD_YOUR_OWN.md](https://github.com/francescogalletta/aienyc-harness-workshop/blob/main/workshop/BUILD_YOUR_OWN.md) |
| 「改掉乘法，存檔會成功，但分析會被擋」 | **成立，但機制和演講說法略有差異**。README 的練習是把 `wedding_total_cost/module.py` 第 9 行的 `*` 改成 `+`（原始碼第 9 行確實是 `total = Decimal(guest_count) * dinner_cost_per_guest`），結果是該步驟變成 `Stale · rebuild`。`gate.py` 會先比對檔案指紋，檔案在測試通過後被改過，就拒絕執行（`FILES_CHANGED`）；指紋相符時還會在**每次執行前**重跑測試（`TESTS_FAIL`）。所以擋下來的第一道關是「檔案變了」，不只是「測試失敗」 | [gate.py](https://github.com/francescogalletta/aienyc-harness-workshop/blob/main/harness/calc/gate.py)、README §4 |
| 「記錄程式碼版本，函式名稱沒變也要標出來」 | **成立**。實作方式是檔案指紋加上步驟在計畫裡的 fingerprint，步驟定義變了，模組就會變成 stale | BUILD_YOUR_OWN §2、`SPEC.md` §1 |
| 三種資訊要分開標記 | **成立**。計畫裡每一項都帶來源標記：`❝` 是本人原話、`✎` 是 assistant 提議、`↗` 是查到的。validator 會拒絕「引號裡的字不在使用者訊息中」的計畫 | README §3、BUILD_YOUR_OWN §1 |
| 每個數字都能追回 | **成立，但有限度**。`provenance.unbacked` 會檢查回覆、傳給程式的值和存檔裡的每個數字，必須能在已知來源找到；第二次還找不到來源的回覆就扣住不發。原始碼註明 0–12 的小整數**不檢查**，並自承「This is not a proof」，只是抓捏造數字的 tripwire | [provenance.py](https://github.com/francescogalletta/aienyc-harness-workshop/blob/main/harness/calc/provenance.py)、`SPEC.md` §1 rule 1 |
| Golden examples 由誰驗 | **要注意**。worked example 寫好後，由第二個模型盲答核對，寫程式的模型看不到 example。但 README 明說「核對的是第二個模型，不是人」，人要逐筆或一次全部核准。**兩個模型犯同樣的錯，就會一起通過**，README 建議自己拿計算機驗算 | README §4 |
| Reviewer 怎麼運作 | **成立，且比演講講得更嚴**。reviewer 讀計畫、spec、假設、決策和最近的執行結果，但**不讀程式碼、不回答使用者**。每輪最多保留 3 個 challenge，依「可能翻轉結果」的程度分 high、medium、low。它可以用 `look_up` 查一般性名詞，每輪最多 4 次，查詢字串裡不能有數字，也不能帶任何個人資料。它不能做算術，challenge 裡出現沒有來源的數字就會被丟掉。Use 會記成一個決策，Dismiss 之後的 pass 會被告知、不會重提 | [reviewer.md](https://github.com/francescogalletta/aienyc-harness-workshop/blob/main/harness/review/reviewer.md)、BUILD_YOUR_OWN §5 |
| 「外部參照」的實作 | **有限**。工作坊版的外部參照是一個 researcher，用 web 或 Wikipedia 查財務名詞的標準定義，也可以設定成只查本機的 `reference/terms.json`。演講裡「另一個團隊的人知道一年大概賣多少」這種**領域內的外部估計**，repo 沒有自動化，只能靠使用者在決策上加 note | README §9、`grounding/researcher.md` |
| 20,000 入帳和第三筆付款同一天 | **對得上**。README 範例的家人贈款日和第三筆付款的到期日都是 2027-05-29 | README §5 |
| 模型來源 | 支援三種：Claude Code 登入（用量算進你的方案額度）、Anthropic API key、OpenRouter。只有 `harness/model/` 會 import provider SDK，harness 本體只用標準函式庫 | README §1、`SPEC.md` §1 |
| 講者身分與 Agent Chip | **成立**。官方講者頁有兩人的職稱；Felisola Caso 的頁面寫他參與開發 Agent Chip（從 Slack 呼叫的內部 agent），隔天的 Monzo 場次也列在講者頁上 | [Galletta](https://ai.engineer/speakers/francesco-galletta)、[Felisola Caso](https://ai.engineer/speakers/felippe-felisola-caso) |
| 聽眾說「`/btw` 的側問題最後會變成 session 的一部分」 | **和現行官方文件不符**。文件寫明 `/btw` 的問答「never enter the conversation history」：它可以讀整段對話但沒有工具，一次只回一則，要繼續可以 fork 成背景 subagent。聽眾的經驗可能來自早期版本，也可能是誤解，演講中沒有驗證 | [Claude Code interactive mode：Side questions with /btw](https://code.claude.com/docs/en/interactive-mode) |

## 證據強度與限制

- **全部是個人軼事，沒有對照**：月結預算第四次出錯、master file、簡報範例污染、BI dashboard 被外部利害關係人抓錯、開車時同一段對話重來三次，都是講者單方面的經驗，沒有量化資料。
- **數字都是示意或自報**：「超過十輪對話」是現場舉手調查；「agent 99% 會照指示做」是口頭估計，**勿引用為量測值**；「50 位 credit analyst」是假設情境；1% 和 5% 是在說明錯誤的代價。閱讀頁也特別註明 1% 不是實測失敗率。
- **Monzo 實務沒有公開**：講者說原則和 Monzo 的做法一樣，但 production 實作沒有展示，被問到也改為預告另一場，Galletta 還提到有些內容受 IP 限制不能講。所以「這套原則在銀行內部 production 有效」是**自報**。
- **工作坊 harness 是示範品**：講者自己說 UI 很粗糙、部分過度工程。repo 星數很少，最後 push 在演講前，看不出會持續維護。
- **適用範圍**：講者自己說這是針對財務這種高風險、需要信任的場景；內容大量產出這類用途不適用。

### 勿引用

- 「`/btw` 的側問題會進入 session context」：這是聽眾說的，和現行官方文件不符（見回查表）。
- 「agent 99% 的時候會照指示做」：講者的口頭估計，沒有出處。
- 「Agents face no real-world consequences. You do.」：講者說不知道出自誰，不要掛在任何人名下。

## 可以直接搬進個人 Claude Code／Codex 工作流程的做法

1. **重複出現的算術改成腳本加測試，agent 只負責呼叫**。像月結、分帳、報價這種每次都要算的東西，寫成一支有 unit test 和 golden example 的腳本（golden example 要自己用計算機驗過，不能只讓另一個模型核）。在 `AGENTS.md` 或 skill 裡寫「數字只能來自這支腳本的輸出」。但要知道這仍然是文字指示（見第 6 點）。
2. **把結果和程式版本綁在一起**。腳本輸出時一起印出腳本檔案的 hash，或 git 短 SHA，以及輸入檔路徑。下個月數字對不上時，先比對 hash，就能分出是輸入變了還是方法變了（對應 master file 事件）。
3. **要求每個數字標出來源**。請 agent 輸出表格時加一欄「來源」，分成「你說的」「我推的」「查到的」「紀錄（對帳單）」，對話裡的「可能」「大約」這類限定詞要保留在表格裡。想要更強的保證，可以參考 repo 的 `provenance.py`，寫一個小檢查：回覆中每個數字都要出現在腳本輸出或輸入裡。
4. **只設高訊號閘門**。讓 agent 把不確定的值展開成兩到三個情境並排呈現，你只在「要選哪個情境」和「要不要真的動錢」這兩個地方決定；算術和程式碼交給測試把關，不要逐筆核准。
5. **題外話不要進主對話**。在 Claude Code 裡，用 `/btw` 問只需要讀現有對話就能回答的問題，依官方文件，問答不會寫進歷史；需要工具的題外話，就 fork 成背景 subagent，或另開 session。結論要併回主線時，自己明確地講一句，不要讓它無聲地混進去。
6. **規則一定要成立時，從文字搬到程式**。判準和講者一樣：這個 skill 會不會給別人用、錯了代價多大、同一個錯有沒有一再發生。三項都中時，與其在 skill 裡多加一段「如果使用者這樣做就回答那樣」，不如把條件寫成腳本裡的檢查、讓它直接失敗，或用 hook 在檢查點強制執行。
7. **另派 reviewer，而且給它限制**。用一個 subagent 只讀「計畫、假設、最近的輸出」，不讀程式碼。請它最多提 3 個 challenge，依「會不會翻轉結論」排序，並規定它不准自己算數。每一條由你決定採用或駁回，駁回的要記下來，下一輪就不會重提。
8. **判斷要不要自建工具，先數手動交接的次數**。如果你一再複製上一個聊天的內容、重新解釋背景、開新 session，同一串動作重複三到五次，就是做成工具的訊號；還沒到這個程度，就繼續用 skill 和 command。
9. **想親手體驗**：clone repo 之後跑 `uv run python -m harness check`，接著跑 `HARNESS_EXAMPLE=wedding uv run python -m harness ui`，依 README 一節一節練習。用 Claude Code 登入時，用量算在你的方案額度內，`ANTHROPIC_API_KEY` 要先 unset。

**不適合照搬的部分**：決策圖 UI、主幹加分支的資料庫，以及每次執行前都重跑測試的 gate，對個人日常 coding 來說成本太高。這些是為「財務決策、多人共用、錯了很貴」的情境設計的。寫一般程式碼時，測試和 CI 已經扮演 gate 的角色。

## 與既有頁的關係與張力

- **和 [[Lauren-Tan-把糾正寫進程式庫]] 同一方向，但用在不同的領域**：兩邊都主張關鍵約束不要寫成文字，要寫成程式強制執行。Tan 把約束推進 API、架構和 lint；Monzo 則把它推進 harness 的後端，例如 gate、number check、只有使用者點頭才能改數字。Tan 的倒金字塔把「散文」放在倒數第二層，和 Felisola Caso 說的「拜託不要出錯」是同一個判斷。
- **和 [[Brian-Douglas-把糾正存成團隊-review-資料]] 有張力**：Douglas 認為把糾正寫成 skill，多半就能拿到大部分效益；Monzo 則認為 skill 的文字不可靠，一旦分發出去，還會和使用者層的 `CLAUDE.md` 衝突，關鍵規則要用程式強制。兩者可以並存：Douglas 談的是 review 判斷，本來就需要詮釋；Monzo 談的是一定要成立的計算規則。這個分歧在 [[AI-Engineer-2026-演講精華-AI-工作流程]] 的「分歧」段已經記錄過。
- **補充 [[Claude-Code-放手運行的安全與驗證]]**：Hallie 用 auto mode 加 deny 規則，把核准從逐次按 Enter 換成分類器和硬規則；Monzo 的「少量高訊號閘門」是同一種思路在**決策層**的版本，人只在選情境、動錢、改自己的數字時介入。
- **和 [[Diogo-Almeida-助理不等於自動化]] 互補**：Almeida 主張把可靠的判斷做成程式的原語，放進控制流程；Monzo 的 harness 正是把「面談、建模組、追溯、決策、審查」都做成有結構的流程，而不是在旁邊掛一個聊天框，演講標題「Stop chatting with spreadsheets」也是同一個意思。
- **對照 [[Rajath-Kotyal-規格先驗再交給-agent]]**：Kotyal 在規格交給 agent 之前，用 solver 抓出矛盾和歧義，交給人決定；Monzo 用面談加上來源標記，讓推斷和限定詞浮上檯面。兩邊都在處理「模型無從得知作者本意」，Monzo 靠的是 LLM 和人的對話，沒有形式化的檢查。
- **[[Agent-Harness-Engineering-框架綜述]]** 收錄的 harness 範疇主要是 coding agent。這場示範的是**非 coding 的分析型 harness**，「spec 拆成分段工作流程」「決策要當成第一級物件」是那頁沒有涵蓋的角度。
