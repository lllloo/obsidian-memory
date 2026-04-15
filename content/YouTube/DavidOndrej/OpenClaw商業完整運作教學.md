---
title: OpenClaw 如何運作我的整個事業（逐步說明）
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-20
source: https://www.youtube.com/watch?v=Cx2oPWU8qjY
---

## 概覽

- 展示如何讓 OpenClaw 在整個公司團隊中運作，提升個人與團隊的生產力。
- 本文包含：VPS 部署、模型選擇、Heartbeat 設定、業務資料夾結構、Slack 整合。

## 部署選擇：VPS vs Mac Mini

- 很多人花數千美元買 Mac Mini 或 Mac Studio，但這不必要。
- **VPS**（如 Hostinger）：費用低、快速部署、可遠端存取、可擴展——是更好的選擇。
- Hostinger 一鍵部署 OpenClaw，不需要 DevOps 知識。

## 模型選擇

- 推薦使用 **Claude Sonnet 4.6**（非 Opus）：
  - 速度比 Opus 快很多，成本更低
  - 在大多數 Benchmark 上與 Opus 差距很小
  - 是 Computer Use Benchmark 上的最強模型（最適合操作瀏覽器）
- 部署後可直接告知 OpenClaw 切換模型並重啟 Gateway。

## 升級搜尋：Perplexity Sonar Pro Search

- 預設搜尋為 Brave API，建議升級至 **Perplexity Sonar Pro Search**（via OpenRouter）。
- 非 Sonar、非 Sonar Pro，而是 **Sonar Pro Search**——這是用於快速 Agentic 搜尋的最強版本。
- 設定步驟：取得 OpenRouter API key → 告知 OpenClaw 切換搜尋工具並重啟 Gateway。
- 驗證：在 OpenRouter 日誌中確認出現 Sonar Pro Search 的 API 呼叫（約 0.01 美元/次）。

## Heartbeat 設定

- 預設每 30 分鐘觸發，讀取 `heartbeat.md` 確認是否有需執行的任務。
- **建議調整**：
  - 頻率改為每 10-15 分鐘
  - 模型改為 **MiniMax M2.5**（via OpenRouter，強力且便宜）或 Gemini Free Flash
- 在 `heartbeat.md` 加入自動更新提示：「若有新版 OpenClaw 且支援 Sonnet 4.6，自動更新並在 Slack 發送更新摘要，然後重啟 Gateway。」
- 設定方式：直接告知 OpenClaw 用網路搜尋學習如何設定 Heartbeat，然後讓它執行。

## 業務資料夾結構（活文件理論）

OpenClaw 工作區的 `business/` 資料夾應包含：

| 資料夾/檔案 | 內容 |
|-----------|------|
| `agent-zero/` | 專案基本資料、策略 |
| `assets/` | 品牌、Logo、圖片 |
| `books/` | 商業書籍、重點摘要 |
| `coding/` | 開發筆記、腳本、SOP |
| `comms/` | 重要溝通記錄 |
| `copywriting/` | 文案框架、CTA、影片腳本清單 |
| `emails/` | 郵件行銷策略、序列 |
| `high-ticket/` | 加速器課程相關資料 |
| `journal/` | 每日問題、思考、商業動態 |
| `metrics/` | CTR、流量、轉換率、流失率等關鍵指標 |
| `paid-ads/` | 廣告 Hook、腳本、再行銷 |
| `playbooks/` | 各流程的 SOP（新人入職、YouTube 縮圖等） |
| `research/` | 所有研究結果（以 Markdown 儲存） |
| `sales/` | 銷售流程、話術 |
| `team/` | 成員資料、角色分工 |
| `business-priorities.md` | 主要任務與問題 |
| `deep-work-options.md` | 8-9 個需要深度專注的重要策略任務 |
| `mistakes.md` | 重要商業錯誤記錄 |
| `names-and-lingos.md` | 術語縮寫（如 NS = New Society） |

## 活文件理論（Living Files）

- **死文件**：存在 Google Drive、ChatGPT 聊天記錄、Perplexity 歷史或本地電腦的內容——AI Agent 無法存取。
- **活文件**：存在 VPS 上的 Markdown 檔案——Agent 可搜尋、引用、修改、建構。
- OpenClaw 內建向量嵌入（vector embeddings），可自動搜尋相關歷史研究。
- 所有研究結果都應指示 OpenClaw 儲存為 `business/research/` 內的 Markdown 檔案。

## 公司組織架構（Agent 結構）

1. **個人層**：每位員工都有自己的 OpenClaw（含個人習慣、偏好、目標）。
2. **公司層**：一個中央 OpenClaw，存放公司文件、財務資料、目標與問題。
3. 個人 OpenClaw → 詢問公司 OpenClaw → 取得上下文 → 完成任務。
4. 新員工可透過對話快速了解公司知識，無需花數週時間入職。
5. 重複性的管理任務（週報、日程準備、指標追蹤）可完全自動化。

## VPS 分散部署的優勢

- Mac Mini 在固定地點，VPS 可在全球任何地方存取。
- 多個 VPS 分散在不同地區，確保即使某個資料中心出問題，業務仍可繼續運作。
- Markdown 格式比 HTML 更節省 token，更適合 AI Agent 讀取。

## 設定 Slack 整合

1. 前往 api.slack.com/apps，建立新 App（從頭開始）。
2. 啟用 **Socket Mode**，產生 App Level Token（記下 `connections` scope）。
3. 前往 **OAuth & Permissions**，新增所需的 Bot Token Scopes：
   - `chat:write`、`channels:read`、`files:read`、`files:write`、`im:read`、`im:write`、`mpim:read`、`app_mentions:read` 等
4. 前往 **Event Subscriptions**，開啟並訂閱事件：`app_mention`、`message.channels`、`message.im` 等。
5. 儲存並重新安裝 App 到工作空間。
6. 取得 Bot Token，告知 OpenClaw 進行設定並重啟 Gateway。
7. 在 Slack 建立私密頻道（如 `#team-openclaw`），邀請 Bot 加入。
8. 在頻道中 tag Bot 測試是否有回應。

## Slack 整合注意事項

- 若 OpenClaw 收不到訊息或無回應，可能原因：
  - OpenClaw 最新版本啟用了 Streaming（兩三天前的更新），可能導致問題
  - 解法：告知 OpenClaw 關閉 Streaming 功能（快速修復）
  - 或：在 Slack App 設定中啟用 `assistant` scope
- 若遭遇連線中斷：Hostinger 安全機制會在長時間連線後斷開，重新貼入 Gateway Token 即可。
- 安全建議：不要嘗試設定過於複雜的 Channel 白名單（容易出錯），確保只把 Bot 加入受信任的頻道即可。

## 結語

- 現在能文字化自己的思考、偏好、判斷，是 2026 年最關鍵的技能。
- 一週花 1-3 小時，持續將商業知識轉化為 Markdown 活文件，回報是永久性的。
- 每一個加入 OpenClaw 的整合、每一個改善都會「永遠複利增長」。
