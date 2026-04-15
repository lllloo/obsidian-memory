---
title: Kimi K2 模型評測：Claude 殺手？
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-07-14
source: https://www.youtube.com/watch?v=Y4VEAI04W_U
---

## Kimi K2 簡介

- 中國 AI 公司 Moonshot 推出的開源模型
- 定位：編程能力介於 Claude 3.5 和 Claude 4 之間
- 最大優勢：**價格比 Claude 4 低 80%**

### 價格對比

| 模型 | 輸入（每 1M tokens） | 輸出（每 1M tokens） |
|------|---------------------|---------------------|
| Claude 4 | $3 | $15 |
| GPT-4.1 | 相近 | 相近 |
| Kimi K2 | $0.60 | $2.50 |

## 整合 Kimi K2 到 Claude Code

```bash
export ANTHROPIC_AUTH_TOKEN="moonshot-api-key"
export ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"
```

- 在 platform.moonshot.ai 取得 API key
- 充值 $10 可測試大量功能

## 實測結果

### UI 元件測試

- 一個 session 完成：file explorer、rich text editor、resizable panels、app view
- 整合為線上 IDE UI
- 錯誤出現時貼入即可修復

### 遊戲開發測試

- 從零建立 Mario 風格遊戲（使用網路上的資源）
- 第二次嘗試後產出完整可玩遊戲

### 成本比較

- 建立 IDE UI 元件 + Mario 遊戲：總花費約 $0.50
- 估計用 Claude 4 同等任務：約 $2

## 適用場景

- AI 編程 agent 的底層模型（大幅降低 API 成本）
- 一般 UI 開發任務
- 需要多 agent 並行時的低成本選擇

## 限制

- API 速度比 Anthropic 稍慢
- 不適合需要最高品質輸出的複雜推理任務
