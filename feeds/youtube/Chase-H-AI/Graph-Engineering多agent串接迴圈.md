---
title: Graph Engineering：把多個 loop engineering 的 agent 串成圖
description: 把單一 agent 的大迴圈拆成各自帶成功標準的原子 agent 並互相連接，換來品質、速度與可除錯性；只在 context rot、需獨立審查、講究時效三種情境才值得。
created: 2026-08-03
updated: 2026-08-03
source: https://www.youtube.com/watch?v=Joqh7Tui9B8
published: 2026-07-21
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - loop-engineering
  - sub-agent
  - workflow
---

## 定位

繼 context engineering、loop engineering 之後的新名詞。作者的判斷是：這不是硬掰出來的炒作題目，但也**不是每件事都用得上**——它是 loop engineering 的延伸與演化，主要對「會用到複雜迴圈」的人有意義。

## 先回顧 loop engineering

任何迴圈都有三個部分：

1. **Trigger（觸發）**：這東西怎麼啟動。理想上要自主——每天固定時間跑，或事件驅動。
2. **Task（任務）**：它實際要做什麼。
3. **Success criteria（成功標準）**：怎麼知道它做對了。做錯就從頭再跑一次。所有執行紀錄與資料若能存起來，還能再加上自我改進的機制。

範例：每天早上 7:00 觸發的晨間簡報迴圈。任務是掃 YouTube、Twitter、Reddit 找 AI 的趨勢資訊，再檢查 email，最後整合成一份報告。成功標準在這個案例中偏模糊，所以要明訂——報告必須包含哪類資訊、要多長、必須附連結。整條迴圈由**單一 agent** 執行。

## 同一任務改成 graph 長什麼樣

目標報告不變、trigger 不變（一樣每天早上 7:00），差別在於從一個 agent 包辦全部，變成**多個 agent 各司其職且彼此相連**：

- 一個 agent 只看 YouTube，一個只看 Twitter，一個只看 Reddit，一個只處理 email。
- 每個 agent 取得自己該取的資訊，各自先做一次綜合。
- 各自把綜合結果送給 **report agent**，由它收攏所有資料、進一步整合成要的報告。
- 還可以再加一個 **review agent**：獨立檢視產出的報告，對照事先定義的「成功的報告」長什麼樣，決定要整輪重跑，還是可以推上線。

## 為什麼多加 agent 有意義

關鍵不在「agent 變多」，而在於**每個任務本身都被變成一個獨立的 loop engineering 構造**。

原本的做法是在很高的層級、一次塞很多事情進去檢查成功與否。改成 graph 之後，鏡頭拉近到單一任務：那個只做 YouTube 研究的 agent 一樣有 trigger（同樣是 7:00）、一樣有 task（找 YouTube 上的 AI 資訊並綜合）、一樣有成功標準——只是現在標準可以**針對每一段旅程講得很具體**：至少要五個來源、綜合至少兩段、每個來源與每條資訊都要說出一個「so what」。

由此帶來的好處：

- **品質更好**：一個 agent 只做一件事，context window 相對乾淨；對照另一個要同時處理十件事的 agent，輸出品質天差地別。
- **速度更快**：四個 agent 平行做四件事，優於一個 agent 依序做十件事。
- **更好除錯**：可以立刻分辨這是 YouTube 的問題還是 Reddit 的問題。單一大迴圈裡很難從雜訊中撈出訊號，往往搞不清楚是路徑上哪一段出錯才導致報告被退回重做。

一句話總結：不是一個 agent，而是一系列以各種方式互連的 agent；任務被拆成原子級，因此每個任務都能明確定義要做什麼、成功長什麼樣；每個 agent 本身就是一個 loop engineering 構造——graph engineering 就是把一堆迴圈接起來。

## 三種該用 graph 的情境

大多數任務用簡單的迴圈就綽綽有餘，只有以下三種要考慮升級：

### 1. Context 問題（context rot）

如果一個 agent 反覆迴圈、每輪要做四到八件事，跑到 context window 累積到 30 萬、40 萬、50 萬 token 的量級，就該拆開。沒有理由在可以避免的情況下，讓自己承受 context 塞爆導致的品質下降。

### 2. 需要獨立審查

要問自己：產出東西的那個 agent，適不適合自己評判自己的產出？晨間報告這種案例大概可以——不太複雜、賭注不高、判準本來就相當主觀。但如果賭注高、需要第二雙眼睛，就該引入完全不同的 agent 來檢視，甚至不必是 Claude Code 的 agent，可以是 GPT-5.6 之類的其他模型。這種多 agent 協作正是 graph engineering 的典型場景。

### 3. 時效

需要多快完成。沒道理讓一個 agent 依序看完 YouTube 再看 Twitter 再看 Reddit 再看 Gmail。Claude Code 自己就不這樣做——跑 deep research 時不是一次一個來源循序處理，而是同時部署上百個 sub-agent。實際上 Claude Code 在 ultra code 與 dynamic workflows 底下生出來的東西，幾乎都是某種形式的 graph engineering：多個 agent 收集資訊、多個 agent 做綜合、多個 agent 對收集到的資訊做對抗式審查。那些複雜配置中沒有任何一處是靠單一迴圈撐起來的，全是互相連接的迴圈化 agent。

## 判準

不屬於上述三種情境就沒必要用。它只是工具箱裡的一項工具，有時需要、有時不需要；反面代價是替根本不需要的東西加上複雜的步驟與基礎設施。**不確定自己的任務需不需要 graph engineering 時，答案通常是不需要。**
