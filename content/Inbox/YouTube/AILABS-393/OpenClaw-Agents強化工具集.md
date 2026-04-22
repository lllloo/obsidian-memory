---
title: OpenClaw Agents 強化工具集
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-07
source: https://www.youtube.com/watch?v=JC53AcoFh-Q
parent: "[[01.index]]"
---

## 安全問題與 Clawsk 工具

OpenClaw 是目前成長最快的開源專案之一，但 Cisco 已公開指出其安全漏洞，且隨著第三方整合增加，成本也快速攀升。Clawsk 是由 Sentinel 1 旗下 Prompt Security 開發的完整安全工具包，針對 OpenClaw 和 NanoClaw agents：

- 包含多個 skills：soul guardian、openclaw watchdog 等，各針對不同安全面向
- 首次安裝遇到 registry rate limit，需改用 git clone 安裝
- 執行 `claw secuite heartbeat` 產生完整安全報告，涵蓋 CVE 等級漏洞與修復建議
- 內建 hash 完整性驗證 + 自動從可信 release 重新下載的自修復機制
- 持續執行 CI/CD pipeline 進行安全檢查

## AntFarm 多 Agent 工作流系統

AntFarm 是在 OpenClaw 內協同運作的多 agent 系統（1.9K stars），由 Ryan Carson 開發：

- 安裝後啟動本地 dashboard，顯示 kanban board 呈現工作流進度
- 特色：確定性工作流（deterministic workflow）按固定步驟執行，行為可預測
- 每個 agent 獨立 context window，避免 context bloat
- 內建驗證 agent 負責審核每個 agent 產出，失敗自動重試
- Workflows 以 YAML 撰寫，比大型 Markdown 更節省 token

## LanceDB Pro 記憶外掛

提升 OpenClaw 內建記憶的混合向量搜尋外掛：

- 安裝路徑：OpenClaw folder → workspace → plugins folder
- 核心功能：reranking（重新排序最相關記憶而非最新記憶）、跨對話 session memory
- 使用 GINA embedding model（可免費取得 API key，上限 10,000 tokens）
- 安裝後需執行 `openclaw gateway restart` 完成註冊

## Unbrowse Agent 原生瀏覽器

以 API 反向工程而非截圖像素操作的 agent 原生瀏覽器：

- 直接讀取瀏覽器 cookies，支援跨 session 操作（不同於 Playwright）
- 所有擷取執行程式碼保留本地，不外傳
- 安裝後需手動將 skill 複製到 OpenClaw skills 資料夾才能被識別
- 首次使用由 OpenClaw 自動完成環境設定，之後獨立運作

## Molt Worker（Cloudflare 雲端部署）

Cloudflare 官方 repository，用於在 Cloudflare Workers 無伺服器平台執行 OpenClaw：

- 目前為實驗性質，存在部分安全問題（secrets 在 process arguments 中可見）
- 支援 Telegram、Discord、Web UI 等頻道
- 架構結合 sandbox containers、R2 buckets
- 可透過 Cloudflare AI Gateway 隨時切換 model provider，無需重新部署
- 預裝 Cloudflare Browser Use skill 支援瀏覽器自動化

## OpenClaw Dashboard

視覺化監控所有 agents 指標的控制中心：

- 顯示：active sessions 數量、累計費用、費用趨勢、agents 趨勢、所有 cron jobs
- 可直接針對 dashboard 資料提問，底層使用 OpenClaw 作為回答 agent

## Awesome OpenClaw Skills 精選清單

因 ClawHub 上 15,000+ community skills 中混有惡意程式（Cisco 標記為 malware），有人建立了篩選後的精選清單：

- 從 15,000 篩選至 5,400 個可信 skills
- 過濾詐騙、重複、惡意 skills
- 依類別分類：Git/GitHub、coding、automation 等
