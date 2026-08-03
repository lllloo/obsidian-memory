---
title: last30days 技能：介於 web search 與 deep research 之間的輿情研究
description: 開源 skill 讓 Claude Code 平行爬 Reddit、Hacker News、X、YouTube、TikTok 等平台的貼文與留言，抓真實用戶情緒後排序綜合成報告。
created: 2026-08-03
updated: 2026-08-03
source: https://www.youtube.com/watch?v=ShYfGB3x5mM
published: 2026-07-28
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - social-media
  - workflow
---

## 要解決的兩難

用 Claude Code 做研究時只有兩個極端可選：

- **web search**：本質是包裝過的 Google 搜尋，只拿得到 SEO 排名好的文章與新聞標題，停在表層。
- **deep research**：動輒 5 到 20 分鐘、數百個 sub agent、可能燒掉數百萬 token。

last30days 這個開源 skill 卡在中間：爬一大票平台、抓真實的用戶情緒，而不只是標題與 SEO 贏家。作者評價它在「用戶情緒」這一項甚至可能勝過 deep research。

## 涵蓋的平台與成本

repo 有約 55,000 顆星，曾登上當日 GitHub 第一。可爬的來源包含 Reddit、Hacker News、Polymarket、GitHub、YouTube、TikTok、Instagram，另有 LinkedIn、Pinterest、Bluesky 等。

各來源的接入難度分三級：

- **免設定**：安裝 skill 時自動配好，不需要 API key、不需付費。
- **需要相依套件**：Claude Code 在執行 skill 時會帶你裝。
- **需要 API key**：X／Twitter 需要 X AI 的 API key，是唯一真正要花錢的來源，作者實測每次執行平均約 10 美分。TikTok 與 Instagram Reels 需要 scrape creators 的 API key，但安裝流程會幫你開一個補貼帳號，附帶數千次免費呼叫——每天用也足夠撐約半年不必付費。

repo 內有表格說明哪個來源需要什麼、成本多少。

## 運作方式

1. 在 Claude Code 內呼叫 skill（`/last30days` 或直接用自然語言說「用 last 30 days skill」），給一個主題。
2. skill 會先把使用者隨手寫的 prompt 改寫得更好。
3. 判斷主題該打哪些平台的哪些角落——它知道該看哪些 subreddit、哪些 Twitter 帳號相關，然後**平行**搜尋，所以整體並不慢。
4. 深入到留言層，不只讀貼文標題。
5. 排序與綜合：跨平台重複出現的訊號會被大幅加權，避免單一 Reddit 留言歪掉整份報告；同時會標示哪些留言拿到高票。
6. 實際抓取由一支 deterministic 的 Python 腳本執行。

安裝只要一行指令（在 repo README 內）。repo 也說明了 Codex、Cursor 等其他 agent 的裝法，甚至涵蓋 claude.ai 網頁版。

## 實測對照

作者用同一個問題「大家怎麼看 Claude Opus 5」跑兩邊：

- **純 web search**：等於把 Google 上那幾篇主要文章摘要一遍，不算錯，但沒有再往下一層看 Twitter、Reddit 上真正的討論，摸不到草根層的聲音。
- **last30days**：涵蓋 22 個 Reddit 討論串、13 則 X 貼文、14 支 YouTube 影片、26 則 TikTok、13 則 Instagram Reels、16 則 Hacker News、25 個 GitHub 項目，加上 Polymarket。產出能講到短影音圈的反應、當前主流的敘事框架（例如「Opus 5 成本約為 Fable 5 的一半」）、留言區的反彈聲浪，以及專業評測者的整體態度。

所有原始素材（transcript、留言等）會另存成 JSON 檔，報告末尾會標出 raw markdown 與 raw JSON 的位置供回查。

第二次實測改問「大家怎麼看 last30days 這個 skill」，約 5 分鐘完成，產出含一句話總結、即時數據、關鍵模式，並依平台拆解來源數量。

## 使用取捨

- 預設不給 flag 時會判斷相關性、動用所有來源；也可以縮限範圍，例如只查 Reddit 或只查 YouTube。
- 不確定怎麼用時直接問 Claude Code——skill 下載後它就知道有哪些用法與最佳實務。
- **不要每件事都用它**。日常在 Claude Code 內問的隨機小問題，web search 就夠了；last30days 是相對重的動作，該留給真的需要輿情深度的題目。
- 唯一容易卡關的是特定來源的接法，把 repo 連結丟給 Claude Code 讓它帶你設定即可。
