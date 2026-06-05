---
title: actions-status-discord
created: 2026-06-05
updated: 2026-06-05
source: https://github.com/sarisia/actions-status-discord
tags:
  - github-actions
  - discord
  - deploy
  - workflow
---

`sarisia/actions-status-discord` 是 GitHub Action，在 workflow job 結束後發 Discord 通知。搭 `if: always()` + `status: ${{ job.status }}` 會自動依結果上色、設狀態文字，省去手刻 webhook 的 Embed JSON。觸發情境：CI build/deploy 要把成敗狀態通知到 Discord、又不想自組 payload 時。多 job 部署可在最後一個 job 設 `if: always()` 配 `needs.<job>.result` 互斥條件，確保只發一則。

## 連結

- Repo：<https://github.com/sarisia/actions-status-discord>

## 相關

- [[GitHub-Actions-PR-merge-Discord-通知]] — 手刻 webhook + jq 的另一條路徑（可控 Embed、就地擋 injection）
- [[bookmark-Discord-Webhook-CI通知用|Discord Webhook]] — Webhook 原理
