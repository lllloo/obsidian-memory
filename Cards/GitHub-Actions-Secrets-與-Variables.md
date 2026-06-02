---
title: GitHub Actions Secrets 與 Variables
created: 2026-06-02
updated: 2026-06-02
source: https://docs.github.com/actions/security-guides/encrypted-secrets
tags:
  - github-actions
  - workflow
  - deploy
  - api
---

repo → **Settings → Secrets and variables → Actions**。兩條軸交叉成四格：**敏感與否**（Secrets / Variables）×**作用範圍**（Repository / Environment）。案例見 [[GitHub-Actions-PR-merge-Discord-通知]]；鍵名怎麼取見 [[環境變數-Secret-命名規範]]。

## Secrets vs Variables

| | Secrets | Variables |
|---|---|---|
| 儲存 | 加密、log 遮蔽、建立後讀不回 | 明文、可見 |
| 用途 | token、webhook URL、密碼 | region、image tag、flag |
| 取用 | `${{ secrets.NAME }}` | `${{ vars.NAME }}` |

判準：**有資安風險放 Secret，純設定放 Variable**。Webhook URL 雖只是網址，誰拿到都能發訊，算機密。

## Repository vs Environment

- **Repository**：全 repo workflow 直接可用。適合通用、無需審核的值。
- **Environment**：綁定 environment（如 `production`），job 須宣告 `environment:` 才讀得到；可掛保護規則（required reviewers、wait timer、branch 限制），同名變數還能分環境給不同值。

四象限即兩軸相乘：Repository / Environment × secrets / variables。

## Fork PR 限制

Secrets 與 variables **不傳給 fork 發出的 PR 所觸發的 workflow**——防惡意 PR 在 workflow 裡 echo 出 secret 竊取。跑在 base repo context 的事件（merge 後的 `closed`、`push`）不受限。凡有 collaborator 權限者皆可使用這些值，故「誰能進 repo」就是信任邊界。
