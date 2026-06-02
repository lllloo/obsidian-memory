---
title: GitHub Actions PR merge Discord 通知
created: 2026-06-02
updated: 2026-06-02
tags:
  - github-actions
  - deploy
  - discord
  - workflow
  - api
---

obsidian-memory repo 在 `.github/workflows/discord-notify.yml` 設定 PR merge 後送 Discord Embed 通知。Webhook 原理見 [[bookmark-Discord-Webhook-CI通知用]]；Secret 放哪層、怎麼命名見 [[GitHub-Actions-Secrets-與-Variables]]。

## 觸發條件

```yaml
on:
  pull_request:
    types: [closed]

jobs:
  notify:
    if: github.event.pull_request.merged == true
```

`closed` 同時涵蓋「關閉未 merge」與「merge」，靠 `merged == true` 只留後者。

## 重點

- Webhook URL 存成 **Repository secret** `DISCORD_WEBHOOK_URL`，以 `${{ secrets.DISCORD_WEBHOOK_URL }}` 取用；不需 Bot token，無需開 Environment。
- Embed `color` 吃**十進位**：`` `#57F287` `` 要先轉成 `5763719`。
- URL 外洩時去 Discord 頻道設定刪掉重建，比 git history rewrite 快。
