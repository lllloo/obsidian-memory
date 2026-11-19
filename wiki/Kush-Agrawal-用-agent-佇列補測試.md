---
title: Kush Agrawal 用 agent 佇列補測試
description: Duolingo 以 Temporal 排程 coding agent 補 iOS 單元測試：選檔評分、PR 生命週期狀態機、防作弊三層與自報數字的回查落差
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-duolingo-tests
published: 2026-11-11
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - testing
  - automation
---

# Kush Agrawal 用 agent 佇列補測試

來源：AI Engineer CODE 2026 線上場次〈225,000 Lines of Tests, Written and Merged by Agents〉的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-Agrawal-225000-Lines-of-Tests]]（Day 1 直播影片 `ZZ19zhYnDKY`，本場約 12 分半）。回查另讀了講者本人在 Duolingo 工程部落格的兩篇文章：[iOS 單元測試產生管線](https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/)（2026-06-24，作者署名 Kush Agrawal）與[共用 agent 平台](https://blog.duolingo.com/production-ready-ai-agent-platform/)（2026-08-04）。

**一句話**：讓 agent 大量產 PR 不難，難的是 PR 開出來之後——選對要測的檔、限制 agent 能改什麼、CI 紅了怎麼修、修不好何時放棄、找誰 review、被退件後別再煩同一個人。Duolingo 的「coding agent」實際上是一條**有拒收與修復機制的工作佇列**，設計心力花在拒絕與修復的不比花在產生的少。

## 講者與立場

Kush Agrawal，Duolingo 平台團隊 staff engineer，負責為 100 多位 client app 工程師做開發工具與 AI 輔助流程；自述之前在 Stripe、Uber 待了近十年。他講的是**內部工具**，沒有對外販售的產品要推；但演講與部落格最後都帶到徵才，且全部數字都是 Duolingo 自己量的。用到的外部工具（Temporal、Claude Code、Codex、GitHub、Datadog）都是現成服務，沒有為哪家背書的跡象。

## 演講脈絡（按順序）

### 1. 背景：成長中的老程式庫

- iOS 與 Android app 都超過 10 年，每週上架一次，同時跑 600 多個 A/B test。
- iOS repo 可執行程式碼從 2019 年約 20 萬行長到近 200 萬行（閱讀頁寫 180 萬），他指出 AI 輔助寫碼普及後曲線開始往上彎。
- 貢獻者從去年約 200 人到今年已超過 250 人，很多不是 iOS 工程師：後端、Android 工程師，甚至 PM、設計師，他歸功於 Cursor、Claude Code 這類工具。
- 程式庫在轉型中：幾年前統一採用 MVVM，目前約一半符合、另一半是待遷移的 legacy。**MVVM 那一半最好測，所以只從那裡下手。**
- 起點（2026 年 3 月）：整體單元測試覆蓋率 11%；repositories 11%、view models 9%、data sources 5%，MVVM 合計約 9%。

### 2. 為什麼現在要補測試

他的論點：人和 agent 寫碼都變快後，難的不再是寫，而是**確認改動安全可上線**，瓶頸從寫轉到驗證。單元測試在測試金字塔最底層，便宜、跑得快，同時有三個作用：保護上線、讓 agent 的改動在 CI 立刻拿到「哪裡壞了」的回饋、當作「程式應該做什麼」的活文件。

八個月後的結果（自報）：整體 11% → 24%；repositories 11 → 72、view models 9 → 58、data sources 5 → 41，MVVM 合計 9% → 59%。

### 3. 迴圈與積木

紙上是五步：**identify**（找出需要測試的檔）→ **write**（agent 寫測試）→ **verify**（測試品質夠、CI 綠）→ **resolve**（工程師 review 並 merge）→ **iterate**（把回饋折回去，下一批更好）。

實作是幾個 Temporal workflow 透過 S3 共享狀態協調，每個方塊都對應五步之一：

- **Temporal**：durable workflow 引擎，用一般 Python 寫 workflow，worker 當掉會從中斷處接著跑。他認為這很適合 agent，因為一次 agent session 可能跑幾秒到幾小時，還會呼叫 GitHub、CI、S3、Claude。用到的內建功能：類 cron 的 schedule、可組合的 child workflow（平行 fan-out）、內建 retry／timeout，以及冪等性（同一個檔不會被重複啟動兩次）。
- **Claude Code** 當 coding agent；**S3** 放共享狀態；**GitHub** 負責 Actions、label、PR；**Datadog** 監看管線健康度。

專案切成四個里程碑：本地驗證 → 排程回補 → PR 生命週期 → label 觸發。

### 4. 里程碑一：本地驗證「到底可不可行」

先用最少的工夫確認 agent 能不能把這件事做好、能不能放大規模。做法是一個 Claude Code command 當 orchestrator：跑 Xcode build script 產出本地覆蓋率報告 → 交給他們寫的選檔 script → 每個選中的檔交給兩個 subagent，一個寫測試、一個開 PR。迴圈跑了兩批：

| 批次 | PR 數 | merge 數 |
|---|---|---|
| 第一批 | 17 | 8 |
| 第二批 | 40 | 19 |

約五成 merge 率。他強調這一階段的目的**不是多 merge，而是看 agent 怎麼失敗、在上線前把小毛病修掉**。看到的失敗類型與修法：

- **XCTest 與 Swift Testing 混在同一檔**：給 agent 明確規則，寫清楚什麼時候用哪一個（散文層修正）。
- **巨大的 user client singleton**：有些程式傳具體類別（很難 mock），有些傳 protocol 版。他們把**整個程式庫遷移到 protocol 版，並加 lint rule 強制**。這讓一大批檔案對 agent 和人都變得好測（程式庫層修正）。
- **Swift 並行（concurrency）問題與 agent 寫出依賴時間的測試**：後者是 CI flaky 的大來源；靠在 testing skill 裡補規則與範例改善。

### 5. 里程碑二：排程回補（backfill）

覆蓋率落後太多，最大槓桿是替已經 merge 的程式碼補測試。

- **identify**：每次 PR merge 進 main，GitHub Actions job 產出 Xcode 覆蓋率報告上傳 S3，成為「最新覆蓋率」的唯一真相來源。backfill workflow 取這份報告、跑選檔 script。
- **選檔 script 不是挑覆蓋率最低的檔**，而是替每個 Swift 檔打分：「我們多有把握 agent 能替它寫出好測試」。最強訊號是檔案類型——view model、repository、data source 加權 2.5 倍，legacy 檔往下壓；UI 程式碼直接跳過（那裡 snapshot test 更合適）；檔案越大扣分越多。
- **write**：每個檔一個 child workflow，全部平行。agent clone iOS repo → 讀 repo 裡的 testing skill（寫明什麼叫好測試）→ 寫測試加上需要的 mock 與 fake → 開 PR 並貼 `generated-test` label 方便之後辨識。
- 這些 agent 跑在 Duolingo 自建的 cloud coding agent 平台上，他形容為「雲端上 Claude Code 與 Codex 的抽象層」：可從 Slack、Temporal 或 GitHub 呼叫，經 MCP 接內部工具，並記錄事件以追蹤每次 agent run 在做什麼、花多少錢。一開始跑在 Linux 機器，後來搬到 Mac runner（下面會說為什麼重要）。
- **PR 長相**：描述用固定模板，明寫是 AI 產生的。reviewer 有四個選擇：核准（PR 已開 auto-merge）、直接 push 修改、改派給更合適的人、附理由關掉。

### 6. 里程碑三：PR 生命週期 workflow

回補上線後冒出新問題：同時有幾十到幾百個開著的 PR，沒人管得動。生命週期 workflow 可視為**狀態機**：每隔幾小時掃一遍所有 `generated-test` PR，**每個 PR 每輪只做一個動作**，涵蓋 verify 與 resolve 兩步。決策樹：

1. 有 merge conflict，或開了約 3 週 → 關掉、標為 stale。
2. CI 還在跑，或已經有 reviewer 在看 → 跳過。
3. CI 綠且沒有 reviewer → 找人指派。
4. CI 紅 → 嘗試修。
5. reviewer 退件 → 該檔進 **30 天冷卻**，免得一直拿同一個 PR 煩工程師。

CI 失敗時先看是哪個 job：

- **pre-commit 失敗**：交給 GitHub Action 自動套修正。便宜、確定性、不需要 agent。
- **真的測試失敗**：再啟一個 agent 讀 CI log、push 修正。**整個修復迴圈上限 5 次**，超過就關 PR，不無限修下去。

CI 綠了之後找 reviewer：對被測的原始檔跑 `git blame`，取主要貢獻者指派，並開 auto-merge。核准就 merge，退件就進 30 天冷卻。

### 7. 里程碑四：label 觸發

讓工程師替自己正在寫的新程式碼也拿到測試：在自己的 PR 加上寫測試的 label，就走同一套 Temporal 基礎設施。唯一差別是選檔——不跑選檔 script，直接取該 PR 改到的檔。agent 寫完會開一個 draft PR 連回原 PR。

### 8. 挑戰一：回饋太慢（lint）

Linux 機器沒有 Xcode 和 lint 工具，agent 開 PR 後要等 20–30 分鐘 CI 才失敗，浪費 agent 時間也浪費越來越稀缺的 CI 資源。一度 30.6% 的 PR 因 lint 失敗，深入看發現其中 62% 只來自兩條 lint rule。分層修：

1. prompt 裡給更好的範例與要避開的陷阱。
2. GitHub Action 在 CI 自動修 lint 錯誤。
3. 稽核修不掉的 rule，**刪掉訊號不高的**——這對 agent 和人都變輕鬆。
4. 真正的解法：把 agent 搬到 Mac runner，開 PR 前就能在本地 build 與 lint。

### 9. 挑戰二：PR 品質與 agent 抄捷徑

指派給人的 PR 要是對方「真的敢核准」的東西，但 agent 有時會走最短路徑讓 CI 變綠：為了讓失敗的測試通過去**改 production code**、**修改、刪除或靜音既有測試**、在測試裡**加長時間等待**（讓 CI flaky）。沒有單一解法，所以做了三層：

1. **確定性規則**：PR 只要碰到測試、mock、fake、stub 以外的檔，直接關掉。
2. **既有 AI code review**：Duolingo 用 Claude 與 Codex review 每個 PR，這些 bot 常留言；他們做了一個 agent，在人看到之前先處理掉所有 P0 等級留言。
3. **LLM-as-judge**：專為這類測試 PR 打造的 reviewer agent，讀 diff 後拒收 production 修改、被改或被刪的測試、被停用的測試、長時間等待；學到新東西就持續加檢查項。逐字稿說它已審約「,200」個 PR（數字有漏字，見下方回查）、拒收 73 個。每次拒收都附留言寫明理由，團隊**讀這些回饋、折回 prompt 和 skill**，讓同樣的錯越來越少。

### 10. 成果

- 管線已 merge 超過 700 個測試 PR、約 22.5 萬行測試碼，**每個 PR 都經人 review 並核准**。
- 自 3 月起，管線寫了 repo 裡 34% 的新測試檔、44% 的新測試案例，以及約 10% 的新增程式行（逐字稿此處辨識不清，口徑不明）。
- 這個占比最近幾週反而下降，因為工程師自己寫的測試變多了——他說「這老實說才是最終目標」。
- 覆蓋率曲線自 4 月排程回補上線起算，6–7 月管線完全放量時明顯上彎。

### 11. 學到的事與思想實驗

- **這個模式能推廣**：identify → write → verify → resolve → iterate 不是測試專屬，單元測試只是最容易摘的果子。公司已把同一迴圈用在把畫面現代化成 MVVM 與 SwiftUI、Android 程式遷到 Kotlin coroutines（逐字稿作「Corines」，依上下文推測）、產生 snapshot test。
- **思想實驗**（不是已上線的東西）：有一類新的快速通用分類器（他舉 Jev），吃一塊狀態、毫秒級輸出一個動作。如果把 PR 生命週期 workflow 裡手寫的決策樹換成它——PR 狀態進去、分類器選下一個動作——會怎樣？

## 可搬到個人 Claude Code／Codex 工作流程的做法

Duolingo 的基礎設施（Temporal、S3 狀態、Datadog、自建 agent 平台、Mac runner 池）是為「幾十到幾百個同時開著的 PR、上百名 reviewer」設計的，個人專案不需要照搬。能搬的是**佇列的形狀與拒收規則**：

1. **先手動跑一兩批再自動化**：在本機用 Claude Code 對 10–20 個檔逐一產測試、開 PR，記下每個失敗屬於哪一類（規則不清？程式難測？環境問題？）。五成 merge 率就足以看出失敗分類，先修這些再放量——這和 [[Lauren-Tan-把糾正寫進程式庫]] 的「先穩內圈，再自動化外圈」是同一件事。
2. **寫一個選檔 script，而不是挑覆蓋率最低的檔**：從覆蓋率報告出發，對「結構好測的層」（純函式、service、repository、view model）加權，大檔扣分，UI 層排除或改走 snapshot／E2E。目標是「agent 有把握寫好」的檔，不是缺口最大的檔。
3. **把測試寫法寫成 repo 內的 testing skill**：明定用哪個測試框架、mock／fake 放哪、怎麼命名，**禁止用 sleep／長時間等待**，附正反範例。每次退件理由都回寫進這份 skill。
4. **用確定性檢查限制 agent 能改的檔**：在 CI 加一個 job，`git diff --name-only origin/main...HEAD` 的每個路徑都必須符合測試檔、mock、fake 的 glob，否則失敗。這比在 prompt 寫「不要改 production code」可靠（Duolingo 部落格記錄過 CI 修復 agent 真的去改 production 檔）。另外加一條：既有測試檔只准新增、不准刪改或加 skip 標記。
5. **CI 紅燈修復設上限**：讓 agent 讀 CI log 修，最多 N 次（Duolingo 用 5）；超過就關 PR，並在一個簡單的 JSON 檔記「此檔冷卻到某日」，下次選檔時跳過。可確定性修的（formatter、lint autofix）不要交給 agent。
6. **讓 agent 開 PR 前先在本機跑過 build、lint、測試**：這是 Duolingo 最後真正解掉 lint 問題的那一步。個人在本機跑 Claude Code 本來就有這個條件，在 skill 或指示裡要求「開 PR 前必須本機綠燈」即可。
7. **送人看之前加一道 judge**：用一個獨立的 review prompt 或 subagent，只看 diff、只查固定清單（改到 production、刪改／停用測試、長等待、弱斷言），拒收就附理由。這一道是篩子，不是最後把關。

**不能直接用、或要改的部分**：

- **`git blame` 指派 reviewer、30 天冷卻**：靠「不要一直煩同一個人」成立；個人專案 reviewer 只有自己，冷卻改成「避免同一檔反覆產出被丟掉的 PR」就好。
- **覆蓋率當進度指標**：Duolingo 拿覆蓋率當主要成果，但覆蓋率不證明測試有用（見下方張力）。個人做法建議對補出來的測試抽樣跑 mutation testing，不要只看覆蓋率上升。
- **24 小時不停的排程與 Temporal**：本 vault 已記錄的運行模式偏向「使用者開 session、agent 在 session 內自主」，要不要掛排程是另一個決定；個人規模用 `gh` 加 shell script 或 Claude Code 的 loop 就能撐，不需要 durable workflow 引擎。

## 回查結果（2026-11-19）

| 主張 | 回查 | 結果 |
|---|---|---|
| 本地驗證兩批 17/8、40/19 | [部落格](https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/)表格列同樣數字（47%、48%），並記各批主要失敗類型 | **對得上** |
| 選檔「檔案類型加權 2.5 倍、大檔扣分」 | 部落格列出四項權重：檔案類型 2.5x、覆蓋率缺口 0.5x、檔案大小 -0.3x、模組優先度 0.5x | **對得上**；演講只講了一部分 |
| 「legacy 檔往下壓」 | 部落格的模組優先度寫「Feature and Legacy libraries score highest. Core libraries score lower.」 | **待釐清**：部落格的 Legacy 可能是模組名稱，不等於演講說的非 MVVM legacy 檔；兩者措辭方向相反，未見原文解釋 |
| user client 改用 protocol 並加 lint | 部落格寫 `UserClient` → `UserClientProtocol` 全庫遷移並加 linter rule | **對得上** |
| 過期就關 PR | 部落格寫「Stale (>14 days)」，演講寫約 3 週 | **對不上**：門檻在兩次發表間可能調過，以哪個為準不明 |
| merge conflict 處理 | 部落格補充：conflict 直接關、**不設冷卻**（從乾淨的 main 重產會成功）；stale 與修 5 次失敗才設 30 天冷卻 | 演講略過的細節 |
| 生命週期 workflow 執行頻率 | 部落格圖說寫 hourly，演講說每隔幾小時 | 小差異，可能調過 |
| 回補每輪選幾個檔 | 部落格：過濾已有開著的 PR、已有 `*Tests.swift`、冷卻中的檔後，每輪取前 5 個，約每天 20 個 PR | 演講未提 |
| lint 失敗率 30.6%、其中 62% 來自兩條 rule | 部落格（2026-06）寫最近一批失敗率 13.6%、多數是 SwiftLint、兩條 rule 占 62% | **部分對不上**：62% 一致，30.6% 與 13.6% 不同，可能是不同期間或口徑；引用時兩個數字都附來源 |
| 搬到 Mac runner | 部落格寫「即將升級到 Mac」；演講說已搬 | 兩次發表之間完成，**時序對得上** |
| agent 改 production code | 部落格記錄一起事故：CI 修復 agent 在測試 PR 改了 production 檔，當時「正在加 guardrail」 | **對得上**，且演講的第一層確定性規則就是這次事故後的結果 |
| LLM-as-judge | 部落格當時只寫「計畫加第二個 reviewer agent」；演講時已上線 | 時序對得上；**審查數「about,200」是逐字稿漏字**，可能是 1,200，未能從一手文字確認 |
| 成果數字 | 部落格（約 17 週）：250 個 PR、約 8.5 萬行、4,460 個測試函式、233 個 class，MVVM 9% → 30%，首次 CI 通過率 76%；演講（約 8 個月）：700+ PR、22.5 萬行、MVVM 9% → 59% | 兩次快照方向一致、可視為持續成長；**8 個月版本沒有獨立來源** |
| 「tripled coverage」 | 講者 2026-09 在 [WeAreDevelopers World Congress](https://www.wearedevelopers.com/videos/100523-how-ai-agents-tripled-our-test-coverage-on-a-1-8m-line-ios-codebase) 的場次標題寫「tripled our test coverage on a 1.8M-line iOS codebase」 | 1.8M 行與閱讀頁一致；「三倍」對應的是哪個覆蓋率口徑未說明 |
| cloud agent 平台 | [平台文章](https://blog.duolingo.com/production-ready-ai-agent-platform/)：agent 以 registry 定義（system prompt、MCP、要 clone 的 repo、輸出型別），由 `AgentWorkflow` 包裝執行；runtime 支援 Claude Agents SDK、Codex CLI，後加 OpenAI Agents SDK；從 Slack、內部網站、CLI、其他 Temporal workflow 都能觸發；label 觸發經 Nexus gateway | **對得上**；逐字稿的「Nepor」應是 Nexus |
| Temporal 防重複啟動 | [Temporal 官方文件](https://docs.temporal.io/workflow-execution/workflowid-runid)：同一 Workflow Id 同時只能有一個開著的 execution，並有 Reuse／Conflict Policy | **機制存在**；Duolingo 實際怎麼設 Workflow Id 未公開 |

平台文章另有一段演講沒講、但對「怎麼驗證 agent」很有用的內容：他們的 agent eval 會讓真的 agent 跑在 fixture repo 上，再用三類 grader 檢查——`structured_output`（結構化回應欄位）、`diff_assertions`（diff 必須包含／不得包含某些字串，例如不得出現 `pytest.mark.skip`，並限制最多改幾個檔）、`no_op_consistency`（回報「沒改」但 diff 有東西、或回報「修好了」但 diff 是空的都判失敗）。LLM-as-judge 只當選配，原文明說「deterministic graders are the foundation」。

## 證據強度與限制

- **所有覆蓋率、PR 數、行數、占比都是 Duolingo 自報**：單一公司、單一程式庫，沒有對照組，也沒有外部稽核。閱讀頁本身就提醒「演講沒有證明每一項變化都是 agent 造成的」——同期工程師自己寫的測試也變多了。
- **覆蓋率不等於測試品質**：演講沒有報告 mutation score、測試抓到幾個真 bug、或補出來的測試之後擋下多少 regression。22.5 萬行是產出量，不是效果。
- **LLM-as-judge 拒收 73 個**：沒有說被放行的 PR 裡漏網多少，也沒有說人工 review 再退件多少，無法算 judge 的精確率或召回率。
- **「每個 PR 都經人核准」**是流程宣稱；核准有多仔細沒有數據。部落格自己承認瓶頸已經變成 reviewer 頻寬。
- **Jev 分類器取代決策樹**只是思想實驗，沒有任何實作或數據。
- **勿引用**：「200,000,000 行測試」（逐字稿辨識錯誤，閱讀頁明確更正為 20 萬以上）；「LLM-as-judge 審了 200 個 PR」（逐字稿漏字，實際數字不明）；「10% of every strip line」的確切口徑（辨識不清）。

## 張力與互補

- **與 [[用測試約束-AI-產碼]] 有正面張力**：該頁的核心警告是 AI 寫的測試驗證的是「程式現在做了什麼」，不是「應該做什麼」。Duolingo 的回補正是替**已經 merge 的程式碼**事後補測試，最容易落入這種同義反覆——測試只是把現有行為（含 bug）釘住。他們擋的是作弊（改 production、刪測試、長等待），沒有擋「斷言太弱」或「把錯誤行為當規格」；判斷「應該做什麼」的唯一關卡是人類 reviewer。若要搬用，該頁第四節的 mutation testing 正好補這個洞。
- **為 [[AI-產碼加速下的-review-瓶頸]] 提供一個生產規模的案例**：部落格直說「產測試已經是簡單的部分，真正的瓶頸是 review」。Duolingo 的回應是讓 review 前的關卡變多（確定性規則、AI review、judge）、用 `git blame` 送到最有脈絡的人、退件後冷卻——是該頁「路線 B 用測試約束」與「路線 A AI code review」的組合。
- **與 [[Lauren-Tan-把糾正寫進程式庫]] 方向一致**：`UserClient` 改 protocol 加 lint rule、刪掉低訊號 lint rule、把禁止事項做成確定性 CI 檢查，都是「把糾正放進程式庫與確定性檢查，而不是多寫一句 prompt」；閱讀頁也總結「沒有任何一條散文指示承擔整個安全邊界」。本地驗證先跑兩批再上排程，也對應她的先內圈後外圈。
- **與 [[Matt-Pocock-的-PR-瓶頸解法]] 互補**：同樣是「自動檢查 → AI review → 人」三層，Duolingo 多了 PR 生命週期的狀態機（何時放棄、何時冷卻、何時改派），這是 Matt Pocock 那頁沒談的佇列管理面。
- **與 [[Uncle-Bob-的不讀碼約束閘門]] 立場相反**：Uncle Bob 主張不讀 agent 產碼、用測試與度量包圍它；Duolingo 雖然閘門很多，仍堅持每個 PR 由人核准後才 merge。
- **思想實驗碰到 [[Jev-與-System-One-模型]] 已記錄的限制**：該頁記錄 Jev 官方文件承認「state 被當資料、預設不視為惡意」，可被注入內容改變判斷，且沒人拿它對比 fine-tuned encoder。PR 狀態裡含 PR 描述、CI log、review 留言等 agent 或外人寫的文字，拿 Jev 取代決策樹前這條要先解；而現行手寫決策樹本來就是確定性的，換掉的收益（毫秒級）在每幾小時跑一次的批次流程裡也不明顯。
