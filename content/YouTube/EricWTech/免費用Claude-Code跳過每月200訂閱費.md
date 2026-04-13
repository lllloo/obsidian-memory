---
title: "免費用 Claude Code，跳過每月 $200 訂閱費"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-28
source: https://youtu.be/o85Y5omRQq0
---

## 影片描述

示範如何完全免費使用 Claude Code，不需要 Claude Max 或 Pro 訂閱方案，也不需要在本機安裝任何本地模型。同時比較各種替代模型的性能與成本效益。

## 重點摘要

### 核心方法：透過 OpenRouter 連接 Claude Code

- 前往 [openrouter.ai](https://openrouter.ai) 建立免費帳號並取得 API 金鑰
- 在專案根目錄建立 `.claude/settings.local.json` 設定檔
- 設定環境變數：
  - `ANTHROPIC_BASE_URL` 指向 OpenRouter API
  - `ANTHROPIC_AUTH_TOKEN` 填入 OpenRouter API 金鑰
  - 指定要使用的模型名稱（例如 `openrouter/auto`）

### 免費模型選項

- OpenRouter 提供「Free Models Router」，會隨機路由到可用的免費模型
- 免費模型回應較慢（約 31 秒），準確度有限，適合學習或 demo 用途
- 不建議用於正式開發工作

### 推薦的中價位模型

- 在 OpenRouter 的 **AI Model Rankings** 頁面可依程式語言篩選熱門模型
- **MiniMax M2.5** 是 Programming 排行榜上的高人氣選擇，每百萬 token 成本不到 $2 美元
- 相較之下，Claude Sonnet 4.6 約 $18/百萬 token，Opus 4.6 約 $30/百萬 token
- 整個示範 session 的完整成本僅約 $0.20

### 設定層級

- **專案層級**：設定只在特定資料夾生效，不影響其他專案
- **全域層級**：設定在根目錄，對所有專案有效

### 實際測試

- 使用 MiniMax M2.5 透過 OpenRouter 成功觸發 Claude Code 的子代理（sub-agents）功能
- 示範以 4 個平行代理並行審查 QA 文件，找出未覆蓋的邊緣案例
