---
title: ChatGPT Dots
description: OpenAI 在 ChatGPT 推出的常駐 agent：雲端電腦、plugin 連接、背景主動研究與記憶共享機制，含方案地區限制與隱私缺口
created: 2026-10-15
updated: 2026-10-29
source: https://openai.com/index/introducing-dots/
published: 2026-09-29
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - memory
---

**一句話**：dot 是 ChatGPT 內的**常駐（always-on）agent**，2026-09-29 於 OpenAI DevDay 發表。每個 dot 有自己的雲端電腦與瀏覽器，連接你授權的 app 承接持續性工作，在對話之間（裝置關機時也行）繼續推進，有結果或需要你決策時主動回報。

本頁由 deep-research 多來源對抗查證彙整（2026-10-15）。openai.com 與 help.openai.com 會擋直連，官方頁面是透過代理讀取的，只有 learn.chatgpt.com 可以直接讀。**官方文件在推出後兩週內就改過好幾處**，下方標「推出期」的項目引用前要回官方頁再確認。

## 是什麼、怎麼用

**證據強度：高。** 官方公告、release notes、Help Center、learn.chatgpt.com 的說法逐字一致。

- **用法**：給 dot 一個目標，連接它需要的 app，再設定哪些事它可以自己做、哪些要先問你（Help Center 稱為 custom rules）。結果交回給你審，可以隨時暫停。
- **驅動模型**：官方寫的是 GPT-6 Astra。
- **運算環境**：雲端電腦會跨次保留狀態，用來做研究、處理檔案、執行軟體。可以選擇連接你自己的電腦，此功能預設關閉，一次只能連一台，而且那台電腦要在線、開著 ChatGPT app。
- **app 連接**：走 plugin 生態，官方宣稱可連 4,000 個以上 app（官方數字，未獨立驗證）。**plugin 權限由 dots、ChatGPT、ChatGPT Work、Codex 共用**，dot 只能在你既有的授權範圍內使用已設定的連線。
- **主動研究（proactive research）**：你沒在用它時，它會用已連接的 app 在背景找可以幫忙的事，並存成私人筆記。這時的工具限定唯讀，不能發訊息、不能改 app 內容、不能操控瀏覽器或電腦。**唯讀只限這個背景模式**，dot 正式執行任務時不受此限。
- **聯絡管道**：可在 ChatGPT 桌面版、網頁版、行動 app 傳訊息或語音通話，也能接 Slack 與 Teams。訊息管道要從桌面端設定。2026-10 下旬起另有簡訊管道（美國 Pro beta），見下方方案表的簡訊列。
- 官方另預告「specialist dots」：給企業用，每個 dot 有自己的身分與憑證，負責明確的職務。目前只有企業試點，沒有公開推出。

「24/7 朝目標工作」「隨回饋持續學習」是行銷文案，沒有獨立驗證。

## 記憶與隱私：最需要注意的一節

**證據強度：高。** 來源是官方 Privacy／Safety FAQ 原文，MemoryLake 部落格也逐字引用同一段。

- dot 與 ChatGPT Memory **雙向共享**：dot 會收到 ChatGPT 的記憶與近期對話脈絡，你和 dot 的對話也會回寫到 ChatGPT Memory。dot 也會從已連接的 app 自己建立記憶。
- 關掉 ChatGPT Memory **只會停止之後的共享**，dot 已經收到的資訊不會刪除。
- **推出期**：無法逐條檢視、刪除或修改 dot 的個別記憶，要清除只能整個 dot 重置。重置後，dot 產生的檔案與對話仍會保留。
- ~~這個按鈕的名稱，第三方說已從 Reset 改為 Delete，但本次透過代理讀到的 Help Center 仍寫 Reset，未能確認。~~ **已被取代（2026-10-29）**：官方 [learn.chatgpt.com Controls 頁](https://learn.chatgpt.com/codex/dots/controls)現有「Delete your dot」一節，按鈕名稱是 **Delete**（刪除 dot、無法復原），一手確認了第三方說法；對話、記憶、排程任務怎麼處理，官方只寫「看確認視窗」。上一條「重置後檔案與對話仍保留」是推出期 Reset 的說法，是否適用於 Delete，官方頁未寫明、未查證，Help Center 現況也沒有重讀，**引用前回官方確認**（強度中）。

這和 [[Mem0]] 記錄的「LLM 寫入時自行抽取事實，錯誤會自我放大」屬於同一類設計風險。dot 的情況更麻煩：推出期無法逐條清理，記憶還會回寫到主 ChatGPT。

## 方案、地區、平台（推出期，2026-10-15 查證）

| 項目 | 狀態 | 強度 |
|---|---|---|
| 方案 | Pro（Pro 100／200／500 各層）、Business Premium。Enterprise／Edu／Healthcare 是 beta，預設關閉，須由管理員開啟「Use dots (Beta)」權限 | 高 |
| 地區 | Pro 推出時排除 EEA、瑞士、英國（原文寫「at launch」）；Business Premium 開放所有支援 ChatGPT 的地區 | 高 |
| 年齡 | 須滿 18 歲 | 高 |
| 推出節奏 | 漸進推出，符合資格的帳號也可能晚幾天才看到 | 高 |
| 費用 | 第一個 dot 含在方案內，不另收費。加購 dot、提升單一 dot 速度或每月工作量的價格未公布 | 高（含在方案內）／中（額度細節） |
| 額度 | 和 dot 對話不計入 ChatGPT 用量；dot 在 Codex 或 ChatGPT Work 啟動的任務會計入。首月的說法從「不計入額度」改成了「額度放寬」 | 中 |
| 平台 | iOS／Android app、桌面 app（含 Windows）、桌面網頁。**行動版網頁不支援**。入口是 `chatgpt.com/dots` | 中（說法有版本落差，見下） |
| 簡訊 | 2026-10 下旬起以 beta 對美國 Pro 漸進推出，走 iMessage 或 Android RCS，一對一對話，可傳文字、照片、語音訊息，需在 dot profile 驗證手機號碼（[官方 Channels 頁](https://learn.chatgpt.com/codex/dots/channels)，2026-10-29 查）。推出期另有「由第三方供應商傳送」「Business／Enterprise 不能用」兩點，現行官方文件未載，引用前回查 | 高（推出現況）／低（推出期兩點） |
| 其他 | 推出時 dot 不能主動打電話給使用者，也不能有獨立的 email 地址（可以連接你自己的信箱） | 高 |

**平台的版本落差**：推出當天的公告與 release notes 都寫「首次建立要在桌面完成，之後才能在行動 app 傳訊息」。現行 Help Center 已改成行動 app 也能建立。兩份都是官方文件，差別在修訂時間；轉折點是下節 2026-10-05～09 那輪更新。

Business Premium 至少要兩個席位，這一點只有單一第三方來源（usecarly），強度低。

## 推出後更新

### 2026-10-05～09

**證據強度：高。** 來源是官方 [What's new：Create your dot in the ChatGPT mobile app](https://learn.chatgpt.com/docs/whats-new/dots-october-9-2026)（learn.chatgpt.com 可直讀，已回讀原句）。

- **手機建立 dot**：iOS／Android 的 ChatGPT app 可直接建立 dot、命名、自訂外觀、連接 plugin，並直接開啟該 dot 的對話。推翻推出當天「首次建立限桌面」的說法。
- **委派 Codex**：dot 可以在 Codex 開始工作、跟進既有 thread，並引用 ChatGPT 對話、既有 Codex thread 與 automation 的脈絡；判斷該延續舊 thread 還是開新 thread 的能力也有改進。
- **讀寫 ChatGPT Work automations**：dot 可檢視排程中的工作並修改定期任務。
- **thread 管理**：dot 管理的 thread 會隨工作內容自動改名，重複的「created task」訊息變少。

OpenAI Developer Community 在 2026-10-13 有一篇[使用者轉貼](https://community.openai.com/t/dots-received-another-round-of-updates/1405896)（發文者身分未標示為 OpenAI 員工），內容與上列一致，另列雲端瀏覽與側邊欄載入加快、行動通知減少、審批按鈕不再被裁切、Enterprise 網頁與語音存取修正等小修。這些小修在官方頁屬一般性改進、未明指 dots，強度中。

### 2026-10-12～16

**證據強度：中。** 來源是官方 learn.chatgpt.com 的 what's new（2026-10-29 時效核對時讀到，本頁未保存該期原句）。

- **iOS 入口**：新增「Your dot」Home Screen widget，以及 Apple Shortcuts 的「Open your dot」動作；需較新版 iOS app（官方寫明 1.2026.279 以上，最低版本以官方 what's new 為準）。

### 2026-10-26～30

**證據強度：高。** 來源是官方 [Channels 頁](https://learn.chatgpt.com/codex/dots/channels)：「Reach your dot through iMessage or RCS on Android. Texting supports one-to-one conversations. It’s rolling out in beta to ChatGPT Pro users in the U.S.」

- **簡訊正式推出**：兌現推出公告的「texting coming soon」，細節見上方方案表的簡訊列。

### 首月額度

第三方指南（codersera）稱首月「dot 用量不計入額度」的期間在 2026-10 下旬結束；單一第三方來源、未對官方查證，**引用前回官方確認**。

## 評價：證據不足

查證後沒有留下任何關於實測品質、錯誤率或使用者口碑的主張。媒體報導多半只是轉述官方規格，DataCamp 明說推出時沒有獨立第三方評測。官方自己也警告 dot 會犯錯，包括在遵循你設定的規則時，重要工作要自行審閱。來源清單裡有 DevDay 現場出包、實務者存疑之類的報導，但相關主張都沒有通過查證，本頁不引用。

## 查證翻案紀錄（2026-10-15）

- **「可語音通話、可接 Slack 與 Teams、簡訊即將推出」**：自動查證以 1 比 2 的票數否決，但回讀[官方公告](https://openai.com/index/introducing-dots/)原文後確認逐字存在（「message or call dots in ChatGPT on desktop, web, and mobile」「message your dot in Slack and Teams, with texting coming soon」），**已翻案、可引用**。
- **「只能在桌面建立、行動裝置不行」**：同樣以 1 比 2 被否決。這句是推出當天的官方說法，現行 [Help Center](https://help.openai.com/en/articles/20001530-getting-started-with-your-dot) 已改成行動 app 也能建立。**已被取代（2026-10-15）**：現況見上方平台列。`chatgpt.com/dots` 這個入口確實出現在 Help Center 的疑難排解段落。

## 開放問題

- Pro 在 EEA、瑞士、英國何時開放？當初排除是因為法規，還是單純分批推出？
- 加購 dot 的價格與額度單位是什麼？首月放寬期結束後的實際額度有多少？
- 實測的任務完成品質、錯誤率，以及主動研究實際上有多好用？

## 關聯

- [[LLM-方案定價與-coding-agent-比較]] — dot 只有 Pro 與 Business Premium 才有，而且推出時出現了 Pro 500 這一層，比該頁記錄的 $100／$200 多了一級。dot 在 Codex 啟動的任務會吃同一份 Codex 額度。
- [[長跑-Agent-的目標定義與計畫工具]] — dot 的「給目標＋設定自主規則＋持續推進」是該頁目標檔機制的產品化形態。但官方沒有公開停止條件或驗收判準怎麼定，該頁對 reward hacking 與走偏的警告同樣適用。
- [[Mem0]] — 同屬「agent 自行累積記憶」的設計；dot 推出期無法逐條刪除記憶，與該頁的記憶污染問題屬於同類風險。
