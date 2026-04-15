---
title: AI週報：Claude Code 洩漏揭示 AI 未來架構
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-04-03
source: https://www.youtube.com/watch?v=BZ1hs2ZcnJc
---

## Claude Code 原始碼洩漏

透過 npm registry 的 map 檔案洩漏，Anthropic 正積極 DMCA 下架，但原始碼已在 GitHub 廣泛流傳。工程師失誤（手動 deploy 步驟未自動化）造成，無客戶隱私資料外洩。

### 三層記憶架構

洩漏內容揭露的記憶系統設計：
- **MEMORY.md**：作為輕量索引，永久載入 context；儲存指標位置，不儲存資料本身
- **Raw transcript**：從不完整載入 context，只用 grep 搜尋特定識別符
- 整體為「自我修復記憶系統」，移離傳統的全量儲存/全量取回模式

### Chyros：背景 Daemon Agent

最重要的發現——Chyros 是一個「always-on 主動式 Claude」：
- 每幾秒收到一次 heartbeat prompt（「現在有沒有值得做的事？」）
- 可自主修復 bug、回應訊息、更新檔案、執行任務
- 三個 Regular Claude Code 沒有的專屬工具：
  - Push notifications（主動推送到手機或桌面）
  - File delivery（不需要請求就主動送出建立的檔案）
  - Pull request subscriptions（監控 GitHub，自動反應程式碼變更）
- 每日記錄所有行動日誌

這代表 AI 從「被動回應」進入「主動背景運作」時代——使用者不需要坐著下 prompt，AI 會學習使用者需求並主動處理。

### 其他洩漏發現
- 更多 Capiara / Mythos 模型證據
- Hidden Buddy System：類似電子雞的終端機寵物（chaos、snark 數值），疑似 4/1 愚人節玩笑被迫中止

## OpenAI 史上最大融資

- 募資 $122B，估值 $852B，史上最大單次融資
- 月營收達 $2B
- 成長速度為 Alphabet 和 Meta 在各自互聯網與移動時代的 4 倍
- Microsoft 仍持續投入，否定外界傳言的決裂

### OpenAI Super App 計畫

從融資公告末尾揭露：將 ChatGPT、Codex、瀏覽器、Agent 整合為單一平台，方向與 Anthropic 的 Claude App（含 Co-work 和 Code）雷同。

### Sora 每日燒錢 $1M

Sora 在停止前每天虧損約 $1M，年虧損超過 $3.65 億，這解釋了為何必須關閉。

## 模型新聞

### Gemma 4（Google）
- Apache 2.0 開源，設計用於 Android 裝置與 laptop GPU
- 支援 agentic 工作負載，適合本地跑 OpenClaw 等 agent

### Qwen 3.5 Omni 與 Qwen 3.6 Plus（Alibaba）
- **3.5 Omni**：全模態（文字、圖片、音訊、影片），聲稱在音訊理解超越 Gemini 3.1 Pro
- **3.6 Plus**：專注 agentic coding，預設 1M token context window，Terminal Bench 超越 Opus 4.5

### Arcee Trinity-Large-Thinking
- Apache 2.0 開源，美國公司出品
- 整體表現與 Opus 4.6、GLM-5 相近

## 其他快訊

- **Microsoft MAI-Transcribe-1**：語音識別，25 語言最佳準確率，處理同音異義詞表現良好；已在 Microsoft Foundry 開放給開發者
- **Veo 3.1 Lite**：Google 降低影片生成定價（720p 每部僅 $0.05），4/7 進一步降價
- **Google AI Inbox**：郵件智慧摘要與優先排序，目前限 $250/月 Ultra 方案
- **Recraft V4**：品牌視覺 AI 工具，新增真正可編輯 SVG 的向量生成
- **Computer Use in Claude Code**：已加入 Claude Code，Pro/Max 方案可預覽
- **Codex Plugin for Claude Code**：可在 Claude Code 內使用 OpenAI Codex key
- **ChatGPT in CarPlay**：可在車內與 ChatGPT 對話
- **OpenAI 收購 TBPN**：Tech Business Production Network 每日直播新聞節目
- **Perplexity 稅務 AI**：可協助填寫聯邦報稅表、審查 CPA 準備的申報書
- **New AI Slackbot**：30 項新功能，含會議轉錄、MCP client、Salesforce 客戶管理
- **AI 汽車設計（GM）**：將手繪草圖轉為概念影片、模擬空氣動力學
- **AI 智慧購物車（Instacart）**：搭載 Nvidia Jetson，即時追蹤購物車內容與位置
