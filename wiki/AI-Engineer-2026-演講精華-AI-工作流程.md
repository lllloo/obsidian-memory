---
title: AI Engineer 2026 演講精華：AI 工作流程
description: 綜合 AI Engineer 頻道 28 場近期演講，歸納 merge 瓶頸、驗證證據、skill 設計、多 agent 協作、自主分級與改進迴圈六大主題
created: 2026-11-19
updated: 2026-11-19
source: https://www.youtube.com/@aiDotEngineer/videos
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - testing
  - context-engineering
  - evaluation
---

2026-11-19 回存。取 AI Engineer YouTube 頻道「影片」頁當日最新約 30 場，扣掉已有專頁的 Lauren Tan 場和沒抓到 ID 的 Gemini 4 場，共 28 場，由多個 subagent 分頭讀官方閱讀頁（ai.engineer，含整理稿與機器逐字稿）後綜合。

**證據強度與限制**：

- 本頁是第一輪粗讀的跨場綜合。同日第二輪已逐場深讀（全文逐字稿＋回查引用的 repo、論文、官方文件），每場一頁，見文末「逐場深讀頁」；**細節與勿引用清單以各場專頁為準**，本頁只留跨場比較。第二輪回查推翻或修正的句子已就地標註。
- 第一輪 27 場讀 ai.engineer 官方閱讀頁；OpenAI Codex 場沒有閱讀頁，第二輪改讀 YouTube 字幕，見 [[Kundel-Guo-Codex-的新工作方式]]。
- 文中所有數字都是講者**自報**，沒有外部對照；多數講者是廠商或自家產品團隊，有推廣立場。
- 本頁是二手綜合；要引用單一主張前，回對應的逐場深讀頁與其 raw 原文確認原句。

已有專頁的相關演講：[[Lauren-Tan-把糾正寫進程式庫]]（同屆 CODE 2026，糾正要變成確定性檢查）、[[Matt-Pocock-的-PR-瓶頸解法]]（AI Engineer Paris，三層 review），本頁第 1、2、6 節是它們的延伸。Hallie 場另有專頁 [[Claude-Code-放手運行的安全與驗證]]。

## 1. 瓶頸從寫 code 移到 merge 與周邊系統

**共識**

- agent 產 PR 已經不是限制，卡住的是 merge queue、CI 容量、rebase 連鎖、人到 merge 為止的時間。Harvey（Joey Wang）：PR 量一個月漲約 60%，merge 時間從 15–30 分鐘拉長到超過 1 小時。Debois：每 merge 一個，排隊中的 PR 都要 rebase、重跑 CI。Sankar 場閱讀頁的提煉是「效率算到 merge 為止」（逐字稿沒有這句原話，見 [[Prasanna-Sankar-雲端-agent-的瓶頸一路移到開工]]）。
- 基礎設施要改成 agent 能自己跑起整套服務：Yan（Cognition）用 Docker Compose 加 mock、每小時重建快照；Harvey 保留本地 repo 副本省掉 checkout；Duolingo 改 Mac runner 讓 agent 能本地 build。
- 無人看管的自動化需要護欄：Harvey 一個 alert bug 讓任務 4 小時內從每天約 50 個暴增到約 900 個，之後規定連續失敗 5 次停用、設預算或到期日。Sankar：別下「修掉所有 alert」這種指令，要寫清觸發訊號、結果歸誰、預算。
- 人能同時追的 session 有上限：Sankar 約 10 個；Carson 一個 manager 帶 5–25 個 builder，上限取決於人跟得上多少更新。

**分歧**：Carson 主張一個 manager session 帶約 20 個 builder，Sankar 認為約 10 個就成了專案管理工作。Yan 談的是組織改成 2–3 人小 pod，Debois 談的是整隊 agent 同時合進同一個 main，兩者不是同一層問題。

## 2. 驗證：測試全綠不等於對，要附證據

**共識**

- 「完成」「測試通過」要附證據，而且是對最終提交跑的：Chin 實例是 `bun test` 與 `tsc` 並行跑、PR 卻宣稱通過；Carson、Yan、Sankar 要求附運作中的錄影或截圖；Harvey 每 20 個 merge 只有 1 個附了有效證明。
- 測試本身會騙人：Buykin（Maersk）故意改壞指令，很多測試沒抓到，沒有任務走到的分支要記「沒有證據」而非「正確」。
- 防 agent 偷吃步：Duolingo 用確定性檢查限制只能改測試檔，禁止改正式程式碼、刪或停用測試、加長等待；修 CI 最多 5 次，被拒檔案冷卻 30 天。
- 規格也要驗：Kotyal（AWS）把同一條需求翻譯多次，分歧代表歧義，再用 SMT solver 抓規則矛盾與缺漏。
- 審查要獨立：Buykin 讓第二個 agent 只拿 checklist、看不到作者推理；Monzo 另派 reviewer agent 提質疑，由人在分支裡決定採納。

**分歧**：Chin 認為小模型只在證據整理好時才適合做審查，Sankar 提到很多人用不同家模型交叉審（Claude 建、GPT 審），Vorflux 讓它可設定，並非他本人推薦的配置。自動合併上，Duolingo 一定排在人核准後，Robinhood 約 60% data PR 不經人審合併，Hallie 的立場是「通過自動化只是政策決定的依據」。

## 3. Skill、context 與指示的設計

**共識**

- 多寫的指示不是免費的：Hallie 說糾正舊模型的強調語句會讓新模型多做工具呼叫；Petrov（Intel）發現有些條目「載入 skill 答錯、不載入反而答對」，屬有害內容要優先修；Bhardwaj 的案例是舊旗標已成 no-op，skill 仍叫 agent 用，95 次搜尋全部沿用；Buykin 指出重複路徑收進 workflow tool 後舊 prose 要一起刪，否則 agent 會重做。
- 改完要量測：Petrov 把任務評測分「載入／不載入」兩組跑，刪減後重跑分數維持才算數；Bhardwaj 主張看任務結果不只看 token，DuckDB 案例輸出少 59%，省下的 token 只佔約 0.5%。
- 關鍵規則不能只寫在文字裡：Monzo 發現 skill 叫腳本時模型仍可能不叫，關鍵計算移到後端強制；Hallie 用 hook 在檢查點驗證。
- 第三方 skill 當軟體依賴管理：Ben Chaim（Zenity）主張只讀 SKILL.md 判斷不了行為，要在沙箱實跑看行程、檔案與網路。
- 文件就是介面：Bhardwaj 指出 agent 不會抱怨難用的 CLI，而是自己 pipe 進 `head`／`grep` 繞過，這些重複繞路就是改 CLI 的依據。

**分歧**：Hallie 傾向刪掉模型已知的內容；Petrov 明說「模型已知」不等於「可刪」，嚴格評分下確切參數與步驟要保留、刪後要重跑評測。Douglas 主張把修正寫成 skill 多半就拿到大部分效益；Monzo 認為 skill prose 不可靠，關鍵規則要用程式強制。

## 4. 多 agent 協作：當成分散式系統

**共識**

- sub-agent 要回傳結構化結果：Konda（Microsoft）的 SAFE handoff 回傳 status、證據來源與讀取時間、已做的副作用；partial、unknown 是正常結果；timeout 的寫入先 read back 再決定重試。
- 共享 context 會汙染：Konda 舉例一個 worker 的猜測寫進共享 context，被另兩個引用後看起來像三方一致；Buykin 讓 agent 看全部資料，它自己發明了價格檢查，改成只給決策需要的事實。
- 動工前協調：Debois 先 claim ticket、公告預計改的檔案，再用 worktree 隔離；Carson 一張 ticket 一個 PR，另設 merge queue manager 處理跨 PR 問題（如 migration 編號撞號）。
- 巡視與重試由程式保證：Carson 用排程腳本每 10–15 分鐘叫 manager 巡所有子 session；Jain & Khatri 主張 429 降並行、503／529 遵守 Retry-After 加 jitter，重試設預算。
- 能確定性處理的就不用 LLM：Weitekamp 讓分類器處理「從已知選項挑一個」；Schroeder 指出決定可靠性的是 harness 行為，prompt 和 MCP 都帶不走。

**分歧**：語意衝突上 Debois 提議讓 agent 比對多個 PR 的意圖（方向性提案），Konda 主張由程式驗 schema 與證據、不信 agent 文字判斷。Konda 自己也說 SAFE handoff 只適合會碰正式環境的委派，純起草多半只是負擔。

## 5. 自主程度與權限：依可逆性逐項放行

**共識**

- 信任以單一行動為單位累積：Meta 值班 agent 分三級（只調查 → 草擬修復待核准 → 自行處理低關鍵度），某行動要升級需錯誤成本低、易發現、有良好紀錄；Sankar 把常駐 agent 當新人帶。
- 判準是錯誤能不能收回：Hallie 用 deny 擋不可逆操作（auto mode 約攔下 89%，約一成仍通過）；Thomas（ArtCraft）讓 schema migration、API 決策由人深度介入，桌面 app、遊戲這類「基本上不可變」的東西才放手；Robinhood 把敏感授權與改語意的 migration 留給人。
- 無人值守步驟縮成可驗證決策點：Almeida（TypeSafe AI）指出自動化流程沒有人在旁修正，必須每次都做對；Robinhood 把能寫成腳本的是非檢查做成硬 gate，agent 只判斷風險且要交代搜過哪裡。

**分歧**：Yan 宣稱 Android 案例多數天零人類訊息、日 merge 約 40–50 PR（已被取代（2026-11-19）：Devin Bots 文寫 44 天中 22 天零訊息，40–50 是高峰、平均約 26，見 [[Walden-Yan-軟體工廠與給-agent-長期-job]]）；Almeida 認為示範表現好不代表適合無人值守；Meta 明說還沒量到省下的值班時間。Willison 提醒持續追求目標的能力本身有風險（他轉述的 agent 逃出評測環境事件，閱讀頁註明未獨立查證），Yan 則以「給 agent 長期 job」為主要方向。

## 6. 改進迴圈：把糾正與失敗變成 eval

**共識**

- 給可量測目標與自我驗證手段，不 one-shot：Willison 對 RTS 遊戲下「make it more fun」，模型長時間自跑、大量模擬戰鬥（演講說 12 小時、約一千場；部落格原文只寫 many hours、1,200 場，見 [[Simon-Willison-2026-LLM-三個轉折點]]）；Yan 給 agent p99 latency 這類持續目標。
- 人的糾正就是資料：Douglas 保存完整 session、加標籤，同類糾正累積成 skill；Ara Khan（Cline）把一次糾正寫成可重現任務；Meta 記憶條目附來源並定期評分淘汰。
- 改進要能遷移、評估器也要驗：Ara Khan 指出只修眼前任務等於過擬合；LinkedIn 在 held-out set 比前後，L1 judge 與人的一致率在 1 分時只有約 55%，且原本診斷選項沒有「judge 判錯」，錯被推給沒問題的 rubric；Robinhood 每次漏判手動補一條 review 規則，不重訓模型。

**分歧**：Ara Khan 讓監督 agent 自改 harness 再重跑，89 題從 77.5% 升到 86.5%（最佳一輪 88.8%、重複平均 87.1%；改 harness 的是另一家模型，原 PR 未合併而拆成兩個，見 [[Ara-Khan-讓-agent-自動爬升-harness-與選題]]）；LinkedIn、Robinhood 都把放行留給人。Willison 說能力越強工作越累（簡單的被 agent 吃掉、剩下都是決策），與 Yan「每位工程師生產力超過 10x」的敘事方向相反。

## 個人開發者最值得試的 5 招

1. **「完成」一律附證據**：PR 說明的每條「測試通過」附對最終提交跑的指令與退出碼，沒證據的刪掉；UI 改動附錄影，先讀預期行為再看；腳本與 hook 設 `set -o pipefail`，免得 `cmd | head` 吃掉失敗。出處 Chin、Carson、Yan、Bhardwaj。強度中低：多位獨立講者方向一致，但都是經驗談。
2. **不可逆操作用 deny 擋，檢查點用 hook 強制**：push、對外發訊息用 deny，不只靠分類器；編輯後 lint、結束時測試用 hook 強制。出處 Hallie、Monzo。強度中低：攔截率為 Anthropic 自報。
3. **每次糾正存成可重跑的小任務**：存「輸入＋驗證指令」，同類糾正第二次出現就寫進 skill 或 `AGENTS.md`，改完重跑整批確認可遷移。出處 Ara Khan、Douglas、LinkedIn。強度低至中：benchmark 提升自報、各改動貢獻未分離。
4. **SKILL.md／CLAUDE.md 做有無對照**：把 skill 拆成約 25 條問答，不載入時問模型、用另一家模型當評審；只在不載入時答對的條目先修，確切參數與步驟保留，刪後重跑任務。出處 Petrov、Hallie。強度低：「70%」依「知道」的定義與選樣而變，投影片的 Opus 數字與 Dokimi 文件對不上，見 [[Nikolay-Petrov-量出-skill-裡模型已知的內容]]。
5. **寫死邊界與重試上限**：補測試時 diff 只准動測試檔，動到正式程式碼、skip 測試、加 sleep 就退回；修 CI 最多 5 次、reviewer 來回最多 3 輪後交人；排程自動化連續失敗 N 次停用並設預算。出處 Duolingo、Carson、Harvey。強度中低：三方各自得出類似上限，皆自報、無對照。

## 逐場深讀頁

2026-11-19 第二輪，每場一頁（含 raw 原文、演講脈絡、可照做步驟、回查結果與勿引用）：

- [[Walden-Yan-軟體工廠與給-agent-長期-job]] — Cognition 的 Walden Yan 談內部軟體工廠：Docker Compose 加 mock 的單 VM 環境、影片證據交付、改給 agent 可量測的長期 job；附 Bots 文與 CoreWeave 回查
- [[Simon-Willison-2026-LLM-三個轉折點]] — Willison 以三個轉折點回顧 2026：coding agent 日常化、給目標與工具就能長跑的「Fable 級」模型、生成遊戲變好玩；逐段回查 repo 與部落格，附可照做步驟與勿引用項
- [[Kundel-Guo-Codex-的新工作方式]] — OpenAI 講者示範 Codex 的 plugin context、Ultrafast UI 迭代、Codex Cloud、Sites 與 Voice／Dots 委派；附官方文件與原始碼回查、可搬做法與勿引用項
- [[Brandon-Thomas-用-agent-重做並開源桌面應用]] — Brandon Thomas 用 agent 以 Rust 重做 Photoshop 等應用並開源：大規格提示、每個動作都是命令、依可逆性分流 review；回查 star、下載、Autocraft 現況
- [[Diogo-Almeida-助理不等於自動化]] — Diogo Almeida（TypeSafe AI）主張助理不等於可無人值守的自動化：要先挑對任務，再把可靠的語意判斷放進程式；含完整脈絡、回查結果與勿引用清單
- [[Claude-Code-放手運行的安全與驗證]] — 深讀 Lydia Hallie 整場逐字稿，依時序整理人退出迴圈後由 auto mode、deny、沙箱、cloud、hook、CI、Projects 接手的論證，附官方文件回查與 Claude Code／Codex 照做步驟
- [[Rohan-Pandey-用貝氏最佳化找-serving-設定]] — DigitalOcean 線上場：依流量組合與 goodput 用 Optuna 迴圈調自架模型 serving 設定，附 vLLM 官方工具對照與證據限制
- [[Nikolay-Petrov-量出-skill-裡模型已知的內容]] — 把 SKILL.md 拆成原子問答、有無 skill 對照量出模型已知、新知、有害內容；嚴格評分下已知僅約兩成，附 Dokimi 回查與照做步驟
- [[Rajath-Kotyal-規格先驗再交給-agent]] — AWS Kotyal：規格交給 agent 前先驗，LLM 多次翻譯成邏輯、SMT solver 抓矛盾與缺口、歧義交人二選一；對照 Kiro 原文，附可照做步驟與勿引用數字
- [[Kush-Agrawal-用-agent-佇列補測試]] — Duolingo 以 Temporal 排程 coding agent 補 iOS 單元測試：選檔評分、PR 生命週期狀態機、防作弊三層，對照講者部落格回查自報數字落差
- [[Dmitry-Buykin-每週小幅修剪取代大重寫]] — Buykin（Maersk）以六顆寶石串起每週修剪法：專家擁有決策表、控制模型所見、凍結真實任務重播、退役變體連測試一起刪，附回查與自報數字強度
- [[Ara-Khan-讓-agent-自動爬升-harness-與選題]] — Cline 讓 GPT-5.6 Sol 監督跑 Terminal-Bench、讀失敗、改 harness，自報 69→77/89；回查發現 PR 未整包合併、SOTA 宣稱違反自家 prompt 規則，附個人可縮小照做的 eval 迴圈與選題建議
- [[Raymond-Weitekamp-遞迴決策模型與分類器當根節點]] — Weitekamp 主張以只會挑選的決策模型當 agent 根節點、LLM 降為選項；含 RDM 三規則、map、arbiter、Earshot 與 rdm repo 回查落差
- [[Girish-Konda-把-sub-agent-當分散式系統]] — Konda 把 sub-agent 交接視為分散式系統：部分失敗、逾時、dirty read、fan-out、重試寫入，提出 SAFE handoffs，附 Pacemaker 回查與個人工作流程做法
- [[Patrick-Debois-多人多-agent-同時合進同一-main]] — Debois 的 concurrent delivery：派工時 claim 並公告預計改動、檢查意圖衝突、跑 speculative merge train、依上線風險決定 review 深度；附 GitLab／Zuul 回查與個人落地做法
- [[Justin-Schroeder-把整個-harness-標準化]] — Schroeder 主張 agent 可靠性在 harness，發表 Standard Agent Spec 規範整個 agent 與 runtime；回查發現 Builder 閉源、「首個規範」說過頭
- [[Stephen-Chin-與-Cassandra-Chin-PR-描述要附證據包]] — Chin 主張 PR 描述從確定性證據圖寫成、驗證段由執行紀錄產生，強 writer 配便宜 reviewer；回查發現口述品質數字對不上、token 減半只在 Codex 成立
- [[Brian-Douglas-把糾正存成團隊-review-資料]] — Brian Douglas（Paper Compute）主張保存 agent session、標記 pushback 等標籤，先把團隊糾正寫成 skill 並用 eval 驗證，再考慮微調 reviewer；附 tapes 與部落格回查
- [[Ayush-Bhardwaj-把-agent-繞路當成-CLI-的-bug-report]] — 從對話紀錄挖 agent 重複的 pipe 繞路當 CLI bug report：選擇型旗標、fail loudly、skill 同步、重播驗收，含 Infracost／DuckDB 回查與自報數字強度
- [[Meta-值班團隊-給每個輪替一個-AI-隊友]] — Meta 值班 AI 隊友：每個輪替一個常駐迴圈，自主權以單一行動逐級賺取，記憶屬團隊、可糾正可淘汰；附回查、勿引用數字與個人可照做步驟
- [[Roey-Ben-Chaim-讀-skill-看不出它會做什麼]] — Zenity 在沙箱實跑數千個 agent skill（world builder、operator、行程／檔案／網路三層紀錄）與 Paperclip 仿冒竊密案；附回查、數字強度與個人導入第三方 skill 的七步檢查
- [[Prasanna-Sankar-雲端-agent-的瓶頸一路移到開工]] — Vorflux 的 Sankar 依序拆解雲端 agent 從環境、規劃、拆工、測試、review 到 merge 的六個瓶頸，再談人成為專案經理後改由常駐 Autobot 從訊號自己開工，附回查與強度標註
- [[Joey-Wang-agent-量放大後壞掉的周邊系統]] — Harvey 內部 agent 平台 Spectre 量放大後，壞掉的是 alert 觸發、叢集容量與 merge queue；整理 follow-up loop、公平佇列、自動化護欄與個人可搬做法
- [[Chetas-Joshi-Robinhood-資料-PR-混合審查]] — Robinhood data PR 審查分三層：腳本對權威來源查事實、agent 讀 repo 判風險並交代搜過哪裡、敏感授權與改語意 migration 永遠歸人；60% 免人審等數字皆自報
- [[Saloni-Gandhi-與-Ziwei-Guo-先驗證-judge-再讓-agent-自改]] — LinkedIn 用 judge、根因反思與 GEPA 定期改使用者理解 agent 的 prompt；L1 在低分側最不準、L2 會誤怪 rubric，先校準評估器
- [[Galletta-與-Felisola-Caso-可信任財務分析-harness-五原則]] — Monzo 兩位資料人用婚禮付款示範財務 harness 五原則：共識、一致、證據、問責、驗證；核對工作坊 repo 的 gate、數字檢查與 reviewer，附可搬做法
- [[Harshul-Jain-與-Parv-Khatri-自架-LLM-要會說不]] — 自架 LLM 被 coding agent 一次幾十個呼叫灌爆時，在 ingress 先 admit／defer／reject、回可照做的錯誤碼，並以含拒絕數的 goodput 驗證；附 AdmitPerf 與事故回查
- [[Ryan-Carson-一個-manager-session-帶-20-個-builder]] — Untangle 的 Carson 讓不寫碼的 manager session 每 15 分鐘排程巡視約 20 個 builder，review 最多 3 輪、人看錄影驗收，並以錄影招募；附 Devin 文件回查
- [[Lauren-Tan-把糾正寫進程式庫]] — 同屆 CODE 2026，糾正 agent 要變成程式庫裡的確定性檢查（先前已建頁）
