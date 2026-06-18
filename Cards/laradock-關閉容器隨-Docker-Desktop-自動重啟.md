---
title: laradock 關閉容器隨 Docker Desktop 自動重啟
created: 2026-06-18
updated: 2026-06-18
tags:
  - laradock
  - docker
  - docker-compose
---

## 問題

Docker Desktop 一啟動，laradock 容器就全部自動跑起來。

## 根因

不是「Docker Desktop 開機自啟」，而是 `docker-compose.yml` 裡 65 個服務全部寫死 `restart: always`。容器一旦被 `docker-compose up -d` 建立，就帶著「daemon 啟動即自動拉起」政策，所以 Docker Desktop 重開時容器就復活。

## 採用解法（不改檔、用指令）

對現有容器直接改重啟政策為 `no`，零檔案改動、立即生效：

```powershell
docker ps -aq --filter "label=com.docker.compose.project=laradock" | ForEach-Object { docker update --restart=no $_ }
```

驗證：`docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' <容器>` 顯示 `no`。本次 6 個容器（nginx / mariadb / php-fpm / workspace / docker-in-docker / phpmyadmin）已全部改成 `no`。

## 重要限制：改的是容器實例，不是 compose 檔

這是改在「容器實例」上，不是改 compose 檔。

- `docker-compose down` 後再 `up -d` 重建容器，會從 compose 重新讀到 `restart: always`，政策被打回，需再跑一次上面指令。
- 單純 start / stop / restart 既有容器**不會**重置，只有「重建（recreate）」才會。

## 一勞永逸的替代解法（本次未採用）

改 `docker-compose.yml`：把 `restart: always` 改成 `restart: "no"`，或做成 `.env` 變數（如 `DOCKER_RESTART_POLICY`）驅動，re-up 也不復發。

## 回查線索

- 專案：`C:\code\laradock`
- 關鍵檔：`docker-compose.yml`（65 處 `restart: always`）
- `COMPOSE_PROJECT_NAME=laradock`

## 相關

- [[laradock-初始化要改的東西]] — build-time 設定與 restart/recreate 的差異（`restart` 不會換 image，`up -d` 才重建）
