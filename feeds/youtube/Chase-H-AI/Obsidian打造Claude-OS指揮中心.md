---
title: Claude Code × Obsidian Agentic OS 會成為新主流
description: 用自製 Obsidian 插件當 Claude Code 指揮中心，整合語音三層路由、skill 與 automation 骨幹與索引式 vault 記憶層
created: 2026-08-17
updated: 2026-08-17
source: https://www.youtube.com/watch?v=njHuj8OxIVI
published: 2026-08-15
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - obsidian
  - automation
  - workflow
---

## 這套 Claude OS 想解決什麼

多數人把 Obsidian 當成 Claude Code 的 markdown 檔案倉庫，只用到皮毛。作者的主張是把它升級成整個 Claude OS 的指揮中心：一組 skill 與 automation 的骨幹、一層記憶，再加上一個視覺化外殼，提供終端機與 Claude 桌面 App 給不了的洞察，另外掛上完全在本機跑的語音能力。

這套系統前後迭代過幾版：早期是 Obsidian 版，中間做過 web 版（優勢是本地語音），現在把 web 版最好的部分搬回 Obsidian，合成單一入口。

作者反覆強調的取捨：**沒有底層的 skill／automation 骨幹，這個介面就只是沒有實質內容的視覺秀**。介面上顯示的每一塊都應該是某個 skill 或 automation 的產出，否則沒有資料會流進來。

## 視覺化指揮中心提供的價值

介面本身是 Claude Code 自己寫出來、再裝進 Obsidian 的自訂插件，內容 100% 可自訂。作者自己放的東西包括：

- token 用量的即時概覽
- 各社群平台的數據指標
- 從 Google Calendar 拉來的行程，並自動拆解成當日任務
- 早間頭條
- 一排可一鍵執行的 skill 與 automation 按鈕
- 分頁式的每日報告，例如 research 分頁（morning intel automation 產出：GitHub 近 7 天／30 天 trending repo、YouTube 的異常高表現影片、內容切角、Hacker News 熱門）與 audience 分頁（自家內容在 YouTube 的表現、什麼有效、為什麼）

因為底層是 Obsidian，不受限於這個面板——終端機可以直接開在 Obsidian 裡面。

## 語音層：三層路由架構

語音流程是這樣串起來的：

1. 說出指令 → 語音模組（作者叫它 Jarvis）
2. 用開源的 **faster Whisper** 在本機轉成文字
3. 文字送給 **Haiku 4.5** 做路由判斷（選它是因為最小、最便宜、最快；有足夠硬體的人可以換成任何本地模型，作者沒預設本地模型是因為這套要發給別人用、無法預期對方硬體）
4. 依判斷分成三層執行
5. 結果用開源的 **Kokoro** 轉回語音回覆

三層路由的分工：

| 層級 | 情境 | 行為 |
|---|---|---|
| Tier 1 | 「跑一下 morning intel report」 | 直接執行對應 skill，不加工，做完回報 |
| Tier 2 | 「今天最大的 AI 新聞是什麼」 | 只讀已產出的報告（例如 research 分頁），刻意不許它自行搜尋，換取速度 |
| Tier 3 | 「開 Fable 5 對某題做深度研究並擬計畫」 | 不屬於既有 skill 也不是既有指標，實際起一個 headless 的 Claude Code 實例跑完再回報 |

Tier 2 之所以回應很快，是因為它只是查已經跑完的報告，不需要現場上網找資料。Tier 3 最慢但最萬用。

實用性的關鍵在於**切換到別的視窗時也能用**：按熱鍵就能出聲問問題，不必切回 Obsidian。作者做這層的動機是 Claude 桌面 App 的語音模式不夠好，而 Codex／ChatGPT 的 live 語音體驗值得移植過來。

## Skill 與 automation 骨幹

這是整套系統的實質內容，作者認為概念簡單但很少人做對。

建立流程：

1. **定義任務**。AI 本質是非決定性的，同一件事叫它做十次會有十種做法；把做法與終態明確寫下來變成 skill，才能盡量逼近決定性。
2. **找出自己到底在做什麼**，有三種方式：
   - 開麥克風對 Claude Code 意識流地講自己每天、每週在做什麼，再請它判斷哪些可以變成 skill
   - 讓 Claude Code 去讀本機日誌——每一次工具呼叫、每一條指令、每一段文字都有紀錄，掃過去 30／60／90 天就能反推真實用途
   - 兩者合併（作者推薦），因為腦中認知的自己和日誌裡的自己往往不一樣
3. **判斷哪些該升級成 automation**。通常很明顯：需要每天固定時間跑的就變成 routine。
4. **先當 skill 用一段時間**，確認產出符合期望，再轉成不用手動觸發的 automation。

作者的 skill 依領域分類：memory、productivity、research、content、community、agency、sales 等。以 research 為例，底下有 YouTube pipeline、特定主題的深度研究、寫進 light RAG 資料庫的流程、morning trend scan、競品觀察等。

再往上可以疊 loop engineering 的概念：讓 automation 比對自己歷次產出、設定目標與判準，沒達標就持續調整，形成自我改進的迴圈。影片沒有展開這段，只標記為進階方向。

語音層不需要額外設定就知道有哪些 skill 存在，因為模型本來就拿得到清單。

## Obsidian 記憶層：它到底做了什麼

作者花了一段篇幅澄清常見誤解：**Obsidian 的圖譜看起來很像 graph RAG，但它完全不是 graph RAG**。Obsidian 做的事是把資訊整理成 markdown 檔案，主要是給人看的。

對 Claude Code 的好處是附帶的、而且只在檔案量很大又結構合理時才成立：好的結構讓它容易導航、更快給出準確答案、省 token。這個好處完全取決於你怎麼設定，不是裝了 Obsidian 就有。

引發這波熱潮的是 Karpathy 在 4 月的推文（近 2200 萬次瀏覽），結構相當簡單——vault 資料夾底下三個子資料夾：

- `raw/`：研究時抓回來的原始資料與來源
- `wiki/`：把 raw 綜合成 Wikipedia 式文章（例如 RAG systems 底下再分向量資料庫、chunking 策略）
- `output/`：從綜合內容產出的實際交付物，例如簡報

真正關鍵的不是這個資料夾切法，而是**每一層都有一個 index markdown 當目錄**。進到 wiki 先讀索引，知道底下有哪些子主題；進到子主題再讀一層索引。三個子資料夾當然不需要目錄，但 3000 個、30000 個、300 萬個就需要。

作用有兩個：人自己找得到東西；以及給 Claude Code 一張地圖，因此答得更快、燒更少 token。用作者的話說，Obsidian 記憶層不是給它更多記憶，**是給它一張地圖**。

實務上不必照抄 raw／wiki／output。作者自己的 vault 分成 content、daily notes、inbox、ops、project、systems、wiki，比較零散；補救方式是在 vault 內的 `CLAUDE.md` 裡把 vault 結構與導航方式明確寫出來——有結構加上讀法說明，地圖就成立了。真的不知道怎麼開始，可以直接把 Karpathy 那則推文整段貼給 Claude Code，叫它照著原則建起來。

## 自己做出這個插件

實際做法比想像中直接，因為介面就是一個 Claude Code 自己寫、自己裝進 Obsidian 的插件。

前置：除了自製插件外，一定要裝 **hot reload** 這個社群插件。它在 Obsidian 官方社群插件介面上找不到，要去 GitHub 搜 hot reload，把連結丟給 Claude Code 讓它裝。

設計流程：

1. 去 Pinterest 之類的地方搜 dashboard／command center 找視覺參考，截圖備用。
2. 把截圖丟進 Claude 的設計功能，說明要做 Obsidian 插件的 mock-up、要顯示哪些指標（行事曆、skill 清單、token 消耗等），並要求「產出五個明顯不同的版本」——這樣它會把五版排在同一頁比較。
3. 挑中喜歡的那版之後**再針對它做多輪變體**。作者的路徑是先選了黏土質感那版，再加背景圖層，最後收斂到玻璃擬態效果，背景雲層透出來，另外加了很淡的星光閃爍與點擊時的數字跳動動畫。
4. 定案後告訴它，它會把所有 mock-up 的程式碼打包成 zip；把 zip 丟進 Claude Code 說「照這個做成插件」，它會建好並安裝，然後就能在 Obsidian 裡看到。

想更省事的話，可以在 Claude Code 裡啟用 computer use，讓它一邊自己截圖一邊跑設計迭代，過程幾乎不用插手。
