---
title: Walden Yan 軟體工廠與給 agent 長期 job
description: Cognition 的 Walden Yan 談內部軟體工廠：可本地重建的測試環境、證據式交付、從任務改給 agent 可量測的長期 job，附數字回查
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/walden-yan
published: 2026-11-13
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - testing
---

# Walden Yan 軟體工廠與給 agent 長期 job

來源：AI Engineer CODE 2026 演講〈40x More Merged PRs With 2.7x the Engineers〉（閱讀頁場次名為 A New Age of Software Engineering）的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-Yan-40x-More-Merged-PRs]]。剪輯單場版 YouTube ID `U92J5mCDLMc`，約 14 分鐘。數字另以 Cognition 部落格、Devin 文件與 CoreWeave 新聞稿回查（2026-11-19）。

**一句話**：買了 coding agent 不會自動變快。要先把整套服務改成 agent 能在一台乾淨 VM 裡自己跑、自己測、自己交出影片證據，再把工作從「一次性任務」改成「有指標、會持續回報的長期 job」，人只處理升級上來的判斷。

## 講者與立場

Walden Yan 是 Cognition 共同創辦人兼產品長，Cognition 的產品是 Devin。他開場說要「從產品抽離、講內部工程團隊怎麼做」，但整場的工具、流程、案例都是 Devin，而且他提到這套做法「也在幫很多大型組織導入」。演講後幾天（2026-11-17）Cognition 發表 [Devin Bots](https://devin.ai/blog/introducing-devin-bots)，標題就是「from tasks to outcomes」，演講裡的 Android 與版面位移案例都是該文的範例。所以這場演講實際上是新產品上市前的內部案例展示，**數字全部是廠商自報**。

他也是 Cognition 2025 年〈Don't Build Multi-Agents〉的作者，這和本場「每個 pod 配一群 agent」的說法有張力，見文末。

## 演講脈絡（依順序）

### 1. 開場數字：merged PR 40 倍、工程師 2.7 倍

- 投影片是約 12 個月的 merged PR 走勢：同期 merged PR 數成長 40 倍，工程師人數成長 2.7 倍。
- 他據此說每位工程師的生產力「超過 10 倍」，並說這些 PR 品質「一樣高，甚至更高」。
- 40 ÷ 2.7 約 14.8，算術上對得上「超過 10 倍」，但這是把 PR 數當成生產力。閱讀頁自己也註明：PR 數量不是完整的生產力指標，品質不變是公司自評。

### 2. 軟體工廠的基本定義：預設自駕，人只接升級

- 「預設一切都應該 self-driving」：有些 PR 從客戶 bug 回報、修正、合併到上線後監控與維護，全程沒有人參與。
- 需要人判斷時走 escalation，但預設整個開發流程都由 Devin 端到端跑。

### 3. 工程師角色改變：小 pod、垂直責任

- 他說大約今年 3 月和工程團隊談過：如果你的工作只是從 Linear 看板拿 ticket 丟給 agent 實作，在 AI 時代不會有好下場，因為「凡是能描述清楚、能實作的東西，都可以直接丟給 Devin」。
- 做法是把大團隊拆成 2–3 人的小 pod。每個 pod 除了配一群 agent，還要負起工程以外的事：聽客戶 bug 回報、做 QA、做產品管理。每位工程師管自己的 Linear 看板，再把項目丟給 agent 實作。
- 閱讀頁的解讀：agent 擴大的是實作產能，不提供對客戶的理解；理解客戶仍是 pod 的責任。

### 4. 在 Slack 完成整個開發循環，用影片當證據

- 客戶在 Slack 傳來一段重現 bug 的影片。他們直接轉進內部頻道、tag Devin 叫它修。
- Devin 開出 PR，同時回傳一段修好後的影片當證明。工程師把影片轉給客戶，大多時候不用開 IDE，甚至不用開 GitHub。
- 他說的終點是：整個開發循環都不必開 IDE，也不必開任何 coding agent 介面。
- 閱讀頁的重點補充：流程變短，是因為每次交接都帶著證據（失敗的影片、修好的影片），不只是打字變快。

### 5. 最難的部分：讓 agent 能在乾淨環境自己測

他強調「不是買一個 coding agent 就好，你得改變建構方式」。

| 項目 | 以前 | 現在 |
|---|---|---|
| 測試對象 | 雲端 staging 環境、staging 資料庫、live 服務，工程師手動點一遍流程 | 每個服務都能用 Docker Compose 在本地跑起來 |
| 第三方服務 | 直接連 | 每一個都有可在本地跑的 mock 版本 |
| 執行位置 | 分散 | 全部塞進同一台 VM，每個 Devin 都有一台；測改動完全不碰 live 服務 |
| 環境新鮮度 | — | **每小時**拉最新程式碼、從零重建整個 VM snapshot；建置失敗時由 Devin 第一線修 |
| 每次開工 | — | 從 Slack 叫起的 agent 都拿到一台新機器、最新版程式碼 |

- **測試 skill 由 agent 自己維護**：agent 要學會怎麼測你的程式庫。程式庫會變，測法也會變；Devin 自己寫「怎麼測這個程式庫」的 skill，並在程式變動後持續更新。閱讀頁的說法是：只有乾淨機器不夠，指示還描述著上個月的 UI 就沒用。
- **不用筆電**：已經有幾位工程師改用 iPad 開發。他另外主張這樣更安全：近期很多入侵來自開發者機器上外洩的金鑰，環境全在受控的雲端 VM 比較好。
- **複雜互動也要可測**：開發 Devin 加入 Zoom 語音的功能時，測試會在同一台 VM 裡開多個帳號、加入同一場通話、互傳語音訊息，確認功能正常。他的意思是只要肯推，連多人情境都能讓 agent 自己測。

### 6. 工廠自己改善自己：分析執行紀錄

- 雲端 agent 的每一行程式、每個 PR、每個決策都有紀錄，可以再跑 agent 做資料分析：哪裡浪費時間、哪裡浪費 token、什麼可以寫成腳本、該加什麼測試。
- 他們有一個頻道，Devin 每天貼改進點子，例如「改 node 的設定可以讓 CI 少一分鐘」「改這個 lint 腳本，可以在 AI code review 之前多抓 20% 這類 bug」。
- 閱讀頁把這說成第二個回饋迴路：一個修客戶的問題，另一個問「為什麼修這類問題要這麼多步」。沒有後者，組織會把同樣昂貴的調查重跑幾百次，把忙碌當進展。

### 7. 從給任務到給 job

他認為下一步是從「給 agent 任務」轉成「給 agent 工作職責（job）」，「要開始把它當同事」。

- **p99 latency 範例**：你只說「我想改善 p99 latency」，由 agent 自己：加 telemetry 找出目前的 p99、設 alert、拆出所有要做的任務、建 Datadog alert、在 Slack 發週報、每天推送進度到你手機。
- 「我們大多時候甚至不希望你在 prompt agent，而是給它能長期朝著走的目標。」
- **把看似不可量測的東西量化**：點擊延遲；用元素 bounding box 的變化量化版面位移（layout shift）；onboarding 留存率。能濃縮成一個數字的工作，就讓 agent 24/7 優化那個數字。
- 閱讀頁的補充：「讓它更快」不是能持續評估的控制訊號；要有量測過的目標、重現退步的方法、約定的回報節奏。

### 8. 案例一：新 GPU 的推論吞吐

- 他說 Cognition 是 NVIDIA Vera Rubin 的首批使用者，拿到時沒有現成 kernel，推論堆疊得從頭建。
- 做法是告訴 agent「我們在意這批 GPU 上的吞吐（TPM），去推到極限」，並固定撥一組 GPU 給它。約一週內 agent 自己找策略、測試，最後由人類工程師核准；大約發現了 8、9 種有效做法。
- 他說吞吐從「比 GB300 還差」推到「明顯優於 GB300」。

### 9. 案例二：Android 版本與 iOS 保持一致

- 團隊小，沒人力做 Android。一位工程師（逐字稿作 Sam Yoke，Devin Bots 文作 Samyok）提議：既然 iOS 有團隊在做，就拿它當藍圖，叫 Devin 端到端維持 Android 與 iOS 一致。
- 不是開一個 session 了事，而是設常駐 hook 監看 iOS 程式庫的變動、聽 Slack 的使用者回饋頻道、持續改進、做每個細節的 live QA。
- 他說：44 天後有了一個可用的 app，即將推出；多數天沒有任何人類訊息，那些天每天合併 40–50 個 PR；對著 iOS 逐像素做 live QA；只在一天結束時把最重要的決定升級給人；工程師多半只在 Slack 看它傳回的錄影。他強調「這不是 slop app」。

### 10. 結語

「把 agent 的迴路設好，就能做到很驚人的事。」他認為多數團隊受限於野心，「是時候野心大一點了」。

## 可以搬到個人 Claude Code／Codex 工作流程的做法

以下是個人規模、一人一 repo 能照做的版本，順序照依賴關係排。

1. **一條指令起整套服務，且不碰外部**：把專案依賴的服務寫進 `docker compose`，第三方 API 換成本地 mock，目標是 `docker compose up` 加一條 seed 指令就能完整跑起來、測到端到端。資料庫隔離的做法見 [[E2E-測試的資料庫隔離]]。做不到的那個外部服務，就是 agent 無法自己驗證的區域，要在指示檔裡明說。
2. **在 repo 裡放一個「怎麼驗證」的 skill，並規定改流程就要改它**：內容寫怎麼起服務、怎麼登入、主要流程怎麼點、證據存哪。在指示檔加一條：改到使用者流程的 PR，同一個 PR 要更新這份 skill。這等於 Yan 的「agent 自己維護測試 skill」，也和 [[Lauren-Tan-把糾正寫進程式庫]] 的驗證 skill、feature map 同一路。
3. **交付附證據**：UI 改動要求 agent 用 Playwright 這類工具錄影或截圖，放進 PR 說明；先看預期行為再看影片。純後端改動附對最終提交跑的測試指令與退出碼。
4. **讓環境定期從零重建**：個人沒有每小時重建的 VM 池，可用 CI 在預設分支上排程跑「從零起服務＋跑 smoke test」。失敗時再開 session 叫 agent 修。用 Devin 的話，產品本身就有 snapshot 定期重建與「每次 push 到預設分支就建置」的選項（見回查）。
5. **定期回看執行紀錄找浪費**：每隔一段時間讓 agent 讀近期的 CI 時間、失敗紀錄和 session 紀錄，只產出「可以變成腳本或 lint 的重複動作」清單，由你挑要做哪幾條。這和 [[Matt-Pocock-的-PR-瓶頸解法]] 的 `retro` 是同一件事。
6. **把任務改寫成 job 檔**：對真的能量化的目標（測試時間、bundle 大小、某 API 的 p99），寫一份目標檔：指標與量測指令、目前基準值、目標值、每輪最多改什麼、何時停、何時要找人。目標檔的寫法見 [[長跑-Agent-的目標定義與計畫工具]]。

**不能直接搬的部分與原因**：

- **小 pod 重組**是團隊組織問題，一人開發者沒有對應物。
- **24/7 常駐 job** 需要長駐的雲端 agent 與排程，加上預算。個人環境無人值守前，要先補權限、沙箱與停止條件，見 [[Claude-Code-放手運行的安全與驗證]]。
- **每天 40–50 個 PR** 的規模，前提是 2,800 多個截圖測試這類密度的自動驗證（見回查）。沒有這層就照抄節奏，只會把 review 壓力推給自己。
- **專用 GPU 跑一週的推論優化**屬於 Cognition 的特殊資源，不是通用做法。

## 回查結果（2026-11-19）

| 演講說法 | 回查結果 | 依據 |
|---|---|---|
| merged PR 一年 40 倍 | **無法核對**：沒有公開基準值。旁證是 2026-02 的文章說前一週合併 659 個 Devin PR（2025 年最好的一週是 154），2026-11 的 Bots 文說 Cognition 每週合併超過 2,000 個 PR，方向一致 | [How Cognition Uses Devin to Build Devin](https://cognition.com/blog/how-cognition-uses-devin-to-build-devin)、[Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) |
| Android 44 天做出可用 app | **對得上**：Bots 文說 Android Bot 於 2026-09-28 建立，44 天後合併 1,134 個 PR、約 34 萬行 Kotlin、2,841 個截圖測試、關閉 1,217 張 ticket，已在 Google Play 開放測試 | Bots 文 |
| 多數天沒有任何人類訊息 | **說過頭**：Bots 文是 44 天共 183 則訊息，其中 22 天零訊息，剛好一半，不是多數 | Bots 文 |
| 那些天每天合併 40–50 個 PR | **只能當高峰值**：1,134 ÷ 44 平均每天約 26 個 | Bots 文，自行換算 |
| 量化版面位移 | **對得上**：Bots 文的 Layout Bot 每 3 小時跑一次版面檢查，三週合併 159 個 PR、lag 降 70% | Bots 文 |
| Vera Rubin 首批使用者 | **對得上**：CoreWeave 說 Cognition 是第一個在 Vera Rubin NVL72 跑生產負載的客戶，2026-09 初建置 | [CoreWeave 新聞稿](https://coreweave.com/news/coreweave-delivers-nvidia-vera-rubin-nvl72-performance-at-production-scale-starting-with-cognition)（2026-09-30） |
| 從比 GB300 差推到明顯優於 GB300，靠 agent 找到 8–9 種做法 | **公開來源沒有這個說法**：新聞稿的數字是 SWE-2 推論總 token 吞吐**對 GB200 NVL72** 最高 4.8 倍、RL 輸出吞吐 3.8 倍，沒提 GB300，也沒提 agent 參與優化 | 同上 |
| VM snapshot 每小時重建 | **是內部做法**：Devin 產品文件寫的是存檔 blueprint 時自動建置、約每 24 小時定期重建，可選「每次 commit 到預設分支就建置」；每個 session 都從 snapshot 的新複本開機，結束即丟棄；測試指令放 blueprint 的 `knowledge` 段，長篇慣例改用 Skills 功能 | [Devin environment blueprints](https://docs.devin.ai/onboard-devin/environment/blueprints) |
| Devin 加入 Zoom 語音並用多帳號測試 | **查不到公開功能頁**：Devin 文件只有和 Devin 本身對話的 voice mode | 搜尋 docs.devin.ai，未找到 |

## 證據強度與限制

- **全部是 Cognition 自報**，沒有對照組，沒有外部量測。PR 數是產出量，不是價值或品質；品質「一樣或更好」是公司自評，沒有給 revert 率或事故率。
- **PR 粒度可能改變**：agent 傾向開小 PR，PR 數成長不等於工作量等比成長。演講沒有交代 PR 的平均大小。
- **單一公司、單一產品**：Cognition 自己就是 agent 公司，工程師全員熟悉 Devin，推論成本對他們是自家成本，外部團隊的條件不同。
- **利益衝突**：演講是 Devin Bots 上市前的展示，案例挑的是成功的。
- 獨立評測的落差可參考 [[AI-自主工作流的實證檢驗]] 記錄的 Answer.AI 實測（20 項任務成功 3 項）；那是較早版本的 Devin，只能說明廠商宣稱與獨立評測曾有大落差，不能直接推翻本場數字。

## 與既有頁的關係與張力

- **和 Lauren Tan 互補**：[[Lauren-Tan-把糾正寫進程式庫]] 主張先穩內圈（程式庫、lint、驗證）再自動化外圈；Yan 講的幾乎都是外圈（環境、Slack 交付、長期 job），內圈只帶過「agent 自己維護測試 skill」。兩人在「review 縮成看證據」上一致。照 Tan 的順序，Yan 的做法應排在內圈穩定之後。
- **和自己的舊主張有張力**：[[Context-優先與多-agent-的適用邊界]] 記錄 Yan 2025 年主張單執行緒 agent，後來修正成「寫入保持單執行緒、額外 agent 只給建議」。本場的「pod 配一群 agent」和 Devin Bots「一個 Bot 帶多個 Devin 平行做事、各自開 PR」看起來是多個寫入者並行。可能的解讀是每個子 session 寫的是不重疊的 PR，由 Bot 收斂決策；但演講沒有說明怎麼避免衝突，這點是推論，未查證。
- **和 DORA 的觀測方向相反**：[[AI-產碼加速下的-review-瓶頸]] 記錄 DORA 大樣本觀察到 AI 採用同時關聯 throughput 上升與 instability 上升。Yan 說品質不變或更好，但沒給 instability 類指標，兩者無法直接比較。
- **長期 job 的寫法**：Yan 只給方向（指標、alert、週報），沒給目標檔格式；[[長跑-Agent-的目標定義與計畫工具]] 補的是驗收判準與停止條件怎麼寫，且提醒這些機制都沒有效果實證。
- **同屆的反面聲音**：[[AI-Engineer-2026-演講精華-AI-工作流程]] 記錄 Willison 認為能力越強工作越累、持續追求目標本身有風險，Almeida 認為示範表現好不代表適合無人值守，都和 Yan 的方向相反。
- **iPad 比較安全的說法**：方向和 [[Claude-Code-放手運行的安全與驗證]] 一致（雲端環境不放本機金鑰），但該頁也記錄雲端不是零風險：push、connector 和 network secret 都還會留下後果。

## 勿引用

- 「Android 案例多數天零人類訊息」：Bots 文的數字是 44 天中 22 天零訊息，引用時改用原始數字（183 則訊息、22 天零訊息）。
- 「每天合併 40–50 個 PR」不能當平均值，平均約每天 26 個。
- 「Vera Rubin 吞吐從不如 GB300 到明顯優於 GB300」：公開來源只有對 GB200 的 4.8 倍，且沒有提到 agent；只能當講者口述。
