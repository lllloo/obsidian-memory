---
title: 50 分鐘換 1000 小時的 Claude Code 完整指南（2026）
description: 從桌面版設定、plan mode 提問法，到 skill、CLI 串接、loop 與 graph engineering、模型路由的分階段學習路線
created: 2026-08-17
updated: 2026-08-17
source: https://www.youtube.com/watch?v=U6k4MeVks_Y
published: 2026-08-11
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - workflow
  - automation
  - loop-engineering
---

作者把 Claude Code 的學習路徑切成新手、中階、進階三段，主張這支影片可以取代上千小時的試錯。

## 新手：該在哪裡跑 Claude Code

Claude Code 有三個執行環境：雲端 web 版、桌面 App、終端機。作者的建議在近幾個月變了——以前會推終端機或 VS Code 擴充套件，現在**非技術背景的人直接用桌面 App**，而且不算錯過什麼。

理由是桌面 App 已經有終端機沒有的功能（語音模式、瀏覽器自動化、inline artifacts），整體體驗對沒碰過終端機的人友善得多；而且桌面 App 裡面本來就能開終端機，不是二選一。

### 設定速覽

- **Customize → General → Instructions for Claude**：這是全域指示，會套用到所有專案與所有 prompt。作者自己留空，也建議一般人留空——門檻應該是「這件事真的跟你未來每一次對話都相關嗎」，達不到就別寫。
- **Capabilities**：`tool access mode` 設成 load tools when needed，該頁其餘全開。
- **Claude Code 分頁**：general 全開；local sessions 全開。例外是 pull requests——不知道 PR 是什麼就先關掉。
- **Claude in Chrome**：作者開啟，但要另外裝 Chrome 擴充套件才有用。
- Artifacts 在 Claude Code 裡基本不用管；Routines 是後面談的自動化。

### 主畫面上的幾個控制項

- **執行位置**：cloud、remote control、WSL、SSH 這些若都不懂，99.99% 的情況該用 **local**（除 WSL 外其餘都是為了人不在電腦前時使用）。
- **工作資料夾**：可指定任一資料夾，例如桌面開一個 Claude Code projects；所有產出都住在那裡。
- **main / worktree**：屬於 git 的概念，新手保持 main、不勾 worktree。旁邊的加號可以再掛一個資料夾，讓工作內容同時存在兩處。
- **權限模式**共五種，光譜兩端是 manual（每件事都問）與 bypass permissions（下載、安裝、刪除、修改都放行）。中間的 **auto 是預設也是常駐選擇**：相當於 bypass，但有一個分類器會檢視 Claude Code 要跑的指令、判定危險就攔下來。另一個會用到的是 plan。

### 模型與 effort 的取捨

- $20 方案基本用不動 Fable，額度燒太快，只能待在 Opus。
- Max 方案（5x／20x，即每月 $100／$200）作者建議多數時間用 Fable，它明顯是最好的模型；但額度有三重上限——5 小時限額、每週限額，以及 Fable 專屬限額（**每週額度只有一半能給 Fable**），所以不能太早燒完。
- **effort level 才是真正該調的旋鈕**。想得越多表現越好，但**不是線性的**：從 extra high 拉到 ultra code 可能只換到 1% 的提升，卻付 5 倍代價。新手階段大多數問題連 medium 都用不到，low 通常就夠。作者自己常駐 **Fable medium**，只有遇到複雜問題、或快到額度重置時才往上拉。

### 提示的正確方式：plan mode 加意識流

開任何新專案**一律先進 plan mode**。原因不只是先對齊，而是它會**反過來問你問題**。非技術背景的人、或做不熟領域的專案，最大的障礙是「你不知道自己不知道什麼」——這些未知的未知只能靠 Claude Code 主動提出來照亮。

至於 prompt 本身，作者直接否定「有某種魔法格式」的說法（目標、脈絡、角色扮演那一套）：**買支麥克風，打開，用意識流講**。示範是講一個虛構 AI 分析公司 Lighthouse 的網站需求：只講了想要結尾有預約通話的 CTA、目標客群是小型新創，其餘不知道，然後補上一句「請問我任何你覺得相關、而我沒想到的問題」。

那句補語是重點——**任何 prompt 結尾都可以加「我漏想了什麼？你有什麼問題要問我？」**，把互動推成一來一回。

### 遇到不懂的選項，不要按「推薦」

當它問「要用什麼 tech stack：純 HTML/CSS/JS、Next.js + Tailwind、還是 Astro + Tailwind」，而你根本不知道 tech stack 是什麼時，直覺反應是按推薦選項。作者認為這是最該改掉的習慣：

- 模型夠好，按推薦確實還是會得到不錯的產出，問題出在**重複這個行為**。
- 一直按推薦的結果是：你跟隨便一個路人坐在你電腦前做出的東西沒有差別，護城河為零。
- 更關鍵的是你什麼都沒學到。總有一天會碰到 Claude 也不知道怎麼下手的獨特專案。

正確做法是回一句「可以解釋一下什麼是 tech stack 嗎？這幾個選項我也看不懂，給我快速拆解」。**你不需要再學會寫程式，但需要開始累積 AI 軟體工程的基本盤**——這些積木怎麼組起來的大局觀。持續數週、數月、數年這樣做，才不會變成 vibe coder 的漫畫人物。

### plan mode 的互動

計畫產生後會顯示在右側面板，可以直接選取某段文字加註解（例如把受眾從「小型新創」擴充到也包含中型公司），註解會累積成修訂意見，再叫它 revise。滿意後選 **accept with auto mode**（不要只按 accept，否則會落回 manual 模式）。

## 中階：context 與 skill

### context window 要盯著看

每個送出與收到的字都算 token，**token 是 LLM 的貨幣，context window 是預算**（單次 session 100 萬）。

關鍵不是額度夠不夠，而是**塞越滿表現越差**——腦子裡東西太多，問到中段發生的事就答不好。所以：

- 大約到 30%、40%，肯定到 50%（50 萬 token）時就該問自己要不要繼續這個 session。作者自己的門檻是 **30%**。
- context 裡除了訊息，還有 system、tools、skills，但訊息才是大宗。

滿了只有一種解法——開新對話，三種做法：

| 做法 | 行為 |
|---|---|
| `/clear` | 全部清空，全新 context，效能最佳 |
| `/compact` | 讀完整段對話史、生成摘要，帶著摘要開新對話 |
| 按加號 | 在同一資料夾開新對話，隨時可回頭引用舊對話 |

從 web 版過來的人會怕清掉對話等於失憶，但這裡不一樣：**你是在某個資料夾裡工作**，對話沒了，檔案與程式碼都還在，它讀得到、看得懂進度。開新對話不是從零開始，不必怕。

### 為什麼產出這麼醜：context engineering

第一版網站很難看，原因是只講了「乾淨的 SaaS 風格」，沒給靈感、沒給截圖、沒給足夠脈絡。中階的核心主題就是 **context engineering**：不只是把你的想法餵給它，還要讓它接得到外部工具與 skill。

### skill 是升級表現最重要的一件事

**Skill 最化約的定義就是「叫 Claude Code 用特定方式做特定事情的 prompt」**。例如各種前端設計 skill，本質就是一段指示：做網站時避開某些漸層、避開看起來像 AI slop 的東西等等。

取得途徑：

- **Claude App 內建**：Customize → Skills 可看已有的；Plugins → Browse 可看 Anthropic 官方外掛。skill 與 plugin 的界線相當模糊，可以先當成同一種東西（plugin 可以包含多個 skill，但劃分頗隨意）。
- 官方的 frontend design plugin 裝的就是 frontend design skill，它的完整 prompt 公開在官方 GitHub 上——把整段複製貼進對話，效果等同呼叫該 skill，只是沒人會每次都這樣做。
- **GitHub**：世上絕大多數 skill 在這裡。官方外掛清單能選的很少。安裝不必照 README 一步步做，**直接複製 GitHub 網址貼進 Claude Code，說「把這個 skill 加進來」**即可。

呼叫方式：可用 `/` 斜線指令，也可以直接用自然語言說「用 frontend design skill」，它聽得懂。**注意**：若裝了多個功能重疊的 skill，只說「我要做網站」它可能挑錯，需要明確指名。

**最該先裝的是 skill creator**（在 plugins → browse 裡），因為它是一個「用來生出其他 skill」的 skill，附帶效能量測、測試、eval、benchmark。典型用法：做完一整輪工作後說「用 skill creator 看完整段對話紀錄，把我們今天做的事變成一個 skill」。凡是一再重複的事都能這樣固化。

skill 之所以重要，是因為 **AI 本質非決定性**——同一件事做十次可能十種做法；skill 讓它趨近決定性、讓你拿回控制權。

### 實測：一張截圖加一個 skill

作者去 Pinterest 搜 SaaS landing page 找了一張參考圖，丟進去說「用 frontend design skill 重新設計這頁，做三個版本一起顯示在瀏覽器面板讓我挑，風格一致但要有足夠差異」。結果三版都跟原本天差地遠。用的只是 Anthropic 通用的前端設計 skill 加一段普通 prompt 加一張截圖——**一張截圖、一個 skill，結果完全不同**。

（順帶一提，桌面 App 的瀏覽器面板可以直接在頁面上選取元素加註解，註解會進 prompt，適合做微調。）

### 接外部工具：connector、plugin、CLI

要讓 Claude Code 控制外部應用，有三條路：

1. **Connectors**（Customize → Connectors）：Gmail、Google Calendar、Google Drive 這類最容易接，連上之後直接用講的就能讀信。大多數主流 App 都有。
2. **Plugins**：Browse 裡除了 Anthropic 官方（其實多半就是 skill），Partners 分頁有 GitHub、Supabase 等，底層通常是該服務的 MCP。
3. **CLI**：不是 MCP、不是外掛、不是 connector。GitHub 同時有 CLI 和 MCP，差別在實務上不大，但**CLI 通常提供比 MCP 更多功能，而且往往自帶 skill**。安裝一樣簡單：把 CLI 的網址貼進 Claude Code，說「把這個 CLI 加進來」。

作者的實例是完整部署管線：GitHub 建 repo 放程式碼，再自動接上 Vercel 拿到公開網址，全程沒有進過 GitHub 或 Vercel 的網頁介面。之後在 Claude Code 改網站，要同步上線也只是講一句。

更省事的做法是連工具都不用自己找，直接問：「我想部署這個網站，聽說有 GitHub 和 Vercel，也聽說可能有 CLI 或 MCP，你去看看合不合用，需要的話就裝起來，然後把部署管線接好。」沒帳號的話它會帶你註冊。

**核心心法**：只要在 Claude 之外操作任何東西，先問自己「這個能不能直接讓 Claude 控制？」——尤其你對那個應用不熟時，它多半操作得比你好。而隨著這類 agentic coding harness 越來越普及，幾乎每個 App 都會端出自己的 CLI／connector／MCP。

## 進階

### 長時程任務與 `/goal`

長時程任務由三部分組成：**觸發（trigger）、任務（task）、成功判準（success criteria）**。但不是所有長時程任務都是迴圈——有些只是要跑兩小時、十二小時甚至數天的單一任務，你不想讓它每次 context 塞滿就停下來。

Claude Code 內建 `/goal` 解決這件事。關鍵在於除了目標，**你還必須傳入成功判準**——不是「我要你做 X、Y、Z」，而是「終態長什麼樣」。運作方式是跑第一輪、比對成功判準，沒過就開新 session 再跑一輪，每輪都回看前幾輪哪些有效哪些沒效，直到達標為止（概念上類似 Ralph loop）。

因此**判準越客觀越好**。「做一個看起來很酷的網站」這種東西它無從在每輪結束時判定自己過了沒。

### Loop engineering

`/goal` 有明確終點；真正的 loop engineering 是要永遠跑下去、而且會自我改進的東西。在三要素之外要多加一個**紀錄（logging）階段**。

作者的示例是每日晨間簡報：

| 要素 | 內容 |
|---|---|
| 觸發 | 每天早上 7 點 |
| 任務 | 抓 YouTube、Twitter、Reddit 與 Gmail，彙整綜合成報告 |
| 成功判準 | 難的部分。可以塞入偏客觀的規則，例如每份報告至少要有 5 支 YouTube 影片、5 則 Twitter、5 則 Reddit，並點名 Gmail 裡的某幾類事項 |
| 紀錄 | 每份報告寫進資料庫，讓它能回看過往產出並與新產出比較 |

（作者坦承這比「對某個 Python 應用做迴圈、目標是跑到某個速度」難訂得多。）

實作步驟：

1. 用 skill creator 把上述描述做成一個 skill。
2. **手動反覆執行這個 skill 直到滿意**。
3. 滿意後在 skill 裡補上「產出要寫進資料庫，每次執行都要回看前幾次能不能做更好」——自我改進來自這一段。理想上還能替每份舊報告評分，給它一個客觀基準。
4. 轉成 automation：左側 Routines → New routine → Local，指示就寫「執行某某 skill」，排程可設每日、每小時、平日或自訂。

### Graph engineering

把整段流程包成一個大迴圈，改成**在每一步各跑一個小迴圈**：抓 YouTube 的 agent 自己有觸發、抓取、依過往結果自評、自我改進；抓 Twitter、Reddit、Gmail 的各自也是。一堆巢狀的微迴圈彼此對話，這就是 graph engineering。作者明說**對多數人來說完全是殺雞用牛刀**，知道概念即可。

### 動態工作流與 ultra code

**ultra code 不只是更高的 effort**：它會針對你的問題**現場組出一套客製 harness**，實務上通常是開一批 subagent。非常有效，也非常貴。

`/deep-research` 是預先做好的動態工作流範例。一般網路搜尋大概開五個 subagent 做 Google 搜尋，deep research 會開遠多於此——作者遇過**超過一百個**。流程是：出去抓資料 → 生出對抗式 agent 檢視資料、比對哪些禁得起檢驗 → 綜合 → 產出報告。示範那次它把問題拆成五個搜尋角度、開五個平行搜尋 agent、取前 15 個來源、**每條主張做三票對抗式查核**、最後綜合。

成本的實感：六個 agent 一開場就燒掉 31.4 萬 token；那次完整跑完是 **103 個 agent、600 萬 token，而且全在 Fable 上**。

**成本控制**：跑 ultra code 時若不特別交代，subagent 會沿用你當下的模型（Fable 就全部用 Fable，很危險）。可以在 prompt 裡明確限制「最多 20 個 subagent」「最多 50 個」，或指定「subagent 用 Sonnet／用 Opus」。

Anthropic 有一篇部落格說明動態工作流：底層是寫出編排腳本，在單一 session 內跑十到數百個平行 subagent，在結果送到你面前之前先自我檢核。常見型態包括 classify and act（分類器挑最適合的 subagent）、fan out and synthesize、adversarial review（後兩者合起來就是 deep research 在做的事）、generate and filter（錦標賽式多方案競爭加評審）、loop until done。跑 ultra code 時由 Claude Code 自行判斷該用哪一種，也可能是全新的組合。

作者認為 deep research 是其中最常用得到的：**要開始一個複雜專案、想在進 plan mode 之前先摸清全局時**，很值得先跑一輪。

### 模型路由：找第二雙眼睛

出發點是一個明確的限制：**AI 不擅長評自己的作品**。叫 Claude Code、Opus 或 Fable 評自己的產出，答案基本上都是「我做得很好」。當被評的東西又超出你自己的判斷力範圍時，問題更嚴重。

解法是引入另一個前沿模型。OpenAI 官方有給 Claude Code 的 **Codex plugin**（一樣是貼網址說要安裝），可以讓 Codex 對已寫好的程式碼做對抗式審查，或直接讓它負責特定功能。

作者自製的 **Grill Me** skill 把 Matt PCO 的 groom skill 與 Codex 的對抗式審查結合，專門用在規劃階段：你和 Fable 先談出計畫，計畫被路由給 Codex，Codex 與 Fable 最多來回五輪——Codex 指出哪裡錯、為什麼，Claude 或修正或表達不同意，直到達成共識為止。

同樣的模式可以往下延伸到更便宜的模型甚至本地模型。重點是**你不必被綁在 Opus、Haiku、Sonnet、Fable 上**，想接什麼都行，做成 skill 即可（一樣用 skill creator）。作者也提到 GPT 的 Sol 5.6 很強、Luna 與 Terra 極度 token 有效率。

### 客製 agentic OS

視覺外殼（社群數據、每日研究彙整、一排可點的 skill 按鈕、語音模式）確實好用，但作者強調**真正的價值不在那層視覺，而在背後的 skill 架構**。

所謂 agentic OS 的本質是：**把你每天要做的事全部盤點、對應成 skill，合適的再升級成 automation**。作者自己的 skill 依領域切成 memory、productivity（Gmail、行事曆）、research、content、community、AI agency、sales 等，每一項原本都是手動做的事。

建法就是前面講過的那套：用 skill creator，打開麥克風意識流講出自己每天每週在做什麼，問 Claude Code 哪些可以變成 skill，合適就做，反覆累積成一整套 skill 語料庫。

底下墊著的是 **Obsidian 記憶層**——就是傳說中的 Karpathy Obsidian 系統，本質只是**一套連貫的檔案結構**：一個 vault 資料夾，底下 `raw/`（原始資料與研究）、`wiki/`（把 raw 整理成的文章）、`output/`（從 wiki 產出的交付物，例如簡報）。**不必照抄這個切法**，重點是每往下一層都有一個 index markdown 當目錄。這樣即使有數十萬個檔案，人和 Claude 都導得動；導得動就更準、也更省 token。作者再次澄清：**Obsidian 本身不會給 Claude Code 什麼神奇加成**，它做的是讓一切可追蹤。

這類系統實際運作時用的是 **headless Claude**（`claude -p`），指令送進終端機、Claude 在背景隱形執行。作者補充：曾有一陣子傳言 Anthropic 要對這種用法收不同費率、不計入額度，**現在已經不是那樣**，所以這類系統在花費上跟其他用法一樣。

最後的結論是：agentic OS 這層外殼**不是必要的**，但底下那套 skill 架構是——那才是整件事的骨幹。
