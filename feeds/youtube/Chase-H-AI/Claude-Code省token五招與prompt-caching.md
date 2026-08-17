---
title: 你付給 Anthropic 的錢可能是實際需要的 20 倍
description: 拆解 prompt caching 的 20 倍價差與快取失效條件，並帶出 cache 冷掉後的收拾方式、模型路由與省 token skill
created: 2026-08-17
updated: 2026-08-17
source: https://www.youtube.com/watch?v=V0XbuApxlhg
published: 2026-08-05
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - token-optimization
  - workflow
---

作者的主張是：多數人在 Claude Code 上付的錢可能是實際需要的 20 倍而不自知，而問題的根源不是在 `CLAUDE.md` 裡寫一句「回答簡短一點」能解決的——是不理解 prompt caching 怎麼運作。影片給了五個層次的做法，並明說**第一個的效益大過其餘四個加起來**。

> 以下所有價格數字皆為影片錄製當時（2026-08）引用的官方定價文件內容，回查請以官方文件為準。

## 一、prompt caching：唯一真正重要的那一項

### 先理解 token 怎麼累積

Token 是 LLM 的貨幣，context window 是預算（Opus、Fable、Sonnet 都是 100 萬）。使用者送出的是 input token，模型回覆的是 output token，兩者**價格不同——output 大致是 input 的五倍**。

真正的問題出在後續訊息。你以為第二則訊息只送出了那幾個字，實際上**每一次都會把當下為止的整段對話重送一遍**，模型才有脈絡可讀。所以第二則訊息送的不是 6 個 token，而是前面所有 token 加上這 6 個。這件事會迅速滾成每則訊息 5,000、10,000、100,000 個 input token，而且你都在付錢。

### 快取如何介入

那為什麼大家沒有立刻燒光額度？因為有快取系統。

可以把 message cache 想成**擺在 Claude 面前的一份文件**，裡面是你們到目前為止的完整對話。送新訊息時，那整段歷史仍然要被讀，但是**以讀快取的價格讀**，而不是重新寫入的價格。

影片引用的價格結構：

| 項目 | Fable | Opus |
|---|---|---|
| output token | $50／百萬 | $25／百萬 |
| 基礎 input token（名目） | $10／百萬 | — |
| **1 小時 cache write** | **$20／百萬** | — |
| **cache read（cache hit）** | **$1／百萬** | — |

關鍵在於：**「基礎 input $10」某種程度上是個誤稱**，因為實務上你永遠在做 cache write，而訂閱制用的是 1 小時快取，寫入是基礎價的兩倍，即 $20／百萬。（定價表上還有一個 5 分鐘 cache write，那是給走 API 的人用的。）

$20 對 $1，就是那個 **20 倍**。

### 有快取與沒快取的實際差距

假設一段 50 萬 token 的對話，接著要送出一則 1,000 token 的新訊息：

- **有快取**：50 萬歷史以 $1／百萬 讀取 ≈ $0.5，新的 1,000 token 以 $20／百萬 計費（下一輪它就會併進快取文件）。
- **沒快取**：整個 50 萬要以 cache write 的 $20／百萬 重新計費，這一則訊息就要**約 $10**。

**同一則訊息，$0.5 變成 $10，差別只是你離開超過一小時。**

### 快取什麼時候會消失

- **閒置一小時**。注意是「無活動一小時」，每送一則訊息就重新計時；59 分鐘時再敲一則，計時器歸零。一旦過期，就算你只打了一句「嗨」，也會被以完整 50 萬 token 的全價計費。
- 除了時間，以下動作依 Claude Code 官方文件也會**直接重置快取**：切換模型（例如 Fable 換 Opus）、更改 effort level、fast mode、連接或斷開 MCP server、plugin 變動、拒絕工具呼叫、compact 對話，以及**升級 Claude Code 本身**。

任一項發生，下一則訊息就是本來的 20 倍價。

## 二、快取冷掉之後怎麼辦

離開太久，手上一段 20 萬到 50 萬 token 的對話已經失去快取，有三個選項：

| 做法 | 摘要放在哪 | 適用情境 |
|---|---|---|
| `/clear` | 不留摘要 | 有 code base 或專案檔案時通常就夠了——做過什麼，專案本身留有證據，新對話讀檔就能接上進度 |
| `/compact` | 注入新對話的訊息歷史中 | 對話裡有重要資訊、判斷光看程式碼不足以還原時 |
| 自訂 handoff skill | **寫成磁碟上的 markdown 檔** | 想要一份可以持續更新、能反覆叫它去讀的活文件 |

`/compact` 與 handoff 的差別只在摘要住哪裡：前者是那次對話裡的一則訊息，後者是實體檔案，開新對話時叫 Claude Code 去讀那份交接文件即可。作者自己有做一個 handoff skill，放在他的免費社群裡。

兩點提醒：

- Claude Code 有 auto compact，但**不要等它自己觸發**。到 60 萬至 80 萬 token 區間時已經開始遇到 context rot——更大更強的模型仍有這個問題。可以隨時手動 `/compact`。
- 更根本地說，這三個選項通常都比硬送新訊息好，因為**你本來就不該長期在 40 萬到 60 萬 token 的區間運作**。

## 三、模型路由：不要什麼都用 Fable

問題是：簡單任務能不能交給更小、更便宜、更笨的模型？可以，而且路徑不只一條。

### Advisor mode（留在 Anthropic 生態內）

作者認為這是最容易上手的方式。原始的 advisor 部落格文章示範的是 Opus 加 Sonnet，但同一套機制在 Fable 上一樣成立：

- 大模型（Fable 或 Opus）**負責出計畫**
- 小模型（Sonnet）**負責執行**
- 小模型遇到問題時可以把自己的 context 分享回大模型

宣稱的效果是**成本更低、結果更好**。而且呼應前面的主題：**advisor 與 executor 各自擁有自己的 prompt cache，同時運作**。

### 外部模型

- **Codex plugin**：Claude Code 有官方 Codex plugin，可從介面直接呼叫 Codex，等於把 advisor mode 的顧問角色換成 GPT 系模型。另有 Fable advisor 之類的 repo 做同一件事。
- 作者強調**自己寫一個做同樣事情的 skill 其實相當簡單**。
- 想找便宜模型的話，他特別推薦 GPT 的 **Luna 與 Terra**：一來價格大幅調降，二來 Anthropic 家族在那個價位帶沒有對應產品。
- 任務性質合適的話，也可以再往下接本地模型。

## 四、設定衛生：跑 `/doctor`

近期流傳 Claude Code 作者 Boris Cherny 說「你該把 `CLAUDE.md` 刪掉」的影片。作者的判斷是不必真的刪，但**該跑 `/doctor` 指令**（這個指令最近幾週有更新）。

它與 token 的關係有兩層：

**第一，精簡 `CLAUDE.md`。** 五系列模型**不需要那麼多指示**。三、六、九個月前大家寫的 `CLAUDE.md` 極度規範化、極度細節，當時或許還說得過去，現在已經不是這樣了。臃腫的 `CLAUDE.md` 不只讓它變慢，是實實在在在燒你的 token；`/doctor` 會把不必要的部分砍掉。

**第二，清理開場就佔掉 context 的東西。** 即使開一個全新對話、一則訊息都沒送，跑 `context` 一看就已經用掉一些額度——作者跑過 `/doctor` 清理後，全新對話**仍有 4 萬 token 起跳**，來源包括 skill、system prompt 與 memory 檔案。`/doctor` 會檢視 skill 與 MCP，把你根本沒在用的裁掉。

作者誠實標注：**這一項省下的 token 不多**，只是邊際效益，但簡單到沒有理由不做，尤其是過去半年不斷囤積 skill 卻從沒清理過的人。額外好處是**清乾淨後 skill 觸發得更準**——如果你有十個都跟前端設計有關的 skill，Claude 會搞不清楚該叫哪一個。

## 五、省 token 的 skill 與 scaffolding

作者明講這是五項裡**效益最低的一項**。

- **Ponytail**：目前最流行的，作用是在維持效果的前提下減少 Claude 寫的程式碼量，因而更便宜也更快。作者做過專門的驗證影片——該 GitHub repo 只提供了 Haiku 4.5 的數據，明顯過時；他用 Fable 實測，**數字站得住，而且在更好的模型上表現更佳**（用的是 repo 自附的 benchmark，實際效果會依專案複雜度而異）。
- **Caveman**：近期宣稱能減少 65% 的 output token。
- 還有很多人主張在 `CLAUDE.md` 裡寫一句「be brief」之類的單行指令，這確實會減少 output token。

但作者的收尾很直接：**output token 只是拼圖的一塊，而整張拼圖是被 prompt caching 主宰的**。這支影片如果只帶走一件事，就帶走第一項。
