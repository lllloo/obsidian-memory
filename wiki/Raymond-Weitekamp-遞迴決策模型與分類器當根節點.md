---
title: Raymond Weitekamp 遞迴決策模型與分類器當根節點
description: Weitekamp 主張讓只會挑選的決策模型當 agent 根節點、LLM 降為選項之一；整理 RDM 三規則、map、arbiter 與回查落差
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/talks/hFNbPmzzcEs-your-agent-doesnt-need-llm-every-decision
published: 2026-11-10
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - agent-framework
  - evaluation
---

# Raymond Weitekamp 遞迴決策模型與分類器當根節點

**一句話主張**：很多看似需要推理的任務，其實可以拆成一連串「從已列好的選項裡挑一個」的極快判斷；把只會挑選、不會生成文字的決策模型（decision model／System One model）放在 agent 的**根節點**，LLM 或 coding agent 只當它可以選的其中一個選項，必要時才生成。

原始逐字稿與官方閱讀頁見 [[AI-Engineer-Weitekamp-Recursive-Decision-Models]]（YouTube `hFNbPmzzcEs`，2026-11-10 上傳，約 51 分鐘預錄線上演講）。

## 講者與立場

- 官方標題掛 OpenProse；講者 GitHub 個人頁寫的是 polySpectra 創辦人，個人站 raw.works。**整場沒提 OpenProse**，掛名與內容無關。
- 他不是 TypeSafe（Jev 廠商）員工，談 Jev 時都用「他們」；但他是 Jev 生態的積極建構者：自己寫了 DSPy fork 上的 RDM 模組、Rust 套件 `rdm`、Jev 閘道 `one-system`。
- **有在推自家東西**：演講後段是 oSo（Operating System One）的預告，結尾邀請加入 waitlist。前段的 RDM 是開源的（MIT）。
- 他自己說原標題是「Recursive Decision Models」，投稿後才發現真正要講的是「Operating System One」，所以官方標題「你的 agent 不需要每個決策都用 LLM」只對應演講前三分之二。
- 他在 AI Engineer World's Fair 講過另一場「Recursive Coding Agents」，本場的 RLM 背景都推給那一場。

## 演講論證脈絡（按演講順序）

### 1. 名詞：System One、decision model、zero-shot classifier（0:00–3:00）

- 「System One」借自 Kahneman《快思慢想》：系統一是快速、直覺的判斷，系統二是慢速、刻意的推理。TypeSafe 發表 Jev 時用了「System One model」這個名字。
- 他接受另一種說法：Jev 做的是「判斷」，真正的「決策」由你的程式碼下。也有人堅持只叫它 zero-shot classifier。他表明不想爭名字，三個詞在本場指同一件事。
- **整場反覆回扣的問題**：「如果推理其實是很多個小決策呢？」——那些我們以為需要大量推理的任務，能不能用很多個非常小、非常快的決策解掉？

### 2. 收斂 vs 發散：為什麼要有決策模型（3:00–6:30）

- RDM 是兩件事的結合：MIT 的 Recursive Language Models（RLM，Alex Zhang 與 Omar Khattab 那一組）和 Jev。
- 生成式 AI 是**發散**：給無限 token 就能產出無限多候選，但總得有人決定什麼進 production，code factory 裡的 agent 也只是替你做這些決定。
- 決策模型是**收斂**：不能生成文字，只能在給定選項中排序、挑選。他用「陰陽」形容兩者互補。

### 3. RLM 對應到 RDM，以及根節點放誰（6:30–9:50）

- RLM：根節點 RLM 可以呼叫子 RLM，子 RLM 還能再呼叫，程式設定最大深度，到深度上限就是一次普通 LLM 呼叫。
- RDM 原樣對應：根決策可以選擇「再問一個更窄的子決策」，到深度上限就是一次單純的決策呼叫。
- 兩種擺法：
  - **decision as a tool**：決策模型當 agent 的工具。Jev 開放後 24 小時內就有大量例子：拿來做 compaction、判斷某個 tool call 能不能執行、當 router 決定請求要送哪個模型。他認為這是「顯而易見」的用法。
  - **decision at the root**：根節點是決策模型，呼叫 LLM 或 agent 只是它的選項之一。他說本場幾乎所有例子都在這個範式，也是他覺得新、但不明顯該怎麼搭的部分。

### 4. Doom：兩組決策組合成能過關的 agent（9:50–12:30）

- TypeSafe 發表時的「Jev plays Doom」影片：一組決策處理當下動作（站住、前進、閃避），組合成玩家下一步，隨遊戲變化反覆跑；另一組用鳥瞰地圖決定往哪探索。兩組耦合，就成了純決策呼叫的 Doom agent。
- 他認為這個例子被看了很多次、卻被嚴重低估，幾乎沒人往下發展「把多組決策系統組合起來」。

### 5. RDM 三規則（12:30–15:00）

1. **context 留在模型外**，由程式切片。Doom 裡完整遊戲狀態在程式手上，移動控制器只拿到局部視角，探索控制器拿到地圖視角。
2. **決策可以選擇呼叫另一個決策**，程式強制最大深度。（前兩條直接抄自 RLM：context 外部化、可以開子呼叫。）
3. **先在完全沒有生成模型的情況下能跑**，同時必須能和 LLM、agent 組合。他的理由：沒有生成模型也能跑，才證明架構本身是對的；「decision as a tool」雖然有用但不新，純決策才可能打開新能力。

### 6. Galton board：視覺化的玩具例子（15:00–17:30）

- 理想 Galton board 每根釘子左右各 50%，球堆成鐘形。換成「會判斷的釘子」：每根釘子讀球上的數字，像二分搜尋一樣把球分到對應的桶。
- 決策模型一次可以問多個問題，所以可以在 3D 同時依顏色與數字分類。
- **他自己承認**：這個例子一次分類呼叫就能做完，不需要遞迴；放出來只是為了讓觀眾記住「早期選擇限制後面選擇」的畫面。

### 7. 分層搜尋與影像裁切（17:30–21:00）

- TypeSafe 發表時有一份 cookbook：Shopify 約 12,000 個商品分類，用 beam search 加分層 Jev 呼叫，把使用者查詢（例如 laptop backpack）對到正確分類。
- 他的做法是「不用 beam 的 beam search」：每層只給分類器「查詢＋目前父分類的子分類」，問下一步要展開哪個。一次塞 12,000 個分類會撐爆 context window。
- **分類器只負責排名，程式決定走幾條路**：greedy 只走第一名，省探索但太早押注；保留前三名，可能讓排名較低的分支在更深處走到更合理的分類。
- 影像：Jev 約在發表一個月後支援多模態。一個做法是有命中就放大、在更小的框再問一次（找甲蟲）；另一個做法是 TypeSafe 團隊成員把影像遞迴對半切再分類各區塊。**他承認**：好的 vision model 可能一次就答得出來，這些例子是為了展示遞迴能控制「每次判斷看的範圍」。

### 8. Factorio：沒有 LLM 的維修 agent（21:00–23:30）

- 他用 RDM 玩 Factorio：先挑出有問題的生產線群組，再縮到一條線，再指出要換的 inserter，角色跑過去修，接著修下一個。**整個迴圈沒有任何生成模型**。
- 他自己點出限制：工廠是一排排一樣的元件，像矩陣，每題選項都不多，算是玩具；角色走遠路去下一個維修點，他想過加一個尋路元件。
- 他的長期目標是讓 RDM 教他玩 Factorio，並認為開放式遊戲是評估這類系統的好方式。他把這類 demo 比作「Claude plays Pokemon」那個等級，但不用生成模型。

### 9. 純決策的弱點：選項從哪來（23:30–26:00）

- 決策模型只能挑，選項必須由腳本、應用程式本身或另一個 agent 事先列出來。他說 TypeSafe 申請 API key 要過一個小測驗，問「Jev 能不能生成文字」，答「能」就拿不到 key。
- 他認為在遊戲、瀏覽器、甚至很多 computer use 情境，「事先列舉」其實就夠：遊戲可以用程式列出狀態與可用動作；他的投影片網站 DOM 上只有三個互動元素（上一頁、下一頁、播影片）；桌面上可見控制項和快捷鍵雖多，只要能列舉，就能用挑選的方式操作。
- 推論：computer use 一向被當成只有頂尖推理模型做得到的 benchmark，但如果能列出全部選項，也許很多小決策就夠快、夠用。

### 10. 必須能和生成模型組合：智慧家庭與 map（26:00–32:00）

- 純決策的路徑是預先定義的（例如 outline walk：標題→H1→小節→段落→句子→字）。加入生成節點後，呼叫樹會長出不規則、湧現的形狀；他展示的是 smart home demo 的實際呼叫樹。
- 他擴充了 TypeSafe 的 smart home demo：更多房間與家電。「我們要睡了」→ 鎖門、留一盞燈、其他關掉；「看部電影吧」這種更隱晦的要求，系統要學會對應到一組家電指令。
- **map 是決策模型與 LLM 的共用介面**：每個條目有名字、簡短描述，和一個指向行為的指標。`TV on` 可以指向一個設 Boolean 的函式，另一個條目可以指向整個迴圈。決策模型只判斷哪個條目適合，程式執行背後的函式，所以分類器選一個複雜操作和選一個開關一樣容易。
- LLM 拿到結構化的方式新增、修改條目。例如學到「movie time」＝開電視＋關燈，下次決策模型就只要選一個條目。學到的偏好存在 map 裡。
- map 可以有多個維度：他提到 Every 的 Kieran Klaassen 用 Jev 產生低維、但每一維都有語意的 embedding，他的 RDM map 也支援這種表示。

### 11. arbiter：平行判斷、單一寫入（32:00–35:00）

- 決策模型快又便宜（他說有些能在手機或十年老筆電上跑），所以不確定時可以投機地平行跑一堆。
- 問題：如果每個都直接改狀態，完成順序就會決定結果。快的模型先改了狀態，慢的模型還在用舊狀態判斷，可能要求相反的改動。
- 他類比 CPU：讀可以並行，寫要上鎖。**arbiter** 綜合各通道當下的證據，判斷信心是否足夠，才讓某個動作改變狀態；它比鎖多一層判斷：這次寫入到底該不該發生。
- 語音的例子：話還沒說完，不同通道已經各自傾向某個動作，arbiter 決定何時放行。
- 他說這受 RLM 作者 Alex Zhang 的「speculative programmatic tool calling」想法影響。

### 12. 實作（35:00–36:30）

- 第一版是 DSPy 模組：DSPy 團隊很快就加入 System One API 支援，而 DSPy 的強結構讓他能驗證 RDM 的模組有沒有照預期組合。
- 另有獨立 Rust 套件 `rdm`，給需要快速、可攜實作的應用。

### 13. Operating System One 與身體（36:30–43:30）

- 雙關：這是一個「operating system one」，也是在學怎麼「operate System One models」。
- 動機很個人：長期用滑鼠造成肩頸緊繃，研究所趕 deadline 時出現重複性勞損，各種直立滑鼠、軌跡球、人體工學鍵盤都買過。他想繼續在電腦上工作，但減少身體綁在鍵盤滑鼠上的時間，語音是最近的入口。
- 他回顧近 20 年前的實驗：筆電內建加速度計，敲機殼四個位置由分類器分辨，變成鼓組；傾斜控制效果；敲擊觸發 side-chain compressor。
- 他透過 Princeton Laptop Orchestra 學會寫程式和機器學習：用 Rebecca Fiebrink 的 Wekinator 做即時機器學習，模型是 k-nearest neighbors、單層神經網路這類小東西，能邊演奏邊學、分類手勢、做非線性插值；樂手能直接聽到延遲的代價。

### 14. Earshot：先學會在逐字稿出來前就動作（43:30–47:30）

- 任務：唸數字一到八切換桌面工作區。一開始是轉錄音訊、辨認數字、再切換，聽得到數字、看得到桌面慢半拍。
- 兩條路同時聽：轉錄路徑負責動作並提供教學訊號；另一個用 ChucK 的 ChAI 寫的極小監督式模型，只看 40、80、100 毫秒的音訊切片的粗略頻率 bin。一開始小模型什麼都不會、不能信；另一層判斷何時夠可信才跟隨它。
- 用 Philip Glass《Einstein on the Beach》的數數片段當輸入：1–4 出現較多，先學會、先跟上節拍，後面的數字還在落後。他說最後學到的反應約 **45 毫秒**，偶爾有 blip。
- 他也推了別人的 Hunch：在瀏覽器用 WebGPU 跑 embedding 模型玩 Pictionary，分類塗鴉約 150 毫秒。他的結論：小型 embedding／encoder／classifier 模型正在復興，架構得好就能做很強的事。

### 15. oSo：決策優先的 computer use agent（47:30–51:00）

- oSo（oso.computer）是 Operating System One 的縮寫，當時還沒推出。目標是不碰電腦、甚至不看電腦也能工作，第一個輸入是語音。
- 設計：決策優先，熟悉的指令由 RDM 直接處理，開放式工作再交給一般 coding agent（他點名 Claude Code、Codex）或 RLM agent。
- 要學兩件事：使用者想要什麼（像 movie time），以及哪個模型能可靠辨認這個意圖。一旦 arbiter 從過去表現建立信任，就把重複出現的決策交給最小、最快的可用模型（Earshot 是這件事的實例）。
- 他對工程師回到終端機的解讀：終端機不是最好的介面，大家湧進去是因為意識到預設應用介面、滑鼠鍵盤觸控的限制；但打字對肩痛的人仍是身體問題。

## 可以搬進個人 Claude Code／Codex 工作流程的做法

以下是從他的架構抽出、不需要 Jev 也能照做的部分；需要 Jev 或 oSo 的部分另外說明。

1. **先列選項，再讓模型挑**。寫 skill、hook 或 subagent 指令時，把「請判斷該怎麼做」改成「從以下 N 個選項選一個，並說明理由」。做法：在 skill 中把可走的分支寫成具名清單（名字＋一句描述＋對應動作），要求 agent 先輸出選中的名字，再執行對應步驟。這等於在 LLM 上模擬 map：選項固定，輸出可檢查。
2. **context 留在外面、按題切片**（規則一）。派 subagent 時不要把全部背景丟進去，主 agent 持有完整狀態，每個子任務只給回答那一題需要的切片，例如 review 只給 diff 與相關測試、查資料只給問題與已知條件。
3. **分層縮小再判斷**（分層搜尋、Factorio 的模式）。大範圍問題（哪個模組壞了、哪段 log 有問題）讓 agent 先在高層挑一個區塊，再往下一層問，不要一次讀完整個 repo 或整份 log。可以照他的建議決定要 greedy（只追第一名）還是保留前幾名，避免太早押注。
4. **平行讀、單一寫入**（arbiter）。多個 subagent 平行調查、提出修改建議，但只讓主 agent 一個寫檔、在綜合所有回報後決定採用哪個。這可以直接避免他講的「快的先改、慢的用舊狀態判斷」的衝突。
5. **把穩定的判斷降級成腳本**（Earshot 的 fast path 思路）。同一類決策若反覆出現、結果一致（例如某類檔案永遠走同一種處理），就把它寫成 hook 或 shell 腳本，不再每次問 LLM；新情況或腳本信心不足時才回到 LLM。要留觀察期，不要第一次成功就固化。
6. **不建議照做**：
   - 拿決策模型當 Claude Code 的工具權限 gate（他列為「decision as a tool」的常見用法）。Jev 官方文件承認 state 裡的對抗內容能移動判決，第三方實測過 prompt injection 能把 block 機率從 0.76 壓到 0.48（細節見 [[Jev-與-System-One-模型]] 第六節）；權限 gate 應該用確定性規則。
   - 讓 LLM 自動往 map 寫新條目並期待效果更好：他自己的部落格寫到，目前試過的專案中 LLM 寫的條目都沒有勝過單純挑選（見下方回查）。
   - oSo、Earshot 目前無法使用（oSo 只有 waitlist；Earshot 沒有公開程式碼可查）。Rust `rdm` 適合要自建應用的人，對日常寫 code 的個人流程是過度工程。

## 回查結果（2026-11-19）

| 演講說法 | 回查來源 | 結果 |
|---|---|---|
| RDM 有獨立 Rust 套件 | GitHub `rawwerks/rdm` | ✅ 存在，MIT、Rust，2026-11-08 建立（錄影前兩天），回查時 15 星，所有 commit 在同一天推上。四個 crate：`systemone`（協定）、`one-system`（閘道）、`rdm`（迴圈與 map、Near、Rlm 等）、`rdm-wasm` |
| 第一版是 DSPy 模組 | `rawwerks/dspy` 分支 `feat/rdm-v0`；上游 `stanfordnlp/dspy` PR | ✅ fork 上有 `dspy/predict/rdm*.py` 與文件，最後 commit 2026-10-04。**RDM 本身未進上游**（上游未搜到 RDM PR）；但「DSPy 很快支援 System One API」屬實：上游已 merge #10463（experimental decision types 與 System One clients）與 #10510（Jev 教學） |
| arbiter 是 RDM 的原語 | `rdm` README | ⚠️ 部分屬實：README 明寫 arbitration **只有 Rust 版有**，`dspy.experimental.RDM` 沒有對應，會等所有工具跑完並全部採用 |
| map、smart home、分層搜尋 | `rdm` README 的 examples | ✅ `home`、`map`、`dimensions`、`hierarchy` 範例都在；沒有 API key 時用寫死規則的 stand-in 跑，也可接本機開源決策模型 Laya（經 llama.cpp）或 hosted Jev。**Factorio、Doom、Earshot 不在範例清單中**，只有影片 |
| Shopify 約 12,000 分類 | `rdm` README | ✅ README 寫 12,378 個分類，演講的「12,000」是約數 |
| map 讓 LLM 學會新條目（movie time） | 講者部落格 raw.works〈Recursive Decision Models〉（2026-10-01） | ❌ 與演講語氣有落差：部落格寫「誰該寫新的 map 條目」尚未解決，**LLM 寫的條目在他試過的專案中都沒有勝過單純挑選**；決策模型也從不選擇遺忘。保留舊動作的 map 正確率 87% 對 66% 的數字來自模擬玩具房屋，沒有用 LLM |
| 部落格的其他自陳限制 | 同上 | 他說還不知道 RDM 擅長什麼，目前做新奇性探索、不做 benchmark；分層分類 8 次請求到達預期葉節點、約 20 行程式對比 cookbook 約 150 行，但明說「不是說比較好」；對半搜尋在實務上是「糟糕的做法」；smart home 四次執行出現四種呼叫圖形，最大一次是 80 次請求的循環，靠上限才停 |
| Jev 不到兩個月前發表 | TypeSafe 官方 blog | ✅ blog 標 2026-09-15，影片 11-10 上傳，相符。官方 blog 另寫 Doom bot 約每秒 10 次查詢、約每小時 7 美元，**用的是結構化文字狀態、不是影像**——補充了演講沒講的條件 |
| 官方發表時有 hierarchical search、smart home cookbook | TypeSafe 官方 blog | ❓ 發表 blog 只提 Doom 與 Wikiracing，未提這兩份 cookbook；可能在其他文件，未查到 |
| 申請 API key 要過「能不能生成文字」小測驗 | — | ❓ 未查到一手來源 |
| RLM 出自 MIT 的 Alex Zhang 與 Omar Khattab | arXiv 2512.24601 | ✅ 作者 Alex L. Zhang、Tim Kraska、Omar Khattab；v1 2025-12-31。abstract 自報 RLM 能處理超出 context window 兩個數量級的輸入，對 GPT-5 的中位改進為比 compaction 高 26%、比 Claude Code 高 13%（作者自報） |
| ChAI 是 Wekinator 的後繼 | ChucK 官方 ChAI 頁、NIME 2024 論文 | ⚠️ ChAI 存在，由 Ge Wang 與 Yikai Li 主導，內含 Wekinator 的完整移植並標 Rebecca Fiebrink 為原作者；官方描述是「整合」而非「後繼」 |
| oSo | oso.computer | ✅ 只有 waitlist 表單，沒有產品說明、平台或定價 |
| Hunch（WebGPU Pictionary，150 毫秒） | 網路搜尋 | ❓ 未找到一手頁面 |
| speculative programmatic tool calling 出自 Alex Zhang | — | ❓ 未查 |

## 證據強度與限制

- **所有延遲數字都是講者自報、單一 demo、無對照**：Earshot 約 45 毫秒只適用「重複出現的八個數字」這個任務，fast path 只需分辨少數熟悉聲音；Hunch 約 150 毫秒未能回查來源。
- **Factorio、Doom 都是 demo 影片**，沒有成功率、比較基準或公開程式碼（Doom 是 TypeSafe 的 demo，不是他的）。他自己也說 Factorio 是矩陣般重複的玩具場景。
- **RDM 尚無 benchmark**：講者部落格明說刻意先做新奇性探索；`rdm` 範例預設跑的是寫死規則的 stand-in，輸出固定，證明的是程式管線可跑，不是決策品質。
- **「推理其實是很多小決策」是假說，不是結論**：演講用例子示意，但沒有任何場景比較過「同一任務用 RDM vs 用推理模型」的成功率或成本。
- Jev 本身的速度、價格、可靠性宣稱有已知落差（廠商峰值 193 倍未被第三方重現、能被 prompt injection 影響），演講把「快又便宜」當前提，但沒有討論這些落差；整理見 [[Jev-與-System-One-模型]]。

### 勿引用

- 「LLM 透過 map 學會新條目能讓系統變好」——講者自己的部落格寫到目前沒有勝過單純挑選；演講中的 movie time 只是示意，不可當成效果證據。
- 「Factorio／Doom 證明 computer use 不需要推理模型」——兩者都是選項可程式列舉、結構重複的遊戲，且 Doom 用的是結構化文字狀態，不能外推到一般桌面操作。

## 張力：與 vault 既有頁的關係

- **翻轉 routing pattern 的位置**：[[Building-Effective-Agents-Anthropic]] 的 routing 是 LLM workflow 裡的一個分類步驟；Weitekamp 把它推到極端，讓分類器當根、LLM 只是被路由到的選項之一。兩者不衝突，但他的版本只在「選項能事先列舉」時成立，這正是他自己指出的弱點。
- **與 Jev 頁互補也互相牽制**：[[Jev-與-System-One-模型]] 列出的「該不該換掉既有 fine-tuned encoder 沒人測過」缺口，演講沒有回答；反過來，演講補上 Jev 頁沒有的東西——多次決策的組合方式（遞迴、map、arbiter）。Jev 頁的 prompt injection 證據直接限制了演講中「拿 Jev 判斷 tool call 能否執行」這個用法。
- **複雜度 gate**：[[Agent-工作流-Pattern-藍本庫]] 的選用 gate 要求先用簡單解。Galton board、分層搜尋、影像裁切三個例子他自己都承認一次呼叫或好的 vision model 就能解，遞迴是為了展示，實際採用前應先過這個 gate。
- 與 [[AI-Engineer-2026-演講精華-AI-工作流程]] 的「能確定性處理就不用 LLM」那條相呼應：該頁把本場濃縮成一句，本頁補完整論證與回查。

## 主要來源

- 官方閱讀頁與逐字稿：[ai.engineer](https://ai.engineer/talks/hFNbPmzzcEs-your-agent-doesnt-need-llm-every-decision)；影片 [YouTube](https://www.youtube.com/watch?v=hFNbPmzzcEs)
- 講者實作：[rawwerks/rdm](https://github.com/rawwerks/rdm)、[rawwerks/dspy feat/rdm-v0](https://github.com/rawwerks/dspy/tree/feat/rdm-v0)、[rawwerks/one-system](https://github.com/rawwerks/one-system)
- 講者部落格：[Recursive Decision Models](https://raw.works/recursive-decision-models/)
- TypeSafe：[Introducing System One Models and Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- RLM 論文：[arXiv 2512.24601](https://arxiv.org/abs/2512.24601)
- ChAI：[ChucK for AI](https://chuck.cs.princeton.edu/chai/)
- oSo：[oso.computer](https://oso.computer/)
