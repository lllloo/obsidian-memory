---
title: 你用錯 GPT-6 Astra 了（以及修正方法）
description: 使用 GPT-6 Astra 常犯的五個錯誤：effort 開太高、沒用瀏覽器與 computer use、skill 未清理、忽略 voice mode、prompt 沒交代遇到分岔時該問還是自行決定
created: 2026-09-15
updated: 2026-09-15
source: https://www.youtube.com/watch?v=5EhrMJ9HIfU
published: 2026-09-10
parent: "[[01.index]]"
tags:
  - youtube
  - codex
  - prompt-engineering
  - workflow
---

## 錯誤一：effort level 開太高

- 很多人在 Codex 直接把 effort 拉到 max 甚至 ultra，以為輸出一定更好——事實並非如此
- 除非是極複雜的專案，否則不該超過 high，很多情況 medium 甚至 light 就夠
- 講者引用的長時間 agentic 任務 benchmark（transcript 稱 Deep Sweep）數據：

| effort | 分數 | 每任務平均成本 |
|---|---|---|
| max | 73% | $12 |
| extra high | 高於 max | 約 max 的一半 |
| high | 與 max 相同 | $5.72 |
| medium | 與 max 幾乎相同 | — |
| low | 67% | $2.19 |

- 對照 Fable 5：Astra 的 low 大約落在 Fable 5 high 與 medium 之間，而後者約 $7 的價位
- Artificial Analysis coding agent index：low 為 $1.50、62.6 分；max 為 $4.98、67 分
- 部分 benchmark 上 max 在兩端確實較好，但 Terminal Bench 上 high 反而比 max 分數高且更便宜
- 前端設計實測（虛構的 Joshua Tree 沙漠精品旅館 Dune House 首頁，同一 prompt）：
  - light：13 分鐘完成、用 91,000 tokens
  - max：30 分鐘完成、用 152,000 tokens
  - 成品差異不大，兩邊都說得通
- 原則：less is more，從低開始，輸出不滿意再逐步調高；沒有理由一開始就用 extra high、max 或 ultra
- 訂閱方案雖不按任務計費，但低 effort 燒掉的每週用量明顯較少

## 錯誤二：沒善用瀏覽器與 computer use

- 這兩項能力讓 Astra 連接沒有 CLI、MCP 或 API 可用的應用程式
- 範例：要改進前述網站時，不自己上網找參考，而是讓 Astra 在右側瀏覽器開 Dribbble，搜尋 hotel website、點進個別作品截圖，再帶回 Codex 產出新版網站
- 瀏覽器會保存登入狀態；Astra 也照慣例確認手機版與跑測試，還產出參考對照表（使用了哪些截圖、筆記與 Dribbble 原始連結）
- 講者更喜歡新版與它生成的主視覺圖
- 可延伸到 Pinterest、Twitter 等任何想擷取資訊但沒 API 的應用

## 錯誤三：skill 配置不對

- Codex 現在的處境如同幾週前的 Claude Code：Boris Cherny 曾說要刪掉 CLAUDE.md 與 skills，重點不是為刪而刪，而是 Astra、Fable 這類模型已強到讓許多為舊模型設計的鷹架型 skill 失去作用，甚至拖累表現
- 講者認為 superpowers、GSD 這類重鷹架 skill 大多該淘汰
- 就算不同意，context window 也多半塞滿久未使用的 skill：光是 description 就會累積，可能有 30～50 個與現在工作無關
- 講者做了 **skill audit** skill，基於 Anthropic 的 skill creator skill（因其含 benchmark 與測試機制；Codex 自己的 skill creator 較不完整）：
  - 附安裝方式與可直接執行的 prompt
  - 掃描所有 skill 與使用紀錄，找出完全沒用、該修剪的 skill
  - 檢查 skill frontmatter 的 description 是否合理
  - 可逐一對 skill 跑 benchmark 測試，判斷搭配 Astra 是否仍有意義
  - 分組為：fix now、review for retirement、test next、test later、preserve
- 效益：釋放被閒置 skill 佔用的 context；灰色地帶的 skill 經 benchmark 後可改進，不再猜測是否有幫助

## 錯誤四：沒用 voice mode

- Codex 的 voice mode 被講者評為同類最佳，勝過 Claude Code desktop，並隨 Astra 升級
- 以前由 GPT Terra（講者認為是 light effort）驅動，且只能在獨立聊天面板當 orchestrator 使用
- 現在可選 Astra high 或 Astra low，並有兩種用法：
  - **orchestrator**：在獨立 voice chat 指揮開新 chat、派工，一個語音面板控制多個 agent
  - **單一 chat 內**：直接在既有對話中用語音下指令
- effort 建議：在 chat 內要它實際做事（如加表單）用 high；當 orchestrator 或只是來回對話用 light
- 示範一：語音要求在網站 footer 附近加「索取更多資訊」表單，研究該放哪些欄位的最佳實務，暫不需串接 Resend 等實際功能；回應非常迅速，完成後它用瀏覽器游標實際測試表單
- 示範二：以 light 開 orchestrator，要求開新 chat 讓 Astra 研究 voice mode 前五大使用案例並寫成 HTML 文件；新 chat 標示由 ChatGPT 發送，並顯示轉派的 prompt
- 講者認為 voice mode 最大的突破是當 orchestrator，適合同時跑多個 agent 的人

## 錯誤五：prompt 寫法不對

- OpenAI 表示：遇到分岔或需要假設時，Astra 比 GPT-5.6 Sol 等舊模型**更傾向詢問釐清**，而舊模型會自行假設
- 因此在長時間、複雜的 agentic 任務 prompt 中，應寫明遇到分岔時要一律提問，還是自行帶著使用者意圖完成任務
- OpenAI 提供了對應 prompt，講者也提供模板；關鍵是你要清楚自己希望它怎麼表現
- 兩種路線各有利弊：放手讓它「自己想辦法」容易 regression to the mean，除非事先設好足夠的鷹架指引分岔時的方向
- 另一個 OpenAI 建議的做法：要求模型**只在準備好具體、可審閱的成果之後才請求批准**，避免在本可自行完成時卡住任務——不要只帶問題來，要帶問題加解法

## 結語

- 講者認為 Codex 在 browser use、computer use、voice mode 上領先 Anthropic 與 Claude Code desktop app，建議都試試
