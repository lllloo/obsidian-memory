---
title: 值得用的 17 個 Claude Code Plugin
description: 依 design、productivity、data 三類整理 Claude Code 進階堆疊的 plugin、skill 與 CLI，涵蓋前端設計、token 節省、研究抓取、資料庫與記憶系統等實用工具。
created: 2026-06-29
updated: 2026-06-29
source: https://www.youtube.com/watch?v=V2RIVnGCy74
published: 2026-06-26
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - workflow
---

Claude Code 原生已經很強，但加上 plugin、skill 與 CLI 可以再放大能力。作者把自己實際在用、認為值得花時間的工具分成三桶：design、productivity、data，逐一說明是什麼、怎麼運作、為何值得用。

## Design（設計）

常有人說 AI 缺乏「品味」，這桶工具都在處理前端設計、對抗 AI slop。

- **taste skill**：開源 GitHub repo，主打打敗「AI slop 怪獸」。內含多個子 skill（image-to-code、redesign、output 等），目標是讓前端設計、網站更好看。不限 Claude Code，適用所有 agent。適合用 AI 做 landing page 或設計導向頁面。
- **Impeccable**：另一個開源前端設計 skill，同樣在改善 Anthropic 預設的設計品質。近期被 GitHub Copilot app 納為內建層。單一 skill 但含 23 個指令（記錄、批判、polish、變大膽、變安靜等）。官網 impeccable.style 可看每個指令的前後對比。另有 beta 的 browser editor：在瀏覽器叫出網站、選取元素直接下指令改，即時看到變化，不必全部走 terminal——這個 live editor 是它和 taste skill 的主要差異。
- **awesome design.md**：把「已存在的網站」當成要打造頁面的範本，基於 Google Stitch 的 design.md 原則。例如點選 Airtable，就會拆解該站的結構、配色、surface、文字、字體、間距、按鈕等，當成自己網站的building block——不是複製網站，而是借用其設計語言。依用途（fintech/crypto、設計與創意工具、productivity SaaS 等）分類。

## Productivity（生產力）

- **Ponytail**：成長最快的 AI repo 之一，讓 Claude Code 更快、更便宜、寫更少程式碼但維持相同產出。官方數字（用 Haiku 測）：少寫 50% 程式碼、少用 22% token、便宜 20%、快 27%。運作方式是寫程式前先問幾個問題：這需要存在嗎？code base 已有嗎？標準函式庫做得到嗎？原生平台功能有嗎？是已安裝的依賴嗎？是一行就能解的嗎？通過後才寫，且只寫剛好能動的最小量。用 Opus 測時數字更誇張。
- **NotebookLM CLI**：把 Claude Code 接上 Google NotebookLM（免費）。NotebookLM 沒有 API，這個 CLI 繞過此限制，讓你在 terminal 做 NotebookLM 能做的事（丟 PDF、文件、YouTube 影片進去再對話，產出簡報、圖片、infographic、影片等）。CLI 甚至比 web app 多功能：批次下載、quiz 與 flashcard 匯出、存對話到 notes。作者最常搭 YouTube 用（取連結、抓 transcript、回答問題）。
- **Playwright CLI**：瀏覽器自動化，被作者視為最強工具之一。沒有 API 時讓 Claude Code 像人一樣上網站點選、填表單。也很適合前端設計：例如測試網站表單的各種 edge case，可同時開大量瀏覽器自動測完。注意別跟 Playwright MCP 搞混——CLI 比 MCP 更有效、用更少 token。
- **Codex plugin**：OpenAI 官方 plugin，把 Codex 與 GPT 模型接進 Claude Code。適合 code review 或對抗式審查（Claude Code 偏愛自己寫的程式碼，需要第二雙眼）。含 `codex rescue` 等指令，可把整個 feature 丟給 Codex，讓 Claude Code 與 Codex 同時各做一塊。
- **GWS（Google Workspace CLI）**：非官方，由 Google 工程師做（後來因太紅而被解雇）。比 Google connector 多功能（例如可寄 email），含 40+ skill（weekly digest、report、meeting prep、email to task 等預載工作流）。安裝設定較複雜。
- **GitHub CLI**：人人都該有，建議第一個裝。用 Claude Code 做東西最終都要 push 到 GitHub，CLI 讓這件事極簡單。
- **skill creator skill**：Anthropic 官方 skill。不只建立新 skill，還能修改、改進既有 skill 並衡量效能。可自動做 AB test 比較 skill 的不同版本、或有無 skill 的差異，得到客觀證據。安裝：Claude Code 內 `/plugin` 搜 skill creator 即可。作者認為它是最重要的 skill。

## Data（資料）

涵蓋資料庫、研究、抓取與記憶。

- **last 30 days**：曾是 GitHub 第一名 repo，做的研究遠超單純 web search，深入特定來源（Reddit、Twitter、YouTube、TikTok、Reels、Hacker News、Polymarket 等），看人們在各平台怎麼談某主題。適合 daily briefing 或需要真實資料的產出，也是 `/deep research` 之外較省 token 的替代。
- **Firecrawl CLI**：最強的 web 抓取工具之一，尤其面對有 bot 防護的頁面。有付費版（專有模型，攻克 bot 防護最強）與開源版（功能大致涵蓋）。除了抓取還能與頁面互動、發現並爬遍網站所有 URL，設定可細調。適合「只要一個工具做特定抓取」的情境。
- **auto research（來自 Karpathy）**：machine learning in a box。給一個有客觀、可量化成功標準的應用（例如 Python 程式跑更快，1 秒 → 0.99 秒），它就一輪輪自動跑實驗試圖改進，並記錄每次試了什麼、有效與否。範例跑了 83 次實驗、得到 15 項改進，全自動。輕量，但只適合有明確客觀成功標準的任務。
- **Supabase CLI**：免費額度大方，涵蓋建應用的多數需求。可由 Claude Code 用自然語言建資料庫（例如存表單蒐集的 email），也處理 authentication（網站登入）。可本地執行。
- **Obsidian**：改善 Claude Code 記憶最簡單的方式之一。把電腦資料夾指定為 vault，在 vault 內開 Claude Code，它就透過文件的 knowledge graph 取得整套文件地圖，能有效率地回答相關問題。
- **Obsidian skills**：GitHub 搜「Obsidian skills」可找到，由 Obsidian 創辦人建立的簡單 repo，教 Claude Code 整合進 Obsidian 堆疊的最佳實務。
- **LightRAG**：真正的 RAG / knowledge graph + embedding（相對於 Obsidian 的「偽 knowledge graph」）。輕量、快，是入門複雜 RAG 系統的好起點，查詢全程可走 Claude Code。
- **RAG-Anything**：LightRAG 之後的進階版，從純 PDF / 文字擴展到圖片、graph、chart 等傳統 RAG 或 Obsidian 較難處理的內容。
- **Stripe CLI**：要靠應用賺錢、處理交易時用。Stripe UI 操作繁瑣，CLI 讓透過 terminal、自然語言與 Claude Code 控管應用變得容易。
