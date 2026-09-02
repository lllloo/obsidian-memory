---
title: OpenClaw 與 Hermes 的實地使用心得
description: HN 使用者對兩套常駐 agent 的第一手證詞：熱度崩落、維護成本吃掉價值、自我進化的複利同時是負債，與少數撐住的日常用例
created: 2026-09-02
updated: 2026-09-02
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - agent-framework
  - memory
---

# OpenClaw 與 Hermes 的實地使用心得

[[OpenClaw-與-Hermes-Agent-比較]] 收的是官方文件講的**能力**；本頁收的是使用者講的**實際跑起來如何**。兩者刻意分頁：證詞的強度與官方 release notes 差一個量級，混在一起會稀釋強度標註。

> **證據強度（適用全頁）**：全部為 Hacker News 個別使用者的自陳，非實測、非抽樣調查。三重偏誤要先扣掉——HN 群體對 AI agent 明顯偏懷疑；會留言的人本身有立場（狂熱或幻滅），中間狀態的人不發言；使用時長差異極大（下引證詞從「試 10 分鐘」到「用了幾個月」都有，已逐條標註）。留言 id 皆可回 [news.ycombinator.com](https://news.ycombinator.com) 查證原句。主要來源：[49505310](https://news.ycombinator.com/item?id=49505310)（OpenClaw 2.0, Accidentally，173 則）、[48419000](https://news.ycombinator.com/item?id=48419000)（Hermes Agent，42 則），2026-09-02 經 Algolia API 逐則核對原文。

## 貫穿兩者的共同失效模式：自主生長會把自己壓垮

這是本頁最值得留下的一條，因為它是**兩套系統各自獨立長出來的同一個病**：

- **OpenClaw 靠功能堆積壓垮自己**：`LaurensBER`（從發布用到現在）說「stuff breaking with every update... my primary usecase seems to be to use the CLI to fix whatever broke this week」——維護成本吃掉了工具本身的價值。
- **Hermes 靠 skill 累積壓垮自己**：`iagooar` 說「it tends to keep growing skills and overhead over time, **to the point it is becoming utterly slow and sluggish**」，同時明確區分「core 是紮實的，Desktop 那層像沒品味的 vibecode」。

**這正是本 vault 給 [[MEMORY]] 訂 40 行上限、給 `vault-lint` 訂「只抓真的壞了、不抓能更好」的同一個問題**，只是載體不同——他們長的是 skill 與功能，本 vault 長的是筆記。差別在本 vault 的上限是**硬性報錯**而非軟性建議，這與 [[Hermes-Agent]] 有界核心記憶「寫爆時直接報錯、不自動摘要」的設計同源。相關失效機制見 [[Agent-維護知識庫的已知失效模式]]。

## OpenClaw

### 熱度崩落是留言區的共同前提

2.0 發布串的第一則就是 `minimaxir` 問「who is still using OpenClaw?」，稱熱度在三月後掉下懸崖已是個梗（附 Google Trends 連結，該圖本頁未查證）。**整串沒有人反駁這個前提**——在一個慶祝重大版本的討論串裡，這件事本身就是訊號。

### 反覆出現且彼此獨立的抱怨

| 抱怨 | 證詞 | 使用時長 |
|---|---|---|
| 已有 coding agent 的話加值有限 | `atonse`：「it mainly brought the power of do-everything coding agents to your phone... **you exchange a low quality messaging interface for that ease of access**」 | 自 1 月起試過多輪 |
| 功能被 coding agent 吸收 | `stingraycharles`：coding agent 自己長出了遠端存取、instance 互相對話 | — |
| 不給回饋、難建立信任 | `soundworlds`：Claude Code 與 Hermes 會「take you along for the ride」，OpenClaw 的感覺是「**trust me bro, I've got this**」 | **僅 10 分鐘，樣本很輕** |
| 文件量嚇退人 | `whinvik`：「every time I go to the docs I give up... I would want something simpler, maybe an `OpenClaw-lite`」 | 多次嘗試未成 |
| 臃腫遲滯 | `saratogacx`：「quickly turned into a lethargic mess」，改用 10MB 的 Go 實作 picoclaw | 試用後放棄 |

最後一條有結構性意義：**輕量分身生態（picoclaw、nanoclaw、`rcarmo` 自寫的 piclaw）的存在本身就是對臃腫的投票**。

### 安全：兩造都在

- ⚠️ **勿引用**：`Topfi` 稱「almost 600 CVEs in less than a year, roughly two per day」——單一留言宣稱，本頁未查證，引用前必須自行核實。
- 反方：`stbenjam` 認為 prompt injection 風險被誇大，「vanishingly small with the latest frontier models」，並說自己不會給它 bitwarden 全權但有部分登入權。
- 打臉反方的具體證詞：`mechazawa`「prompt injection has been super easy for ages. Heck I do it sometimes against coworkers who process my review comments using claude. I'll tell claude to edit its global claude.md file or even dump a key from their env and **it'll do it without confirming with their user**」——這是宣稱的實作經驗，非受控實驗。

### 撐住的日常用例（形狀比清單重要）

- `teekert`：爬 API、收職缺 email 比對個人檔案、email 轉 PDF 進記帳軟體。他自承「in many cases the AI just sets up a cronjob and a script」，價值在**它處理 edge case、會自己修腳本**，且能用 Telegram 下「pause all processing until further notice」。跑在與重要資產隔離的 Hetzner VM、只碰公開資料。
- `xcjs`：逆向工程被 Google 政策淘汰的 Android 遊戲做媒體保存。相對一般 harness 的優勢是「**automatic session resumption after power loss**」與長時 loop 工具。
- `tidbeck`：幼稚園通知截圖丟給它，之後問它、讓它提醒特殊放假時間。
- `rcarmo`：自寫 piclaw 管 homelab（scoped Proxmox token + Portainer），**刻意不走 messaging app**：「I don't think any messaging app will provide a good (or trustworthy) way to get to my own machines, so Tailscale+web it is」。

`camillomiller` 提了最誠實的質疑——「all you describe would be easily scriptable like 5 years ago」。最有力的回應來自 `oarsinsync`：重點不是做了以前做不到的事，而是「**it enables more people to do the thing that was limited to fewer people**」；但他隨即補刀，說搞不懂本來就會寫 script 的技術朋友「crying about burning through multiple $200 claude subscriptions a month, filtering email」。

## Hermes

### 正面：與本 vault 幾乎同一套做法

`igorhvr`（2026-06）是本頁**對 LLM Wiki 模式最有價值的一則證詞**：

> Hermes basically rules my personal life at this point - it is a _very_ useful personal assistant. [...] Hermes uses an **llm-wiki** as a source of information when drafting suggested replies - I have a **cronjob that feeds it all emails, slack messages, meeting minutes every single day**.

他直接連 Karpathy 的原始 gist，用 LLM Wiki 當回信的知識來源，每日 cron 餵 email／Slack／會議記錄，並用 humanizer 校準自己的語氣。**這是目前唯一一則「LLM Wiki 模式在真實日常負載下跑得動」的第一手證詞**（見 [[LLM-Wiki-知識管理模式]]、[[LLM-Wiki-生態實作比較]]）。與本 vault 的關鍵差異：他是**自動餵**，沒有本 vault「使用者精選原料進 `raw/`」那道閘門——長期品質如何未知，該串無後續。

`rnxrx`（2026-04，用了幾週）：跨三四台機器與多個帳號，「having a competent agent with constant state has been good for memorializing and organizing important info (**directly into Obsidian, too**)」，跑在鎖緊的便宜 VPS 上，並說 self-reinforcement learning 與 skill 累積確實越用越有用——「Surprised even」。

### 負面：全部指向自我進化的代價

- `iagooar`：skill 與 overhead 越長越多，慢到不堪用（見上「共同失效模式」）。
- `sshine`（試過 claude／opencode／pi／hermes／openclaw 五套）：「Hermes: Sluggish, very slow to start, a lot is going on in the background... Seems over-engineered... **I'd rather have full session logs rather than these MEMORY.md summaries of what a session did.**」

最後那句是**對摘要式記憶最直接的反對票**，且出自試過五套 harness 的人。它打在本 vault 的設計選擇上：`schema/MEMORY.md` 走有界摘要，而完整時序真相放 git——等於兩邊都留，`sshine` 要的 full log 在 vault 裡是 `git log`。這條分歧的更完整框架見 [[Agent-記憶兩大路線-知識庫與-memory-bank]]。

### 治理爭議

- `jdiff`：CLI 卡頓閃爍、每次啟動強制掛 header 且確認過無法關閉；並提及抄襲爭議。
- `cassianoleal` 記錄了處理方式：`teknium1` 把 GitHub issue 全文替換成一個句點、Nous 刪除後續留言——「Whether the claims have merit or not, attempting to make the claim go away in this way is at best unprofessional and childish」。
- ⚠️ **抄襲指控本身本頁未查證**，此處只記錄「**處理方式**引發社群反彈」這件事，不對指控是否成立表態。

## 對本 vault 的三點

1. **自主生長的系統會自己把自己壓垮**（見開頭）——OpenClaw 從功能側、Hermes 從 skill 側，殊途同歸。本 vault 的硬上限與「只抓真的壞了」的 lint 紀律是對症的，這兩則證詞是外部支持。
2. **`igorhvr` 證明 LLM Wiki 撐得住每日 email／Slack 量**，但他沒有原料閘門；本 vault 的手動 ingest 是更保守的一端，兩者的長期品質差異目前無證據可判。
3. **摘要 vs 完整日誌是真實分歧，不是已解問題**——`sshine` 的反對票值得留著，日後若有人抱怨 vault「記得不夠細」，這就是同一個張力，而不是本 vault 獨有的缺陷。

## 關聯

- 能力面對照：[[OpenClaw-與-Hermes-Agent-比較]]——官方文件講的能力，與本頁的實跑證詞互為表裡
- 實體頁：[[Hermes-Agent]]
- 失效機制：[[Agent-維護知識庫的已知失效模式]]——本頁「自主生長壓垮自己」的機制層對照
- 記憶路線：[[Agent-記憶兩大路線-知識庫與-memory-bank]]、[[LLM-Wiki-知識管理模式]]
