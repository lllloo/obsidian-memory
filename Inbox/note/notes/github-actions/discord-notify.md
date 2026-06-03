---
title: GitHub Actions 寄送 Discord 通知
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/notes/github-actions/discord-notify
tags:
  - github-actions
  - discord
  - workflow
  - deploy
---

# GitHub Actions 寄送 Discord 通知

透過 [`sarisia/actions-status-discord`](https://github.com/sarisia/actions-status-discord) action，可以在 GitHub Actions 工作流程完成後，自動發送通知訊息至 Discord 頻道。

## 設定 Discord Webhook

1. 在 Discord 頻道設定中，選擇「整合」→「Webhook」→「建立 Webhook」
2. 複製 Webhook URL
3. 前往 GitHub 儲存庫的「Settings」→「Secrets and variables」→「Actions」
4. 新增 Secret，名稱設為 `DISCORD_WEBHOOK`，值貼上剛才複製的 Webhook URL

## 基本用法

最簡單的方式是搭配 `if: always()` 與 `status: ${{ job.status }}`，讓 action 自動依結果設定顏色與狀態文字：

```yaml
steps:
  - name: Build
    run: npm run build

  - name: Discord 通知
    if: always()
    uses: sarisia/actions-status-discord@v1
    with:
      webhook: ${{ secrets.DISCORD_WEBHOOK }}
      status: ${{ job.status }}
```

> `if: always()` 確保無論成功、失敗或取消都會執行通知 step。

### 自訂通知訊息

透過 expressions 可以根據結果顯示不同的標題與說明：

```yaml
  - name: Discord 通知
    if: always()
    uses: sarisia/actions-status-discord@v1
    with:
      webhook: ${{ secrets.DISCORD_WEBHOOK }}
      status: ${{ job.status }}
      title: ${{ job.status == 'success' && '✅ 部署成功' || '❌ 部署失敗' }}
      description: ${{ job.status == 'success' && '服務已成功部署' || '服務部署失敗' }}
```

### 常用參數

| 參數 | 說明 | 預設值 |
| --- | --- | --- |
| `webhook` | Discord Webhook URL（必填） | — |
| `status` | 顯示狀態，自動設定顏色（Success / Failure 等） | 自動偵測 |
| `title` | 通知標題 | job 名稱 |
| `description` | 通知內容說明 | — |
| `color` | 訊息左側色條顏色（十六進位色碼） | 依 status 自動設定 |
| `url` | 標題連結 URL | 當前 workflow run URL |
| `username` | Discord Bot 名稱 | GitHub Actions |
| `avatar_url` | Discord Bot 頭像 URL | — |
| `nodetail` | 隱藏詳細資訊（`true`/`false`） | `false` |

## 完整範例：多 Job 部署流程

當 workflow 有多個 job 時，可以只在最後發送一個通知。透過在 deploy job 加上 `if: always()` 搭配 `needs.build.result` 判斷，即使 build 失敗也能收到通知：

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

  deploy:
    needs: build
    if: always()
    runs-on: ubuntu-latest
    steps:
      # 以下為示意，請替換為實際部署步驟
      - name: Deploy
        if: needs.build.result == 'success'
        run: echo "部署中..."

      - name: Discord 打包失敗通知
        if: always() && needs.build.result != 'success'
        uses: sarisia/actions-status-discord@v1
        with:
          webhook: ${{ secrets.DISCORD_WEBHOOK }}
          status: failure
          title: '❌ 打包失敗'
          description: '專案打包失敗'

      - name: Discord 部署通知
        if: always() && needs.build.result == 'success'
        uses: sarisia/actions-status-discord@v1
        with:
          webhook: ${{ secrets.DISCORD_WEBHOOK }}
          status: ${{ job.status }}
          title: ${{ job.status == 'success' && '✅ 部署成功' || '❌ 部署失敗' }}
          description: ${{ job.status == 'success' && '服務已成功部署' || '服務部署失敗' }}
```

重點說明：

- **deploy job 的 `if: always()`**：讓 build 失敗時 deploy job 仍會啟動，通知 step 才有機會執行
- **Deploy step 的 `if: needs.build.result == 'success'`**：build 失敗時跳過實際部署
- **兩個通知 step 的 `if` 條件互斥**：每次只會觸發其中一個，確保只收到一則通知
