---
title: Laradock 常用指令
created: 2026-06-03
updated: 2026-06-04
tags:
  - docker
  - laradock
  - cli
---

# Laradock 常用指令

[Laradock](https://laradock.io/) 是基於 Docker 的 PHP 開發環境，預先配置了 Nginx、MySQL、MariaDB、Redis、phpMyAdmin 等常用服務，適合 Laravel 專案快速搭建開發環境。

## 啟動服務

依需求選擇要啟動的服務組合：

```bash
# MySQL 組合
docker compose up -d nginx mysql phpmyadmin redis

# MariaDB 組合
docker compose up -d nginx mariadb phpmyadmin redis

# 含 workspace（可進入容器執行 artisan 等指令）
docker compose up -d nginx mariadb phpmyadmin redis workspace
```

> Laradock 的 `docker-compose.yml` 定義了大量服務，只啟動需要的即可，避免佔用過多資源。

## 停止服務

```bash
docker compose stop
```

> `stop` 只停止容器，不移除。若要停止並移除容器與網路，改用 `docker compose down`。

## 進入 workspace

workspace 是 Laradock 提供的開發用容器，內含 PHP CLI、Composer、Node.js 等工具：

```bash
docker compose exec workspace bash
```

在 workspace 內可執行：

- `php artisan` 指令
- `composer install / update`
- `npm` 相關指令

## 重新建構服務

切換 PHP 版本或修改 `.env` 設定後，需重新建構相關服務：

```bash
docker compose build php-fpm workspace
```

> 修改 Laradock `.env` 中的 `PHP_VERSION` 後，必須重新 build 才會生效。

## Reload Nginx

修改 Nginx 設定後，不需重啟容器，直接 reload 即可：

```bash
docker exec -it laradock-nginx-1 nginx -s reload
```

> 容器名稱依實際環境而定，可用 `docker ps` 查看正確名稱。
