---
title: Ryan Carson 一個 manager session 帶 20 個 builder
description: Carson 讓不寫碼的 manager session 經排程巡視帶約 20 個 builder，影片驗收與錄影招募，附 Devin 回查
created: 2026-11-19
updated: 2026-11-25
source: https://ai.engineer/talks/BTtyguoPvBU-one-founder-manages-20-ai-coding-agents
published: 2026-11-09
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - automation
---

# Ryan Carson 一個 manager session 帶 20 個 builder

來源：AI Engineer 演講〈How One Founder Manages 20 AI Coding Agents at Once〉的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-Carson-One-Founder-Manages-20-Agents]]（YouTube `BTtyguoPvBU`，約 15 分鐘，2026-11-09 上傳）。本頁按逐字稿順序整理；閱讀頁是主辦方改寫版，兩者有出入處會標明。回查日 2026-11-19。

**一句話**：管 agent 跟管人一樣，所以讓一個**不寫程式的 manager session** 從 ticket 看板派工給約 20 個 builder session，人只跟 manager 講話（多半用語音）；用**程式排程**保證 manager 每 15 分鐘巡一次所有子 session，review 最多 3 輪就往上升級，最後由人親自看每個 PR 的錄影決定能不能 ship。招募也照同一個邏輯：先看候選人操作 agent 的錄影，最後才通電話。

**標題和內容的落差**：題目講「一個 founder 管 20 個 agent」，實際約 10 分鐘講管理架構、4 分鐘講招募。開場說會有 live demo，但逐字稿裡沒有，他提早 3 分鐘結束。閱讀頁把整場改寫成不提任何產品名的版本（「built-in reviewer」「built-in testing tool」），逐字稿則明說全部建在 **Devin** 上。

## 講者與立場

- Ryan Carson，[Untangle](https://untangle.us/) 創辦人兼 CEO。演講自述：做過四家公司並賣掉、上一家（Treehouse）擴到約 110 人、招過「好幾百」個人。個人網站的履歷列出 DropSend（2008 被收購）、Carsonified（2011）、Treehouse（2021）三次收購，Treehouse 團隊寫「100+」；第四家沒在該頁找到（見回查）。
- Untangle：起初是給離婚當事人的消費者 app，很快轉成 B2B 賣給家事律師事務所。他說是「AI paralegal」；官網用詞是給離婚律師的 AI 工作流程軟體（intake、文件蒐集、提醒客戶），宣稱減輕 paralegal 負擔。
- **立場**：他不是 Devin 的員工，但整場是 Devin 重度使用者的心得，多次說「Devin 內建」「我愛 Devin」，並說「你的 harness 大概也有」。個人網站另列他 2025–2026 在 Amp（另一家 coding agent）當 Builder in Residence。所以這不是廠商自家簡報，但內容高度綁 Devin 的功能，可視為**單一客戶的使用見證**。
- 他自己也說這套「明天就會變、一週後可能沒用」，只是目前在 production 跑得不錯，迭代過「好幾百次」。

## 演講脈絡（依順序）

### 1. 開場：做離婚這個痛點、管人就像管 agent（0:12–1:58）

- 現場調查誰離過婚、誰認識離過婚的人，最後全場舉手。他兩個姊妹和父母都離過婚，想讓這件事少痛一點。
- 先做消費者 app，很快轉 B2B 賣給家事律所，說已有 product-market fit、成長很快。
- 主張：上一家公司擴到約 110 人時學到的管人經驗，搬到管 agent 上幾乎一樣。本場分三段：怎麼管 agent、怎麼招人、live demo（最後沒做）。

### 2. 組織圖：人在最上面，下面是「只是 session」的 manager（1:58–3:11）

- 人負責設優先順序、跟客戶談、所有「人的事」。下面是 **manager agent**，他強調「就只是一個 session」，命名為 engineer manager，**永遠不寫程式**。他主要跟這個 session 講話，由它管一堆子 session。
- 他從手寫程式、用 Cursor，一路到全部在雲端用 Devin。
- **用語音跟 manager 溝通**：他說自己讀得不快、聽比讀更容易吸收，所以多半用 audio 跟 manager 對話。閱讀頁把這點解讀成「可以一邊聽一個對話，一邊有多個變更在進行」。

### 3. 派工單位：一張 ticket 一個 PR（3:11–3:35）

- manager 從 ticket 看板（他們用 Linear，「用什麼不重要」）拿工作，看板是「要做什麼」的單一真相來源。
- 規則：**每張 ticket 應該就是一個 PR**。manager 依 ticket 之間的**相依關係**決定下一張開哪張。他自己說這是「很基本的工程經理工作」。

### 4. 一個 manager 帶約 20 個 builder，人不進子 session（3:35–4:22）

- 一個 manager 同時帶**約 20 個 builder**，範圍大約 5 到 25。上限主要卡在「你跟 manager 對話、理解發生什麼事的能力」，推太多會很快失控。他同一段又說「我們能同時帶約 25 個」，兩個數字並存。
- 關鍵規則：**你永遠不進 builder 的 session**，不跟它們講話、不管它們，一切透過 manager。manager 通常在回答「不需要我回答」的技術問題，或排除小障礙。閱讀頁補充推理：如果每個問題都要他自己開 session 撈 context，就等於又要顧 20 個對話。

### 5. 用排程逼 manager 巡視：每 15 分鐘（4:22–5:10）

- 他另外做了一個 **automation**，強迫 manager **每 15 分鐘讀一遍所有子 session**、把卡住的推一把。投影片寫 10 分鐘，他後來定在 15。
- 理由：「你不能信任 manager agent 自己做到這件事，它不是確定性的。」所以巡視的**時機**由腳本保證，巡到之後**該做什麼**仍由 manager 判斷。實作是 Devin 的 automation，「告訴它每 15 分鐘去讀每一個 child，推進度」。
- 他自己說「這不是火箭科學，很多人大概已經這樣做」。

### 6. review 最多 3 輪、QA 另開子 session（5:10–6:22）

- 每個 builder 會呼叫 **review agent**（Devin 內建 review，「每個 harness 大概都有」）。builder 跟 reviewer 最多來回**約 3 輪**；3 輪後還有重要 bug 沒修好（逐字稿字面是「have been fixed」，依上下文應為「還沒修好」），builder 就往上丟給 manager，manager 需要時再丟給他。
- 底層是常見的東西：程式碼加測試。另外有一個 **QA 流程**：從 builder 再開一個**子 session** 專門跑 QA。這是新進工程師 Dale 幫忙裝的，「目前看起來不錯」。
- 成本觀：「agent 很便宜，能開多少就開多少，**只要不卡住 merge queue**。」他說大家都會遇到 merge queue 變慢；要在「把 PR 啄到死」跟「直接合進去」之間找平衡。3 輪上限就是為了不讓一個 PR 一直等。

### 7. 影片驗收：讀摘要、在大螢幕看完（6:22–8:18）

- 每個 builder 會錄一段**功能實際被使用、並通過測試的影片**。Devin 內建（他說叫 test），會產生測試案例、錄影、每個案例給綠或紅。沒有內建的話「你應該自己做，但很難」。
- UI 改動「你一定要看」：測試結果說哪些檢查過了，影片才看得出它長怎樣、行為對不對。這是**人必須說 ship it 的那一步**。
- manager 會通知他「有影片可以看了」。他的流程：**先讀一段摘要，知道這個 PR 應該做什麼**，再看影片並認真投入。
- 他明說這是最想偷懶的地方，但這就是產品負責人必須親自承擔的瓶頸：通常要在筆電上看。實例：演講前他在手機上跟 manager 語音，收到影片通知，手機上幾乎看不清變更，很想說「OK ship it」，最後還是忍住，回到電腦再看。

### 8. 不要在本機開發（8:18–8:43）

- 他講得很重：「如果你還在本機寫程式，停下來。」要用雲端 agent（Devin 或其他），否則你、你的團隊都被拖慢，因為本機做不到上面那套。

### 9. 多人多 manager：session 彼此直接傳訊（8:43–9:55）

- 假設 10 個人同時在做事，每人通常各有一個 engineering manager session，有人開兩個（他當時就開了兩個）。
- 這些 session **要知道彼此存在、能直接互傳訊息**。Devin 內建，「你用的 harness 大概也有」。他說它們很擅長這件事，訊息清楚、快，而且不是閒聊，是解除彼此阻塞的必要資訊。不讓 session 互相溝通，「大概在出比較爛的軟體」。

### 10. merge queue manager：協調 migration 編號（9:55–11:07）

- 即使 session 會互相溝通，還是需要一個 **merge queue manager**，協調湧進來的一波 PR。例子：**資料庫 migration 編號**。每個 builder 在自己的 PR 裡拿「下一個編號」都合理，合在一起就撞號。merge queue manager 讓這類問題消失，也會更聰明地處理 merge queue 的順序。
- 它跟 engineering manager 一樣**只是一個普通 session**，他只是用職責替它命名，然後給它空間自己想辦法。他引 OpenAI 講者的說法「unhobble」：設好角色，然後別綁住模型，叫 merge manager「把這些弄好」就有效。
- 實際排隊用 **GitHub merge queue**，「沒什麼特別，運作得不錯」。
- 中間他問誰覺得這是胡說，現場一兩人舉手。

### 11. 招募第一關：免費 45 分鐘錄影（11:07–13:28）

- 他說招募的舊做法「全部過時」。**前面完全不做 pre-screen、不視訊、不接觸本人**，因為會被偏見帶走：你會喜歡他的嗜好、說話方式，覺得他有趣，「全是雜訊，不是訊號」。唯一重要的是：**他會不會操作 agent**。
- 第一關：候選人交一段**約 45 分鐘、全螢幕的錄影**，用 agent 出一個 feature PR，通常是在**自己已在維護的 app** 上。**不給任何指示**，方法自選。這關不付錢，是入門門檻。
- 把影片和逐字稿丟給一個 **ranking agent**，叫它看完排序。他第一次不信它的排名、不喜歡結果；事後回頭看，排第一的那位「我應該錄取」，他歸因於自己的偏見。閱讀頁特別註明：這是他對**單一次**招募的事後判斷。
- 限制：有些候選人會含糊自語，或完全不出聲思考，很難看出在想什麼；有些則講很多。

### 12. 前五名付費 16 小時試做真 PR，最後才通電話（13:28–15:28）

- 取排名前五，邀請參加**付費專案**：固定費用買 16 小時，簽 NDA，給一個 Devin 席位，任務是把一個**真的 Untangle PR 弄到能 merge**。全程用 Loom 錄影。
- 影片再丟給 agent（Devin）問「該選誰」。上一輪他自己也看完 16 小時影片，「很折磨，但讓我很了解這些人」。
- 先決定 finalist，**這之前不打電話**，免得被愉快的對話帶偏。最後打給 finalist 說「我們想錄用你，聊一下」：讓人做最後一次判斷，也建立一點人與人的連結；但他說看了那麼多小時影片，其實不太需要那通電話。
- 他宣稱「大家都會這樣招人」「比以前容易、也好太多」。

## 可以搬到個人 Claude Code／Codex 工作流程的做法

這場的規模（20 個雲端 builder、多人多 manager）個人搬不動，但其中幾個**機制**可以縮小照做。

1. **一張 ticket 一個 PR，寫好相依關係再開工**。開平行 session 前，先把工作切成每份剛好一個 PR 的大小，各標 depends-on。沒有相依的才平行；有前置的等前面合進去再開。Claude Code 的 agent teams 共享 task list 支援相依，被 block 的任務 teammate 不會自己領（見回查）。
2. **巡視交給排程，不要靠 agent 自覺**。Claude Code 在 session 內可用 `/loop 15m <prompt>` 或叫它建排程：例如「每 15 分鐘：列出所有子任務狀態；卡超過 2 輪沒進度的，讀它最後輸出、給一句指示或標成需要我；其餘不打擾我」。注意官方文件寫明 session 內排程只在 session 開著且閒置時觸發、週期任務 7 天後自動過期，而且有 jitter（每 10 分鐘的任務會晚 0–5 分鐘）。要不依賴 session 的巡視，改用雲端排程或 GitHub Actions。
3. **人只跟一個 lead 講話**。用 Claude Code agent teams 時，問題先由 lead 回答，你不要逐一點進 teammate 改方向，除非 lead 升級上來。這是 Carson「永遠不進 builder session」的單人版。但官方建議 3–5 個 teammate 起步，而且 teammate 不能再開自己的 teammate（沒有巢狀），所以「manager 底下 20 個 builder、每個 builder 再開 reviewer 與 QA 子 session」這種三層結構無法照搬。
4. **review 寫死輪數上限**。在 builder 的指示裡寫：「完成後請 reviewer subagent 審；最多來回 3 輪；3 輪後仍有 high 等級問題，停止修改，把問題清單回報給 lead（或我），不要繼續改。」上限的目的是不讓 PR 卡著，不是品質保證。
5. **QA 另開一個 session，不跟 reviewer 混在一起**。reviewer 看 diff，QA 實際跑起 app 操作。UI 改動要求它用 Playwright 之類錄影或截圖附在 PR。
6. **看影片前先讀「這個 PR 應該做什麼」**。要 agent 在 PR 說明最上面寫 3 行預期行為，你看錄影時逐條對照；在手機上看不清楚就不核准，等回到電腦。
7. **共用的序號類資源交給一個協調者**。多個平行 PR 都會碰 migration 編號、設定檔版本號、changelog 這類「下一個號碼」時，指定一個 session（或乾脆你自己在合併時）統一重編，不要讓每個 builder 各自拿。若框架支援用時間戳命名 migration（如 Laravel、Rails 預設用時間戳），撞號機率本來就低，這一項可省。
8. **session 互傳訊息**：Claude Code agent teams 的 teammate 可依名字直接互傳訊息；不開 team 時也有跨 session 傳訊。注意：傳來的訊息會被標為來自另一個 Claude session，不能代替你核准權限。

**不能直接搬的**：

- **語音跟 manager 對話**：需要產品支援語音模式；個人終端機流程通常沒有。真正可搬的是背後的原則：把 manager 的回報壓成你能快速吸收的格式。
- **20 個雲端 builder 同時跑**：需要 Devin 這類每個 session 一台 VM 的平台與預算。個人能盯的量遠低於此（見下方張力）。
- **「本機開發就是錯的」**：這是 Devin 使用者的立場。個人專案、需要本機硬體或私有網路的工作不一定適用。
- **錄影招募流程**：與個人工作流程無關；團隊招募要搬時，要自行處理候選人錄影的隱私、NDA 與付費試做的法律面，演講沒談。

## 回查結果（2026-11-19）

| 主張 | 結果 | 來源 |
|---|---|---|
| Untangle 是家事律所用的 AI paralegal | **大致成立**：官網寫給離婚律師與律所的 AI 工作流程軟體，處理 intake、文件蒐集、提醒客戶與例行問題，宣稱減輕 paralegal 負擔；官網沒提 Carson | [untangle.us](https://untangle.us/) |
| 做過四家公司並賣掉；上一家擴到約 110 人 | **部分成立**：個人網站履歷列 DropSend（2008）、Carsonified（2011）、Treehouse（2021）三次被收購，Treehouse 團隊「100+」；第四家未在該頁找到。Untangle 列為 2024 年起。同頁另列 2025–2026 在 Amp 當 Builder in Residence | [ryancarson.com/history](https://www.ryancarson.com/history) |
| 用排程 automation 每 15 分鐘叫 manager 巡所有子 session | **機制成立**：Devin 文件的 Automations 有 Schedule trigger（可自訂每 N 分鐘），動作可選「Start session」開新 session 或「Message session」對既有的長期 session 傳訊，後者正是他描述的做法；預設 rate limit 每小時 50 次 | [Devin Automations 文件](https://docs.devin.ai/product-guides/automations) |
| manager 管子 session、session 彼此能傳訊 | **成立**：Cognition 2026-03-19 公告 coordinator session 能拆工、把每塊派給在獨立 VM 跑的 managed Devin、追進度、解衝突、彙整結果，可對子 session 中途傳訊，也能替自己排 follow-up 檢查點。公告範例上限是同時 10 個，沒寫最大值 | [Cognition 部落格](https://cognition.com/blog/devin-can-now-manage-devins) |
| 張力點：為什麼還需要外部排程 | Devin 文件寫 coordinator 在子 session 完成或需要輸入時會**自動被喚醒**、不必輪詢。Carson 仍另加 15 分鐘排程，理由是「agent 不是確定性的」；這屬他的經驗判斷，演講沒說明自動喚醒哪裡不夠 | 同上；[Devin advanced capabilities](https://docs.devin.ai/work-with-devin/advanced-capabilities) |
| builder 錄功能使用影片並給綠／紅 | **成立**：Devin 文件的 testing and recordings 寫開 PR 後可在瀏覽器實際操作 app、錄下過程並加註解寄給使用者；可在設定中預先核准免詢問；登入牆或 VPN 擋住時會求助 | [Devin testing and recordings](https://docs.devin.ai/work-with-devin/testing-and-recordings) |
| GitHub merge queue | **成立，但不處理 migration 編號**：官方文件寫每個排隊 PR 和最新 base 及前面的 PR 組成暫時分支跑必要檢查，失敗就移出並重建後面的分支。文件完全沒提 migration 或任何語意協調，所以撞號仍要靠他的 merge queue manager session | [GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) |
| （對照）Claude Code 能否照搬 | agent teams 為實驗功能、預設關閉；lead 指派、teammate 依名字互傳訊息、共享 task list 支援相依；官方建議 3–5 個 teammate 起步、無巢狀 team、in-process teammate 不能 resume。session 內排程（`/loop`、cron 工具）最短 1 分鐘、週期任務 7 天過期、需 session 開著 | [agent teams 文件](https://code.claude.com/docs/en/agent-teams)、[scheduled tasks 文件](https://code.claude.com/docs/en/scheduled-tasks) |

Codex 是否有對應的「巡視排程＋session 互傳」功能，本輪**未查證**。

## 證據強度與限制

| 主張 | 強度 |
|---|---|
| 一個 manager 帶 5–25 個 builder，約 20 個 | **自報**經驗值，同一段裡 20 和 25 並存；沒有量測，沒說合併量、失敗率 |
| 巡視間隔 15 分鐘比 10 分鐘好 | **自報**，沒說依據什麼判斷 |
| review 3 輪上限 | **自報**慣例（「typically」），沒給數據 |
| 「這樣出了很多高品質 PR」 | **自報**，沒有任何數字：PR 量、revert 率、bug 率都沒給 |
| 迭代過好幾百次 | **自報** |
| session 互傳訊息後軟體品質較好；不讓它們溝通「大概在出比較爛的軟體」 | 講者**意見**，無對照 |
| 本機開發是錯的 | 講者**意見**，且與他使用的雲端產品利益一致 |
| ranking agent 排第一的人他應該錄取 | **單一案例**的事後判斷，閱讀頁也特別標註；沒說後來是否錄取、錄取者表現 |
| 這種招募方式「比以前好太多」、大家都會這樣招 | 講者**意見**，沒有任何結果指標 |

整體限制：

- **單一新創、單一產品**：整套架構綁在 Devin 的 automation、managed session、內建 review 與 test 錄影上。他說「你的 harness 大概也有」，但沒驗證其他工具。
- **沒有任何結果指標**：同屆 [[Walden-Yan-軟體工廠與給-agent-長期-job]] 至少給了 PR 數與工程師數（同樣自報）；Carson 一個數字都沒給。
- **閱讀頁去品牌化**：閱讀頁完全不提 Devin，讀者只看閱讀頁會以為這是工具中立的做法。

### 勿引用

- 「Carson 做過四家公司並賣掉」當作已查證事實：個人網站只列出三次收購，第四家本輪未找到。可以引用為「他自述」。
- 「一個 manager 能穩定帶 25 個 builder」當作上限：他同時說了「約 20」「5 到 25」「推太多會失控」，25 是他口頭的一個說法，不是測出來的上限。
- 「ranking agent 比人準」：只是他對一次招募的事後感想，沒有後續驗證。

## 與既有頁的關係與張力

- **供應商與客戶講同一套**：[[Walden-Yan-軟體工廠與給-agent-長期-job]] 是 Devin 的廠商 Cognition 自己的內部做法：雲端 VM、影片當交付證據、人只在一天結束時看升級上來的決定。Carson 是 Devin 客戶，描述的流程幾乎一樣。這可以互相印證「產品能這樣用」，但兩者都依賴同一個產品，**不能當作兩個獨立來源**互相佐證效果。
- **同一個數字，兩種解讀**：[[Prasanna-Sankar-雲端-agent-的瓶頸一路移到開工]] 說雲端能平行 20–30 件、但超過 10 件他就吃不消，所以讓常駐 agent 當專案經理；Carson 的解法相同（加一層 manager），但宣稱人能跟 manager 帶約 20 個。[[多-agent-的人類監督與介入]] 整理的經驗值是 foreground 2–4 個、超過約 8 個就改由 lead agent 協調、人只管 lead，Carson 正是這個轉折之後的形態。該頁也記錄 fan-out 取決於 agent 能被放著多久，Carson 的 15 分鐘巡視和 3 輪上限就是在拉長「可被放著的時間」。
- **巡視交給程式，與 Konda 一致**：[[Girish-Konda-把-sub-agent-當分散式系統]] 主張子 agent 交接的檢查要由程式碼強制、不靠 prompt。Carson 的「不能信任 manager 自己巡，要用 automation」是同一個原則的實務版。但他只保證巡視**時機**，子 session 回報什麼、算不算卡住，仍是 manager 用自然語言判斷，沒有 Konda 主張的具名狀態。
- **影片證據的弱點**：[[Stephen-Chin-與-Cassandra-Chin-PR-描述要附證據包]] 要求驗證段由執行紀錄產生；[[多-agent-的人類監督與介入]] 則提醒 approval gate 會退化成橡皮圖章。Carson 自己就差點在手機上「OK ship it」，正好是這個失效模式的現場例子；他的對策是先讀預期行為再看片，和 Chin 的方向一致，但影片只能證明畫面，不能證明沒畫到的路徑沒壞。
- **merge 這段比 Debois 淺**：[[Patrick-Debois-多人多-agent-同時合進同一-main]] 把多人多 agent 合進同一個 main 拆成派工公告、意圖衝突檢查、speculative merge train。Carson 的 migration 編號撞號只是其中最表面的一類，他交給一個「自由發揮」的 merge queue manager session，沒說它怎麼檢查語意衝突。[[平行-agent-產出的合併與-review]] 也記錄文字無衝突不代表語意正確。
- **與「先穩內圈」的順序**：[[Lauren-Tan-把糾正寫進程式庫]] 主張先把糾正變成 lint、型別與可執行檢查，再放大外圈的自動化。Carson 的品質關卡是 reviewer agent、QA agent 和人看影片，幾乎都是 agent 判斷加人眼，沒談程式庫本身的確定性檢查。
