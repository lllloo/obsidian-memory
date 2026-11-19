---
title: Justin Schroeder 把整個 harness 標準化
description: Schroeder 主張可靠性在 harness，以 TypeScript 規範整個 agent 與 runtime，讓小模型 agent 可攜可組合
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/talks/3Krz7Rdd4JI-every-company-is-building-agents-that-cant
published: 2026-11-10
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - agent-framework
  - evaluation
  - mcp
---

# Justin Schroeder 把整個 harness 標準化

來源：AI Engineer 2026 演講〈Every Company Is Building Agents That Can't Work Together〉的官方閱讀頁與機器逐字稿（YouTube `3Krz7Rdd4JI`，約 35 分鐘），落地於 [[AI-Engineer-Schroeder-Standard-Agent-Specification]]。規範、Builder 與論文的回查見文末。

**一句話**：企業一直在自建 agent，不是因為搞錯方向，而是因為讓 agent 可靠的東西都在 harness 裡：step 上限、tool 執行順序、失敗後保留什麼。prompt、skill、MCP 都帶不走這些。所以他要標準化整個 agent 加 runtime，讓窄領域、綁定小模型的 agent 可以打包、安裝、組合，「放進 USB 隨身碟交給別人」。

## 講者與立場

- Justin Schroeder，GitHub 自述是 Standard Agents 與 FormKit 的工程師，做過 dmux、ArrowJS、FormKit、AutoAnimate（[GitHub 個人頁](https://github.com/justin-schroeder)）。`standardagents` 組織底下確實有 arrow-js、dmux 等 repo。
- **這場是產品發表**：同場發表規範與自家 runtime「Standard Agents Builder」。規範由同一團隊維護；Builder 是 Standard Agents 自家產品，原始碼私有，正式部署走他們的付費 hosting（見回查）。所以「需要標準 runtime」這個結論，剛好也是他公司的商業模式，閱讀時要記得。

## 演講脈絡（照演講順序）

### 0:00 開場觀察：主流建議和市場行為不一致

主流說法是：用 MCP server 開放業務能力，再寫幾份 Markdown（skill、`AGENTS.md`），交給夠聰明的大模型就好。可是他觀察到大家還是在自己建 agent。他不認為這只是市場犯錯，而是有理由的，並歸納成三個因素。

### 1:05 因素一：Integration——企業就是它的流程

- 舉例：HVAC 維修公司的保固申請（是否在保固期、是否在保固範圍）、維修班排程、向州政府申請許可、行銷活動、帳戶擴展、工料管理；大學的助學金、補助行政、宿舍分配；雲端業者的濫用偵測與帳單爭議；還有薪資、合約審閱。
- 主張：「企業其實就是它的流程」。關係、網路效應、專有資料，都是流程跑得好的結果。
- 所以把核心流程整包交給通用大模型（他用 Grok Bot 當例子），即使大概跑得動，企業也不願意，風險太高。企業要的是**控制權**、可信任、**可重複**（同一張申請單每次得到同樣結果），而且不能太通用，要保留自家口吻。

### 4:16 因素二：Trust——「agent 什麼都能做，它就可能什麼都做」

- 玩笑例子：「保固申請送了嗎？」「登不進保固入口網站，所以我開了一個新帳號。順便回了幾封信、看了選舉結果。」它會這樣做，只是因為手上有這些工具。大模型通常不會犯這種錯，但不是不可能。
- 解法：由明確事件觸發（例如收到保固申請），agent 只拿到 `lookup equipment`、`attach photos`、`submit claim` 這類專屬工具。它仍然是完整 agent：可以多輪、追問缺漏、自己決定下一個工具，但**能做的範圍由工具決定，而不是靠相信模型不亂來**。

### 5:21 因素三：Efficacy（不是 efficiency）

- 問題不是模型夠不夠聰明，而是能不能把交辦的事做好、整體上是否比原本的流程更好。
- 保固申請這種小任務本身就是一個好 agent。重點是**每個業務流程都可以各自做 eval**：同樣的申請應該得到同樣處置，特殊個案就交給人。這些個案可以收集、標註、重跑。
- **Benchmaxing 翻成優點**：通用大模型被很多 benchmark 評測，會往被觀察的指標最佳化，但那些指標不一定是你要的。窄領域 agent 只有一件事要做，針對它的 eval 拚高分正好是目標。
- 對比現況：用頂級大模型（他舉 Opus 等級）加越來越多工具和 skill。他承認這樣行得通，只是很龐大。另一種做法是用 DeepSeek 的 Flash 級便宜小模型，只做一件事。
- 金句是「**Gmail agent 勝過 Gmail skill**」：不是說 skill 不能用，而是小模型 agent 更便宜，也能被 eval。
- 引 GEPA 論文：最佳化 agent 的 prompt 比微調模型更有效（他說「absolutely true」，回查後發現有過度概括，見下）。小模型只做 Gmail agent 時表現很好，要它做更多事才會崩。
- 組合方式：把 Gmail agent 以 MCP server 形式交給大模型，或者在一個任務明確的上層 agent 下面掛一層小 agent。

### 8:31 為什麼小 agent 還沒普及：因為大家各寫各的 harness（閱讀頁第 02 節）

- 大家其實都在建 agent，但用不同語言、工具、agentic loop，一團亂。agent 的基本結構很簡單（model、system prompt、tools、message history），真正難的是：loop 編排、能跑幾步、平行 tool 執行要有非同步機制、出錯後能接續的 durability。**「建 agent 其實就是在建 harness。」**
- 閱讀頁的例子：A 團隊做了好用的 Gmail agent，B 團隊要搬到自己的環境跑。只拿到 prompt 和 tool 描述，會漏掉關鍵程式：模型同時呼叫兩個 tool 時怎麼辦？最多幾步？請求失敗後哪些對話留下？兩家公司都講 MCP，這些問題仍可能各有不同答案。skill 能說明「應該做什麼」，A2A 能在 agent 之間傳訊息，但接收方還是要自己重做讓原 agent 可靠的那些行為。
- 只走 MCP 也會走回頭路：不少企業發現 tool 本身需要 inference 才有價值，接著需要多步 inference，最後等於在 MCP 裡重做了一個 agent 系統。
- 自訂 harness 會碰到三個問題：彼此無法分享（不一定能在對方的 hosting 環境跑）、難以組合（做法不同就根本不相容）、無法規模化（不可能每家自己做幾百個 agent）。他拿 skill 當對照：skill 也不是一個人寫完的，而是一整個生態系。agent 也需要「可分享的 agent 生態系」。

### 10:37 周邊都有標準，唯獨 harness 沒有

- 已有的標準：MCP（工具分發）、skill 與 `AGENTS.md`（某種 prompt 標準化）、A2A（agent 間溝通）、ACP，以及付款用的 x402（逐字稿誤辨為 X42）。他的說法是「harness 本身沒有任何標準，沒有 agent runtime 標準」（回查後發現此說過頭，見下）。
- 規範帶來四件事：**speed**（不必每次重造 loop，agent 作者不負責那一層）、**consistency**（每個 agent 用同樣方式建，但保留深度客製，客製要能在任何相容 runtime 自動生效）、**portability**（打包後放進 zip 或 USB 交給別人）、**composability**（小零件組成大系統，是領域 agent 能上市的關鍵）。
- 同場宣布 Standard Agent Specification 開源，網址是 standardagentspec.org。

### 12:44 規範的定義與五原則

- 定義：「agent 是**確定性軟體**，駕馭模型產生的非確定性結果，以達成目標。」他說名稱裡刻意有 harness 的意味：好 agent 就是好 harness，agent 可以看成 harness 的一個實例。
- 五原則：vendor-agnostic、domain-specific、**coupled to a model**、composable、portable。
- 他特別解釋兩條看似矛盾的原則。vendor-agnostic 指的是**部署和模型選擇不被單一廠商綁住**；coupled to a model 指的是**單一 agent 最好綁定一個特定模型**，因為不同 harness 會產生不同結果，大模型也一樣。

### 14:52 規範導覽：agent 是一包程式

agent 跑在 runtime 上，就像語言跑在 runtime 上：agent 定義是「語言」，runtime 才是被詳細規範的部分。一個 agent package 包含 model、system prompt、tools、subagents、agent rules、hooks、effects、thread。

- **一切都是程式碼**，理由有兩個：要能打包、發佈到 package registry；也要能「用 agent 寫 agent」（「手寫 agent 太瘋了」），所以這是 agent-first 生態系。
- **為何選 TypeScript**：他說不是因為偏愛，而是「在這個時代語言幾乎沒價值，只看產出物」。他認為只有兩類語言重要：Rust 類（極致效能）和 TypeScript。TypeScript 哪裡都能跑（edge、電腦、手機），而且是直譯式的，agent 寫完 agent 可以**不經建置或編譯步驟直接執行**。他也刻意避開 MCP「要有 server 才能提供工具」的模式，想把一切打包在一起。寫法是 `defineModel`、`definePrompt`、`defineAgent` 等強型別定義。

### 18:01 Models：釘死模型，利用 jaggedness

- 在程式裡定義的 model 就是**確切的模型**。可以設 fallback，他建議主模型失敗時改用更聰明一級的模型。
- **Jaggedness 當優勢**：他們有個 Model Zen Garden 專案（生成 3D 禪園），發現某個不算強的模型（逐字稿聽來是騰訊的模型，未核實）生成 3D 禪園特別好，成本又只有其他模型的零頭。對窄領域 agent 來說，模型偏科是好事。
- 反對「寫好 agent 後隨意換模型、然後祈禱」。他說效能要求高，所以幾乎總是應該**連同 quant 與 provider 一起釘死**。

### 19:06 Prompts、Tools、兩邊對話

- **Prompt** 負責對話的其中一邊。prompt 可以 include 其他 prompt，在 runtime 渲染（例如把公開的環境變數寫進 prompt）。所有 subagent 共用一份「語氣 prompt」，就能統一對使用者說話的方式。
- **Tool 有三種**：function（跑 TypeScript）、prompt（sub-prompt，用來在別處做一點推論，例如叫圖像模型生圖，或某模型講話較像人，不需要整個 subagent），以及 agent（把整個 subagent 當 tool 呼叫）。
- **對話一定有 side A 與 side B**，可以這樣搭配：
  - prompt 對人（像 ChatGPT）。
  - AI 對 AI，等於內建 QA：asset worker 生出帶浮水印的圖，asset reviewer 退回，worker 道歉後重生。
  - handler，也就是純程式。最簡單的 handler 不管收到什麼都回「continue」，所以甚至可以做出完全沒有 AI 的 agent。閱讀頁的重點是：**可預測的決定交給程式，推論只花在真正需要判斷的地方**。
  - prompt 對人，但其中一邊是 subagent。他說這有點繞，但「你的 coding agent 會搞懂何時該用」。

### 22:14 Subagents、parent hooks、hooks、effects

- **Subagent** 是有自己 side A／B 的完整 agent。例子：同一個 calendar agent 開兩個實例，一個管工作行事曆、一個管私人行事曆，各自在 parent 裡負責不同工作。
- **Parent hooks**：child 安裝到 parent 底下時，會自動掛上並修改 parent 的 hooks，**不必改 parent 的 prompt 告訴它「你有個子 agent」**。例如裝上 Gmail agent，parent 就自動知道怎麼用它。
- **Hooks**：在生命週期固定時點執行的確定性事件，例如 filter messages、before tool call、after update message，都寫在規範裡。
- **Effects**：排程執行的程式。通常由 tool call 排程，例如「別讓我忘了明天孩子的鋼琴發表會」就是 tool 排一個隔天觸發的 effect。閱讀頁特別區分：effect 在未來時間點執行，hook 在當前回合的固定時點執行（例如 tool call 前）。

### 24:22 Thread：每個 thread 是一個小沙箱

- 每個 thread 有自己的 messages、tools、subagents、**KV store**、**檔案系統**，也可以寫程式並執行（前提是你給它這個能力）。
- **Code execution**：agent 寫程式、存進 thread 檔案系統，再讀出來執行。作者要明確指定可以 import 什麼，也能禁止上網。他自己常配 code mode 使用，但規範對此不預設立場。
- **Decisions**：用決策模型判斷情緒，例如客戶是否不滿、要不要升級給真人（他提到某個型別安全的決策模型工具，逐字稿聽不清，未核實）。
- **Endpoints**：agent 可以開放自己的 HTTP endpoint，例如自己的 OAuth endpoint 或 API。他舉例可以做出開源、自架的 Grok Bot，或做出類似 Claude artifacts 的東西。
- **Packing**：可以打包成 npm package，發佈後任何人都能安裝、載入、直接跑。

### 27:34 Runtime contract：規定狀態怎麼處理，不規定怎麼實作

- 規範不決定實作方式，只規定各種 runtime 狀態怎麼處理：一步怎麼跑、執行程式時怎麼確保安全、檔案怎麼存。
- 例子是 `readFile`：他們的 hosted 版跑在 Cloudflare Durable Objects 上，`readFile` 實際上是讀資料庫，**根本沒有檔案系統**，但 thread 看到的就是檔案系統。換成本地 runtime，可以真的存在磁碟上。這個契約就是可攜性的關鍵。
- 自報案例：他們用很多小 subagent 組成一個完整 coding agent，「運作得很好」。因為都是 standard agent，還能像加 skill 一樣，把生態系裡其他人的 agent 裝進來。

### 28:36 Standard Agents Builder

- 他稱 Builder 是「規範的第一個公開 runtime」，已在 production 用一段時間（自報），說「今天就能 clone 到你的機器」，本地免費跑，推上他們的雲就能進 production。之後只要叫 coding agent 建新 agent，它知道不必重造 harness，只要確定性地定義該有的零件。
- 規範開放：把 coding agent 指向規範，叫它「幫我建這份規範的 runtime」。官方網站會連結大家做的 runtime。

### 29:39 Demo：電池保固 agent

- 他給 Claude Code 一份電池保固流程 PDF。影片有快轉，前段是 Opus 在讀 PDF。Claude Code 依流程寫出專屬的 tools、model 定義和 prompt。他說因為「架構已經被解決」，所以比平常快很多。**實際耗時 5 分 21 秒（自報）**。
- 產出：battery warranty agent 的 prompt 與 tools（`check battery`、`escalate to lead`、`offer trade-in`、`report safety issue`，還有 demo 中被呼叫的 `ship replacement`）。side A 是 prompt、side B 是人。model 定義名為 `warranty`，用 DeepSeek 的 Flash 級小模型。他強調這些 tool「只能做被指派的事」。閱讀頁補充：工程師 review 時可以直接拿這些操作和原始政策 PDF 對照。
- Builder 的管理介面可以看到所有 thread、呼叫的 tool、確切模型、成本、token 數、**cache hit 94%（單一請求的數字）**、送了哪 6 個 tool 給模型挑、模型選了 `ship replacement`，以及完整 request body。閱讀頁點出實用價值：如果該升級處理卻寄出了替換品，操作者可以回頭查模型當時有哪些選項。
- 對外介面：網站上的客服 chatbot 背後就是這個 agent。規範要求同時提供 HTTP API 和 WebSocket API。同一個 agent 也能以 MCP server 對外，讓用 ChatGPT 之類助理的人，透過他們的 agent 跟這個 agent 對話。

### 32:49 結尾：邀請大家來實作與挑錯

- 歡迎用任何語言實作 runtime（Rust、Go 都行），只要能執行規範裡的 TypeScript。也歡迎做領域 agent，並且「try breaking the spec」。他說「我們絕不是帶著完成品來的」。
- 類比早期 web：各家瀏覽器搶推獨家功能，靠一群熱衷規範的人做出全世界共有的標準。他希望 agent 也走一樣的路。

## 回查結果

| 對象 | 演講說法 | 核對結果 |
|---|---|---|
| [standardagentspec.org](https://standardagentspec.org) | 開源規範、今天發表 | 存在，首頁的定義句與五原則和演講逐字相符。首頁內嵌的正是這支演講。規範仍是 0.x 早期版本。[spec repo](https://github.com/standardagents/spec) 的 README 和 community 頁寫 MIT License，但 GitHub API 偵測不到授權檔（`license: null`）。repo 2026-01 就已建立，所以「今天發表」指的是公開亮相，規範之前已發展將近一年 |
| Runtime 契約（[runtime 頁](https://standardagentspec.org/0.2.0/infrastructure/runtime)） | host 要保證儲存與順序 | 對得上：runtime **MUST** 每個 thread 一次一步、**先持久化 messages 與 tool results 再繼續**、強制執行限制與停止條件。prompt 側的 step cycle 固定 7 步（drain queue → 組 context → 呼叫模型 → 持久化回應 → 執行 tools → 持久化結果 → 評估停止）。tool 錯誤必須存成 tool result，不得讓 loop 崩潰；單一 thread 不得同時跑多個 flow。**值得注意**：演講把「平行 tool 執行」列為 harness 難題，規範給的答案是「tool calls **MUST** 依回傳順序**序列**執行」，也就是用禁止平行來換取一致性 |
| 規範的組成 | model、prompt、tools、subagents、hooks、effects、thread 等 | 規範目錄有 Providers、Models、Tools（function／prompt／agent 三類）、Effects、Prompts、Handlers、Agents（兩邊各由人／prompt／handler 撐）、Subagents、Threads、Hooks、Type Registry；thread 層有 Messages、File System、Code Execution（沙箱的 `globalThis` 只留 ECMAScript intrinsics，host API 要明確橋接才有）、Decisions、Endpoints；另有 Packaging（npm）。與演講一致 |
| Standard Agents Builder | 「今天就能 clone」「本地免費跑」 | **部分對不上**：[builder repo](https://github.com/standardagents/builder) 只是 issue tracker，README 寫明「**The Builder source is private**」，不收 PR。實際以 npm 套件 `@standardagents/builder` 發行，授權欄是「SEE LICENSE IN LICENSE」，不是 OSI 開源。issue 範本有「local or hosted」選項，[Builder 文件](https://standardagents.ai/docs)寫「Production deployment uses Standard Agents hosting」，每個 thread 是一個 Cloudflare Durable Object 加獨立 SQLite，和演講說的 `readFile` 實作一致。[runtimes 頁](https://standardagentspec.org/runtimes)目前**只列這一個 runtime**，並註明「列名不代表背書，也不認證合規」 |
| GEPA 論文（逐字稿誤辨為 Jeepa） | 「最佳化 prompt 比微調模型更有效，absolutely true」 | 論文存在：[arXiv 2507.19457](https://arxiv.org/abs/2507.19457)，標註 ICLR 2026 Oral。實際範圍是：反思式 prompt 演化在 **6 個任務**上平均勝過 RL 方法 GRPO 6%、最多 20%，rollout 最多少 35 倍；也勝過 prompt 最佳化器 MIPROv2 一成以上。方向支持他的說法，但**比較對象是 GRPO，範圍是 6 個任務**，「absolutely true」是過度概括 |
| 「沒有任何 harness／runtime 規範」 | 「no such spec exists until today」 | **說過頭**：Oracle 的 [Open Agent Specification](https://arxiv.org/abs/2510.04173)（2025-10，[oracle/agent-spec](https://github.com/oracle/agent-spec) repo 仍在維護）就是「定義一次、跨 runtime 執行」的框架無關 agent 規範，附參考 runtime 與跨 runtime 評測 harness。差別在於 Agent Spec 是**宣告式**語言，Standard Agents 是**程式碼加 runtime step 語意**。可以說取向不同，不能說之前沒人做 |
| DeepSeek Flash 小模型 | demo 用 DeepSeek 的 Flash 款 | DeepSeek API 的[新聞頁](https://api-docs.deepseek.com/news/)確實有 V4 世代的 Flash 型號，存在無誤 |
| 官方 skills | 結尾叫大家「幫 coding agent 加個 skill」 | [standardagents/skills](https://github.com/standardagents/skills) 目前只有 bro、code-quality-setup、papercuts、streamline 四個，**沒有撰寫 standard agent 的專用 skill**。規範站提供 [`llms.txt`](https://standardagentspec.org/llms.txt) 與 `llms-full.txt` 給 coding agent 讀 |

未能核實：5 分 21 秒（影片有快轉，數字是自報）、94% cache hit（單一請求）、「已在 production 用一段時間」、用小 subagent 組成 coding agent「運作很好」、Model Zen Garden 與某模型擅長 3D 禪園的說法、決策模型工具的名稱（`standardagents` 組織下有個 jevpilot repo 自述「Jev-powered autopilot」，推測是同一工具，未確認）。

## 搬到個人 Claude Code／Codex 流程

**可以直接用的：把他的設計原則落到 subagent 與 eval 上**

1. **用工具清單劃權限，不要靠 prompt 叮嚀**：在 `.claude/agents/<name>.md` frontmatter 用 `tools`（允許清單）或 `disallowedTools`（拒絕清單）限縮能力，例如審查用 subagent 不給 `Write`／`Edit`；`maxTurns` 對應規範的回合上限 rule（欄位見 [Claude Code subagents 文件](https://code.claude.com/docs/en/sub-agents)）。這就是「什麼都能做就可能什麼都做」的個人版。
2. **固定模型，換模型要先過 eval**：同一份 frontmatter 用 `model` 釘住模型。想把重複性高的窄任務（分類、格式轉換、批次摘要）換成便宜模型時，先準備 10–20 個真實案例加上預期結果，新舊模型各跑一次比對，不要直接改了就用。
3. **重複流程先做成可重跑的案例集**：把「同樣輸入應該得到同樣處置」的標準寫成案例檔放進 repo，改 prompt／skill 後重跑。這比追通用 benchmark 更能回答「下一次會不會做對」。
4. **能確定的步驟交給程式**（他的 handler 思路）：固定格式檢查、路由、繼續／停止判斷，用 hook 或腳本做，模型只處理需要判斷的部分。這和 [[Lauren-Tan-把糾正寫進程式庫]]「把糾正變成確定性檢查」是同一方向，只是一個講 agent 架構、一個講程式庫。
5. **共用片段只寫一份**：好幾個 subagent 都要遵守的口吻或格式，抽成一份 skill 或共用指示讓它們引用，不要每個 agent 複製一遍（對應他的 prompt include）。
6. **出錯時回頭看模型「當時有哪些選項」**：他的 inspector 重點是看送出的 tool 清單和 request body。個人環境的對應做法是查 session transcript，確認當時載入了哪些工具和指示，再決定改工具清單還是改 prompt。

**想試規範本身的話**：把 coding agent 指向 `https://standardagentspec.org/llms-full.txt`，請它依規範寫一個單一用途 agent 的 TypeScript 定義（model、prompt、2–4 個 function tool）。要真的跑起來就需要 Builder（npm 套件，原始碼私有）。

**不建議搬的，以及原因**：

- **個人開發工作流不需要採用這份規範**。它要解決的是「把業務 agent 交給別的團隊或客戶，在不同環境照樣運作」。個人用 Claude Code／Codex 寫程式時，harness 已經由工具提供，缺的多半是知識和慣例，用 skill 或 `AGENTS.md` 補比較便宜。這也是 [[Context-優先與多-agent-的適用邊界]] 的判準：缺知識就補 context，不要新建 agent。
- **生態系還沒形成**：規範是 0.x 版，runtime 只有一個，而且是發起公司自家的閉源產品，也沒看到第三方實作或合規測試。現在投入等於綁在單一廠商上，正好違反它自己的 vendor-agnostic 原則。
- 「Gmail agent 勝過 Gmail skill」的前提是**大量執行、在意單位成本、能為窄任務做 eval**。個人偶爾查信沒有這些前提，交給手上的 coding agent 加 skill 就夠了。

## 證據強度與限制

| 主張 | 強度 |
|---|---|
| 可靠性取決於 harness 行為（step 上限、tool 順序、失敗持久化），只交出 prompt／MCP 帶不走 | 中：架構論證合理，也和 [[Agent-Harness-Engineering-框架綜述]]「Agent = Model + Harness」的業界共識一致；但「換 harness 結果就變」他沒有給量化證據 |
| 窄領域小模型 agent 比大模型加 skill 更便宜，且可以被 eval | 中低：成本面是常識；「效果一樣好甚至更好」只有 Model Zen Garden 等自報軼事，沒有對照實驗 |
| GEPA：prompt 最佳化勝過微調 | 論文本身是同儕審查（ICLR）證據，但僅限 6 任務、對比 GRPO；演講的「absolutely true」**勿引用**為通則 |
| 5 分 21 秒做出保固 agent | 自報、單一 demo、影片有快轉、沒說人工改了多少，也沒有對照組 |
| 94% cache hit | 單一請求的畫面數字，不代表平均 |
| Builder 已在 production 穩定運作 | 自報，沒有外部佐證 |

**勿引用**：

- 「在 Standard Agent Specification 之前沒有任何 agent runtime 規範」：Oracle Open Agent Specification（2025-10）是反例，只是取向不同（宣告式 vs 程式碼）。
- 「Standard Agents Builder 開源、可以 clone 下來跑」：Builder 原始碼私有，開源的是規範文字。
- 「最佳化 prompt 比微調模型有效，絕對成立」：GEPA 只在 6 個任務上對比 GRPO。

## 張力與互補

- **與 [[Context-優先與多-agent-的適用邊界]] 的衝突**：該頁判準是「缺知識就補 context（skill／`CLAUDE.md`），不建新 agent」，Schroeder 則說「Gmail agent 勝過 Gmail skill」。兩者適用場景不同：該頁處理的是個人 coding 這類寫入多、需要全域一致的任務；Schroeder 處理的是**大量重複、可窄化、要交付給別人跑**的業務流程，看重單位成本、權限邊界和可 eval 性。他的組合方式（parent 下掛多個 subagent）仍要承擔該頁 MAST 證據列出的多 agent 協調代價，演講沒有談到這點。
- **補充 [[Agent-Harness-Engineering-框架綜述]]**：該頁整理 harness 的範疇（loop、tool routing、停止、錯誤恢復、狀態持久化），本場把這些範疇**寫成規範條文**（runtime MUST 先持久化再前進、tool 序列執行、單 thread 不並行），等於把 harness 從「各家實作」推向「可互換的契約」。
- **呼應 [[Lauren-Tan-把糾正寫進程式庫]]**：兩人都主張把可靠性放到確定性機制上，而不是靠散文指示。Tan 寫成 lint／型別／架構，Schroeder 寫成工具白名單、handler 與 runtime 契約。
- **與 MCP 的關係**：他沒有否定 MCP，而是把它降級成分發和對外介面（agent 可以用 MCP server 對外），認為 MCP 只標準化工具，沒有標準化 loop 行為。MCP 協議本身的演進可對照 [[MCP-無狀態化-2026-07-28]]。
- 本場在 [[AI-Engineer-2026-演講精華-AI-工作流程]] 的綜合頁中被歸在「能確定性處理的就不用 LLM」一類。
