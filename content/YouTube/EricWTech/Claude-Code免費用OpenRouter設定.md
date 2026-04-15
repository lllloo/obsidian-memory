---
title: 免費使用 Claude Code：透過 OpenRouter 跳過訂閱費用
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-28
source: https://www.youtube.com/watch?v=o85Y5omRQq0
---

## 核心概念

透過 OpenRouter 將 Claude Code 連接到第三方模型（含免費模型），不需要 Claude Pro/Max 訂閱。

## 設定步驟

### 1. 建立 OpenRouter API Key

前往 openrouter.ai → API Keys → Create，建立免費 API key。

### 2. 建立設定檔

在專案根目錄建立 `.claude/settings.local.json`（只影響此專案，不影響其他目錄）：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://openrouter.ai/api/v1",
    "ANTHROPIC_AUTH_TOKEN": "你的 OpenRouter API key",
    "ANTHROPIC_MODEL": "openrouter/auto"
  }
}
```

### 3. 選擇模型

**免費模型（學習/Demo 用）：**
- 模型 ID：`openrouter/auto`（自動路由到可用免費模型）
- 缺點：回應較慢（約 31 秒），準確度低於頂級模型

**全域設定（所有專案）：**
改在 root directory 的 settings.local.json 設定（而非專案層級）。

## 模型選擇策略

OpenRouter 提供 AI Model Rankings，可按程式語言篩選：

| 模型 | 用途 | 費用（每 1M tokens） |
|------|------|-------------------|
| openrouter/auto | 免費，學習用 | $0 |
| MiniMax M2.5 | 程式設計高人氣，高 CP 值 | ~$2 |
| Claude Sonnet 4.6 | 程式設計 Top 5 | ~$18 |
| Claude Opus 4.6 | 程式設計 Top 4 | ~$30 |

**推薦**：MiniMax M2.5（OpenRouter 程式設計排行榜高名次，費用約 Sonnet 的 1/9）

## 實際測試結果

使用 MiniMax M2.5 運行 sub-agent 平行審查任務（QA 文件 edge case 分析）：
- 啟動 4 個平行 sub-agent（end-to-end、security、data、performance）
- 完整 session 總費用：**約 20 美分**

## 注意事項

- 免費模型適合學習和 Demo，不適合生產環境
- 若只用 Sonnet/Opus，直接買 Claude Pro 反而更划算
- 可在 VS Code status bar 查看當前使用模型與 context window 消耗量
