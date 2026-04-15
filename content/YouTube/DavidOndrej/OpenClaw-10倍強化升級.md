---
title: OpenClaw 10 倍強化升級教學
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-09
source: https://www.youtube.com/watch?v=cod50CWlZeU
---

## 概覽：為什麼要強化 OpenClaw

- OpenClaw（又稱 Clawbot）是目前最受歡迎的 AI Agent，可存取電腦完整資源，能寄信、管理行事曆、預訂餐廳、開發軟體，甚至經營事業。
- 大多數人的 OpenClaw 設定非常基礎——本文展示如何打造最強大的設定。
- 核心理念：**將整台電腦（Mac Mini 或 VPS）交給 AI Agent**，讓它能執行機器上的任何操作。

## VPS vs Mac Mini

- Mac Mini：至少 $600 購買成本，運算能力強但本地限制多。
- **VPS**：更便宜、可遠端管理，本文採用此方案。
- 推薦：Hostinger 的 OpenClaw 一鍵部署，不需要 DevOps 知識。

## 部署 OpenClaw 到 VPS

1. 前往 Hostinger 選擇 OpenClaw 方案（24 個月方案省最多，輸入折扣碼可再折 10%）。
2. 選擇伺服器地點（如歐洲 Lithuania）。
3. 貼入所需 API key（如 Anthropic），Hostinger 自動完成部署（約 1 分鐘）。
4. 複製並妥善保存 **OpenClaw Gateway Token**（登入入口需要）。
5. 點擊連結進入 OpenClaw 登入頁，貼入 Gateway Token 即可。

## 設定主要模型

- 預設為 Claude Sonnet，建議升級至 Opus 4.6（更強但較貴）。
- 直接在聊天框輸入：「Browse the web to find the official Anthropic API name for Opus 4.6 and then update your model config to make this the primary model.」
- OpenClaw 可**自行升級自己**——不需要進入終端機或手動修改設定。
- 升級後自動重啟 Gateway，確認模型名稱正確（Anthropic 用 `-`，OpenRouter 用 `.`，兩者不同）。

## Gateway 儀表板功能

| 功能 | 說明 |
|------|------|
| 頻道（Channels） | WhatsApp、Telegram 等連接狀態 |
| 執行個體（Instances） | OpenClaw 執行個體 |
| Sessions | 目前活躍工作階段 |
| Cron Jobs | 定時排程任務（類似 n8n） |
| Agents | 主 Agent 與子 Agent 管理 |
| Skills | 告訴 Agent 如何使用特定工具的指令集 |

## 必知指令

- `/compact` — 壓縮 context window 節省 token（從 30,000 降至 12,000）
- `/status` — 查看版本、模型、token 消耗等狀態
- `/help` — 列出所有可用指令
- `/new` — 開啟新對話
- `/think` — 調整思考深度
- `/model sonet` / `/model opus` — 快速切換模型

## 升級搜尋工具：從 Brave Search 到 Perplexity Pro

- 預設搜尋：Brave Search API（不支援 Agentic 搜尋）。
- 升級目標：Perplexity Sonar Pro Search（一般搜尋）+ Sonar Deep Research（深度研究）。
- 步驟：
  1. 在 OpenRouter 取得 Perplexity Sonar Pro 模型名稱與 API key。
  2. 直接告知 OpenClaw：「Change the default web search to use this endpoint. Update tools.md and memory.md to document this.」
  3. OpenClaw 自行修改設定並重啟 Gateway。
  4. 設定規則：一般查詢用 Sonar Pro，只有明確說「deep research」才用深度研究端點。

## 九大核心 Markdown 檔案

OpenClaw 工作區內建九個重要設定檔，每次對話都會載入：

| 檔案 | 用途 |
|------|------|
| `agents.md` | 通用系統規則、工作流程、安全邊界、溝通規則 |
| `soul.md` | Agent 個性、語氣、價值觀、行為預設 |
| `user.md` | 使用者個人資訊、偏好、工作情境 |
| `memory.md` | 長期記憶、API ID、重要事實、錯誤教訓 |
| `tools.md` | 各 API 工具的使用文件、限制、最佳實踐 |
| `identity.md` | Agent 名稱、角色定位、職責範圍 |
| `heartbeat.md` | 定時主動檢查的指令（如查看行事曆、信箱） |
| `boot.md` | 啟動時執行的初始化指令 |
| `bootstrap` | 系統初始化設定 |

## 建立個人資料夾結構

- 建議建立 `personal/` 和 `business/` 兩個資料夾。
- 在這兩個資料夾內持續新增 Markdown 檔案：
  - `goals.md` — 個人目標與商業目標
  - `playbooks.md` — 標準作業流程（SOP）
  - 任何可以文字化的偏好、習慣、判斷原則

## 「活文件」理論

- **死文件**：存在 Google Drive、Obsidian 或本地電腦的文件——除非你人看著它，否則完全沒有作用。
- **活文件**：存在 VPS、可被 AI Agent 存取、修改、引用、共享的 Markdown 檔案。
- 每一小時投入改善 OpenClaw，回報是永久性的（VPS 上的知識不會消失在聊天記錄中）。

## Heartbeat 設定

- 預設每 30 分鐘觸發，讀取 `heartbeat.md` 確認是否有需要執行的任務。
- 建議調整：
  - 頻率改為每 15 分鐘。
  - Heartbeat 使用的模型改為 `Haiku 4.5` 或 `Gemini 3.0 Flash`（比 Opus 快 10 倍、便宜很多）。
- 直接用自然語言告知 OpenClaw 執行以上兩項修改即可。

## Cron Jobs（定時任務）

- 用自然語言設定定時自動化任務，OpenClaw 負責完成語法轉換。
- 實用範例：
  - 每晚 11 點提醒就寢
  - 每 24 小時追蹤產業最新趨勢
  - 每早整理當日行程與會議簡報
  - 每 7 天自動檢查是否有更好的 AI 模型並更新設定

## 利用 ChatGPT 訂閱免費使用 OpenClaw

- 若有 ChatGPT Plus（$20/月）或 Pro（$200/月）訂閱：
  1. 執行 `openclaw onboard --oauth openai`，取得授權 URL。
  2. 用瀏覽器開啟並登入 ChatGPT 帳號。
  3. 將 URL 貼回終端機完成驗證。
  4. 預設模型為 GPT-5.3 Codex，可像其他模型一樣設定快捷別名（如 `/model codex`）。

## 安全最佳實踐

- 不要將 API key 隨意分享給聊天機器人（本文示範僅為教學速度）。
- 不要把 OpenClaw 連到 Mold Book 等公開平台（容易 Prompt Injection）。
- 每週花 30-60 分鐘定期檢查 VPS 安全性。
- 可讓 OpenClaw 自己執行安全稽核（告知它執行即可）。
- Hostinger 的預設部署已做了部分安全加固。

## 組織架構：Agent 公司結構

1. 每位員工部署自己的個人 OpenClaw（含個人生活、工作習慣）。
2. 建立一個**公司共用 OpenClaw**，存放公司文件、財務資料、目標與問題。
3. 個人 OpenClaw 可向公司 OpenClaw 請求上下文、完成任務後回寫更新。
4. 各個 OpenClaw 之間可互相溝通，形成「Agent 蜂群」架構。

## 結語

- 現在能言語化自己的偏好、目標、判斷原則，將成為 2026 年最關鍵的技能之一。
- 初學者（只用免費 ChatGPT）與進階用戶（多個 OpenClaw + 活文件 + 最新模型）之間的差距，比以往任何時候都更大。
