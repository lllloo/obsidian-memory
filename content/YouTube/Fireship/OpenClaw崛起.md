---
title: OpenClaw 的崛起：全天候自主 AI 助理
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-30
source: https://www.youtube.com/watch?v=ssYt09bCgUY
---

## 是什麼

- 原名 Claudebot → 因 Anthropic 威脅商標侵權改為 Maltbot → 再改為 **OpenClaw**
- 由 Peter Steinberger（PSDFKit / Nutrient 創辦人）開發，以 TypeScript 撰寫
- 包裝 Claude 與 GPT 模型，24/7 自主運作，可自架在 VPS、Raspberry Pi 或 Mac Mini

## 核心能力

- 管理行事曆、整理 email、執行腳本
- 追蹤股票，價格大幅波動時主動通知
- 部署程式碼（帶著滿滿自信地部署有 bug 的版本）
- 透過 **Telegram、Slack、WhatsApp、Discord** 等傳訊 app 互動
- **MoltHub**：第三方 skill 市集

## 安裝與設定

```bash
# 安裝
curl -sSL https://openclaw.ai/install.sh | bash

# 啟動後執行 onboarding：
# 1. 設定 AI 模型 API key（支援 Anthropic、開源模型等）
# 2. 設定 Telegram Bot（透過 BotFather 取得 access token）
# 3. 設定 skills（內建 + MoltHub）
# 4. 設定 hooks（生命週期事件，如記憶持久化、後續自動化）
```

## 使用 Telegram 配對

1. 啟動後出現 gateway dashboard
2. 在 Telegram 傳訊給剛建立的 bot
3. 收到 `access not configured` 訊息，回傳 pairing code
4. 在終端執行配對指令
5. 完成後可直接透過 Telegram 與 AI 對話並建立自動化

## 為何爆紅

- 65,000+ GitHub stars（創歷史紀錄速度）
- Mac Mini 因此銷售一空
- 免費自架，不需付 $29/月 給其他 AI 助理服務
