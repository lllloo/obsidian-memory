---
title: 安裝 OpenClaw 前必須了解的安全風險
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-04
source: https://www.youtube.com/watch?v=M3P0hQMQtq0
---

## 重點摘要

- OpenClaw 原名 ClawdBot，後改名 MoltBot，最終定名 OpenClaw，現為成長最快的開源 AI 專案
- 安裝過程踩到的坑：WhatsApp 408 錯誤、channel 整合不穩定
- 實際使用場景：自動 email 摘要、cron job 自動化；但 token 成本容易快速失控，即使用小模型也是
- 安全警告：Cisco 已將部分社群製作的 skills 標記為「功能性惡意軟體」，且 prompt injection 被官方列為範圍外問題
- 建議用 Docker sandbox 隔離執行環境，並對 OpenAI、Gemini 等 provider 設定 API 預算上限
- 影片同時涵蓋如何安全評估自架 AI agent 的安全取捨
