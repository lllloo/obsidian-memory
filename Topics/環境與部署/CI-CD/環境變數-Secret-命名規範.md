---
title: 環境變數 / Secret 命名規範
created: 2026-06-02
updated: 2026-06-02
tags:
  - github-actions
  - workflow
  - api
---

CI secret、環境變數、`.env` 鍵名的命名慣例。實際取捨脈絡見 [[GitHub-Actions-Secrets-與-Variables]]。

## 規則與慣例

- **UPPER_SNAKE_CASE**：作為環境變數注入的慣例寫法。
- 只能字母／數字／底線，不可數字開頭。
- GitHub Actions 另禁 `GITHUB_` 前綴（保留）。

## 結構：`<服務>_<資源>_<型別>`

- **服務前綴** 標歸屬：`DISCORD_`、`AWS_`、`SLACK_`。
- **型別後綴** 標「是什麼」：`_URL`、`_TOKEN`、`_KEY`、`_ID`。

## `DISCORD_WEBHOOK` vs `DISCORD_WEBHOOK_URL`

選後者。補 `_URL` 才明確是整條網址（而非 webhook id 或 token），也與 `SLACK_WEBHOOK_URL`、`OPENAI_API_KEY` 等命名一致。
