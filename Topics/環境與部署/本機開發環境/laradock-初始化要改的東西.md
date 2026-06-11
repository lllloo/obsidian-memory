---
title: laradock 初始化要改的東西
created: 2026-05-19
updated: 2026-06-11
tags:
  - laradock
  - docker
  - sop
---

## 為什麼有這篇

laradock clone 完不是 just works，至少有三件事要先處理才跑得起來。下次再 clone 一份新環境時照這張單子改，省得重新踩。

## 1. `.env` 必改三處

從 `.env.example` 複製出 `.env` 後，依本機環境調整以下三項：

| 設定 | example 預設 | 我的值 | 為什麼改 |
|---|---|---|---|
| `PHP_VERSION` | `8.4` | `7.4` | 既有專案還在 PHP 7.4，相容性需要 |
| `PMA_DB_ENGINE` | `mysql` | `mariadb` | 配合本機 DB 改用 mariadb |
| `PMA_PORT` | `8081` | `8088` | 避免跟本機其他服務 8081 衝突 |

前兩項是長期值（跟著手上專案綁），第三項看本機其他服務佔用情況再決定。

注意：`PHP_VERSION` 這類 build-time 設定改完**必須重新建構才生效**，重啟容器沒用：

```bash
docker-compose build php-fpm workspace
docker-compose up -d php-fpm workspace
```

build 完要 `up -d` 重建容器才會用到新 image——`restart` 是同一個容器 stop/start，跑的仍是舊 image。

## 2. `nginx/sites/` 加自訂 vhost

laradock 預設 `nginx/sites/` 底下只有 `default.conf` 跟一堆 `*.conf.example`，要跑自己的專案必須**新增一份 `<專案>.conf`**。

做法：複製對應的 `.conf.example` 改名成 `<專案>.conf`，按專案實際需求改 `server_name`、`root`、`fastcgi_pass` 等欄位。

gitignore 已涵蓋 `*.conf`（`.conf.example` 例外），新增的 vhost 不會被 commit，每台機器各自管理。

## 3. Laravel 專案 `.env` 只要改 5 處連線設定

關鍵觀察：專案已經有 `.env.develop` / `.env.formal` / `.env.master` 當部署模板，第三方 key、命名空間（`CACHE_PREFIX` / `REDIS_PREFIX` / `REDIS_QUEUE`）、業務 flag、`APP_BRANCH`、`GMAIL_MAIL_*`、`FTP_*`、`JWT_SECRET` 等**全部已經在裡面**——本機不必重填。

做法：

1. 從 `.env.develop` 複製成 `.env`（不是從 `.env.example` 起步）
2. 只改 5 處連線設定，把本機 laradock 容器接上：

| 鍵 | 部署值 | laradock 本機值 |
|---|---|---|
| `DB_HOST` | `127.0.0.1` | `mariadb` |
| `DB_USERNAME` | 環境帳號 | `root` |
| `DB_PASSWORD` | 環境密碼 | `root` |
| `REDIS_HOST` | `127.0.0.1` | `redis` |
| `REDIS_PASSWORD` | `null` | `secret_redis` |

理由：Laravel container 走 Docker 內部網路，hostname 是 service 名；`root/root` 與 `secret_redis` 都是 laradock 容器的預設帳密。

## 相關

- [[Laradock-多專案架構]] — 為什麼一份 laradock 能服務多專案、加專案動什麼不動什麼、PHP 版本共用限制
