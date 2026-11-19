---
title: Joey Wang agent 量放大後壞掉的周邊系統
description: Harvey 內部 agent 平台 Spectre 量放大後，壞掉的是 alert 觸發、叢集容量與 merge，附 follow-up loop 與限流做法
created: 2026-11-19
updated: 2026-11-19
source: https://www.ai.engineer/talks/ktbAVYsAxpk-agents-were-fine-everything-around-them-broke
published: 2026-11-10
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - automation
---

# Joey Wang agent 量放大後壞掉的周邊系統

來源：AI Engineer 演講〈The Agents Were Fine. Everything Around Them Broke.〉的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-Wang-Agents-Were-Fine-Everything-Around-Them-Broke]]（YouTube `ktbAVYsAxpk`，約 13 分鐘，2026-11-10 上傳）。回查來源見下方「回查結果」。

**一句話**：agent 本身是簡單的部分。量放大以後，壞掉的是 agent 周圍的東西：alert 觸發、叢集容量、repo checkout、merge queue。值得投資的是「寫完 code 之後」那一段 harness：顧 CI、排隊、限流、合併。

## 講者與立場

Joey Wang 是 Harvey（法律 AI 公司）的 engineering lead（[Background Agents Summit 講者頁](https://background-agents.com/summit/sessions/joey-wang/)），負責內部 cloud agent 平台 Spectre。Spectre 只給 Harvey 內部用，沒有對外販售，所以這場**不是在推銷可購買的產品**。不過 Harvey 的部落格把 Spectre 當成自家法律 agent 產品的試驗場（見回查結果），演講等於公司技術品牌的一部分。所有數字都是 Harvey 內部自報，沒有公開資料可以核對。他開場明說不談模型、eval 或排行榜，只談 harness。

## 演講脈絡（依時間序）

### 0. 開場：規模與定位（0:00–2:38）

- 演講前一個月：平台平均**每分鐘啟動超過一個 agent**，日夜都是；約 **460 人**用過；agent 累計寫了 **10,000 個 PR**。
- 用途超出寫 code：有人在 Slack 問資料問題拿到答案；行銷同事丟一個 prototype 和講稿，請它幫忙整理成產品影片的故事。他的結論：「harness 一旦存在，人們會帶來你沒規劃過的工作。」
- 他引用 4 月 Spectre 部落格的說法：「到某個時間點，harness 本身就成了產品。」
- **為什麼不用 Claude Code 或 Cursor 就好**：「我們不跟它們競爭，我們跑它們。」他個人的看法是，筆電上實際只能同時跑 **5–10 個** agent；超過就要上雲。但雲端的 agent 需要公司的 secret、真實 stack、alert 與 ticket、一套統一規則，以及足夠的容量讓沒有人被餓死。Spectre 就是這一層，**而壞掉的也正是這一層**。
- 預告三個故事：不再在「寫 code」上競爭、讓任何 agent 都能驅動平台、驅動之後哪裡壞掉。

### 1. 第一個故事：不跟 coding agent 比寫 code（2:38–5:19）

- **起點**：越來越多工程師改用 Cursor，問題都一樣：怎麼在 Cursor 拿到公司的 secret？怎麼對真實 stack 測試？若把這些接進 Cursor，下次大家換工具又要重做一遍。最後答案變成一句話：「叫 Cursor 去用 Spectre。」
- **設計原則**：每個人都有偏好的 agent，而且偏好一直在變，所以讓人自己選（Claude Code、Codex、Cursor 或自己寫）。session 可以在筆電上開始、推到雲端、再拉回來。Spectre 墊在所有 agent 底下。
- **凌晨兩點的例子**（完整流程）：
  1. alert 在凌晨兩點發到 Slack，agent 自動接手，沒有人下 prompt。
  2. agent 寫修正，啟動一份真實 stack 的副本，把**證據貼到 PR 上**。
  3. CI 失敗時，**follow-up loop** 讀失敗內容再推一版修正，此時所有人都還在睡。
  4. 早上 PR 進到**同一個 review 佇列**，不管是哪個 agent 寫的，都套用和其他 PR 一樣的規則。
  5. 等擁有者的**上班時間開始**才發提醒。
  6. 核准後，agent 可以自動合併。
- **最該先做的一段**：「如果只能做其中一個階段，就做 follow-up loop。」10 月初對所有人開啟；那個月合進 backend 的 agent PR，**每 5 個有 4 個**經過這個迴圈。他的說法是：這就是「會寫 code 的 agent」與「把事做完的 agent」的差別。
- **知識的落點：projects**。每個團隊都有一個人知道怎麼測那個難搞的服務、哪個 flag 絕對不要碰，這些知識只存在那個人的腦子和筆電裡。Spectre 用 projects 收容：人寫下重要的事，agent 寫下它學到的，團隊 pin 住自己信任的 skill，並留下誰跑了什麼的紀錄。在這個 project 裡工作的任何 agent 都看得到同一份內容。他的個人主張：**不管工程師挑哪個 agent，檢查與稽核軌跡都應該相同。**

### 2. 第二個故事：人能點的，agent 就能呼叫（5:19–7:38）

- **起點**：5 月時要用 Spectre，大家是開瀏覽器分頁或在 Slack tag 它；整個月**只有 1 個**任務來自終端機。
- **規則**：「人能點的，agent 就能呼叫。」開任務、開 follow-up loop、開 auto-merge、發佈頁面，全都做成 CLI。所以筆電上的 agent、已經在沙箱裡的 agent、CI job 都能呼叫。
- **結果**：到 10 月，CLI 每月啟動約 **6,500 個任務**，網頁版用量沒有縮，只是其他用法長在它旁邊。出現一種新使用者：一個月開幾百個任務、從不打開 app。一次和 agent 的對話就能啟動一整批工作。（逐字稿另有一句疑似「從終端機啟動的任務 merge 比較多」，辨識錯誤嚴重，閱讀頁也沒收，**不引用**。）
- **兩個方向的用法**（他自己 10 月的例子）：
  - **往外派工**：開一個 coding session 當協調者，把一張大 ticket 切成 10 個 milestone，自己留 1 個，其餘交給 Spectre，變成幾百個任務，每個任務有自己的沙箱做端到端驗證。
  - **把決策收回來**：另一個 agent 盯著 Spectre，找出卡住工作的提問，列出問題、草擬他的回覆，他點頭後再送回去。他不必逐個任務去看它們需要什麼。
- **小插曲：checkout 才是最慢的一步**。量測任務時間花在哪裡，最慢的不是模型思考，而是 git checkout：checkout 公司所有 repo 平均超過一分鐘。修法：每台機器都保留每個 repo 的副本，讓每個任務**借用本機副本**；同一台機器上的一波任務可以重用已經有的 repo。

### 3. 第三個故事之一：一個 bug 開了約 900 個調查（7:38–8:25）

- 8 月中，一個版本帶了 bug，這個 bug 讓 alert **每個 workspace 各發一次**，數百則 alert 落在同一個 Slack 頻道。有人設了 workflow，每則 alert 都 tag agent，每個 tag 都開一個任務。
- 平常這個 workflow 一天約開 **50 個任務**；那天約 **4 小時內開了約 900 個**，全部在追同一個 bug，直到叢集一個 node 都不剩。（投影片說明：27 個 node 全滿、超過 1,000 次 pod 排程失敗。）
- **修法「幾乎很無聊」**：重複的 alert 改成**併入已經開著的調查**，同一個調查可以收集多個 workspace 的回報。原本「又一個 workspace 回報」等於「再開一個 worker」的指令，改完後變成「把回報送到既有工作」。

### 4. 第三個故事之二：一台筆電塞爆叢集與公平啟動佇列（8:25–10:06）

- 兩個月後（10 月）又發生一次，這次不是 bot。一位工程師做了團隊一直鼓勵的事：把工作交給 Spectre。一台筆電約 **3 小時送出約 950 個 CLI 任務**，叢集塞滿，所有人的工作都排在這台筆電後面。他說：「這不是使用者的問題，是我們的問題。」
- **4 天後上線公平啟動佇列**（fair launch queue）：
  - 送出任務就拿到一個**看得見的排隊位置**。
  - dispatcher 在叢集有空位時才啟動任務，**坐在鍵盤前等的人優先**。
  - 每個人有公平份額，叢集閒時可以**借用更多**。大批工作可以用閒置機器，但下一個空位給誰，仍由 dispatcher 決定。
  - 投影片說明的參數：保留 **40 個互動式名額**；每人同時 **25 個**任務，容量允許時可到 **50 個**。
- **壓測與成效**：逐字稿說 300 個任務的突發負載下，延遲從「將近 2 秒」降到「70 毫秒」；投影片說明則寫同時執行的任務從 240 降到 20、p95 worker heartbeat 延遲從 5.3 秒降到 19 毫秒。兩者對不上，閱讀頁正文也沒有收這組數字，見「勿引用」。
- **完成率**：8 月拿來比較的那個忙碌日，約**每 10 個任務有 1 個沒跑完**；11 月 4 日處理量是那天的兩倍以上，完成比例更高。他自己說明：同時改了好幾件事，**說不出哪個修正貢獻最大**。

### 5. 新瓶頸：merge queue（10:06–10:45）

- 10 月底，Harvey 的 dev platform 團隊拉警報：全公司 PR 量一個月內漲約 **60%**；merge 一個改動從 **15–30 分鐘**變成**超過 1 小時**，merge queue 一再被迫關掉。
- 關掉 queue 的退路是：PR rebase 到 `main`、重跑 CI、綠燈就合。所有 PR 都依賴這個共同起點，`main` 壞了，所有人的 CI 跟著壞。
- 公平啟動佇列解決的是「開始工作」的空間；完成的改動怎麼順利合進去，**他們還沒解決**。

### 6. 沒人看的時候誰在開工作：自動化（10:45–12:03）

- Spectre 成長最快的工作來源是**自動化**：排程或事件喚醒 agent，去分類 alert、讀 PR、寫文章。演講前一個月約 **110 人**有自動化在跑。
- 第一天就給的護欄：**連續失敗 5 次就自動停用**；擁有者可以設**預算**或**到期日**。理由是沒人看時，agent 一樣能開出幾千個任務。
- 他接下來想追的問題（自承還沒有答案）：
  - 每個 Slack 頻道都有一個常駐 agent，跟著對話，自己判斷何時開工？
  - 每個 PR 在人看之前就附上「它確實可行」的證明？目前**每 20 個 merge 只有 1 個**附這種證明。
  - agent 不停開 PR 時，要怎麼 merge？「6 個月後再問我壞了什麼。」

### 7. 結語：三件會再做一次的事（12:03–12:53）

1. **擁有寫完 code 之後發生的事**（follow-up loop、review 佇列、合併）。
2. **每個動作都做成 agent 能呼叫的**。
3. **在人、agent 或 alert 發現自己能開多少工作之前，先設上限。**

最後的個人觀點：工程師用哪個 agent 寫 code 都可以；真正留下來的工作，是執行它、檢查它、把它合進去的 harness。

## 回查結果（2026-11-19）

| 主張 | 結果 | 來源 |
|---|---|---|
| 4 月寫過 Spectre，說「harness 會變成產品」 | **成立**。〈Building Spectre〉原文有「At some point the harness becomes the product」；文中把 durable run、短命 worker、沙箱邊界、harness、協作介面、排程列為核心元件，排程工作與互動工作共用同一套 runtime | [Harvey 部落格：Building Spectre](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) |
| Spectre 是內部平台、不和 coding agent 競爭 | **成立**。部落格定位為「internal collaborative cloud agent platform」，從 Slack、web 或自動化接請求，在隔離沙箱執行，回傳摘要、diff、PR。部落格還寫了演講沒講的動機：本機 agent 繼承整台工程師電腦的權限（瀏覽器 session、SSH agent、本機檔案），企業難以回答「這次執行能碰到什麼」 | 同上 |
| Harvey 另有對外的 cloud agent 基礎設施 | **成立，但和 Spectre 不同件**。2026-06 的部落格說明對外法律 agent 為何自建 runtime：多模型（利益衝突）、zero data retention、成本。Spectre 部落格明說兩邊架構平行發展、彼此影響 | [Harvey 部落格：Why we built our own cloud agent infrastructure](https://www.harvey.ai/blog/why-we-built-our-own-cloud-agent-infrastructure) |
| 講者身分 | **成立**：2026-05 Background Agents Summit 講者頁寫 Engineering Lead, Harvey，該場談 Slack thread 當協作面、排程 agent | [Background Agents Summit](https://background-agents.com/summit/sessions/joey-wang/) |
| 每台機器保留 repo 副本、任務借用 | **做法可行，但 Harvey 實際機制未公開**。git 原生的 `git clone --reference`（或 `--reference-if-able`）會設定 `.git/objects/info/alternates`，從本機既有 repo 取 object，減少網路與儲存；`git worktree` 也能從同一個 repo 分出多個工作目錄。Harvey 用哪一種沒講 | 本機 `git clone` 說明文件 |
| merge queue 的運作 | **背景補充**。GitHub merge queue 為每個排隊項建暫存分支，疊在目標分支與前面的 PR 上一起跑 CI，失敗就移出再重建後面的分支；可調 build concurrency 與 merge group 大小（各 1–100）。插隊會讓所有進行中的項目全部重建。PR 量暴增時，這種「每個都要疊前面重跑」的設計正是演講說的瓶頸所在 | [GitHub Docs：Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) |
| 個人工具裡有沒有 follow-up loop | **Claude Code 有對應功能**：Auto-fix 會訂閱 PR 的 GitHub 事件，CI 失敗或有 review comment 時調查並在有把握時推修正；模稜兩可的意見會先問人。需要安裝 Claude GitHub App；終端機在 PR 分支跑 `/autofix-pr` 即可開啟。限制：base 分支前進造成的 merge conflict 沒有 webhook，auto-fix 不會自己處理 | [Claude Code 文件：Auto-fix pull requests](https://code.claude.com/docs/en/claude-code-on-the-web) |
| session 在筆電與雲端之間來回 | **Claude Code 只做到一半**：CLI 的交接是單向的，可以用 `--teleport` 把雲端 session 拉回終端機，但不能把現有終端機 session 推上雲（`--cloud` 是開新 session；Desktop app 可從 Open in 選單送上雲）。Spectre 的雙向交接是它自己的平台能力 | 同上 |
| 重複 alert 併入既有調查 | **一般化工具可對照**：GitHub Actions 的 `concurrency` group 同一時間只跑一個；預設 `queue: single` 只保留一個 pending、新的取代舊的，`queue: max` 最多排 100 個。這是「同一把 key 不重複開工」的現成實作，但它是丟棄或排隊，不是「把新回報附加到舊調查」 | [GitHub Docs：Control workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency) |

演講中所有使用量數字（460 人、10,000 PR、6,500 任務／月、110 人有自動化、4/5、1/20、+60%）都**沒有公開資料可核對**，只能當 Harvey 自報。

## 可以搬到個人 Claude Code／Codex 流程的做法

規模不同：個人沒有共用叢集，公平佇列、dispatcher 這一整段**不需要**。能搬的是「寫完 code 之後」的那些環節，以及上限思維。

1. **先做 follow-up loop，而不是多開 agent**。在 GitHub repo 裝 Claude GitHub App，agent 開完 PR 後在該分支跑 `/autofix-pr`，讓 CI 失敗與 review 意見自動回到 agent 手上。前提是 CI 真的會擋你在意的問題，否則迴圈只是在把紅燈修成綠燈。merge conflict 它不會自己處理，要另外叫它 rebase。Codex 是否有同等的自動跟 PR 功能，本頁未查證，不確定。
2. **自動合併只開給有 required checks 的 repo**。演講的流程是「核准後才自動合」，不是跳過 review。沒設 required status checks 的 repo，auto-merge 等於沒有閘門。
3. **把常用動作做成 CLI 或腳本**。只能在 UI 點的事（開 PR、開 auto-fix、發佈），agent 就無法替你串起來。個人層次的對應是：用 `gh`、`claude -p`、`claude --cloud "<任務>"` 這類可程式化入口，讓一個協調 session 能批次派工。
4. **派工前先設上限**。自己寫批次派工腳本時，用 `xargs -P N` 或類似機制限制同時數量；N 從你能審的量決定，而不是從機器跑得動的量決定（盯著的通常只有 2–4 個，見下方張力）。
5. **排程自動化從第一天就加護欄**。自己的 cron／排程 agent：記錄連續失敗次數，達到門檻（Harvey 用 5 次）就停用並通知；另外設到期日，避免被遺忘的排程一直燒額度。
6. **事件觸發要去重**。如果用 alert、issue 或 webhook 觸發 agent，先用穩定的 key（例如錯誤指紋、issue 編號）檢查是否已有進行中的任務，有就把新事件附加上去，不要再開一個。GitHub Actions 的 `concurrency` group 可以做到「同 key 只跑一個」，但附加到既有調查要自己寫。
7. **大量平行時先看 checkout**。同一個 repo 開很多份工作目錄，用 `git worktree` 或 `git clone --reference` 共用 object，不要每次完整 clone。
8. **讓 PR 附上能運作的證據**。Harvey 自己也只做到每 20 個 merge 有 1 個；個人可以在 PR 模板或 agent 指示裡要求附測試輸出、截圖或重現步驟。

不適合直接搬的：
- **公平啟動佇列與互動優先**：解決的是多人共用叢集，個人沒有這個問題。
- **跨 agent 共用的 projects 知識**：概念上類似把團隊知識放進 repo 的指示檔與 skill，但 Spectre 的版本是平台功能（含稽核紀錄），沒有公開實作可抄。
- **每個 Slack 頻道一個常駐 agent**：講者自己也還沒做出來。

## 證據強度與限制

| 主張 | 強度 |
|---|---|
| 每分鐘超過一個 agent、約 460 人、10,000 PR | Harvey 自報，無公開資料 |
| follow-up loop 開啟當月，合進 backend 的 agent PR 每 5 個有 4 個經過它 | 自報；只說明「經過」，沒說迴圈修好了多少，也沒有對照組 |
| CLI 每月約 6,500 任務，網頁用量沒縮 | 自報 |
| 一個 alert bug 4 小時開約 900 任務（平常每天約 50） | 自報的單一事件，事件經過具體 |
| 一台筆電 3 小時約 950 任務塞爆叢集，4 天後上公平佇列 | 自報的單一事件 |
| 完成率改善（約 1/10 未完成 → 更高完成比例） | 自報；講者自己承認同時改了多處，**無法歸因** |
| PR 量月增約 60%、merge 從 15–30 分鐘拉長到超過 1 小時 | 自報；PR 增加不全是 agent 造成的，沒有拆分 |
| 自動化連續失敗 5 次停用 | 自報的設計選擇，不是實驗得出的最佳值 |
| 每 20 個 merge 只有 1 個附證明 | 自報；「證明」的定義沒交代 |
| 筆電實際只能跑 5–10 個 agent | 講者明說是個人看法 |

## 勿引用（2026-11-19 核對）

- **公平佇列的壓測數字**：逐字稿說延遲「將近 2 秒降到 70 毫秒」；投影片說明寫 p95 worker heartbeat「5.3 秒降到 19 毫秒」、同時任務「240 降到 20」。兩組數字對不上，量的也可能不是同一個指標，閱讀頁正文刻意沒收。要引用請回看影片 9:28 前後的投影片原圖。
- **「從終端機啟動的任務 merge 比較多」**：逐字稿辨識錯誤（「merging mops」），閱讀頁未收。
- **把「4/5 PR 經過 follow-up loop」解讀成「follow-up loop 讓 80% PR 成功合併」**：原句只說合進去的 PR 中有 4/5 經過迴圈，不是成功率。

## 張力與互補

- **與 merge 瓶頸的綜合頁一致**：[[AI-Engineer-2026-演講精華-AI-工作流程]] 第 1 節把 Harvey 的 +60% PR 與 merge 變慢，和其他講者（rebase 連鎖、效率算到 merge 為止）並列為同一現象。本頁補上它的前因後果：先是啟動端的容量問題被公平佇列解掉，瓶頸才移到 merge 端，而且 Harvey 到演講時還沒解。
- **與 [[平行-agent-產出的合併與-review]] 互補**：那頁處理多個 agent 產出之間的衝突與合併順序（含 stacked PR、merge queue 工具）；Harvey 的問題是量本身，即使沒有衝突，每個 PR 都要疊在 `main` 上重跑 CI，queue 也撐不住。那頁的工具（stack-aware merge queue 批次驗證）是可能的解法方向，但 Harvey 沒有說他們試過哪些。
- **與 [[Claude-Code-放手運行的安全與驗證]] 同一條路線**：Lydia Hallie 也把 CI auto-fix、auto-merge 放在人退出迴圈後的關鍵位置，Wang 則用 4/5 的數字說明 follow-up loop 是最值得先做的一段。差別是 Lydia 談單人用 Claude Code 的設定，Wang 談多人共用平台；兩者都是自報經驗。
- **「筆電 5–10 個」與人類監督上限的關係**：[[多-agent-的人類監督與介入]] 整理的經驗值是人能主動盯的約 2–4 個、背景任務另計。Wang 的 5–10 是機器與環境的限制，不是注意力限制；他的解法是把多出來的工作推上雲、並用另一個 agent 收集待答問題回來給人，也就是把「盯」這件事交給 agent。這不代表人能審的量跟著變大，merge 端的瓶頸正好說明了這點。
- **與 [[Lauren-Tan-把糾正寫進程式庫]] 的落點不同**：Tan 主張先穩內圈（程式庫與確定性檢查）再自動化外圈；Wang 談的幾乎全是外圈（觸發、佇列、限流、合併）。Wang 的「每 20 個 merge 只有 1 個附證明」正是 Tan 會警告的狀態：外圈已經放大，驗證層還沒跟上。兩場可以互相補足，但 Wang 沒有談內圈品質。
- **「harness 才是產品」與 [[Agent-Harness-Engineering-框架綜述]]**：那頁把 harness 定義為模型外圍的基礎設施；Wang 的版本更往外延伸到組織層（排隊公平性、merge、稽核），是「多人共用 harness」才會遇到的問題。
