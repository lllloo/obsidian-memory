---
title: Discord Webhook
created: 2026-04-07
updated: 2026-05-08
source: https://discord.com/developers/docs/resources/webhook
tags:
  - api
  - discord
  - workflow
---

Discord 頻道專屬的單向 POST URL，不需要 Bot token，適合 CI/CD 通知、監控警報、表單通知等場景。觸發情境：寫 GitHub Actions / 監控腳本要通知到 Discord 時。Webhook URL 等同機密，CI 用 GitHub Actions secret 注入、本機用 `.env` 並 `.gitignore`；外洩時去 Discord 頻道設定刪掉重生（rotation 比 git history rewrite 快）。Embed color 須給十進位（hex 要先轉換）。

## 連結

- 官方 docs：<https://discord.com/developers/docs/resources/webhook>
