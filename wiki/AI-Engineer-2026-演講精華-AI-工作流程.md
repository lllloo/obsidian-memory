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

- 27 場讀的是 ai.engineer 官方閱讀頁，部分閱讀頁本身是模型整理稿，不是逐字核對；OpenAI Codex 場（Kundel & Guo）找不到閱讀頁，只有 YouTube 描述與章節，不當論據。
- 文中所有數字都是講者**自報**，沒有外部對照；多數講者是廠商或自家產品團隊，有推廣立場。
- 本頁是二手綜合；要引用單一主張前，回對應閱讀頁（見文末來源清單）確認原句。

已有專頁的相關演講：[[Lauren-Tan-把糾正寫進程式庫]]（同屆 CODE 2026，糾正要變成確定性檢查）、[[Matt-Pocock-的-PR-瓶頸解法]]（AI Engineer Paris，三層 review），本頁第 1、2、6 節是它們的延伸。Hallie 場另有專頁 [[Claude-Code-放手運行的安全與驗證]]。

## 1. 瓶頸從寫 code 移到 merge 與周邊系統

**共識**

- agent 產 PR 已經不是限制，卡住的是 merge queue、CI 容量、rebase 連鎖、人到 merge 為止的時間。Harvey（Joey Wang）：PR 量一個月漲約 60%，merge 時間從 15–30 分鐘拉長到超過 1 小時。Debois：每 merge 一個，排隊中的 PR 都要 rebase、重跑 CI。Sankar：效率算到 merge 為止。
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

**分歧**：Chin 認為小模型只在證據整理好時才適合做審查，Sankar 用不同家模型交叉審（Claude 建、GPT 審）未談此前提。自動合併上，Duolingo 一定排在人核准後，Robinhood 約 60% data PR 不經人審合併，Hallie 的立場是「通過自動化只是政策決定的依據」。

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
- 判準是錯誤能不能收回：Hallie 用 deny 擋不可逆操作（auto mode 約攔下 89%，約一成仍通過）；Thomas（ArtCraft）讓 schema migration、API 決策由人深度介入，UI 層放手；Robinhood 把敏感授權與改語意的 migration 留給人。
- 無人值守步驟縮成可驗證決策點：Almeida（TypeSafe AI）指出自動化流程沒有人在旁修正，必須每次都做對；Robinhood 把能寫成腳本的是非檢查做成硬 gate，agent 只判斷風險且要交代搜過哪裡。

**分歧**：Yan 宣稱 Android 案例多數天零人類訊息、日 merge 約 40–50 PR；Almeida 認為示範表現好不代表適合無人值守；Meta 明說還沒量到省下的值班時間。Willison 提醒持續追求目標的能力本身有風險（他轉述的 agent 逃出評測環境事件，閱讀頁註明未獨立查證），Yan 則以「給 agent 長期 job」為主要方向。

## 6. 改進迴圈：把糾正與失敗變成 eval

**共識**

- 給可量測目標與自我驗證手段，不 one-shot：Willison 對 RTS 遊戲下「make it more fun」，模型跑 12 小時、模擬約 1000 場戰鬥；Yan 給 agent p99 latency 這類持續目標。
- 人的糾正就是資料：Douglas 保存完整 session、加標籤，同類糾正累積成 skill；Ara Khan（Cline）把一次糾正寫成可重現任務；Meta 記憶條目附來源並定期評分淘汰。
- 改進要能遷移、評估器也要驗：Ara Khan 指出只修眼前任務等於過擬合；LinkedIn 在 held-out set 比前後，L1 judge 與人的一致率在 1 分時只有約 55%，且原本診斷選項沒有「judge 判錯」，錯被推給沒問題的 rubric；Robinhood 每次漏判手動補一條 review 規則，不重訓模型。

**分歧**：Ara Khan 讓監督 agent 自改 harness 再重跑，89 題從 77.5% 升到 86.5%；LinkedIn、Robinhood 都把放行留給人。Willison 說能力越強工作越累（簡單的被 agent 吃掉、剩下都是決策），與 Yan「每位工程師生產力超過 10x」的敘事方向相反。

## 個人開發者最值得試的 5 招

1. **「完成」一律附證據**：PR 說明的每條「測試通過」附對最終提交跑的指令與退出碼，沒證據的刪掉；UI 改動附錄影，先讀預期行為再看；腳本與 hook 設 `set -o pipefail`，免得 `cmd | head` 吃掉失敗。出處 Chin、Carson、Yan、Bhardwaj。強度中低：多位獨立講者方向一致，但都是經驗談。
2. **不可逆操作用 deny 擋，檢查點用 hook 強制**：push、對外發訊息用 deny，不只靠分類器；編輯後 lint、結束時測試用 hook 強制。出處 Hallie、Monzo。強度中低：攔截率為 Anthropic 自報。
3. **每次糾正存成可重跑的小任務**：存「輸入＋驗證指令」，同類糾正第二次出現就寫進 skill 或 `AGENTS.md`，改完重跑整批確認可遷移。出處 Ara Khan、Douglas、LinkedIn。強度低至中：benchmark 提升自報、各改動貢獻未分離。
4. **SKILL.md／CLAUDE.md 做有無對照**：把 skill 拆成約 25 條問答，不載入時問模型、用另一家模型當評審；只在不載入時答對的條目先修，確切參數與步驟保留，刪後重跑任務。出處 Petrov、Hallie。強度低：任務評測只有 5 題，「70%」依「知道」的定義與選樣而變。
5. **寫死邊界與重試上限**：補測試時 diff 只准動測試檔，動到正式程式碼、skip 測試、加 sleep 就退回；修 CI 最多 5 次、reviewer 來回最多 3 輪後交人；排程自動化連續失敗 N 次停用並設預算。出處 Duolingo、Carson、Harvey。強度中低：三方各自得出類似上限，皆自報、無對照。

## 來源清單

官方閱讀頁（ai.engineer）：

- [40x More Merged PRs With 2.7x the Engineers — Walden Yan, Cognition](https://ai.engineer/code/2026/talks/walden-yan)（閱讀頁場次名為 A New Age of Software Engineering）
- [2026 in LLMs — Simon Willison](https://ai.engineer/code/2026/talks/simon-willison)
- [How I cloned Adobe with AI — Brandon Thomas, ArtCraft](https://ai.engineer/code/2026/talks/brandon-thomas)（閱讀頁場次名為 Let's Open Source the World，依逐字稿判斷為同場）
- ["Where is all the automation?" — Diogo Almeida, TypeSafe AI](https://ai.engineer/code/2026/talks/diogo-almeida)
- [Rethinking Claude Code Best Practices — Lydia Hallie, Anthropic](https://ai.engineer/code/2026/talks/lydia-hallie)
- [Stop Shipping LLM Settings That Only Win on Paper — Pandey & Varadarajan, DigitalOcean](https://ai.engineer/code/2026/talks/online-rohan-optimization)（自架 serving 調校，個人開發者適用度低）
- [Your SKILL.md Is 70% Stuff the Model Already Knows — Nikolay Petrov, Intel](https://ai.engineer/code/2026/talks/online-skills-knowledge)
- [Your Spec Has Bugs — Rajath Mahendrappa Kotyal, AWS](https://ai.engineer/code/2026/talks/online-aws-specification-analyzer)
- [225,000 Lines of Tests, Written and Merged by Agents — Kush Agrawal, Duolingo](https://ai.engineer/code/2026/talks/online-duolingo-tests)
- [Agents Made Code Free. Maintaining It Didn't Get Cheaper. — Dmitry Buykin, Maersk](https://ai.engineer/code/2026/talks/online-dmitry-maintenance)
- [Pick Problems That Survive When AI Solves Coding — Ara Khan, Cline](https://ai.engineer/code/2026/talks/online-cline-rsi)
- [Your Agent Doesn't Need an LLM for Every Decision — Raymond Weitekamp, OpenProse](https://ai.engineer/talks/hFNbPmzzcEs-your-agent-doesnt-need-llm-every-decision)
- [Your Sub-Agents Are a Distributed System — Girish Konda, Microsoft](https://ai.engineer/talks/DxP5aW4VknQ-your-sub-agents-are-distributed-system-treat)
- [Your Team's Agents Are All Shipping to the Same Code at Once — Patrick Debois, Tessl](https://ai.engineer/talks/fTUinMqA1XQ-your-teams-agents-are-all-shipping-same)
- [Every Company Is Building Agents That Can't Work Together — Justin Schroeder, Standard Agents](https://ai.engineer/talks/3Krz7Rdd4JI-every-company-is-building-agents-that-cant)
- [Your PR Says the Tests Passed. Prove It. — Stephen Chin & Cassandra Chin](https://ai.engineer/code/2026/talks/online-stephen-cassandra)
- [Every Correction You Give Your Agent Is Data — Brian Douglas, Paper Compute](https://ai.engineer/code/2026/talks/online-brian-douglas)
- [Your Agent Hates Your CLI — Ayush Bhardwaj, Allos AI](https://ai.engineer/code/2026/talks/online-ayush-cli)
- [Give Your On-Call Its Own AI Teammate — Meta](https://ai.engineer/code/2026/talks/online-meta-oncall)
- [You Can't Tell What an Agent Skill Will Do by Reading It — Roey Ben Chaim, Zenity](https://www.ai.engineer/talks/_7P580m4kPY-you-cant-tell-what-agent-skill-will)
- [Merge Is the Bottleneck — Prasanna Sankar, Vorflux](https://www.ai.engineer/talks/TlOAhw9t5DA-merge-is-bottleneck)
- [The Agents Were Fine. Everything Around Them Broke. — Joey Wang, Harvey](https://www.ai.engineer/talks/ktbAVYsAxpk-agents-were-fine-everything-around-them-broke)
- [60% of Our Data PRs Now Merge With No Human Review — Chetas Joshi, Robinhood](https://www.ai.engineer/talks/MQiojLnK-E0-60-our-data-prs-now-merge-no)
- [An Agent That Fixes Its Own Mistakes — Saloni Gandhi & Ziwei Guo, LinkedIn](https://ai.engineer/talks/yH7_SIIgI-Y-agent-that-fixes-its-own-mistakes)
- [Stop Chatting With Spreadsheets — Galletta & Felisola Caso, Monzo](https://ai.engineer/talks/ATMcd9tkhhc-stop-chatting-spreadsheets)
- [Your Self-Hosted LLM Needs to Say No — Harshul Jain & Parv Khatri, Audible & SAP](https://ai.engineer/talks/ntVpbyDTYaQ-your-self-hosted-llm-needs-say-no)
- [How One Founder Manages 20 AI Coding Agents at Once — Ryan Carson, Untangle](https://ai.engineer/talks/BTtyguoPvBU-one-founder-manages-20-ai-coding-agents)

僅 YouTube 描述（不當論據）：[New Ways of Working with Codex — Kundel & Guo, OpenAI](https://www.youtube.com/watch?v=IPh9YsWvDQk)。
