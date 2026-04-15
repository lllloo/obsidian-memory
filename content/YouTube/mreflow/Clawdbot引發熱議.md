---
title: 為什麼大家對 Clawdbot 瘋了
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 
source: https://www.youtube.com/watch?v=GLwTSlRn6-k
---

## 什麼是 OpenClaw（原 Claudebot）

- 由 Peter Steinberger 開發的開源 AI agent 框架，最初以 Claudebot 命名，後改名為 OpenClaw。
- 核心特色：不只是聊天，而是能在你的電腦或伺服器上**實際執行任務**的自主 agent。
- 一週 200 萬訪客，201,000 顆 GitHub 星，GitHub 歷史上成長最快的開源專案。

## 五大關鍵差異

1. **本地運行**：在你的電腦或 VPS 上執行，可存取本地檔案、系統與應用程式（亦可連接雲端 API）。
2. **多通道控制**：透過 Telegram、WhatsApp、Slack、Discord 等從手機或任何裝置下指令、收通知。
3. **完整系統存取**：可執行終端指令、寫腳本、安裝軟體、甚至修改自身配置。
4. **持久記憶**：記住所有跨對話的偏好、專案背景、溝通風格。
5. **自我改善**：可撰寫並安裝新的 Skill（可重用工作流），自行擴展能力。

## 費用結構

- OpenClaw 框架本身免費（開源）。
- 費用來源：VPS 主機費用 + 所使用 API 的費用（Claude API、GPT API、ElevenLabs 等）。
- 若有 Claude Max 訂閱（$200/月），可用固定費用跑 Opus 模型。

## 安裝選項

- **直接安裝到主電腦**：最簡單但風險最高（對檔案有完整存取權）。
- **獨立電腦（Mac Mini ~$600）**：隔離風險，社群流行做法。
- **AWS EC2 免費方案**：影片中採用的方式，8GB RAM Ubuntu 虛擬機，初始免費。

## 安裝流程（AWS EC2 + Slack 示範）

1. 前往 aws.amazon.com，建立帳號，選 EC2，啟動 Ubuntu 8GB 免費實例。
2. 進入 EC2 終端，執行 claud.bot 提供的快速安裝指令。
3. 選擇 AI 模型（需提供對應 API key 或授權 Claude Max）。
4. 選擇通訊頻道（Slack）：在 api.slack.com 建立新 App，貼入提供的 JSON manifest，取得 Bot Token 和 App Token。
5. 設定允許 Slack 頻道，邀請 Bot 進入私人頻道，完成連線。
6. 選擇初始 Skills：ClaudeHub、Gemini CLI、視訊框提取、URL 摘要、Whisper 語音轉文字、PDF 編輯、Nano Banana 圖像生成等。

## 實測示範

- **大腦傾倒（Brain Dump）**：提供個人資訊後，agent 自動建議適合的自動化任務（AI 新聞聚合、郵件整理、工具監測）。
- **每日 AI 新聞摘要**：下指令後 agent 自動設定 cron job，每天早上 8 點自動抓取新聞並傳送至 Slack。
- **程式碼開發**：請它安裝 Claude Code 和 Remotion，並要求生成動畫——agent 自行解決安裝問題、設定公開存取 URL。
- 動畫品質尚可，但整個過程完全不需手動操作。

## 社群使用案例

- 10 分鐘完成 California LLC 表單（拖延 18 個月的任務）。
- 連接 Meta Ray-Ban 智慧眼鏡：拍照後傳 WhatsApp，自動記錄費用、加行事曆、將白板照片轉為整潔資訊圖表。
- 語音對話管理媒體伺服器（連接 OpenAI + ElevenLabs）。
- 自學如何控制 Sleep Number 床鋪並建立 Skill。
- 連接 LM Studio 在本地 GPU 跑模型，無需付費 API。

## 安全風險與建議

- 93% 的公開 OpenClaw 實例存在安全漏洞，暴露 Email、行事曆、Slack 憑證。
- MoltBook 因資料庫設定錯誤洩漏 150 萬組 API key。
- Gartner 建議企業立即封鎖相關流量，CrowdStrike 發布移除工具。
- **Prompt Injection 風險**：若 agent 瀏覽的網站中藏有惡意指令，可能被劫持執行未授權動作。

**安全建議：**
- 在獨立機器或 VPS 上執行，不要在主電腦。
- 連接 WhatsApp 時使用專用電話號碼，Email 使用全新帳號。
- 不要授予超過「剛雇用的外包人員」所需的存取權限。

## 更大的意義

- OpenClaw 展示了 AI 的發展方向：從「給建議的助理」進化為「去執行任務的代理人」。
- Prompt engineering 將退場，用戶只需說出目標，agent 自行選擇工具、模型與方法。
- 社群稱這是 AI 的「iPhone 時刻」——讓大眾具體理解 AI 的真正潛力。
