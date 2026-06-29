---
title: 10x Claude Code 的 Agentic OS 四層架構
description: 拆解 Claude Code agentic OS 的四層架構——skill 與 loop engineering、記憶與狀態、視覺介面、團隊分發；價值集中在前兩層的工作流編碼與第二大腦建構。
created: 2026-06-29
updated: 2026-06-29
source: https://www.youtube.com/watch?v=HRw-vP0j8OM
published: 2026-06-24
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - workflow
  - obsidian
---

很多人看 agentic OS（AIOS）只看到華麗的 dashboard、按鈕與指標，分成「想擁有」和「只是噱頭」兩派——但兩派都漏掉了底層運作的 AI 基本功：loop engineering、skill 架構、state 管理、第二大腦，把這些打包成為自己量身打造的產品。價值在看不見的引擎，不在介面。這些技能可套用到任何 Claude Code 專案（也適用 Codex 甚至本地模型）。AIOS 可拆成四層，價值集中在前兩層。

## 四層架構總覽

- **Level 1 backbone**：skill 與 loop engineering，把你在 Claude Code 做的每件事編碼成 skill 或 automation。
- **Level 2 memory & state**：讓 AIOS 有可取用的資訊庫，並與 skill / automation 結合成可自我改進的 loop。
- **Level 3 interface / UI**：跳出 terminal，加上客製視覺與介面。
- **Level 4 distribution**：把 AIOS 分享給團隊或客戶，提升組織整體下限。

Level 1 + 2 是 90% 的價值所在，且在標準 terminal、Codex CLI 或 desktop app 內就能做到，與華麗 dashboard 無關。Level 3、4 只是錦上添花。

## Level 1：skill 架構與 loop engineering

分四個子階段：workflow audit、skill creation、automation、loop engineering。

**Workflow audit（先做）**：建 skill 前要先知道該為什麼建。skill 的威力在於指定 Claude 用特定方式做特定事、產出特定輸出；問題是多數人答不出自己日常/每週反覆需要哪些特定輸出，更別說已把它們做成 skill。把工作拆成 domain（作者自己有 research、content、社群、agency、sales 等），每個 domain 下的反覆任務（如做大綱、想 hook、重新利用內容、做 carousel）都該變成 skill。

做 audit 的三種方式：

1. **手動**：自己講出做什麼，用 skill creator skill 轉成 skill。風險是若沒先手動驗證，可能還沒確認 Claude Code 的正確做法。理想是先手動跑通、確認可行，再叫它「照剛剛那樣做成 skill」。
2. **看歷史 session**：Claude Code 能存取你過去的 session、tool call 與完整來回。叫它「看過去 10/20 個 session，找出反覆做、還沒變成 skill 的任務，列成『任務 / 輸出 / 提議的 skill』表格」。這是依真實資料而非猜測。
3. **訪談**：讓 Claude Code 訪談你——你用意識流講日常/每週做什麼，請它對盲點發問，最後從對話中萃取可做成 skill 的任務。

心法：把自己當成請了個私人助理，盡量把任務連同 step-by-step 指示交出去，只是對象換成 Claude Code。

**Automation**：反覆執行的 skill 直接做成 automation。可直接 prompt「能把這個 skill 變成 automation 嗎」，或在 Claude desktop 的 routines 設定（給名稱、指示為「run 某 skill」、排定 schedule）。

**Loop engineering**：在 automation 上加自我改進 loop——讓 loop 能看到過去 run 的結果以改進未來 run，這會和 memory / state 綁在一起。有了 skill 與 automation 的基礎，就已具備做 loop 的條件。

這層是一切的 backbone：把你的工作編碼，讓 Claude Code 對你真正在乎的任務產出一致結果，與 dashboard 無關。

## Level 2：memory 與 state

重點未必是 Obsidian——傳統資料庫也行，核心其實是「coherent 的檔案結構」與讓 Claude Code 有條理。甚至沒有資料庫、沒有 Obsidian，只要檔案結構合理就已完成 99%；Obsidian 只是讓它更簡單。

**接上 Obsidian**：下載後把某資料夾指定為 vault（思考哪個資料夾該裝你要 AIOS 知道的全部資訊，例如把 sales 資料的副本放進去）；在 terminal cd 進該資料夾、開 Claude Code，就等於把 Claude Code 接上 vault。

**檔案結構是關鍵**：若一個資料夾塞百萬個檔、無 backlink、無階層，Claude 會找得慢、用更多 token、花更多錢。心智模型是替 Claude Code 畫一張地圖，讓它對 vault 任何檔案的問題都有清晰路徑找到答案。

**Karpathy 的 Obsidian 結構**（該 tweet 逾 2000 萬次觀看）：主 vault 下三個子資料夾——

- `raw`：放未結構化資料。
- `wiki`：把 raw 整理成結構化的 Wikipedia 式文章（例如把一堆 AI agent 的零散文章整成一篇）。
- 第三個資料夾：放 output（如把 wiki 文章再轉成的簡報等可用交付物）。
- 流程：unstructured → structured → outputs。

**真正的精髓是 index.md**：每一層都放一個 index.md 當該層的目錄，告訴 Claude Code 這層有什麼、各資料夾是做什麼的。例如問「給我 AI agent 的所有資訊」，它先讀 vault 的 index.md 得知有 raw/wiki/outputs，再進 wiki；wiki 資料夾內也有 index.md。資料量小時不需要，但累積上千份文件時，index.md 讓它快速理解該往哪走——這才是力量來源，那些資料夾名稱（raw、outputs 等）反而是任意的。你不必照搬 Karpathy，只要給 Claude Code 一張看得懂的地圖，且結構會因人而異。不知道怎麼建就叫 Claude Code 看你的 vault、參考 Karpathy 的 Obsidian RAG 給建議，再建一個 claude.md 說明 vault 慣例（結構與導航 pattern：要找東西時該走哪條路徑）。作者自己的 vault 不只三個資料夾，還有 content、notes、runs、inbox、ops、projects 等。

memory 也呼應 loop engineering：自我改進的 skill / automation 需要一個地方讓 loop 看到過去 run 做了什麼，才能改進未來——這些都該綁在同一處，形成可被 Claude Code 取用並萃取洞見的第二大腦。掌握 Level 1+2 就握有 AIOS 90% 的力量。

## Level 3：視覺介面

在前面成果外包一層客製視覺，可做成 web app 或 Obsidian 介面，底層都是 Claude Code 接 Obsidian。

- **web app 版**：自訂指標（如 YouTube 訂閱數、Instagram、最新影片、Claude 5 小時用量、從 Google Calendar 拉的 directive），右側把 automation / skill 變成單一按鈕（如 inbox brief，點了會排入佇列、headless 跑 Claude 過 inbox 建草稿並回報）。
- **Obsidian 版 command center**：類似指標（如 token burn）、按鈕跑 skill、分頁。
- 作者還接了完全本地的語音模型（不走 11 Labs，免費），可語音對話、念出報告。

**製作方式**：跟用 Claude Code 做一般 web app 一樣，給視覺參考截圖 + 說明「已有哪些 skill、要接 vault、想看哪些指標」即可。Obsidian 版走 plugin 系統，可叫 Claude Code「把剛做的 web app 轉成 Obsidian plugin 版」。

**底層運作**：點按鈕等於呼叫 headless 版 Claude Code，用 `claude -p` 指令（terminal 不會跳出、隱形執行）。註：`claude -p` 之前有過爭議——Anthropic 一度說它不吃 Claude 訂閱、而是吃綁 API 成本的 $200 額度，後來收回，目前仍是吃 max plan，與自己開 terminal 跑無異。

## Level 4：分發

把接好所有 skill 的 web app 交給別人，他們就離「取得 Claude Code 大量能力」只差一鍵——因為力量都在 skill 與 automation，讓人易於使用等於不必真的 onboard 就把能力交到他們手上。

- **web app 較好分發**：可放 GitHub、打包 zip，容易傳給對方並跑起來。
- **Obsidian 版較麻煩**：需要你較多動手設定，不像「clone repo、指向 Claude Code」那麼直接。

對客戶工作而言客製化是賣點：很多人想用 AI 卻被 terminal 甚至 desktop app 嚇退，「我幫你設好，你只要講話或按幾個按鈕」能走很遠。dashboard 效應對非技術族群改變了他們詮釋技術工具的方式。

## 總結

Level 3、4 是錦上添花，幾乎所有時間都該投在前兩層：skill、loop engineering、automation、編碼、memory 與 state。能對同樣任務每次一致地產出、並記錄下來形成可被 Claude Code 參照與用於自我改進的第二大腦，就能領先多數人。
