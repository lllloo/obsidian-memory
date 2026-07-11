---
title: Jarvis Fable 5 Agentic OS 架構拆解
description: 在 Claude Code 上疊一層 web app，用本地語音模型、skills 變按鈕、Obsidian 串接，把日常工作流封裝成非技術團隊也能一鍵執行的個人助理 OS。
created: 2026-06-15
updated: 2026-06-15
source: https://www.youtube.com/watch?v=PW0sgog3kXY
published: 2026-06-14
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - obsidian
  - workflow
---

## 這是什麼

Jarvis 是一套蓋在 Claude Code 之上的 agentic OS（web app），作者用 Fable 5 建出來，但**執行時不需要 Fable 5**，多數元件可跑本地模型、換成任何模型。定位不是拿來蓋大型專案，而是「個人助理 / 任務管理器」，特別適合包給非技術的團隊成員或客戶使用。

核心價值不在花俏 UI，而在底層那套**完全可客製的 Claude Code skill 架構**：把日常手動工作流與重複任務轉成 skills 與 automations，UI 只是疊在這層基礎上的呈現層。

## UI 上看得到什麼

- **本地語音**：完全本地運作，比起繞 11 Labs 之類雲端服務更快更即時。開場那段「今天的 rundown」不是寫死的腳本，而是 Jarvis 去讀 Obsidian Vault 內自動生成的各種報告，判斷哪些重要再講給你聽。
- **彈出視窗（popups）**：講到某主題時帶出相關報告或連結（最新影片數據、新聞來源文章、morning report 全文）。報告本體存在 Obsidian，可直接「在 Obsidian 開啟」原始檔。
- **skills 變按鈕**：右側把 Claude Code 的 skill / automation 變成一鍵執行的按鈕（如 inbox brief）。對不願開 terminal 的非技術使用者，這是把 Claude Code 的能力交到他們手上的方式。執行時顯示佇列狀態與進度條，完成後可同時產生書面報告與口頭摘要。
- **左右側欄全可客製**：右側有每日行程（串 Google Calendar）、音訊波形、AI 新聞摘要；左側有 vitals（訂閱數、最新影片、近 5 小時 Claude token 用量）、directives（今日該做的前三件事，由 Claude Code 依行程動態判斷）、documents trail（Jarvis 建立或引用過的文件）。作者強調這些都是範例，metrics 與想一鍵執行的東西人人不同。

## 一句話如何被處理（路由架構）

從你開口到 Jarvis 回覆，流程如下：

1. **語音轉文字**：你的聲音送進 **Faster Whisper**（免費、本地），轉成 transcript。
2. **路由判斷**（決定「誰來做、走哪條路」，三選一）：
   - **Regular expressions（regex）**：純程式、不涉 AI，比對預先寫死的觸發詞。例如「rundown」是 trigger word，命中就直接執行對應動作。優點是不花錢、極快。
   - **Haiku**：多數請求語意較模糊、需要一點智能判斷路由時，用最便宜最快的 Anthropic 模型來分流。Haiku 很擅長這種「判斷該走哪條路」的任務，每次請求只花幾分錢的零頭。注意 Haiku **只負責路由，不負責執行**。
   - **本地模型**：也可完全不用 Haiku，改用本機模型做同樣的路由判斷，更貼合整套系統的本地取向。
3. **判斷資料是否已存在**：路由後，先看 Obsidian 裡是否已有對應報告。已存在 → 直接讀取並回應；不存在 → 叫 Claude Code 去生成。
4. **執行（用較強模型）**：生成工作交給 headless Claude Code（等於開一個隱形的 Claude Code，用 `-p`）。預設用 **Opus**，可改 **Sonnet**，未來也可換 Fable 5。產出報告上傳 Obsidian，再讀回、生成摘要。
5. **文字轉語音**：摘要送進 **Kokoro**（本地開源語音模型，類似迷你版 11 Labs），轉成語音回放給你。聲音可任意替換。

## 成本與適用邊界

- headless Claude Code 用 `-p` 的計費：影片提到約一兩天後將**不再從訂閱額度扣**，而是吃 Anthropic 每月給的 $200 額外 API credits。
> 影片為作者當下說法，確切計費政策請回查官方公告，勿釘死。
- 大規模下這可能成問題，所以很多任務建議用 Sonnet。但 Jarvis 的定位是個人助理層級的任務，作者認為一般用 Sonnet 不太會跑完 $200。真有疑慮就別用 Claude Code 做這層 —— 整套基礎設施可換成 Codex、本地模型等，不綁 Claude Code。

## Skill 架構才是真正的骨幹

- 所謂「morning report」其實是一個 **skill**，由多個小 skill 組成（去查這些來源、查這些社群頁面取資訊等）。
- 整套威力取決於 skill 架構建得多紮實。建法是：把你個人或業務中**反覆執行的日常工作流**，跟 Claude Code 一起拆成一個個獨立任務，再把任務轉成 skills，合理時再把 skills 升成 automations。
- 作者實例：把搜 YouTube 找資訊做成 **YT pipeline skill**（抓影片送 NotebookLM 出摘要）；把跨 Twitter / 網路的深度研究做成客製 **deep research skill**；把 LightRAG 的 graph RAG 查詢系統整個包成 skill。然後在內容、社群、agency、銷售等各領域重複這套做法。
- 做法具體到「打開 Claude Code，用意識流講出你每天做什麼，再問能不能把這些變成 skills」即可。
- 為何要 skill 化：當 headless Claude Code 跑的是已 codify 的 skill，輸出會**正確且一致**，因為流程已事先映射、不留給 AI 隨機發揮的空間。AI 系統越偏 deterministic 越好，越少受「也許會做對、也許不會」的不確定性影響。

## 可分享與可換掉

- 因為是 web app，可打包分享給團隊成員或客戶。對方只需告訴你客製需求，任何人坐上這個位子就能拿到作者日常使用 Claude Code 約 80–90% 的能力（那些 skills 與 automations），全在一鍵之遙。
- 整套基礎設施可抽換：Claude Code 可換 Codex 或本地模型；語音、轉錄、路由各環節都可替換成其他開源 / 本地方案。作者最看重的就是這份可客製性與大量本地化的彈性（甚至可接成 Slack 之類的整合）。
