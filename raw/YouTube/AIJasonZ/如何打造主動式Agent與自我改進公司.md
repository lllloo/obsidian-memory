---
title: 如何打造主動式 Agent 與自我改進公司
description: 拆解 AI 原生公司的閉環運作：用記憶層加 cron job 讓 agent 自我迭代，並以 SEO、廣告投放等案例說明 proactive AI loop 的搭建方式與工具。
created: 2026-06-03
updated: 2026-06-03
source: https://www.youtube.com/watch?v=ikH1--DSzMs
published: 2026-06-02
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
---

## 從 AI 增強到 AI 原生的轉變

過去任何公司營運中，人類是「黏合劑」：使用多套不同工具拼湊出某個成果，並由人類決定優先順序與該做什麼。AI 熱潮後多數人轉到「AI 增強工作流」——你叫 agent 或 AI workflow 端到端完成一個任務，但缺一個回饋迴路把結果送回去指導改進，人類仍是主要的優先排序、規劃與觸發者。

真正的 AI 原生迴路（AI native loop）則是：agent 接收某個目標的輸入或觸發，執行任務，最關鍵的是**捕捉回饋**以學習什麼有效、什麼無效，再規劃下一步，確保下次做得更好。YC 已開專場討論這種「自我改進公司」（self-improving companies），當期 batch 的公司宣稱每員工營收較 18 個月前提升 5 倍，agent 自主處理內部營運並自己寫了 45 個工具。

## 閉環 vs 開環的控制系統觀點

YC 的 Diana 用控制系統的概念解釋：

- **開環（open loop）**：系統沒有回饋路徑。
- **閉環（closed loop）**：狀態、決策與結果被持續捕捉並回饋進「智慧層」。

閉環的五個核心要素：

1. 資料如何攝入（ingest）系統。
2. policy 層：類似 workflow 與 SOP 的「契約」。
3. 讓 agent 存取不同系統的存取層。
4. workflow 中的品質閘門（quality gate）：讓人類或 AI evaluator 守住輸出品質。
5. 把學習帶回系統的機制，讓它能改進自身營運。

## 主動式 AI loop 的基本搭建

核心三件套組成閉環：

- **記憶層 / 環境**：讓 agent 保有任務與結果的記錄，以及可用的 skills。記憶層常拆成兩部分：
  - **temporal log**：記錄 agent 每天 / 每週做了什麼。
  - 從 log 持續形成的**最新策略**，把所有學習灌注進去。
- **skills（含 CRI/CLI）**：讓 agent 自行端到端跑完整迴路，例如 SEO 稽核、草擬內容、發布、從 Google Analytics 或 Ahrefs 讀資料。
- **cron jobs**：讓 agent 遞迴地對行動反覆執行；可加一個每週規劃的 cron job 做「auto dreaming」式設定。三者合起來形成閉環——agent 持續監控結果、發布內容、更新假設。

## 案例：SEO 自我維持迴路

SEO 是很好的起步用例，因為它是「可被工程化」的已解問題。人類本來在做的迴路是：跨 Google Search Console、網路、Ahrefs 做研究形成關鍵字策略，依策略產出社群內容與網頁，持續監控成效，必要時更新策略。把這個迴路交給 agent 自我維持即可。

影片提到 HubSpot 的免費 **AEO（answer engine optimization）** 工具：AEO 目標是提升你的產品在 ChatGPT、Perplexity、Gemini 回答中出現的機率，補足傳統 SEO 沒涵蓋的 AI 回答引擎渠道。輸入公司名稱，它會分析 ChatGPT、Perplexity、Gemini 如何描述你的品牌，給多維度評分與可改進的成長領域。可把稽核報告帶回 agent 形成關鍵字與內容策略，甚至包成一個 skill 定期執行取得更豐富資料。

## 案例：自主廣告投放優化

朋友 Gio 用 Claude（power Claude）加 skill 設定，讓 agent 自主投放廣告數個月：

- skills 涵蓋成效分析、文案撰寫、圖像生成、研究。
- 維護一個 state 資料夾記錄所有 change log 與學習，外加 campaign 歷史與 live ads 的 JSON 檔。
- 第一週 agent 測試 10 種廣告格式（白板手繪、筆記頁、紙板科學、推文截圖等），學到「看起來醜的廣告素材反而成效更好」。
- 第二週依學習決策：用白板格式加特定文案，內容圍繞一個免費 skill pack，最終在約 $1,500 預算內數月產出 243 個 leads。

另有 Ankit（AI Buildup）用類似 SEO 迴路，在一到兩個月內把流量提升 3 倍，涵蓋成長分析、設計網站資訊架構、撰寫高品質 SEO 內容。

## 記憶層：事實記憶 vs 程序學習

支撐這些迴路的記憶分兩類：

- **事實記憶（factual memory）**：agent 做過的事的 log，用來記住做過什麼、回顧成效。
- **程序學習（procedural learnings）**：通常可轉成一個 skill。

可以直接 prompt agent 把一切存成 log，但資訊雜亂或結構複雜時日後很難檢索。因此有開源記憶層可重用。

### Jbrain（實體導向記憶）

Gitan 的 **Jbrain** 是可用於 Claude Code 的 plugin，內含處理資料的指令，能存取會議逐字稿、YouTube 影片字幕等原本難擷取的資料：

- 資料存進預定義 entity 的資料夾結構。類比 Andrew Karpathy 的 LLM wiki，但 wiki 主要為消化研究論文設計，Jbrain 則為個人助理用途記錄 entity（會議、人、program、purchase）。
- 每個資料夾有 readme 說明該 entity 該放什麼，每個 entity 用 markdown 結構記錄事實與時間軸 log。
- 附帶檢索 pipeline：所有知識自動轉成 vector DB，搭配 CRM 與 MCP 工具供搜尋，適合管理數十萬 entity 的個人助理場景。

### Looping（公司在迴路中）

講者團隊（Stone X）實驗的另一種 entity 記憶設定，稱為「公司在迴路中」（company in the loop），針對長週期任務與自我學習行為優化記憶層：

- agent 有對應 cron job 輸出學習與 skill 提案。
- 把指令複製給任何 agent（如 open Claude），它就會在電腦上建好記憶層，並有幾個預定義 artifact。
- agent 會一步步問你想建立什麼 AI loop、想讓 agent 驅動什麼 mission。例如說「我想讓 agent 自主草擬社群內容、每天驅動我 Twitter 的成長」，它會逐題詢問需要建哪些 API skill，以及語氣、節奏等程序知識，可來回對話後建立對應 artifact 與 cron job。
- 具體案例：建出一個 post draft artifact，記錄草擬過的內容與回饋，搭配的 cron job 會掃描先前相關節點與資訊並生成新內容；每日 cron 還會抽取學習並提出 skill 更新提案。

## 資料存取與 agent 原生 CLI

agent 常無法存取某些特殊類型資料，因此 loopony plugin 常搭配**資料存取 skill**做資料注入——把「如何存取特定資料」的策略包成 skill 很有幫助。講者把自己的資料存取 skill 放在 agent skill 101 可複製使用。

另一個開源工具 **printing press** 解決的問題：多數 API / MCP / 官方 CLI 不是為 agent 設計，token 效率差，且常見問題包括——可能進入互動模式（agent 不擅長互動）、錯誤訊息資訊不足無法自我修復、CLI 有時回傳大量資料。

Trevor 有篇文章談「設計 agent 原生 CLI 的 10 個原則」，printing press 把這些原則封裝成一個 CLI skill：可請 agent 自主研究並建立任何 CLI（存取內部資料庫，或沒有官方 MCP/CLI 的第三方軟體），照這些原則打造高效的資料注入。
