---
title: Stephen Chin 與 Cassandra Chin PR 描述要附證據包
description: Chin 主張 PR 描述該從預先算好的證據圖寫成、驗證段由執行紀錄產生；強 writer 配便宜 reviewer，附自家 benchmark 數字回查落差
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-stephen-cassandra
published: 2026-11-12
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - knowledge-graph
  - evaluation
---

# Stephen Chin 與 Cassandra Chin PR 描述要附證據包

來源：AI Engineer CODE 2026 線上場〈Your PR Says the Tests Passed. Prove It.〉的官方閱讀頁與整場機器逐字稿（約 23 分鐘），落地於 [[AI-Engineer-Chin-PR-Says-Tests-Passed-Prove-It]]。另於 2026-11-19 回查 [Tracetoon repo](https://github.com/Tracetoon/tracetoon)、[Relate repo](https://github.com/relatedb/relate)、[prbench repo](https://github.com/Tingsters/prbench)、[Showtail repo](https://github.com/Tingsters/Showtail)，以及 Tracetoon 官網的兩份 benchmark 報告（[5 PR 版](https://tracetoon.ai/evidence-graph.html)、[61 PR 版](https://tracetoon.ai/evidence-graph-61.html)）。

**一句話**：AI 寫的 PR 被退，常常不是程式碼爛，而是描述講錯了（說測試過了但其實沒在最終版本上跑過）。與其讓 agent 一輪又一輪重讀 session log 重建歷史，不如先用確定性程式把「哪個請求→哪段改動→哪次測試跑在哪個版本上」的關係算成一張小圖，交給一個強 writer 照著寫，再讓便宜 reviewer 對照同一包證據檢查。

## 講者與立場

- **Stephen Chin**：Neo4j 開發者關係 VP（官方閱讀頁頭銜），演講中自稱「graph guy」。GitHub `steveonjava` 是 Tracetoon repo 的貢獻者之一。
- **Cassandra Chin**：獨立作者、講者、兒童工作坊講師；Tracetoon 的作者。GitHub `Tingsters` 自介含「college student」，prbench 與 Showtail 都在她的帳號下。
- **立場**：整場是在推自家兩個開源專案：Tracetoon（PR 描述工具）與 Relate（嵌入式圖資料庫，演講說當週發表）。所有效果數字都來自作者自建的 benchmark，沒有第三方重現。Relate 在 README 裡沒寫所屬公司；它相容 Neo4j 的 Bolt 協定、可與 Neo4j/Aura 同步，但是否為 Neo4j 官方專案**不確定**。

## 演講脈絡（依時間序）

整場用一部 AI 生成的漫畫串起來：開發者 Alex 想拿 AI Engineer 帽 T、搬證據的 Pip、嚴格的 reviewer Mira、盯 token 帳單的財務獾。

### 1. 問題：PR 被退不是因為程式碼

- Cassandra 的開場：AI 讓開發速度很快，但很多 PR 被退，原因是描述含錯誤資訊或寫得差。
- 漫畫第一個難題：Alex 交出很長的 ledger，Mira 挑出問題，要求補上確切的 preview 連結、指令歸屬（哪個指令在哪個目錄跑），以及對早期工作的限定說明。講者說這是 Tracetoon 自己的一個真實 PR；Cassandra 一邊開發 Tracetoon，一邊用它替自己寫 PR，邊用邊改。
- 反覆重寫 PR 的代價：Alex 一直重試，只換來「token billionaire」卡。Stephen 的結論是 token 有很多好用處，但重複重寫 PR 不該是其中之一。

### 2. 為什麼 agent 寫的 PR 不準

- 一般做法是在當前 session 裡叫 agent 寫 PR，它只能讀自己那段被灌大的 context；context 壓縮後越寫越不準。
- 所以多數 AI PR 讀起來像「逐行解釋 diff」，因為它手上只有 diff。
- Tracetoon 的做法是讀本機上**多個** session 的紀錄，重建這條分支實際做了什麼。好處是能寫出 diff 看不到的東西，例如「在 `cd` 之前先記下 CWD，因為測試資料會漏到別的 repo」。
- 但閱讀頁點出代價：把多份 trace 拼起來，也多了把事實拼錯的機會。

### 3. 起源：Showtail 的教育研究

Cassandra 說這個專案源自她支援的一項學術研究：學生用 AI 寫程式，交出去的只有最終程式，真正的努力在 prompt 與對話裡，卻沒有被交出去。她把同一套「蒐集過程紀錄」的技術轉用到 PR。回查：[Showtail](https://github.com/Tingsters/Showtail) 確實存在，描述是「替學生蒐集 prompt、編輯、決策與反思，形成教師可審的可驗證軌跡」。

### 4. 原始 Tracetoon 流程與它的錯

- 原始流程：找出某分支的所有 trace → 研究 → 寫描述 → review → 不夠就補 context 再迴圈。
- 講者說主觀與 prbench 都顯示它比不用 Tracetoon 好，但仍會出錯，而且錯常出在「帶更多 context 重寫」那一步。
- 具體錯例：PR 寫「沒有記錄到之後通過的執行」，並宣稱測試通過、所有檢查都跑過。實際 trace 裡 `bun test` 與 `bun x tsc` 是同時跑的，而在這個專案兩者要依序跑測試才會過，所以宣稱與實際執行對不上。閱讀頁把教訓收成一句：「驗證成功」的敘述必須對應實際執行與提交的內容，不能只因為 trace 裡出現過測試指令。

### 5. 換便宜 writer 不行

財務要求「別用 Opus、Sonnet、Haiku，用更便宜的」。他們試了換便宜 writer，品質反而變差。這時 Alex 卡在三頭：修訂花太多、沒辦法降 token、PR 品質也不夠。

### 6. 解法：Relate 嵌入式圖資料庫

- Relate 是用 Rust 寫的嵌入式開源圖資料庫，定位是「給 agent 用的輕量圖資料庫」，好處是多跳查詢、可解釋的 trace，而不需要架一套重型資料庫。
- 原本靠 agent 迴圈解決的工作，改由圖資料庫來做：存關係、找出聚在一起的東西、組成 brief，交給 agent（甚至是較便宜的 agent）去寫。
- 講者說建圖是「零 LLM 成本」，只有本機運算與儲存。閱讀頁特別補一句：這不代表整個系統免費，蒐集、儲存、運算都還在，只是換了一個元件做重複的檢索與關聯工作。
- **neighborhood brief**：把「為什麼、程式碼、檢查」三者連上歸屬與關係，回傳一包相連的資訊。writer 拿到的是每個事實都附來源的單一證據包，草稿更準、修訂輪數更少；reviewer 也比對同一包有界證據，不必各自從一大堆歷史重新編一套說法。

### 7. 反直覺的模型配置：強 writer、便宜 reviewer

- 配置：Claude 端用幾個 Haiku 級 reviewer 取代一個 Sonnet 級 reviewer（Codex 端用 Luna 級），找出問題、對照草稿，再保留 Sonnet 級 writer 修稿。
- Cassandra 的理由：一般人習慣讓 planner、reviewer、checker 用最強的模型；但寫作要像人寫的，低階模型不管給幾輪回饋都只會把內容變成機械式 checklist。反而是對照與交叉檢查那一步比較機械。
- 閱讀頁的限定：這是**針對這個工作負載**的論點，不是「reviewer 都該用小模型」的通則；它成立是因為困難的部分已經被搬進確定性的關係與共用 brief。

### 8. 改善後的 PR 長什麼樣

演講展示的輸出分成幾格：

- **Why**：在 `cd` 執行前記下 shell 的 CWD。
- **例外**：`cd` 目標在 repo 內，或指令提到 root 時。
- **What passed**：型別檢查加 71 個測試，在**提交的內容**上跑的，不是之前的版本。
- **從哪開始看**：`correlate.ts`，檢查開頭 `cd` 的例外處理。

### 9. 數字：prbench

- prbench 是他們為此另做的 PR benchmark，用 audit trace＋程式碼＋LLM judge 評分，並有人工複核。
- 講者口述：Claude 與 Codex 兩邊在 1–100 分上都有顯著提升，judge 幾乎一致偏好 Tracetoon＋Relate；口述數字是「74 到 76、82 到 86，加 2 分、加 4 分」（逐字稿原文，語句破碎）。
- token：有圖的版本約用「一半」token，理由是證據圖事先算好，寫和審都變便宜。
- 測試本身很燒錢：一開始依序跑，後來改平行，很快就把高階電競主機的執行緒吃滿。

### 10. 通則與收尾

只要你有資料、有關係、有要比對的證據，都可以先建一層自訂的圖，因為 agent 不擅長資料分析、評估與整理。在前端幫它一把，成本降、品質升。閱讀頁的收法：在要求 agent 再推理一次整個 archive 之前，先找出哪些關係可以可靠地存下來並查詢；一份較小但相連的紀錄，可能比更大的 context window 有用。結尾宣傳 tracetoon 網站與 AI Engineer Kids Day。

## 回查結果（2026-11-19）

| 演講說法 | 回查 | 結論 |
|---|---|---|
| Tracetoon 是開源專案，支援 Claude、Codex 等工具 | [repo](https://github.com/Tracetoon/tracetoon) 存在，Apache-2.0；README 列出 Claude Code、Codex、Copilot、Cursor、OpenCode 為主要支援，另有十多個社群支援的 agent | **成立**。演講說的網址 tracetune.com 是逐字稿辨識錯誤，官網是 tracetoon.ai |
| Relate 是 Rust 寫的嵌入式開源圖資料庫，當週發表 | [repo](https://github.com/relatedb/relate) 存在，Apache-2.0，README 自述 embedded、in-memory、Cypher、Rust；GitHub 最早的 release 在演講前幾天 | **成立**。README 另有 [limitations](https://github.com/relatedb/relate/blob/main/docs/limitations.md) 文件，明說資料要放得進記憶體、一個 process 一個使用者，不是大型分析引擎 |
| 建圖零 LLM 成本 | Tracetoon README 寫「0 tokens to build the graph and the evidence brief」，是確定性步驟；圖以 WebAssembly 形式內嵌在 CLI，每個 PR 重建 | **成立**（就建圖這一步而言） |
| 強 writer＋便宜 reviewer；便宜 writer 不行 | README 與 5 PR 報告都寫：試過讓 Haiku 當 writer，即使有圖仍輸給 Sonnet 的無圖流程（1–16–8、2–14–9，勝–平–負）；「圖不會把小模型變成中模型」 | **成立**，且有作者自己的對照數據 |
| 「測試通過」不能讓模型自己打 | README：Validation 段由工具從最終程式碼上的測試與 build 紀錄產生，「模型永遠不會打出 all tests pass」；另有 `tracetoon query unverified`、`stale` 查「最後一次修改後沒被任何執行看過的改動」 | **成立**，而且這是全場最可搬走的機制 |
| 品質「74→76、82→86」 | 61 PR 報告的綜合分：Codex 72.1→76.3、Claude Code 59.4→63.0；5 PR 報告：Claude 73.7→78.9、Codex 83.2→86.6 | **對不上**。口述數字與兩份公開報告都不完全吻合，比較像是舊版或記錯的讀數 |
| token 約減半 | 61 PR 報告的成本（不是 token）：Codex −46%、Claude Code −31%（成對幾何平均；單純平均是 −50%、−37%）；5 PR 報告：Claude −41%、Codex −35% | **部分成立**。只有 Codex 在 61 PR 版接近一半；Claude Code 約省三成 |
| 品質提升、錯誤更少 | 61 PR 報告：兩位 judge 一致時偏好有圖版本，Codex 83–34、Claude Code 69–17；但專家確認的事實錯誤，Codex 從每 PR 0.22 升到 0.26，Claude Code 從 0.81 降到 0.68。作者自訂的四項採用門檻，兩邊都只過三項，沒過的都是「錯誤不得變多」那項 | **偏好成立，「更準」只部分成立** |

**61 PR 報告自己揭露的限制**（值得原樣記住）：

- 61 個 PR 全部來自作者自己的 12 個 repo（Tracetoon 本身 17 個、prbench 9 個）。
- **沒有 held-out set**：同一批案例既用來調 brief 也用來評估；調整時挑的是「輸最多的 20 個＋5 個對照」。沒用來調整的 36 個案例，分數差 Codex +5.1、Claude Code +2.6。
- 比較對象是 **Tracetoon 自己的舊流程**，不是「不用 Tracetoon」。舊流程的草稿是前一輪寫好重用的。
- judge 一致率 Codex 77%（κ 0.61）、Claude Code 57%（κ 0.33）；Codex 的 judge 之一與 writer 是同一個模型。
- Claude Code 上有圖版本更常忽略事實表裡的不確定性（58% 對 65%），作者自稱是主要的品質缺口；每個 PR 的耗時約 1.6 倍。
- 5 PR 報告：只有一個 repo 的 5 個 PR，held-out 還沒跑；同一版本在 Codex 重跑一次，分數差就從 +3.5 變成 +5.2。

## 證據強度與限制

| 主張 | 強度 |
|---|---|
| AI PR 常因描述錯誤被退 | 講者經驗，無數據 |
| 換便宜 writer 品質變差、強 writer＋便宜 reviewer 較好 | 作者自建 benchmark 的對照，自報；有成對比較，但 judge 也是 LLM |
| 有圖版本被 judge 偏好 | 自報，61 個自家 PR、無 held-out、未第三方重現 |
| 成本降 31%–46% | 自報；Codex 成本由 token 數乘公開價格估算，Claude Code 用工具自報成本 |
| 「品質 74→76、82→86」 | **勿引用**：與公開報告對不上 |
| 「token 減半」 | **勿引用為通則**：只有 Codex 一邊接近；引用時改用報告的分平台數字並標自報 |
| 「事實錯誤更少」 | **勿引用為整體結論**：Codex 端錯誤其實略增 |
| `bun test` 與 `bun x tsc` 必須依序跑 | 單一專案的情況，不是工具通則 |

## 搬到個人 Claude Code／Codex 工作流程

不一定要裝 Tracetoon；核心機制是「驗證段由執行紀錄產生、不讓模型自己宣稱」。

**做法一：手動版，不裝任何工具**

1. 在要開 PR 的 session 裡，請 agent 先列出「最後一次修改每個檔案之後，跑過哪些測試、lint、build，各自的指令、目錄與結果」，要附原始輸出，不接受「都通過了」。
2. 任何在最後一次修改**之前**跑的檢查，在描述裡寫成「修改前跑過」，不得寫成「已通過」。沒跑的寫「未執行」，沒抓到紀錄的寫「未記錄」，不要寫成「沒做」。
3. 要開 PR 前，自己在乾淨 shell 重跑一次測試與型別檢查，把結果貼進 Verification 段。這一步最便宜，也最能擋住演講裡那種「宣稱全過、其實同時跑掛了」的錯。
4. 描述結構：先寫問題與結果，再寫為什麼這樣做、驗證了什麼、從哪個檔開始 review；不要逐檔列 diff。
5. 若要用 AI review 描述，讓 reviewer 只做比對（描述的每一句是否有對應的紀錄或 diff），用便宜模型即可；寫描述本身用強模型。這和演講的配置一致，但要記得作者的前提：reviewer 拿到的是已整理好的證據，不是整份 log。

**做法二：直接用 Tracetoon**

1. Claude Code 可用 plugin 安裝（`claude plugin marketplace add Tracetoon/tracetoon` → `claude plugin install tracetoon@tracetoon`），或用 README 的安裝腳本。
2. 重啟 agent 後說「用 Tracetoon 幫這個分支開 PR」。安裝程式會加一個 hook，攔下 `gh pr create` 等開 PR 的動作改走 Tracetoon；`git push` 不受影響。
3. 只想看證據、不想讓它開 PR：用 `tracetoon query unverified`（最後一次修改後沒被任何執行看過的改動）、`tracetoon query stale <run>`、`tracetoon query why <檔案>`。
4. 預設漫畫是「allowed」，會照 repo 規則決定要不要畫；不想要就 `tracetoon config set comic off`。畫圖要另外核准圖片路線，而且會把漫畫場景送到外部圖片模型。
5. 公司 repo 或不想被攔的情況：`TRACETOON=0 gh pr create ...` 單次關閉，或 `tracetoon off`。

**要注意的地方**（只讀 README，未實跑）：

- 安裝會改各家 agent 的 hook 設定（README 說會先備份並列出改了哪些檔）。和既有的 `gh pr create` 習慣或其他 PR skill 可能衝突，裝前先想清楚要不要它攔截。
- 它讀的是本機所有 agent 的 session log，README 說會遮蔽密鑰、個資、家目錄路徑與使用者名稱，只發布 PR 文字與漫畫；但「遮得乾不乾淨」沒有外部驗證。
- 專案很新、星數很少、版本更新很快，介面可能變動，引用前回查 README。

**不能直接搬的部分**：Relate 那一層對個人開發者來說是 Tracetoon 的內部實作，自己另建圖資料庫來整理 session log 不划算；要搬的是「先把關係算好再交給模型」這個順序，不是資料庫本身。

## 張力與互補

- **與 Walden Yan 的「證據式交付」同向**：[[Walden-Yan-軟體工廠與給-agent-長期-job]] 也主張交付時要附可檢查的證據，本頁補上「證據由誰產生」的細節：驗證段應由工具從執行紀錄生成，不由模型打字。
- **與 Lauren Tan 互補**：[[Lauren-Tan-把糾正寫進程式庫]] 說 review 會縮成看驗證產物；本頁處理的是那份產物本身會說謊的問題，給了一個「宣稱必須對上執行紀錄」的具體做法。
- **與 Matt Pocock 的 PR 模板互補**：[[Matt-Pocock-的-PR-瓶頸解法]] 要求 PR 附前後證據與單向門標記；本頁的「修改前跑過不算通過」可以直接補進那類模板的驗證段。
- **與 context 優先的判準一致**：[[Context-優先與多-agent-的適用邊界]] 認為能力主要來自 context 品質；Tracetoon 的結果也是靠整理 context（證據包）而非加 agent 數取勝，而且有圖之後研究員與獨立 drafter 兩個 agent 反而被拿掉。
- **reviewer 用小模型的張力**：直覺上 reviewer 該用最強模型，本頁的反例只在「證據已整理好、reviewer 只做比對」時成立。另外 benchmark 本身靠 LLM judge，且 Codex 端 judge 與 writer 同模型；[[LLM-as-judge-知識庫頁面評分]] 整理的 self-preference 與 rubric 問題同樣適用，這是這份數據最該打折的地方。
- **和 review 瓶頸的關係**：[[AI-產碼加速下的-review-瓶頸]] 引用的研究建議工具要提供 provenance、標出不確定性；Tracetoon 正是往這個方向做的一個實作，但它目前的自報數據顯示「標出不確定性」在 Claude Code 端反而退步。
