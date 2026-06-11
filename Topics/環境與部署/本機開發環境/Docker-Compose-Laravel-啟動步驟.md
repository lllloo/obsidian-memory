---
title: Docker Compose Laravel 啟動步驟
created: 2026-04-02
updated: 2026-06-11
tags:
  - deploy
  - docker
  - sop
---

## 1. 調整 `docker-compose.yml`

- 主要調 networks 設定
- 確認 port 有用 `ports` 發佈到本機 localhost（`expose` 只在容器間可見，host 連不到）
- 把這個專案用不上的容器關掉（精簡 stack）

## 2. 新增 `.env` 檔案

- 複製 `.env.example` 為 `.env`，再改連線設定

## 3. 啟動容器

```bash
docker-compose up -d
```

## 4. 進到 web 容器安裝 PHP 依賴

```bash
docker-compose exec web composer i
```

## 5. 等待容器就緒（重要）

- `composer i` 完成後，需重啟容器（`docker-compose restart web`）或等容器自動重啟
- 容器啟動時會先執行 `/init/fix-permissions.sh`，對整個 `/var/www/html` 逐一 `chown www-data:www-data`
- 因為 `vendor/` 內有數萬個檔案，加上 Windows Docker 掛載 volume 效能較差，這個過程可能需要數分鐘
- 在 chown 跑完之前，supervisord 不會啟動，nginx 和 php-fpm 也不會運行，此時訪問網站會出現 502
- 確認方式：執行 `docker-compose exec web ps aux`，看到 `supervisord`、`nginx`、`php-fpm` 進程出現即代表就緒

## 6. 執行 Migration

```bash
docker-compose exec web php artisan migrate --force
```

## 7. 執行 Seeder

```bash
docker-compose exec web php artisan db:seed --force
```

## 8. 確認

訪問 http://localhost/ 確認網站正常運作

## 相關

- [[Docker-網路隔離只暴露-Nginx]] — §1 networks 設定的進階版：只暴露 Nginx、DB 走 internal 網路
- [[Nuxt-Docker-多階段構建]] — 同為 Docker 本機/部署情境的 Node (Nuxt) 版模板
- [[Docker-與-PM2-取捨]] — 容器內程序管理的取捨；本篇 web 容器內的 supervisord 即同類角色
