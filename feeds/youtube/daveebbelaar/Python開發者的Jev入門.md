---
title: Python 開發者需要知道的 Jev 全貌
description: 以 Python SDK 實例拆解 TypeSafe 的 Jev 分類模型：Choice、Score、Noul 三型別、多題合併呼叫與對 Haiku 的成本比較
created: 2026-09-23
updated: 2026-09-23
source: https://www.youtube.com/watch?v=JpfLID19QnQ
published: 2026-09-21
parent: "[[01.index]]"
tags:
  - youtube
  - python
  - ai-engineering
  - llm-pricing
---

## 為什麼開發者該關注 Jev

過去一年 AI 業界焦點都在 coding agent 與更強的模型，但打造 LLM 系統或 agentic 系統的工具，自 function calling 以來兩年幾乎沒變。TypeSafe 推出的 Jev（官方稱其模型為 System 1）是這個新類別的第一個模型，作者認為它與打造 AI 應用的開發者直接相關。

### 核心定位：分類模型

- Jev 本質是**分類模型**：可回答是／否、從給定選項中挑一個，或給出各選項的信心分數分布。
- 背景：2023 年前後開發者開始用 function calling 與結構化輸出（JSON）讓 LLM 產出程式可判斷的結果，進而做 if-else、routing。但 LLM 從來不是為此訓練或最佳化，這只是它的附帶能力。
- TypeSafe 把典範倒過來：以一個預訓練語言模型為基礎，在其上加一層額外訓練，讓模型**只能**以這種結構化方式運作。

## 第一個 Python 請求

作者在自己的 AI cookbook repo 提供範例程式（連結在影片說明欄）。

- 安裝 TypeSafe SDK，建立 client，從 console 取得 API key 載入。
- 目前需先登記 waitlist，作者身邊的人通常幾小時內就拿到權限。
- 用法與 ChatGPT、Anthropic SDK 類似：呼叫 client 的 system one 方法，傳入 inputs，取得回應。

範例：

- 狀態（state）：「I was charged twice. Please refund the duplicate.」
- 問題：這張客服單該由哪個團隊處理？選項：billing、technical、other。
- 回傳：`billing`。

單看這一步，和既有的結構化輸出沒有差別。Jev 的賣點在於新模型典範帶來兩個額外屬性：**快**與**便宜**——讓應用程式裡的「智慧 if-else」能以更快、更低成本執行。作者估計比 Claude Haiku 便宜約 20–25 倍。

## 三種問題型別：Choice、Score、Noul

作者認為這是最需要理解的部分。API 與模型都專為分類設計，不必思考 system prompt、user message、結構化輸出資料模型等；API 相當宣告式，輸入格式變化少，這是速度與成本之外的第三個優點。

### Choice：單選

- 從 SDK import `Choice`，建立 input state（字串）、instructions（即輸入提示）與 criteria（類別字典，含類別名與描述）。
- 呼叫 system one 時傳入 state 與 question（question 可另取名稱）。
- 回傳選中的類別，另外可取得各類別機率與信心分數。

### Score：多類別分數分布

- 與 Choice 類似，但 criteria 只給一個清單，不需描述。
- 不是挑一個，而是為每個類別給分數，得到機率分布。
- 範例中「frustrated but civil」信心分數為 1，屬容易分類的案例；訊息越模糊或類別越多，分布就會越分散。

### Noul：是非題

- 本質是布林值（作者猜名稱可能源自 Bernoulli 分布），同樣附信心分數，分數代表「是」的機率。
- 範例問題：客戶是否明確要求退款？回傳 Noul 型別答案，值為 0.98，即 98% 機率為「是」。
- 拿到這個值後即可接各種 if-else 邏輯。

## 速度與成本：與 Claude 比較

作者用 Haiku、Opus 5、Fable 5.1 做速度對照：

- 作者人在歐洲，Jev 平均每次請求約 500–600 毫秒；與同樣適合做分類的 Haiku 相比，並沒有快很多。作者推測在美國、離模型運行地點更近時會更快。
- 對開發者而言更有意思的是成本。以 10 萬次請求、每次約 500 input tokens 估算：Jev 約 2 美元，Haiku 約 50 美元，相差 25 倍。確切價格請見官方定價頁。
- 作為同類首款模型，作者預期價格還會大幅下降。

## 在一次 API 呼叫中合併多題

- API 支援把多個問題組合：以一張客服單作 input state，建立一個包含 Choice、Score、Noul 的問題字典，一次呼叫就同時得到類別、挫折程度與是否要求退款。
- 系統越大、疊加的判斷越多，這種設計越能勝過現有 LLM 做法：API 更簡單、程式碼歧義更少，也少了一堆需要人維護的「假 system prompt」，更偏程式化。
- 因為更快、更便宜，把大量判斷塞進同一系統、依「這件事成立且另外五個條件也成立」細緻分支，會變得划算。
- 作者一直主張：最可靠的 AI 應用仍是 workflow 模式——router、if 判斷分支。這些模式本質上就是組合 Choice、Noul、Score，一路判斷到 workflow 的葉節點，再執行動作或呼叫函式。

## 作者的評價與部署考量

- 可能是 AI 發展的關鍵轉折點，但目前還很早：第一家、第一款同類模型，公司也很新。
- **資料隱私**是作者替客戶建置方案時的主要顧慮。TypeSafe 有資料政策，但作者尚未細讀；即使政策沒問題，要向荷蘭或歐洲客戶解釋資料需分享給一家新的美國公司仍不容易。目前他們透過 Microsoft Azure 使用 OpenAI 模型，這條路已經被接受。
- 預測三個月內 OpenAI、Anthropic 等大廠都會推出類似產品，進一步壓低成本、提升速度。
- 期待開源追上：大模型負責推理與大型任務，可自行架設的小型開源模型負責高精度分類。
- 認為這會帶起新趨勢，尤其對未來幾年會大幅成長的 computer use、browser use 特別有利。
