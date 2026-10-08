---
title: 你用錯 Jev + Claude 的方式了
description: Jev 以機率回答判斷題，又快又便宜；五個常見錯誤：規則書不自我改進、瀏覽器策略、compaction、未稽核、AIOS 路由。
created: 2026-10-08
updated: 2026-10-08
source: https://www.youtube.com/watch?v=1M-z8O29ML8
published: 2026-10-02
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - multi-model
  - token-optimization
  - automation
---

## Jev 是什麼

- Jev 不是聊天機器人，不回傳句子，而是把問題的答案以**機率**回傳。
- 例：客服訊息「我上個月取消訂閱，你們又扣款了」該交給哪個團隊？Opus 會回「這是帳務問題，轉給 billing」；Jev 則回「billing，信心 92%」。答案相同，但 Jev 快約 200 倍、便宜約 400 倍，約每十億 token 43 美元（片尾說 42 美元）。
- 判準：workflow 裡只要有「小而重複的判斷」，就該考慮交給 Jev，而不是 Haiku、Luna 這類小型 LLM。
- 取得管道：Typesafe（typesafe.ai，可能仍需候補，作者幾小時內就拿到）或 OpenRouter。
- Jev 不是執行者：它決定該做什麼、該交給誰做，實際執行仍推給 Claude 或 OpenAI 的模型。

## 錯誤一：當成一次性設定，而非自我改進迴圈

- 情境：每天上百封信，要分成贊助提案、agency 業務、個人、垃圾等類。全交給 Opus 很貴，改由 Jev 快速分類。
- 規則：Jev 信心達 90% 才可歸類，否則交給 Opus。第 1 天只有 43% 達標，第 10 天提升到 81%，大量成本從 Opus 移到 Jev。
- 關鍵做法：每次信心不足轉給 Opus 時，讓 Opus 檢視 Jev 的規則書並提出修訂，下輪更準。
- 每次 Jev 呼叫給三樣東西：
  - 信件本身。
  - 問題：「這封該進哪一堆？brand deal、agency pitch、service pitch、personal、automated，或都不是」。
  - 規則書：定義每一類是什麼。Opus 每輪修改的就是這份。
- 盡量提供「都不是」選項，讓它有出口，避免無處可去而灌水的機率。
- 實務起手式是 **shadow mode**：Jev 先旁觀 Opus 手動分類約 10 天，Opus 回頭依自身行為寫出規則書，之後 Jev 再獨立上線。跟 Opus 說要導入 Jev，它多半會直接提出這個選項。

## 錯誤二：瀏覽器自動化的導入策略不對

操作瀏覽器或在 Doom 中控制角色，本質都是一連串決策，Jev 能大幅加速。但有多種導入策略，要看任務：

| 任務 | Opus 全包 | Opus 規劃一次、Jev 執行 | Opus 與 Jev 迴圈 |
|---|---|---|---|
| Google Flights 查航班（複雜） | 完成，36 輪、約 0.53 美元 | 卡住、失敗 | 最快完成，12 輪、約 0.19 美元 |
| To-do app 建三個任務再逐一勾選（簡單） | 與迴圈相近 | 最快 | 與 Opus 相近（輪數略多、快 2 秒） |

- 迴圈模式：每次需要決策（例如點擊）時，Opus 給一個小計畫，Jev 執行。
- 結論：簡單可重複的任務，讓 Opus 規劃一次後交給 Jev；混亂的真實情境（多半如此）則讓 Opus 規劃、Jev 執行並緊密迴圈。

## 錯誤三：沒讓 Jev 處理 compaction

- 在 400K–600K token 的大 context 中工作既貴、效果也變差（所有模型皆然），通常用 `/compact` 重置並帶入摘要。
- 改由 Jev 處理：600K token 的對話，一般 `/compact` 花 35 秒，Jev 版只要 0.5 秒，也更便宜，因為不必把整段對話送回 Anthropic 伺服器摘要。
- 作者用自己 fork 自 fast Jev compaction 的「Jev compaction plus」skill。
- 原理不是寫摘要，而是逐段問「這段重要嗎」：是就原文保留，否則移出 context（仍存到磁碟，需要時可回查）。
- 作者自行測驗後認為準確度與一般 compact 相當；唯一代價是下一輪起始 token 較多（26K 對 16K，多約 10K）。

## 錯誤四：沒稽核自己的系統哪裡適合 Jev

- 作者提供一個稽核 prompt：讀遍你的 skills、hooks、scripts、automations，找出哪裡正用 AI 做小而重複的判斷、改用 Jev 更合理。
- 作者實跑結果包含：信件分類、AI 新聞過濾；並列出 Jev 要做的判斷、目前怎麼決定、執行頻率。
- 選定一項後再深入討論：選項怎麼設、信心門檻多少才執行。

## 錯誤五：AIOS 裡沒用 Jev 做模型路由

- 作者的 AIOS 語音模式會依任務性質呼叫不同模型（不一定每次都要 Fable、Opus 或 Astra），先前用 Luna 或 Haiku 做分類，便宜但慢，有時路由要花到 5 秒。
- 改用 Jev 後分類只要約 0.1 秒。
- 路由規則分三級：
  - Tier 1：基本 Obsidian 操作，如「在 Obsidian 開 terminal」。
  - Tier 2：如「摘要今天的 AI 新聞」。
  - Tier 3：需要建立專案或產出新交付物、需要更強模型的複雜任務。
- 模型路由與分類不只適用 AIOS，任何 workflow 都是 Jev 的典型用例。

## 總結

五個錯誤的根源都是誤解 Jev 的角色：它把模糊問題轉成機率，適合小而重複的判斷，不負責執行。即使只是大規模試用，成本也低到幾乎不會吃虧。
