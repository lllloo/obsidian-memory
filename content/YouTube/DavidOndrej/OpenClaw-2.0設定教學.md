---
title: OpenClaw 2.0 設定教學
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-11
source: https://www.youtube.com/watch?v=6vPaitNQMGY
---

## 概覽

- 展示一個 OpenClaw 透過 Telegram 語音訊息，同時管理四個 Claude Code Agent 建構軟體的場景。
- 本文從零開始在全新 VPS 上搭建 OpenClaw，讓它成為能 24/7 運作的 AI 開發團隊指揮官。

## 為什麼選 VPS 而非 Mac Mini

- **更快速**：幾分鐘內就能啟動新的 Linux 實例，不需購買硬體。
- **可擴展**：想增加 Agent 或用途，幾個按鍵即可。
- **遠端存取**：在世界任何地方都可 SSH 進入——Mac Mini 只能在家使用。
- 不需要是 DevOps 或開發者，Hostinger 提供一鍵部署 OpenClaw。

## VPS 部署步驟

1. 前往 Hostinger，選擇 OpenClaw 方案（推薦 24 個月）。
2. 輸入折扣碼，填寫帳單資訊完成付款。
3. 選擇最近的伺服器地點，選擇 Ubuntu Linux。
4. 點擊「Generate」產生安全的 root 密碼（勿分享）。
5. 等待 VPS 啟動（約 1-2 分鐘）。

## 安裝 OpenClaw

1. 前往 openclaw.ai，複製官方 oneliner 安裝指令。
2. 在 Hostinger 面板點擊右上角的 Terminal 按鈕（不需要手動 SSH）。
3. 輸入 `clear` 清空畫面，貼上 oneliner 並執行。
4. 安裝程式自動偵測 Linux 環境、安裝 Node.js 等相依套件。
5. 回答引導問題：
   - 安全模式確認：輸入 `yes`
   - 選擇模型提供商：推薦 **OpenRouter**（可存取所有主流模型）
   - 貼入 OpenRouter API key
   - 選擇模型：Opus 4.6（目前最強）
   - 選擇頻道：**Telegram**

## 設定 Telegram Bot

1. 在 Telegram 搜尋 **BotFather**（需有藍色勾勾 + 740 萬月活用戶）。
2. 輸入 `/newbot` 建立新 Bot，設定名稱與 username（需以 `_bot` 結尾）。
3. 複製 Bot Token，貼回 Hostinger Terminal。
4. 搜尋 Provider 步驟選擇 Brave Search（預設，不需額外 API key）。
5. 完成安裝後，在 Telegram 開啟 Bot 輸入 `/start`，測試 OpenClaw 是否有回應。

## 透過 Telegram 設定 OpenClaw

- OpenClaw 安裝完成後，所有設定都可透過 Telegram 自然語言進行（不需再進 Terminal）。
- 確認模型版本：`/status` — 確認為 OpenRouter + Anthropic Claude Opus 4.6。
- 提升思考深度：`/think high`。
- 初始化身份：第一次執行會根據 `bootstrap.md` 問你關於 Agent 角色的問題，設定為「開發者 Orchestrator，負責管理 Claude Code 子 Agent」。

## 安裝 Claude Code

1. 搜尋 Claude Code 官方網站，取得 oneliner 安裝指令。
2. 在 Hostinger Terminal 輸入 `clear`，貼上指令執行。
3. 安裝完成後執行 `export PATH` 指令讓系統找到 `claude` 執行檔。
4. 前往 Anthropic Console 取得 API key（與 Claude.ai 帳號相同）。
5. 執行 `export ANTHROPIC_API_KEY=<你的key>` 設定環境變數。
6. 輸入 `claude --version` 驗證安裝成功。

## 安裝 Claude Code Skill

- OpenClaw 預設不知道如何使用 Claude Code，需安裝 Skill（一組 Markdown 指令）。
- 透過 Telegram 告知 OpenClaw：「Find the official OpenClaw skill file for the coding agent skill on their GitHub and show me the full contents.」
- 確認後回覆「yes, install this as a local skill」。
- **警告**：
  - 避免使用 ClauwHub / ClaudeHub 等第三方 Skill 平台。
  - 研究人員發現 341 個惡意 Skill，15% 以上的社群 Skill 含惡意指令或 Trojan。
  - 惡意 Skill 會偽裝成官方版本，但內嵌 JavaScript 將 API key 與 Prompt 傳送至外部伺服器。
  - 官方 Skill 來源：`github.com/openclaw/skills`。

## 更新 OpenClaw Config（允許執行 Claude Code）

- 預設 OpenClaw 在沙箱模式執行，無法找到 Claude Code binary 也無法傳送 API 請求。
- 需更新 config JSON 新增：
  - Anthropic API key（讓 OpenClaw 可呼叫 Claude Code）
  - 允許執行外部 binary 的權限設定
- 直接告知 OpenClaw：「Find your main openclaw.json config file and update it by adding these settings:」（貼上 JSON 內容）。
- OpenClaw 自動合併設定並重啟 Gateway。

## ISS 軌道追蹤器實測

- **一句 Prompt**：「Build me a 3D ISS orbital tracker using Three.js. Render a detailed 3D Earth with a realistic texture map and show the ISS orbiting in real time. Use Claude Code to build this. Serve it on port 3000.」
- OpenClaw 的處理過程：
  1. 派發 Claude Code 子 Agent 接手建構任務。
  2. 遭遇 root 權限限制（Anthropic 刻意禁止 root 層執行 `--dangerously-skip-permissions`）。
  3. **Agent 自行解決**：建立 non-root 用戶，在該用戶下重新啟動 Claude Code。
  4. 最終在 VPS 的 port 3000 成功啟動 3D ISS 追蹤器。
- 成果：可互動的 3D 地球儀，即時顯示 ISS 位置、速度、高度、經緯度。

## 核心優勢：非阻塞的 Orchestrator 架構

- **傳統問題**：讓主 Agent 執行任務時，無法同時與它對話。
- **OpenClaw 解法**：主 OpenClaw 是 Orchestrator，派發任務給 Claude Code 子 Agent，本身不被阻塞。
- 在 Claude Code 建構軟體的同時，仍可透過 Telegram 和 OpenClaw 對話、交派其他任務。

## 安全注意事項

- API key 當作密碼處理，不要隨意分享。
- 使用 Skill 前必須：閱讀原始內容、用其他 AI 分析確認無惡意 → 才安裝。
- VPS 環境隔離保護本機安全——Claude Code 在遠端伺服器運作，不會影響你的電腦。
