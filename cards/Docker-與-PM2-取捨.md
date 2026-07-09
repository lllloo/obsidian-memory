---
title: Docker 與 PM2 取捨
created: 2026-06-03
updated: 2026-06-11
source: https://pm2.keymetrics.io/docs/usage/docker-pm2-nodejs/
tags:
  - docker
  - pm2
  - deploy
---

**容器內直接 `pm2 start` 是反模式**——兩種跑法各死一條路，而且職責本身就與容器重疊：

1. daemon 模式（預設）：PM2 fork 到背景，容器主程序結束 → 容器立即退出，根本跑不起來。
2. 前景模式（`--no-daemon`）：容器是不退了，但 PM2 作為 PID 1 訊號轉發歷史上不可靠——Node.js 不一定能正確收到 `SIGTERM`，graceful shutdown 行為不確定（官方解法是 pm2-runtime）。
3. 就算解掉上面兩條，容器本身就是隔離單元，Docker / K8s 已負責程序監控與重啟，PM2 是多餘的一層。

## 預設解：純 Docker 取代 PM2

`CMD ["node", "app.js"]` 直跑，crash 重啟交給 Docker 原生機制，有編排工具（K8s / Swarm）則由編排層管，image 也更小。

compose 的 `restart` 選項（選一）：

| 值 | 行為 |
|---|---|
| `no` | 不自動重啟（預設） |
| `always` | 永遠重啟，包含手動 stop 後 daemon 再起也自動復活 |
| `unless-stopped` | 除非手動 stop，否則永遠重啟（手動 stop 後 daemon 重開不復活） |
| `on-failure` | 只在非正常結束時重啟（exit code 非 0） |

一般服務用 `unless-stopped`：既能 crash 自動恢復，手動 stop 後重開機也不會自己跑起來。

## pm2-runtime 的唯一正當場景

PM2 官方為容器提供 `pm2-runtime`：前景執行（容器主程序）、正確轉發 SIGINT / SIGTERM，解掉上面兩個技術問題。但職責重疊仍在，只有這些情境才值得用：

- 單機 Docker、無編排工具，且需要容器內 cluster 模式吃多核心
- crash 恢復速度敏感：pm2-runtime 是容器內立即重啟程序，比 Docker restart 重啟整個容器快
- 從傳統 PM2 部署遷移到 Docker，降低過渡風險

pm2-runtime 不在 node 官方 image 內，需先安裝：

```dockerfile
RUN npm ci --omit=dev && npm install -g pm2
```

啟動：`CMD ["pm2-runtime", "ecosystem.config.js"]`，cluster 數量、`max_memory_restart` 等設定寫 ecosystem 檔；日誌格式參數（JSON 等）查官方文件。

## 相關

- [[Nuxt-Docker-多階段構建]] — 同根因的 `npm start` 版；該模板即採 `node` 直跑
