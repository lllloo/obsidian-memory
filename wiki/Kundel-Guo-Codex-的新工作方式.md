---
title: Kundel 與 Guo 的 Codex 新工作方式
description: OpenAI 講者示範 Codex 的 context 收集、快速迭代、雲端環境、Sites 與委派，附官方文件回查與可搬做法
created: 2026-11-19
updated: 2026-11-19
source: https://www.youtube.com/watch?v=IPh9YsWvDQk
published: 2026-11-17
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - context-engineering
---

# Kundel 與 Guo 的 Codex 新工作方式

**一句話主張**：要讓 coding agent 做好長時間工作，先讓它拿到你所在的所有 context（repo、Slack、文件、畫面、操作習慣），再依任務決定速度與推理量，最後把工作交給雲端、語音或常駐 agent 繼續推進。你不必親自盯每一步。

來源是上傳者提供的英文字幕全文 [[AI-Engineer-Kundel-Guo-New-Ways-of-Working-with-Codex]]，配套的官方 workshop 資源頁另存為 [[OpenAI-AIE-Codex-Workshop-Resource]]。ai.engineer 站內沒有這場的閱讀頁。

## 講者與立場

- **Charlie Guo、Dominik Kundel**：兩人都在 OpenAI 開發者體驗團隊，工作包括寫文件、做發表影片與上台演講。Guo 提到他上次出現在 AIE 是年中的 World's Fair workshop。
- **立場**：這是 OpenAI 員工介紹自家產品的場次，內容幾乎都是產品功能導覽與 demo，沒有和其他工具比較，也沒有失敗案例或量化成效。適合拿來了解 Codex 有哪些功能和官方建議怎麼用，不適合當成「這樣做比較好」的證據。
- 場地是 CODE Summit 2026，影片描述與 workshop 頁都這樣寫。字幕裡把場次稱為 AIE。

## 演講脈絡（依演講順序）

### 1. 開場：Codex 沒有死，而是變成一套共用的 harness（0:00–3:50）

- Guo 回應網路上「Codex 已死」的說法：Codex 現在出現在更多地方、功能更多。今年最大的變化是 Codex 和 ChatGPT Work 合併，因此有「數千萬」更多人用到同一套長時間運行的 agent harness。這個數字是自報，台上有一張使用量曲線圖，字幕看不到具體數值。
- 第一版 Codex 本來就是雲端 agent：在自己的環境 checkout repo、遠端完成工作。之後轉向本機，現在又慢慢回到雲端：一方面做遠端控制你自己機器上 Codex 的工具，一方面提供更強的雲端環境。
- 同一套 harness 驅動 ChatGPT Work、CLI、Slack 裡的 `@ChatGPT`、Dots 和 Agents API。workshop 頁補充，這套 harness 是開源的 `openai/codex`，而且有 App Server protocol 可以把它嵌進自己的 app。
- 他說 7 月到 11 月推出的功能多到投影片放不下。接下來的主題依序是：context、迭代、到處都能跑、出貨、委派，最後是一輪快速 tips。

### 2. Context：從「把 context 拼完美」轉向「模糊下指令」（3:50–13:00）

- Kundel 認為前兩年大家在練 context engineering，現在逐漸變成 **vague prompting**：像跟已經知道背景的同事說話一樣，不必每件事都講清楚。他說「沒有人想和要逐條交代的同事共事」。
- 這要靠 agent 自己會找 context。Codex 一開始就要在 OpenAI 的巨型 monorepo 裡工作，所以模型和 harness 都被要求在大 repo 裡大海撈針。
- **repo 內的規範放 repo**：coding standards 寫進 `AGENTS.md`、linter 和其他檢查。判準是：一個優秀工程師進到 codebase 應該能不犯錯地貢獻，agent 也一樣。
- **repo 外的 context 用 plugin**：plugin 是 MCP server、skill 和其他資源的組合。官方 marketplace 的 plugin 多半用 remote MCP。在一個介面連過一次（例如在網頁 ChatGPT 接 Slack），其他用同一套 harness 的介面（dev box 上的 Codex、Slack 的 `@ChatGPT`）都能用同一個連線。plugin 可以只在公司內分享，也可以在 GitHub 公開一個 marketplace。
- **例子一**：他給 Codex 一句沒寫清楚的指令，沒說是哪個 Slack 頻道、哪位 Katya。Codex 能做是因為它連著 Slack 與 Google Drive，可以自己找到訊息和裡面分享的試算表。
- **例子二（發表日的文件站上線）**：某次發表要在週日午夜更新文件站。他和 Codex 先準備好 PR，然後交代 Codex：持續爭取 approval、盯 Slack 頻道有沒有最後一刻的變更、因為部署要 20 分鐘所以提前 20 分鐘上線，上線後確認網站正常。結果午夜過 4 分鐘 Codex 回報已上線。前一天同事在 Slack 問 preview URL，Codex 也替他回覆了，同事回「looks good」。這是單一軼事，沒有提到失敗或誤回覆的風險。
- **Plugin extensions**：plugin 可以擴充桌面 app 與 ChatGPT 網頁版、行動版的介面，例如側欄入口、側邊面板、整頁視圖、檔案檢視器與 composer。Codex 自己的 Sites、Code Review、Security 等頁面也是用同一套 plugin 機制做的。demo 是他用一個 prompt 讓 Codex 做出的「design system」plugin：在 app 裡瀏覽公司的元件，按「add to composer」就把元件 context 注入對話；在 composer 打 @ 也能搜尋元件。他舉例，裝了 Figma plugin 就能自動完成 Figma 檔名。

### 3. Appshots、Computer Use、Computer History（13:00–17:50）

- **Appshots**：在 Mac 上同時按左右兩個 Command 鍵，Windows 上按左右兩個 Alt 鍵。截圖時會一起送出 accessibility tree 的文字，包括畫面外、要往下捲才看得到的內容。他說這是被低估的功能，現場舉手用過的人很少。
- **Computer Use**：沒有 plugin 可用時，讓 Codex 操作 app 取得資訊或測試，例如操作 iOS simulator。在 macOS 上可以完全在背景執行，它有自己的游標，不會占用你的電腦。
- **Chrome extension**：不想給整台電腦權限時，只讓 Codex 用你已登入的瀏覽器分頁。他說 Windows、Linux、macOS 都能在背景執行，不會搶走你正在用的分頁。
- **Computer History**（目前只有 macOS）：開啟後要累積一段時間才有用。它記錄你怎麼使用各個 app，並轉成記憶。例子是 Codex 學到他寫 blog 會先在 Google Doc 起稿，後來他改在 ChatGPT Space 起稿，Codex 也跟著學到。它用 macOS 的事件串流而不是截圖，所以比較省 token、也比較快。隱私控制包括：隨時暫停、事後清除最近一段紀錄、排除特定網站或 app；無痕瀏覽本來就不收。

### 4. ChatGPT Space：人和 agent 一起改的文件（17:50–20:50）

- 痛點：context 散在 PRD（Google Doc 或 Notion）、repo 裡的架構圖、業務寄來的試算表之間。常見做法是把 Codex 寫的計畫 commit 進 repo 再用 PR review，但這樣很難反覆修改；有人改成在 Google Doc 和 repo 之間來回貼。
- ChatGPT Space 的做法：請 Codex 把計畫變成一個 Page，成為可以直接編輯的富文本文件。在文件裡可以標記 ChatGPT 提問，也可以標記同事；同事也能標記自己的 ChatGPT 或 Dot。頁面裡可以放 HTML 做成的視覺化物件。
- 頁面可以加 **instructions**，他形容是「單頁的 `AGENTS.md`」。agent 改頁時會遵守；開啟 auto update 後，會照排程依 instructions 更新頁面。例子是 on-call runbook 常常忘了更新指令。workshop 頁的例子是每晚把 `#alpha-feedback` 頻道的新回饋加進 bug tracker。

### 5. 迭代：Ultrafast 與 browser annotations（20:50–28:25）

- 情境：沒有設計稿、還在摸索方向時，需要快速來回試。
- **Ultrafast**：他說在 Dev Day 推出，「快 8 倍、成本 6 倍」。他特別強調**不要一律開**：如果任務的時間大多花在編譯、build 或 e2e 測試（例如 iOS app、遊戲），你幾乎感覺不到加速。它適合讓人回到心流狀態：從自己寫 code 變成交給 agent 之後，他懷念的是快速試想法的協作節奏。
- **具體設定**：要有 hot reload 的 dev server，不然 Ultrafast 沒有意義。推理量調到 light；比較複雜或細節多時才調 high，「大多數時候我都開 light」。第一個任務會慢一點，因為要先讀檔，瓶頸常在檔案系統。之後他把需求切得很小、一次一件，有時直接靠在椅子上用語音口述，連續丟出好幾個指令。demo 是一個音樂網站：刪 header、header 改全螢幕、加背景動畫、讓唱片像真的黑膠會轉、讓唱片可以用游標刮。單次改動約 5–10 秒。
- 真實案例：Dev Day 前一晚，他用這種方式把 ChatGPT Space 文件頁上的功能示意做成 HTML 小動畫，不是影片。他說每做一輪，對自己想要的結果就更清楚一點。
- **Annotations**：在桌面 app 的內建瀏覽器點選頁面元素給精準回饋，也可以先在頁面上即時調整樣式看看感覺。預設以 DOM 決定哪些元素可以選。**Annotations API** 讓你自己定義可選範圍，例如 design system 只讓單一元件可選、Storybook 外框不可選；Game Boy 模擬器 plugin 只能標註遊戲畫面，不能標註模擬器本身。workshop 頁給的屬性是 `oai-annotation-container` 與 `oai-annotatable`。

### 6. 到處都能跑：Codex Cloud 與 remote（28:25–37:05）

- 去年大家對 agent 跑 7 小時就很興奮，現在任務能跑好幾小時甚至好幾天。很多人因此買 Mac mini、把舊筆電塞桌下或租 VPS 當 dev box。他認為這樣做好玩可以，但對企業來說要處理設定、更新、擴充、磁碟爆滿等問題，無法長期維持。
- **Codex Cloud 重做**：Codex Cloud 在前一年推出，他說要等模型和 harness 成熟才做得出好體驗，所以在 Dev Day 推出新版。重點有：
  - 可以從 composer 直接開新環境，一次選多個 GitHub repo。
  - **Codex 會自己設定環境**：判斷需要哪些依賴、API key、啟動 dev server 與跑測試的指令。以前要手動設定，現在 Codex 先跑一輪再回報，你仍可以修改。
  - demo 選了 web 和 mobile 兩個 repo。Codex 發現 Linux VM 不能 build iOS，回報做不到，但仍保留 mobile repo 當參考，這樣才能「把 mobile 上的新功能也做到 web player」。他說之後會支援自帶硬體環境，例如雲端 Mac。
  - 環境會做 **snapshot 並持續更新**：隔幾小時再派任務也應該能立刻開始；背景會定期更新依賴、拉 main 的最新變更。
  - 環境設定可以控制網路存取與 secrets，也可以分成團隊共用和個人自填。無法公開連線的內部資源可以用 **OIDC** 或 **Tailscale** 存取，不必把服務開到公網。
- **Codex Remote**：手機可以透過 ChatGPT 帳號遠端操作你的電腦，也可以走 SSH。他說很多人誤以為遠端主機一定要裝桌面 app，其實在 dev box 上執行 `codex remote-control start` 就會啟動 app server，手機就能連上。

### 7. 出貨：ChatGPT Sites 與 Code Review（37:05–45:00）

- **Cutroom**：團隊內部用 ChatGPT Sites 做的剪片網站。攝影師上傳素材，團隊留言、補螢幕錄影或 B-roll，送審後交給遠端的 Codex agent。這個 agent 能操作 DaVinci Resolve，也有剪輯 skill，會自己剪出新版本、上傳並通知大家 review。他說發表影片的剪輯「大部分快要自動化了」，一些次要影片完全由 agent 剪好。這是自報，沒有給影片數量或品質標準。
- **Sites 不只是靜態託管**：有 D1 資料庫、R2 物件儲存、Sign in with ChatGPT 驗證、analytics、secrets、plugin。他最喜歡的是 Sign in with ChatGPT：不必自己做 auth，可以依使用者限制功能，或對不同受眾做不同版本。還有 remix，讓別人複製你的網站再改。
- 他看到的內部用法：把內部資料做得更好讀，例如 8-bit 遊戲風格的發表回顧、書冊風格的架構回顧、iPhone 樣式的社群內容檢視器。他認為這比 Google Doc 或簡報好讀。
- **Wiki race**：用 Sites 加 Agents API 的 computer use，讓模型和他比賽在 Wikipedia 從 Frida Kahlo 頁面點到 Rubik's Cube 頁面。他說試玩時勝負「大約五五波」。這只是展示，不是評測。
- **Code Review 分頁**：桌面 app 會列出你開的或被指派 review 的 PR，可以看 diff 和作者附的截圖。按「review with Codex」會另開 thread，用預設 prompt（可加自訂指示）派 subagent review，結果回到聊天。workshop 頁補充，可以在 PR 畫面問 Codex 這個改動要修什麼、為什麼這樣做、哪些檔案與測試最重要。

### 8. 委派：Voice、Dots、Agents API（45:00–51:40）

- **Codex Voice**：他說多數人只把語音當打字的替代品，但它可以當成整個 app 的「控制平面」，你在 app 裡能做的事它幾乎都能代做，例如管理 threads、查進度、用 computer use 從別的 app 拿資料、開新 thread。現場 demo 一次交代四件事：查剛才的 PR review、看 Matt 在 Slack 說了什麼、開新 thread 評論演講投影片、完成後釘選該 thread。結果 Codex 反問「是哪個 Matt」，列出四個人名；因為時間不夠，沒看到完成結果。他自己常開著語音只讓它操作、不讓它回話。
- **Dots**：他坦白「身為 Codex 重度使用者，Dots 用起來有點彆扭」，因為它是新的工作方式、擅長的事不同。他分三種用法：
  1. **安全網**：主動提醒 PR 有 bug、有 merge conflict、同事在你不在的頻道做的東西和你衝突、行程撞期，甚至 East Bay 山火可能影響通勤。他說一般的 Codex 不會做這些事。
  2. **委派收件匣**：在 Slack 一直把訊息轉給它，請它查清楚或建待辦，當成虛擬同事或直屬部屬。
  3. **到處都在**：ChatGPT、Slack、Teams、電話、簡訊（iMessage／RCS）都能找到它。
- **Agents API**（beta）：把 Codex harness 包成服務，讓你在自己的產品裡開成百上千個短命 session，共用 sandbox 與 plugin。workshop 頁說它處理 session、context compaction 和 subagent 分派，sandbox 可以由 OpenAI 託管或自帶。

### 9. 快速 tips（51:40–結尾）

1. **把推理量調低**：不要直接拉到最高。多數事情從 high 開始就好。新一代模型出來時，如果你原本卡在 extra high，試著降一級看效果是否一樣。他說調到最高可能報酬遞減，甚至想太多。workshop 頁的版本是「從 Medium 或 High 開始，簡單又能馬上驗證的改動用 Low」。
2. **讓 agent 自己決定模型分工**：主模型用 Sol medium，卡住時派 Astra high 的 subagent 求助，繁瑣工作派一群 Luna high 的 subagent。做法是寫成一個 skill（workshop 頁的 `coordinate` skill 全文已存在 raw）。他自己提醒：「不一定比較好、也不一定比較便宜」，模型還不太會判斷什麼任務該交給誰，只是能減少你自己挑組合的負擔。
3. **成對的 peer agents**：任務可以平行做、但彼此有依賴時（例如一個 agent 負責 web 前後端，一個負責 mobile app），不必先拆好計畫再平行實作，而是開一組能互相溝通的 peer subagent，讓模型自己協調後端變動。他承認比較難，因為要讓 Codex 想清楚彼此的溝通界線。他建議把這張投影片截圖給 agent，請它找出適用的情境。
4. **thread of threads**：除了綁在主 session 上的 subagent，Codex 也能開完全獨立的 chat，你可以個別操作；Dot 也能替你開 thread。workshop 頁補充，子 thread 可以在同一台機器、新的 worktree 或遠端環境執行。
5. **CLI 更新**：加了 agents 總覽（他說按左方向鍵切換 session；workshop 頁寫的是 `/agents` 指令配合 Tab 與方向鍵），SSH 進 dev box 時很好用。CLI 也有語音模式了。
6. **自訂快捷鍵**，以及**全域語音聽寫與語音熱鍵**，不必另裝第三方聽寫 app。
7. **申請 Daybreak Blue**：OpenAI 的資安計畫，個人可以申請，條件是要有實體安全金鑰（如 YubiKey，有合作折扣），用來保護自己的應用。
8. **不要太執著現在的用法**：每次新模型出來，考慮丟掉你累積的做法，先試試沒有它們是否更好，再把仍有問題的部分加回來。

## 可搬到個人 Claude Code／Codex 的做法

能照做的：

1. **repo 規範寫成可執行的檢查**：慣例放 `AGENTS.md`，更重要的是 lint、formatter、測試指令都放進 repo，讓 agent 跑的檢查和團隊一樣。判準是「優秀新人進來能不能不犯錯地貢獻」。這和 [[Lauren-Tan-把糾正寫進程式庫]] 的主張相同，該頁說得更深：糾正要變成確定性檢查，而不是多一行警告。
2. **UI 探索期的快速迴圈**：
   1. 先啟動有 hot reload 的 dev server，並用 agent 的內建瀏覽器或旁邊的瀏覽器即時看結果。
   2. 推理量調到最低的可用檔（Codex 的 light／low，Claude Code 的 `low`）。
   3. 一次只提一個小改動，看完再提下一個；不確定想要什麼時，靠一輪一輪的結果收斂。
   4. 方向定了、要進入實作或修 bug 時，再把推理量調回 medium 或 high。
   如果 build 或測試本身就要幾十秒，這個迴圈的好處會消失，此時與其提高速度，不如先縮短驗證時間。
3. **換新模型時，推理量降一級做對照**：原本用最高檔的任務，換模型後先降一級跑同類任務，比較結果再決定。這與 [[Claude-5-世代的指示精簡原則]] 的「較強模型配較低 effort」經驗法則方向一致；但該頁也提醒，降 effort 會減少驗證，重要工作要保留明確的完成條件。
4. **模型分工寫成設定，而不是每次手選**：
   - Codex：照 workshop 頁的 `coordinate` skill，存成 `coordinate/SKILL.md`，用 `$coordinate` 呼叫。重點是子 agent 用 `fork_turns: "none"` 啟動，因為 `openai/codex` 原始碼的提示文字寫明，完整複製歷史的 fork 會繼承父模型與推理量、不接受覆寫。
   - Claude Code：用 `.claude/agents/*.md` 的 `model` 與 `effort` frontmatter 定義「便宜模型做探勘」「強模型當顧問」兩種 subagent（[sub-agents 文件](https://code.claude.com/docs/en/sub-agents)載有這兩個欄位，也說明可以覆寫內建 Explore 改用 haiku）。
   - 兩邊都要記得講者自己的提醒：委派會多花時間和 token，模型分派判斷不一定對。是否值得，看 [[Context-優先與多-agent-的適用邊界]] 的判準：是知識問題還是編排問題。
5. **遠端 dev box 不必裝桌面 app**：在主機上執行 `codex login`（沒有瀏覽器時用 `--device-auth`），再執行 `codex remote-control start`，就能從手機 ChatGPT app 的 Remote 操作；停止用 `codex remote-control stop`。這已在原始碼確認（見回查）。
6. **新模型時清掉舊鷹架**：定期把指示檔裡為舊模型加的規則拿掉重測，再把仍需要的加回來。

不適用或要先確認的：

- **Appshots**：只在 ChatGPT 桌面 app（macOS／Windows）上有；官方功能表顯示 Enterprise／Education 沒有。在 WSL 的 CLI 裡不能建立新的 appshot。
- **Computer History**：只有 macOS 桌面 app，Pro 自己開啟，Business／Enterprise 要管理員授權，而且需要 Memories。在 Windows 或 WSL 上用不到。
- **Ultrafast**：官方 pricing 頁標示只有部分 Pro、Enterprise、Edu 方案有，並另外消耗額度。一般方案無法照抄演講的 Ultrafast 迴圈，只能用一般或 Fast 速度加低推理量來近似。
- **Sites、Space、Dots、plugin 共用連線**：都綁 ChatGPT 帳號生態，Claude Code 沒有對應功能。把計畫移出 repo 改用共享文件，和本 vault「規範與計畫都在 repo 內」的做法不同，要用就是另一套工作流程。
- **讓 agent 代你在 Slack 回同事**（文件站上線的例子）：演講當成好處，但這等於讓 agent 用你的身分對外發言，需要事先限定範圍。可參考 [[ChatGPT-Dots]] 記載的權限與記憶共享問題。

## 回查結果（2026-11-19）

| 演講說法 | 回查來源 | 結果 |
|---|---|---|
| Codex harness 開源、驅動多個介面 | [openai/codex](https://github.com/openai/codex)、workshop 頁 | 相符。repo 為 Apache-2.0，查詢當天仍有 push。workshop 頁列出 desktop app、CLI、Dots、ChatGPT Work、Slack、Agents API 共用 harness |
| `codex remote-control start` 可在沒有桌面 app 的主機啟動 Remote | `openai/codex` 原始碼 `codex-rs/cli/src/remote_control_cmd.rs`、workshop 頁 | 相符。原始碼有 `remote-control` 的 `start`／`stop`／`pair` 子命令；workshop 頁寫明 `codex login --device-auth` 等步驟 |
| Ultrafast「快 8 倍、成本 6 倍」 | [Speed 文件](https://developers.openai.com/codex/agent-configuration/speed)、workshop 頁 | **部分相符、要加條件**。官方寫的是演講當時的 Astra 型號「最高 8 倍」；之後推出的較新型號，官方寫最高約 4.5 倍。「6 倍額度」只有 workshop 頁寫，我讀到的 pricing 表只顯示 Fast 的倍率（2–2.5 倍），Ultrafast 分頁要 JS 才能載入，沒有讀到。方案限制：部分 Pro、Enterprise、Edu，而且 Enterprise 預設關閉 |
| Appshots 會一起送畫面外的文字，Mac 和 Windows 都能用 | [Appshots 文件](https://developers.openai.com/codex/appshots) | 相符，但有官方寫明的例外：Google Docs、Gmail、Sheets、Slides 可能只收到可見截圖，要改用對應的 plugin |
| Computer History 用事件串流不用截圖、可暫停、清除、排除，只有 macOS | [Computer History 文件](https://developers.openai.com/codex/customization/computer-history) | 相符。官方寫明不存截圖、不錄音、不收無痕瀏覽；預設關閉，需要 Memories；是重做的系統，取代先前的 Chronicle 研究預覽 |
| Codex Cloud 自動設定環境、snapshot、背景更新、Tailscale 與 OIDC | [Cloud 文件](https://developers.openai.com/codex/cloud)、[cloud environments 文件](https://developers.openai.com/codex/environments/cloud-environments) | 相符。官方流程是 Codex 檢查 repo、安裝依賴、測試流程，你看過報告後 publish；repo 在背景自動更新並保留依賴快取。Tailscale 是目前唯一支援的 VPN，auth key 要同時開 Reusable 與 Ephemeral。官方提醒保存的狀態不能取代版本控制 |
| Dots 可以在 ChatGPT、Slack、Teams、電話、簡訊找到 | [Dots 文件](https://developers.openai.com/codex/dots) | **Teams 只在推出公告**：本次讀到的開發者 Dots 頁只列 ChatGPT、通話、簡訊、Slack；但[官方推出公告](https://openai.com/index/introducing-dots/)原文寫「message your dot in Slack and Teams」，見 [[ChatGPT-Dots]]。簡訊目前是美國 Pro 的 beta。加進 Slack 頻道不等於開始監看，要另外指定要看哪些頻道與事件 |
| Annotations API 可以自訂可選範圍 | workshop 頁、GitHub code search | workshop 頁給了 `oai-annotatable` 屬性範例。GitHub 上已有第三方採用：WordPress Playground 的網站原始碼使用了 `oai-annotatable` |
| 子 agent 可以指定不同模型與推理量 | `openai/codex` 的 `codex-rs/prompts/src/multi_agent_instructions.rs` | 相符，有附帶條件：完整歷史的 fork 不接受模型覆寫，要用 `fork_turns: "none"`，與 `coordinate` skill 的寫法一致 |
| Daybreak Blue 個人可申請、需要 YubiKey、有折扣 | workshop 頁、[Yubico 合作頁](https://www.yubico.com/openai-and-yubico/) | 部分相符。Yubico 頁有 OpenAI 合作的 YubiKey 組合優惠，但沒有提 Daybreak；「個人可申請」只有 workshop 頁寫，另外要求付費方案與身分驗證 |

## 證據強度與限制

- **全場是廠商自我介紹**：講者是 OpenAI 員工，所有「好用」「被低估」都是推廣立場；沒有對照組，也沒有失敗率。
- **數字都是自報**：用量多了「數千萬」人、文件站在午夜後 4 分鐘上線、單次 UI 改動 5–10 秒、wiki race 勝負約五五波、影片剪輯「快要自動化」，都只來自台上，沒有外部佐證，每項都是單一案例或單一團隊經驗。
- **功能說明的強度較高**：上表中有官方文件或原始碼佐證的部分屬於文件層事實，但我沒有實際操作任何一項。
- **時效短**：這場講的是一年內的新功能，模型型號和倍率在演講後幾週內官方文件就已改寫（Ultrafast 倍率已因新型號不同）。要用之前請回 [Codex 文件](https://developers.openai.com/codex) 和 changelog 確認現況。
- **字幕是上傳者提供的**，有辨識錯誤（例如 Codex 寫成 Codeux）；Voice demo 的結果沒有在影片中出現。

### 勿引用

- 「Ultrafast 一律快 8 倍、6 倍成本」：8 倍只適用特定型號且是「最高」，較新型號的倍率不同；6 倍只有 workshop 頁的單一說法（2026-11-19 核對）。

## 與既有頁的張力與互補

- **「模糊下指令」和 context 紀律的張力**：Kundel 說大家正從 context engineering 轉向 vague prompting，但前提是 agent 連得到 Slack、Drive 等 context 來源。[[Context-優先與多-agent-的適用邊界]] 的核心是「能力來自 context 注入」；兩者其實一致，只是演講把注入的方式從「人寫進 prompt」改成「agent 自己透過 plugin 去拿」。差別在於可審查性：寫在 repo 的 context 可以 review，agent 自己抓的不行。
- **和 Lauren Tan 互補**：兩場都說 repo 規範要落在 lint 和檢查上。[[Lauren-Tan-把糾正寫進程式庫]] 的重點是糾正與驗證，這場的重點是 repo 外的 context 與委派管道，兩場可以合起來讀。
- **和 Claude 5 精簡原則同方向**：最後一條 tip「新模型出來就丟掉舊做法再加回來」與 [[Claude-5-世代的指示精簡原則]] 一致，而且兩邊都來自廠商的建議。
- **Dots 的記載和既有頁不一致**：[[ChatGPT-Dots]] 依推出期資料寫 dot 可以接 Slack 與 Teams；本次讀到的官方 Dots 頁沒有 Teams。但該頁已回讀官方推出公告確認原句存在，兩者是公告與開發者文件的記載差異；要用 Teams 管道前，以當下產品設定為準。
- **Codex 功能面的補充**：[[四套-coding-agent-能力差異對照]] 比的是 CLI 層的機制。這場顯示 Codex 的差異越來越多在 CLI 以外：桌面 app、雲端環境、ChatGPT 帳號生態。只比 CLI 會低估兩者的差距。
