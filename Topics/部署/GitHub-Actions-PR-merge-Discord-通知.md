---
title: GitHub Actions PR merge Discord 通知
created: 2026-06-02
updated: 2026-06-05
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

## 安全：untrusted input 不可內插進 run

PR 標題等欄位是攻擊者可控輸入，**絕不能**用 `${{ github.event.pull_request.title }}` 直接內插進 `run:` script——`${{ }}` 在 shell 執行前先做字串替換，標題塞 `$(...)` 或反引號會被 bash 當指令執行（script injection）。

正解：untrusted 欄位移到 `env:` 當資料傳入，script 只引用 `$VAR`（bash 視為純字串、不再解譯），JSON 交給 `jq` 組（也順帶處理標題含 `"`／換行破壞 JSON 的問題）。並設 `permissions: {}` 走最小權限。

> 另一條路：只要 CI build/deploy 成敗通知、不想手刻 JSON，可用現成 action，見 [[bookmark-actions-status-discord-CI狀態通知Action|sarisia/actions-status-discord]]。

