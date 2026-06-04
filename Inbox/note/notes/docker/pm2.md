---
title: Docker 與 PM2：用或不用的取捨
created: 2026-06-03
updated: 2026-06-04
tags:
  - docker
  - pm2
  - deploy
---

# Docker 與 PM2：用或不用的取捨

在容器化環境中，PM2 的多數功能可由 Docker 原生機制取代，直接在容器內跑 `pm2 start` 是常見的反模式。但 PM2 官方也提供了容器專用的 `pm2-runtime`，有其適用場景。本文整理兩種做法，並比較差異幫助選擇。

## 為什麼不該在 Docker 直接用 PM2

直接在容器內使用 `pm2 start` 會造成以下問題：

- **容器立即退出**：PM2 daemon 模式會 fork 到背景，容器主程序結束後容器隨即停止
- **信號無法傳遞**：PM2 作為 PID 1 運行，`docker stop` 發出的 SIGTERM 由 PM2 接收，不一定正確轉發給 Node.js，導致 graceful shutdown 失效
- **職責重疊**：容器本身就是隔離單元，Docker / Kubernetes 已負責程序監控與重啟，PM2 是多餘的一層
- **增加複雜度**：額外增加 image 大小與啟動流程的複雜度

## 做法一：純 Docker 取代 PM2（推薦）

Dockerfile 直接用 `node` 啟動應用，搭配 Docker 原生機制處理所有 PM2 做的事：

```dockerfile
CMD ["node", "app.js"]
```

### 自動重啟

Docker Compose 的 `restart` 取代 PM2 的 crash 重啟：

```yaml
services:
  app:
    restart: unless-stopped
```

| 值 | 行為 |
| --- | --- |
| `no` | 不自動重啟（預設） |
| `always` | 永遠重啟，包含手動 stop 後再 daemon 啟動 |
| `unless-stopped` | 除非手動 stop，否則永遠重啟 |
| `on-failure` | 只在非正常結束時重啟（exit code 非 0） |

## 做法二：使用 pm2-runtime

PM2 官方針對容器環境提供 `pm2-runtime`，用來解決直接在容器內用 `pm2 start` 時會遇到的主要問題。

### 與一般 PM2 的差異

| 特性 | `pm2 start` | `pm2-runtime` |
| --- | --- | --- |
| 執行方式 | fork 到背景（daemon） | 前景執行，作為容器主程序 |
| 信號處理 | 不轉發 SIGTERM | 正確轉發 SIGINT / SIGTERM |
| 容器相容性 | 容器會立即退出 | 持續運行，相容容器生命週期 |
| crash 處理 | — | 容器內立即重啟，不需重建容器 |

### 基本用法

```dockerfile
FROM node:24-slim
WORKDIR /app

COPY package*.json ./
RUN npm ci --omit=dev && npm install pm2 -g

COPY . .
CMD ["pm2-runtime", "app.js"]
```

### 搭配 ecosystem 設定

建立 `ecosystem.config.js` 啟用 cluster 模式：

```js
module.exports = {
  apps: [{
    name: 'app',
    script: './app.js',
    instances: 2,           // cluster 數量
    exec_mode: 'cluster',   // 啟用 cluster 模式
    max_memory_restart: '500M',
  }]
}
```

```dockerfile
CMD ["pm2-runtime", "ecosystem.config.js"]
```

### 日誌輸出格式

`pm2-runtime` 預設將日誌輸出到 stdout/stderr，也可指定格式方便日誌系統解析：

```dockerfile
CMD ["pm2-runtime", "--json", "ecosystem.config.js"]
```

| 參數 | 格式 | 適用場景 |
| --- | --- | --- |
| `--json` | JSON（logstash 相容） | ELK、Loki 等日誌系統 |
| `--format` | `key=value` | 結構化日誌 |
| `--raw` | 原始輸出 | 開發除錯 |

## 怎麼選

**選純 Docker：**

- 已使用 Docker Swarm / Kubernetes 等編排工具
- 追求最小 image 與最簡架構
- 團隊熟悉容器化最佳實踐

**選 pm2-runtime：**

- 單機 Docker，無編排工具
- 需要容器內 cluster 模式利用多核心
- 從傳統 PM2 部署遷移至 Docker，降低過渡風險

## 參考資料

- [PM2 Docker Integration - PM2 官方文件](https://pm2.keymetrics.io/docs/usage/docker-pm2-nodejs/)
