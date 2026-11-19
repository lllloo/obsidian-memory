---
title: Brian Douglas 把糾正存成團隊 review 資料
description: Brian Douglas 主張保存 agent session、標記 pushback，先把團隊糾正寫成 skill 驗證，再考慮微調 reviewer
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-brian-douglas
published: 2026-11-12
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - evaluation
  - skill
---

# Brian Douglas 把糾正存成團隊 review 資料

來源：AI Engineer CODE 2026 線上場〈Every Correction You Give Your Agent Is Data〉的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-Douglas-Every-Correction-Is-Data]]（Day 2 直播 YouTube `y9JtCCZP2MQ`，約 1:59–2:12，全長約 13 分鐘）。工具與數字另核對 Paper Compute 的 GitHub repo 與兩篇官方部落格（2026-11-19 查）。

**一句話**：資深同事每次對 agent 說「不對」，都帶著編譯器管不到的團隊判斷。把完整 session 存下來、標上 `pushback` 等標籤，就能把這些判斷搬到下一次 review；先寫成 skill 並用 eval 驗證，不夠再拿同一批資料去微調模型。

## 講者與立場

Brian Douglas（網路代號 bdougie），Paper Compute 共同創辦人（Paper 部落格作者頁的職稱是 Co-Founder）。**整場示範的都是自家產品**：capture 工具 tapes、agent runtime stereOS、團隊版 Paper console。他嘴上說「重點不是 tapes，用別的 session capture 也行」，但示範的每一步（集中儲存、標籤、匯出）都靠 Paper 的商業產品。演講本身短（他自己說「沒太多內容」），只示範一個例子，沒有給任何量測結果。

## 演講脈絡（按順序）

### 1. 開場：不會寫 Rust 的人也在產 Rust

- **Rick Rubin 比喻**：他引用 Rick Rubin 的書《The Creative Act: A Way of Being》。Rubin 製作過許多樂團（逐字稿寫「BC Boys」，應是 Beastie Boys），自己卻幾乎不演奏樂器，很多人拿這點類比 vibe coding；同理，現在有人沒寫過 Rust 也能 vibe code 出一堆 Rust。Douglas 說自己正是這樣：公司日常用 Rust，他十年前只用 Rust 寫過練習用的小專案。
- **Addy Osmani 的 junior 論點**：junior 變 senior 靠的是 reps（反覆練習並得到回饋）。把這些 reps 交給 agent，人就失去升級的機會。閱讀頁把這段整理成：有用的教訓被困在只有一個人看得到的互動裡。

### 2. 先把 session 存下來：tapes、stereOS、Sweeper Agent

- **tapes**（tapes.dev，Apache-2.0）：記錄 coding agent 的 telemetry。他強調市面上有很多 OTel collector、session capture 服務，很多 harness 也內建，用哪個都行；重點是**存互動本身，不只存最後的 diff**。
- **stereOS**：他和團隊做的 agent runtime（sandbox），提供可重現的執行環境，讓每次 session 都可記錄。
- **Sweeper Agent**：他的「self-healing infrastructure」小專案，用來平行跑 agent 做定義清楚的雜務：文件、寫測試、清程式碼。他說在自家環境上可擴到約 10 個，在 Daytona sandbox 上同時跑過約 200 個；用途大多是清理他過去 18 個月 vibe code 出來的軟體。
- 但這些都沒改變一件事：他還是不會寫 Rust。

### 3. 集中儲存與標籤：pushback 是訊號

- 本機 capture 只對自己有用；團隊版（Paper console）把**自己和同事的 session 放在同一個資料庫**，而且可以替 session 加標籤。
- 示範一個標著 `pushback` 的 session（主題是 Paper cloud 的匯出記憶體限制）。`pushback` 的定義是「工程師每一次反駁 agent」。
- 他專門篩同事 Matt 在 Rust、Go 程式上的 pushback，因為 Matt 一反駁，就代表他知道 agent 不知道的事。典型內容：
  - 「我們已經決定 API 結構要這樣設計」：Rust 編譯得過，但違反團隊對程式怎麼組織、各部分怎麼互動的決定。
  - agent 重複造出已經存在的服務（因為缺 context）。
  - agent 重新發明團隊已經在用的 Go 函式庫，例如自己寫測試用的 mock 函式庫。他說誇張一點就是「重新發明 Kubernetes」。
- **他自己的盲點**：身為「Rust junior」，他沒有足夠 context 去反駁 agent，通常照單全收。結果 PR 到了 Greptile 拿到 5/5 分，他就放行，然後在人工 review 被資深工程師大量 pushback。問題是：怎麼在送 PR 之前先吸收這些反駁？
- 閱讀頁補充：有價值的是**反對的理由**，不是罵得多兇。
- 順帶提到「傳聞 Anthropic 會封鎖對 agent 很兇的帳號」，他自己說不確定有沒有根據（見「勿引用」）。

### 4. Review 正在搬進終端機，GitHub 資料不夠

- 他的團隊多數人已經改在命令列 review：叫 Claude 或自己的 harness review PR，**不在 GitHub 上留 pushback 或評論**。
- 所以 review 從「GitHub 上人來 review」→「GitHub 上 agent 來 review」→「在各自 harness 裡 review、沒有任何紀錄回到共用 code base」。只收 PR 評論會漏掉真正改變實作的那段討論。

### 5. TwinReview：照 Matt 的糾正訓練出來的 reviewer

- 命令列工具 `TwinReview`，輸入 PR 編號（示範用 381），它「像 Matt 一樣」review 這個 PR。
- 管線：capture traces → 建立標記好的資料集 → post-training（只用 Matt 在 Go／Rust 上的 pushback）。**訓練資料只來自 traces，沒用 GitHub PR review 資料**（他說那條路也可以）。
- 示範畫面上，它只挑一個有架構誤解的 hunk 留意見，其他 hunk 放行。閱讀頁特別註明：畫面上的信心分數是工具自己的輸出，**不是經過獨立驗證的準確率**。
- 預期行為是**選擇性**：只指出和團隊判斷衝突的改動；每個 hunk 都套通用風格建議，就失去資深同事的價值。
- 他先說 TwinReview 開源了，講到一半自己更正：**沒開源，因為資料含敏感資訊**。他用 Fireworks 做 post-training。

### 6. 標籤不只 pushback

除了 `pushback`，他還找：apology（agent 道歉、回頭）、golden session（標記「這個值得注意」的好範例）、regression（agent 常在這裡翻車的地方）。這些標籤分別告訴未來的 agent 該重複什麼、該避免什麼。

### 7. 先寫 skill，再考慮訓練

- 建議是「choose your own adventure」：可以訓練或 post-train 模型，也可以只做自己的本地 review harness；他認為**光靠自己的 harness 就能做到很多**。
- 他實際的起點：從 Paper traces 產生 skill，例如「去查 tapes」的 skill（tapes 在他機器上就是本機 Postgres）。Paper console 目前要排 waitlist，所以一般人先用 tapes、Braintrust 之類的工具 capture。
- 順序：**有 skill → 能做 eval → 有 eval 才去 post-train**（例如判斷 Rust 程式是否符合組織的寫法）。
- 他寫過一篇「訓練模型而不是寫 skill」的文章，但結論是**先寫 skill，今天多半能從 skill 拿到大部分效益**。
- 他說團隊有將近 80,000 個 session 可以拿來產 skill。
- **訓練細節**（全是他個人環境的經驗）：
  - SFT（他說的 specialized fine-tuning）比較可行：用量化在 5090 這種小 GPU 上跑（逐字稿寫「QuickQ」，推測是 QLoRA，未確認）。比喻：模型是書，SFT 是在書頁邊緣寫筆記，筆記就是疊在預訓練模型上的 adapter。
  - 他說示範用的是 Qwen 4B（前面一句又說 Qwen3-8B，逐字稿前後不一致）；「效果還不錯」。
  - DPO 比喻成 CliffNotes，要大很多的運算；他說小模型（4B）做不了，要 70B 以上。他沒有本機硬體，只能用 NVIDIA 的 Brev 服務；Fireworks 上的部分功能一直沒拿到權限，大型資源還要預付。
- 閱讀頁提醒：這些是**他那套環境的觀察**，不是哪種模型大小能用哪種方法的通則。

### 8. 收尾

當互動裡有一個有價值的糾正時，保存那個 session，標上發生了什麼。團隊本來就在產生好的工程判斷範例，記錄下來，才能教會下一個 agent，而不是讓同一位資深工程師在每個 PR 重講一次。最後推薦《The Creative Act》與 Addy Osmani 的系列文章。

## 回查結果（2026-11-19）

| 主張 | 回查 | 結果 |
|---|---|---|
| tapes 開源、Apache-2.0、本機 Postgres | [papercomputeco/tapes](https://github.com/papercomputeco/tapes) README、[tapes.dev](https://tapes.dev/) | **對得上**。README 自述是 agent 對話的 append-only capture＋OpenTelemetry，資料存 PostgreSQL；客戶端 `tapesctl start` 可包起 `claude`、`codex`、`pi` 來 capture。查詢當下 star 數三百多 |
| 從 traces 產 skill | [papercomputeco/skills-cassette](https://github.com/papercomputeco/skills-cassette) | **對得上**。repo 描述「Turn tapes sessions in skills」：從你指定的 session 產生 `SKILL.md`，並儲存、版本化、提供給下一個 agent |
| session 可加 `pushback` 等標籤 | GitHub code search（papercomputeco 組織內搜 `pushback`）、Paper 部落格 | **開源 tapes 裡沒有**這類標籤；標籤功能在 Paper 的商業 CLI `paperctl label` 與 Paper console（部落格有指令範例）。也就是說，演講的核心步驟依賴付費產品 |
| stereOS 是 agent runtime | [papercomputeco/stereOS](https://github.com/papercomputeco/stereOS) | **存在**。描述為「為 AI agent 打造並強化的 Linux 作業系統」；另有 `masterblaster` 負責建立和編排 stereOS sandbox（AGPL-3.0） |
| Sweeper Agent、TwinReview | GitHub 搜尋 | **都沒找到公開 repo**。TwinReview 符合他當場「沒開源」的更正；Paper 部落格有一篇〈Run the Sweep on Daytona. Keep the tapes.〉，只看到標題、未讀內文 |
| 用 Fireworks post-train | [Fireworks fine-tuning 文件](https://docs.fireworks.ai/fine-tuning/fine-tuning-models) | **現況已變**：文件寫「Managed SFT and DPO no longer accept new jobs」，要改走 Training API。照他（或下方部落格）的 `firectl sftj create` 路線做之前要先確認 |
| 他寫過訓練模型的文章 | [Train a Model on Your Own Agent Sessions](https://papercompute.com/blog/train-a-model/)（bdougie，2026-10-01） | **存在**。用 Qwen3-4B＋LoRA，資料放 Databricks、實驗記在 MLflow；標籤用 `golden`（人工挑的好 session）、`regression`、`pushback`、`apology`、`no-outcome`。**文中沒有任何成效數字**，演講說的「效果還不錯」沒有公開佐證 |
| Addy Osmani 在 Anthropic 做 Claude Code | [addyosmani.com](https://addyosmani.com/) | **對得上**。個人網站自述是 Anthropic 的 Member of Technical Staff、做 Claude Code |

### 同公司另一篇更完整的一手資料

Paper 的 DevEx Lead BekahHW 寫的 [A Beginner's Guide to Fine-tuning with Session Data + Fireworks](https://papercompute.com/blog/a-beginners-guide-to-fine-tuning-with-session-data-fireworks/)（2026-10-15）把演講沒講的細節補齊了，也是**全場最有用的延伸資料**。全部數字都是 Paper 團隊自己的 session，屬**廠商自報、單一團隊**：

- **規模**：2026-06-16 到 10-06，593 個 session、5,707 個人類 prompt、1,049 次 pushback。花在被糾正上的錢（被否決的 agent turn＋回應 pushback 的 turn）約 $5,538／$28,415，即 19%；作者說這是下限。
- **pushback 只有約一半是 agent 的錯**；其餘是工程師改需求或補了 agent 不可能知道的資訊，這些要另外標記並排除在訓練外。分類用四種：`agent_correction`（agent 本來能做得更好，這才是訓練訊號）、`user_changed_requirement`、`user_added_information`、`clarification_of_ambiguous_request`。
- **標記方法**：用白話寫一份「什麼算 pushback、算哪一類」的規則，讓 LLM 依規則讀過每個 session 打標籤，再每類抽樣人工檢查。
- **agent 的錯主要三類**：純技術錯誤、誤解需求、**手上已有答案卻沒去看**（檔案、文件、先前的 tool 結果、記憶筆記），三者合計占 agent 造成的糾正成本 68%。她選第三類（context failure）來訓練。
- **重播實驗**：16 個時刻、每組 3 次取樣。資訊「拿得到但沒載入」時，把它補進 prompt，agent 避開錯誤的比例從 0% 升到 52%；資訊「早已在 context 裡卻被忽略」時，再貼一次也沒用。結論是要教的是「去打開檔案」，不是「重讀已有的東西」。
- **寫更好的 spec 也救不了這類錯**：有 spec 的 session 裡，36 次 context 類糾正有 34 次發生在 spec 已經讀進 context 之後。
- **第一次糾正會讓後面加倍**：同一個 session 位置，沒被糾正過時每 100 個 prompt 有 5.9 次後續糾正，被糾正一次後升到 11.9 次。所以只用「被糾正後恢復」的例子訓練會教錯東西，要找 agent 第一次就做對的正面例子（她找到 191 個）。小技巧：agent 讀了檔才給出有把握的答案、工程師沒意見或說「對」的地方，就是正面例子。
- **資料格式與評估**：Fireworks 吃 OpenAI chat 格式 JSONL，每則訊息可設 `weight` 0／1，只有目標那一則設 1；依 session 切分，約四分之一留作 held-out；用 LLM 當評審（不讓它看到原本的糾正），並預先挑 20 個案例人工核對評審，不同意超過 6 個就不採信分數。
- **最重要的一點**：作者明說**這篇不回答微調到底有沒有用**，「訓練後」那一欄刻意留空，要等模型在真實 session 跑夠久再另文報告。

**勿把兩邊的數字混用**：演講說團隊有「將近 80,000 個 session」，部落格的同期窗口只有 593 個 session。兩者口徑不同（時間範圍、session 的定義都可能不同），無法互相印證。

## 能搬到個人 Claude Code／Codex 流程的做法

前提：你沒有 Paper console、也沒有 TwinReview。下面只用本機已有的東西。

**A. 先讓 session 留得住**

1. Claude Code 的對話紀錄存在 `~/.claude/projects/<project>/<session>.jsonl`，內容包含訊息、tool 呼叫與結果（[Claude directory 文件](https://code.claude.com/docs/en/claude-directory.md)）。但它會依 `cleanupPeriodDays` 自動刪除，**預設 30 天**（[settings reference](https://code.claude.com/docs/en/settings-reference.md)）。想從糾正裡挖東西，先在 `~/.claude/settings.json` 把它調長（例如 `365`；設 `0` 會驗證失敗）。
2. 這些檔是明文，會含檔案內容、指令輸出與你貼上的東西。拿去給別的模型或服務之前要先清掉敏感資料，這也是 TwinReview 沒開源的原因。
3. Codex 也在本機留 session 紀錄，但路徑與保存規則本頁沒有核對，用之前自己查。
4. 只有團隊要集中收、或要跨 harness 統一格式時，才值得裝 tapes；個人單機用 Claude Code 自己的 JSONL 就夠。

**B. 每週挖一次糾正**

1. 讓 agent 掃最近一週的 transcript，找出你在說「不對」「不是這樣」「你有看過那個檔嗎」「停」這類話的地方（語意找，不要只比對關鍵字）。
2. 每一筆照部落格的四類分類，**只留 `agent_correction`**；你自己改需求、補資訊、題目本來就模糊的都丟掉。
3. 再替每筆標原因：技術錯誤、誤解需求、有資料沒去看、重造既有的輪子（服務、函式庫）、違反架構決定。
4. 同一個原因出現第二次才往下處理，避免把一次性的糾正推成死規則。

**C. 先寫成 skill，再用 eval 驗**

1. 把同一類糾正整理成 review 用的 skill：寫「我們不這樣做、改用什麼、為什麼」，每條附一個真實發生過的例子（例如「這個 repo 已有 mock 工具，不要自己寫」）。
2. 叫 review 時只回報**與這些判斷衝突的地方**，其餘放行，對應演講說的「選擇性」。
3. 從挖出的糾正裡留幾筆當 eval：給 agent 糾正發生前的對話，看它這次有沒有第一步就做對；有 skill 和沒 skill 各跑一次比較。
4. 能寫成 lint、型別或測試的，照 [[Lauren-Tan-把糾正寫進程式庫]] 的優先序往確定性層推，不要停在 skill。

**D. 什麼時候才微調：個人幾乎不用**

- 個人單人的糾正量太少，而且 Fireworks 的 managed SFT／DPO 已不收新工作；Paper 自己也還沒公布微調的成效。
- 只有在團隊規模、有大量已分類的糾正、而且 skill＋eval 證明不夠時才值得試。DPO 依他的經驗需要大模型與大硬體，個人更不划算。
- 「資深同事的分身 reviewer」需要那位同事的大量糾正資料；單人開發者沒有這個來源，但**自己的糾正**一樣能照 B、C 處理。

## 證據強度與限制

| 主張 | 強度 |
|---|---|
| pushback 裡藏著編譯器管不到的團隊判斷 | 合理觀點，單一案例示範（Matt 的 Rust／Go 糾正） |
| TwinReview 能像 Matt 一樣挑出關鍵問題 | **單一 demo，無量測**；閱讀頁註明畫面上的信心值不是獨立驗證的準確率；工具未公開，無法重現 |
| 團隊多數人改在命令列 review | 講者自報、單一團隊 |
| 先寫 skill 就能拿到大部分效益 | 講者個人判斷，沒給比較數據 |
| 約 80,000 個 session | 講者自報；與自家部落格的 593 個 session 口徑對不上 |
| 平行跑約 10 個／約 200 個 agent | 講者自報，未公開 Sweeper Agent |
| 4B 模型微調「效果還不錯」 | 講者自報；他的公開文章沒有成效數字 |
| DPO 需要 70B 以上 | 他自己環境的經驗，不是通則（閱讀頁也這樣提醒） |
| 部落格的 19%、68%、0%→52%、34/36、5.9→11.9 | 廠商自報、單一團隊；重播只有 16 個時刻×3 次取樣；成本溢價那段作者自承是相關性、分不開任務大小 |

整體來說：演講是**產品導向的做法分享**，不是實驗報告。能搬走的是「保存 session → 分類糾正 → 先寫 skill 並用 eval 驗」這個順序；任何成效數字都還沒有公開證據。

## 與既有頁的關係與張力

- **和 [[Lauren-Tan-把糾正寫進程式庫]] 有張力**：兩人都從「每次糾正」出發，但落點相反。Tan 把糾正往確定性層推（架構、lint、型別），散文（rules、skills）排在倒金字塔下層；Douglas 的推薦落點正是 skill，再往上是模型權重，兩者都不是確定性檢查。可以合起來用：Douglas 解決「糾正散落在各人 session、怎麼收集」，Tan 解決「收集到之後放在哪一層最可靠」。像「不要重寫已存在的 mock 函式庫」這類糾正，其實可以用依賴規則或 lint 擋，不一定要訓練模型。
- **和 [[Ara-Khan-讓-agent-自動爬升-harness-與選題]] 同一個想法、不同儲存單位**：Khan 把一次糾正存成「輸入＋驗證指令」的可重跑任務，Douglas 存整個 session 加標籤。Khan 的做法容易自動評分，Douglas 的保留了比較多脈絡（包括 agent 當時看到什麼），但要另外建 eval。
- **補充 [[AI-產碼加速下的-review-瓶頸]] 的 AI review 工具路線**：Greptile 給 5/5、人工 review 卻大量 pushback 的例子說明，通用 AI reviewer 抓不到團隊特有的架構決定。Douglas 的方向是做「懂這個團隊」的 reviewer，但目前只有 demo、沒有量測。他觀察到 review 正從 GitHub 搬進各人終端機，這也代表 PR 評論不再是完整的 review 紀錄。
- **和 [[Matt-Pocock-的-PR-瓶頸解法]] 的 `retro` 互補**：`retro` 從重複的 review 問題產生檢查或規範候選；Douglas 的資料源更上游，來自 agent session 裡的口頭糾正，這些往往不會出現在 PR 上。
- [[AI-Engineer-2026-演講精華-AI-工作流程]] 已把本場列進「人的糾正就是資料」一節，本頁是該條的完整版。

## 勿引用

- **「Anthropic 會封鎖對 agent 很兇的帳號」**：講者自己說是傳聞、不確定有無根據，本頁未查證。
- **「TwinReview 是開源的」**：講者當場更正為未開源。
- **演講的 80,000 個 session 與部落格的 593 個 session 互相印證**：口徑不同，不可混用。
- **「用 Fireworks 就能照做 SFT／DPO」**：查詢當下 Fireworks 的 managed SFT 與 DPO 已不收新工作。
