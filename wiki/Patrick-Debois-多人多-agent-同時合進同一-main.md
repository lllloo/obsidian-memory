---
title: Patrick Debois 多人多 agent 同時合進同一 main
description: Debois 的 concurrent delivery：派工公告改動、意圖衝突檢查、merge train 與依風險分級 review，附回查與落地判斷
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/talks/fTUinMqA1XQ-your-teams-agents-are-all-shipping-same
published: 2026-11-10
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - automation
---

# Patrick Debois 多人多 agent 同時合進同一 main

來源：AI Engineer 演講〈Your Team's Agents Are All Shipping to the Same Code at Once〉的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-Debois-Agents-Shipping-to-Same-Code]]（YouTube `fTUinMqA1XQ`，約 23 分鐘，2026-11-10 上傳）。本頁按逐字稿順序整理，閱讀頁是主辦方改寫的版本，兩者有出入處會標明。

**一句話**：一個人在筆電上跑多個 agent（他稱為 *solo factory*）時，協調全靠那個人的記憶；一旦整隊人各自帶 agent 同時往同一個 `main` 合（*multiplayer factory*），「同時改」就從例外變成常態。所以要從 continuous delivery 改成 **concurrent delivery**：事前切分與公告、執行中協商、合併時檢查意圖、用 speculative merge train 排隊，review 依風險而不只依品質決定深度。

## 講者與立場

- Patrick Debois，現任 Tessl（[講者頁](https://tessl.io/speaker/patrick-debois)列為 AI Product Engineer），常被稱為「DevOps」一詞的提出者。他從 DevOps／CI/CD 的角度看 agent，這是整場的框架來源。
- **有推自家產品**：結尾邀觀眾試用「Tessl factory」，演講中的聊天室拉 agent、決策紀錄等例子都來自 Tessl 自家工廠。他另經營研究站 [concurrent.cd](https://concurrent.cd)（見回查）。
- 他自己在結尾說「brace yourself, we're not there yet」：這場多數內容是**方向與正在試的做法**，不是已驗證的方法，也沒給成效數據。

## 演講脈絡（按順序）

### 1. 從 solo factory 到 multiplayer factory（0:00–1:58）

- 傳統交付管線（build、test、等 release、merge 進 main）本質上是**序列流程**，自動化讓它穩，但仍一次一個。
- 現在個人在筆電上用 coding agent 搭「工廠」，常跑多個 agent，但決策和 merge 仍由那個人做，他像中央節點，**要自己記住每個 agent 在做什麼**。
- 他列出一個漸進光譜：個人在筆電上做 → 分享自己的 setup（context、skills、loops）給同事複製（他說是現在多數工廠的狀態）→ multiplayer：多人**同時**在同一個 ticket board、同一個 codebase 上作業。
- 兩個張力，也是整場的兩半：**程式碼面**，人人都要合進 `main`；**人的面**，多人在同一個 board 上要協作。

### 2. 開了工廠之後，merge 變成瓶頸（1:58–3:50）

- **PR 量**：他說開啟 multiplayer factory 後 PR 量「almost like a factor 10」。**自報、無量測方式、無基準**，只能當印象。
- **agent 互相來回改**：一個 agent 改了，另一個又改回去，兩邊都在產出 merge queue 的工作，程式碼卻回到原點。
- **最明顯的副作用是等 release 更久**：每合一個 PR，其他排隊中的 PR 都要 rebase、通常要重跑測試。CI/CD 因此變慢、也更貴（他說成本是副作用）。閱讀頁把這畫成「一個 merge → B、C 各自 rebase、各自重測」，佇列愈長，一次成功的合併觸發的 CI 工作愈多。
- **PR 佇列不只是功能**：還有 agent 造成的事故修復，以及「工廠本身的維護」——改 skill、改 loop 的 PR 也要人核准。
- 結論：與其把同時改當例外處理，不如**設計成常態**，他稱為 concurrent delivery。

### 3. 事前：切分、claim、公告、隔離（3:50–5:57）

- **切分**：像分配工作給人一樣，你做 authentication、我做 payment。可以用程式碼的 AST／依賴圖判斷哪些部分好切；兩件任務靠得近時，切分可細到檔案、函式，甚至同一檔案中的個別編輯。在規劃階段做，就能在開工前看出到底有多少能獨立做。
- **claim ticket**：agent 在 board 上認領 ticket，其他 agent 就不會同時接同一件。
- **公告預計改哪些檔、改什麼**：這和 claim 的用途不同。claim 只防「同一張 ticket 重複做」；兩個 agent 各自認領**不同** ticket，計畫仍可能碰到同一個函式。公告預定改動，讓彼此在還能調整時發現重疊。
- **隔離**：很多人用 git worktree 分開工作檔。他主張隔離可以延伸到檔案依賴的東西：每個 agent 自己的機器與 context、鎖定的 API 版本、資料庫快照與自己的測試資料，外部系統用 mock 或 digital twin 代替。這樣 agent 做實驗時，資料不會被別的 agent 從底下改掉，實驗也不會影響外界。閱讀頁補了一句：**隔離到最後，程式碼還是得在 `main` 上和別人的改動碰面**。

### 4. 執行中撞到同一段程式碼（5:57–7:21）

撞上時對「已在執行中的計畫」有三種處理：

1. **等待再重試**：讓一個 agent 先做完，另一個再試。
2. **重新排隊**：把等待中的工作放回佇列，等它依賴的工作完成。
3. **重新協商分工**：執行中改變誰做什麼，若能談出互不重疊的改法，兩邊都繼續。

拖到 merge 時才衝突，他給了一條逐步升級的路：

- 重跑整件工作再合一次（他說這是現在 PR 的常見做法）；
- 讓 agent 不以「行」而以「函式」為單位合併，看整個函式並嘗試同時容納兩邊改動的修法；
- 最終，agent 能**預見**鄰近的改動即將到來，在對方還沒完成時就先調整自己的程式碼。這依賴知道另一個 agent 打算做什麼，也就是第 3 段的公告。

### 5. 意圖衝突：合得乾淨、單位卻錯（7:21–8:20）

這是整場最具體的例子：

- PR 1 把計算發票總額的函式改成回傳「分」（cents）。
- 同時 PR 2 改了報表輸出，報表仍預期收到「元」（dollars）。
- 兩者改不同的行、各自測試都過、合併也沒有文字衝突，但計算的輸出就是報表的輸入，**以分計的數字會被當成元讀**。

他說這是「不在程式碼衝突、而在意圖衝突」。提議：讓 agent 比對進來的多個 PR 的**意圖**是否仍一致，有不一致就警告人或修正 PR。閱讀頁把做法寫得更具體：沿著「總額」這個值追過兩個改動，問「轉成報表要的單位這件事，由誰負責」，兩邊認知不一致就是具體可標記的問題。這是**提案**，他沒有展示實作或效果。

### 6. speculative merge train（8:20–9:40）

- 一般 merge 佇列逐一處理：某個 PR 合不進去時，其他都要 rebase、重做。
- **speculative merge train** 先看所有進來的 PR，**預先成對檢查**哪些彼此相容。某一個掉出去時，佇列已經知道哪些其他改動可以一起過，那些先走，問題那個等著。用事前多花的檢查換事後少等。
- 閱讀頁補了一個重要限制：train 能保證什麼，取決於它測什麼。**只檢查「能不能合、現有測試過不過」的 train，會把第 5 段的單位錯誤原封不動送上線。**
- 他預期規劃、合併處理、concurrent 改動的分析會變成**獨立的開發者基礎設施層**，並說現在多數工廠只是「glorified loops」，但 concurrency 只會增加。

### 7. 人的面：共用 board 與把 agent 拉進聊天（9:40–12:54）

- 大家在同一個 task board 上，能看到哪些改動要來、哪些在做；solo factory 沒有這種中央可見性。
- 但可見性也暴露瓶頸：多個 agent 同時要人注意，把問題全搬上 board，答題的還是人。所以要減少 agent 叫人的次數。
- **把 agent 拉進團隊對話**：不是你 prompt 它，而是把 agent 拉進既有對話。它從多位成員那裡同時取得線索、精煉 ticket，主動問「該做什麼、有哪些需求、怎樣的測試算完成」。ticket 因此變得像 coding agent 的 plan mode，只是放在 board 上大家都能看。他說這等於同時有 agent 的對抗式 review 和多個人類的意見。
- **非工程師也能用**：以前業務、行銷、客服開 ticket 給工程，可能等好幾週；自己 vibe coding 做出來又不符合工程規範。他說在 Tessl 的工廠，同事在組織聊天裡和 agent 討論，用工程的同一套 pipeline、知識、skills、loops 去實驗、精煉，甚至直接開工；原本知道需求的客服同事能在想法成形時參與定義。**單一公司自述，無數據。**

### 8. 卡住時：跳進 agent 的工作區，或只做選擇（12:54–15:06）

- ticket 模式有時太慢，需要快速迭代時可以混合：agent 卡住時開一個 IDE，裡面已有該 agent 的 context 與檔案，人跳進去做實驗、做出缺的那個選擇，再把工作交回 agent 與工廠繼續。逐字稿說這個點子來自 **Helix ML**；閱讀頁沒寫出處。
- 有些任務只需要一個**決定**：agent 列出幾個選項讓人挑或否決，然後繼續。他說這比每次告訴 agent 下一步要做什麼省力（coding agent 已有這種互動）。
- **決策紀錄（decision log／ledger）**：每個決定都寫進共享紀錄。個人工作時這像本機 coding agent 的 context；在 multiplayer 工廠，它是共享的，人可追溯誰在何時決定什麼，下一個 session 的 agent 也能查詢。

### 9. review：依人能讀多少切，依上線風險定深度（15:06–18:03）

- 切小的第二個理由：改動就算和其他 agent 隔開，**對人來說仍可能太大而讀不好**。小 PR 才能分批走 merge train、讓人快速 review。
- 降低失敗機率的一側：給更好的 context 與工具、先讓對抗式 agent 看過再到人手上；並要求 agent 附**螢幕流程截圖、影片、測試結果**當證明，讓 reviewer 看到改動實際做了什麼。
- 有人跟他說「我已經不看 code 了」，他的追問是：**這次改動上線的影響是什麼？** 沒有真實客戶的 app 和有人依賴的服務曝險不同；同一個 app 內也因改動而異：
  - 文件：影響有限，過了適用的檢查就放行；
  - 認證：出錯影響大，值得上線前讓人仔細 review；
  - 能逐步釋出的功能：分階段 rollout，看輸出和錯誤。
- **恢復成本也是一個維度**：若會丟資料，能多快還原？一個節點掛了會怎樣？能多快 rollback？review 與測試降低「失敗機率」，節點容錯、rollback、資料還原這些**架構決定**降低「失敗之後的代價」。要讓出錯時便宜好修。

### 10. 誰跟得上、誰維護工廠（18:03–結尾）

- 他自己遠端工作、團隊多在倫敦辦公室，本來就常跟不上室內討論的改動。agent 大量產碼後，行銷、客服也會陷入同樣處境；只給一串 merged PR，等於讓他們自己推論影響。**用各群人的語言傳達改動**（radiating change）成了交付的一部分。
- 核心原則：能自動化的盡量自動化，把人保留給例外，但要確保**例外能被路由到能做決定的人**。
- **factory team**：類似 platform team 照顧 Kubernetes 叢集，新出現的團隊照顧 coding agent 與工廠本身：確認每個 skill 由誰負責、共享 context 保持最新、agent 接到正確元件、監控工廠。閱讀頁一句話說得好：全隊共用的過時指令，影響範圍和單一開發者筆電上的不一樣。
- **personal agent 進 board**：Tessl 在試讓代表個人的 agent 在 board 上替人做決定、回答其他 agent 的問題。他明說還沒到位。

## 回查結果

| 主張或引用 | 回查結果 | 一手來源 |
|---|---|---|
| speculative merge train：預先檢查組合，一個失敗時其他可繼續 | **概念成立且早有實作**，不是新發明。GitLab merge train 把每個 MR 與「排在它前面的所有 MR」合起來測、平行跑；某個失敗就移出，後面的重開 pipeline（例：A、B、C 中 B 失敗，C 改測 A+C），預設最多 20 條平行、Premium 以上才有。Zuul 的 gate pipeline 做 speculative execution：假設前面的都會過、平行測，一個失敗就把後面的去掉它重測，並以會伸縮的 window 控制浪費。**差異**：兩者都是「依佇列順序疊加」，不是演講說的「成對檢查相容性」；成對檢查的具體實作他沒給出處 | [GitLab merge trains](https://docs.gitlab.com/ci/pipelines/merge_trains/)、[Zuul gating](https://zuul-ci.org/docs/zuul/latest/gating.html) |
| concurrent.cd 研究站 | **存在且是他的**：首頁把問題拆成 Plan、Isolate、Coordinate、Integrate、Verify、Remember 六個張力，正好對應演講結構；起源文署名連到 jedi.be（他的部落格），說靈感來自與 Steve Yegge 談 Beads／Gas Town、Anthropic 重設計 source control 的文章、E2B 的演講。站上收錄引述與工具，如 Steve Kinney「worktree 減少檔案衝突，但不隔離服務、port、資料庫、secret 或決策」 | [concurrent.cd](https://concurrent.cd)、[起源文](https://concurrent.cd/notes/hello-concurrent-cd) |
| Helix ML 的「卡住時人跳進 agent IDE、再交回」 | **部分對得上**：Helix 部落格〈Giving every agent its own desktop〉（2026-06-03）描述每個 agent 有自己的桌面與 IDE，「when the agent needs your help, you've already got a proper IDE to search around in」，也談跨時區由不同人接手。但沒找到「卡住自動開 IDE、做完交回」的文件化流程，搜尋只看到行銷頁的說法 | [Helix 部落格](https://helix.ml/blog/giving-every-agent-its-own-desktop) |
| Tessl factory | **存在**：SD Times 報導 Tessl 於 2026-11-06 發布「open standards platform for building software factories」，以 skills、loops、verifier 組成，附 Ticket to PR、Code Review、弱點修補等起始 workflow。報導**沒提到** multiplayer、merge train、decision log、聊天室 agent 或 board，所以演講中這些功能是否已在產品裡，無法確認。報導中的「80% PR 不需人手修」「每 PR 成本 75→13 美元」是 Tessl 自報 | [SD Times](https://sdtimes.com/?p=61713) |
| PR 量「約 10 倍」 | **無法回查**：演講沒給來源、期間或基準。搜尋只找到第三方摘要轉述同一句 | 無 |
| 意圖衝突（發票單位） | 這就是傳統的 semantic merge conflict，屬 git 逐行合併的基本限制，不需外部證據；「讓 agent 比對意圖」是否有效**沒有實證** | 演講本身 |

## 可搬到個人 Claude Code／Codex 工作流程的做法

前提：個人跑多個 agent 時，問題規模遠小於他說的團隊工廠，speculative train、factory team 都用不到。能搬的是下面幾條，屬推論、非實證。

1. **派工時寫「預計改動」清單，不只分任務**。開平行 agent 前，請每個 agent 在 plan 階段先列出要改的檔案與函式（Claude Code 的 plan mode、Codex 的計畫輸出都可以），由你比對有無重疊；有重疊就改為依序做，不平行。這就是演講「claim 之外還要公告」的單人版。
2. **合併前比對分支重疊**：`git diff --name-only main...branchA` 與 branchB 取交集，有交集就指定先合一支、另一支 rebase 後重跑測試。
3. **隔離不止 worktree**：會碰資料庫、port、外部 API 的任務，每個 worktree 要用各自的測試資料庫與 port，外部服務用 mock。只開 worktree 不夠。
4. **第二支合併前做一次「意圖比對」**：把兩支的 diff 一起給 agent，問具體問題而非「有沒有衝突」，例如：「兩邊有沒有改到同一個值的單位、型別、回傳格式或語意？這個值的轉換由哪一邊負責？」有疑點就補一個跨兩邊的整合測試。這是演講最可直接用的點子，但 agent 判斷可能漏，要以測試收尾，不以 agent 文字為準。
5. **review 深度依路徑與可逆性分級**：先寫一張自己的表——文件、註解類過了 lint 就合；auth、付款、migration、刪資料一律自己讀；能 feature flag 的先上再看錯誤。問自己「出錯能多快 rollback、資料能不能還原」，還原不了的才是要親自看的。
6. **讓 agent 給選項、決定寫下來**：要 agent 停下來時給 2–3 個選項而不是開放問題；做過的取捨寫進 repo 內的決策紀錄（如 `docs/decisions/` 或 PR 描述），下一個 session 才查得到。單人時這等於 ADR，價值在跨 session 而不是跨人。

**用不到或不建議照搬的**：

- speculative merge train：個人同時排隊的 PR 少，序列 rebase 加重跑就夠；GitLab 版需付費方案。
- 讓 agent「預見」別人的改動提前調整、以函式為單位自動合併：演講只是願景，沒有可用工具；LLM 解衝突的既有 benchmark 也只到約五、六成與開發者一致（見下方張力）。
- 把 agent 拉進聊天室、factory team、personal agent 替人決策：團隊與組織層級的事，個人用不上。

## 證據強度與限制

- **整場是方向性提案與單一公司自述**：沒有對照、沒有成效數據，也沒展示意圖比對、成對相容性檢查的實作。
- 「PR 量約 10 倍」：自報、無基準，**勿當數據引用**。
- 「Tessl 同事在聊天室直接開工」「決策 log」：自家工廠的經驗，且講者在推自家產品；回查的產品報導沒提這些功能。
- speculative merge train 的概念有一手文件支持（GitLab、Zuul），但演講說的「成對檢查」與這兩者的佇列疊加做法不同，**「pairwise 相容檢查」勿當成現成機制引用**。
- Helix ML 的接手流程：只對得上「agent 有可進入的 IDE」，自動開 IDE 再交回的流程未查到文件。
- 閱讀頁是主辦方改寫版，有些句子（如「只測能不能合的 train 會放過單位錯誤」）比逐字稿更明確，屬主辦方的整理，不是講者原話。

## 張力與互補

- **補強 [[平行-agent-產出的合併與-review]]**：該頁已把「worktree 擋不住語意衝突」列為基本限制，發票單位例子是同一件事的好示範；該頁也記了 LLM 自動解衝突在 benchmark 上約五到六成與開發者一致，所以 Debois「讓 agent 以函式為單位修 merge」不能免驗，做法 4 要以測試收尾。
- **與 Konda 的分歧**（脈絡見 [[AI-Engineer-2026-演講精華-AI-工作流程]] 第 4 主題）：Debois 想讓 agent 比對意圖，Konda 主張由程式驗 schema 與證據、不信 agent 的文字判斷。兩者可疊用：agent 找疑點，測試或 schema 檢查定案。
- **與 [[Matt-Pocock-的-PR-瓶頸解法]] 互補**：Pocock 要每個 PR 標明單向門／雙向門與影響範圍，Debois 把同一個問題講成「依上線影響與恢復成本決定 review 深度」，並加上「架構上讓失敗變便宜」這一維。
- **與 [[Claude-Code-放手運行的安全與驗證]] 呼應**：兩者都以「能不能收回」決定放手程度；Debois 再往前一步，主張用 rollback、資料還原等架構決定去擴大可放手的範圍。
- **與 [[多-agent-的人類監督與介入]] 互補**：該頁談一人盯多 agent 的上限與何時打斷；Debois 的「agent 給選項、決定寫進 log」是降低打斷成本的具體做法，但他沒給數據。
- **工具面**：[[平行跑多個-coding-agent-的工具選型]] 與 [[Orca]] 的 worktree 隔離，正是 Debois 說「必要但不夠」的那一層。
