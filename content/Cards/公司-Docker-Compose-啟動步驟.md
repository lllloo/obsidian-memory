---
title: 公司 Docker Compose 啟動步驟
tags:
  - deploy
  - docker
created: 2026-04-02
updated: 2026-04-02
---

## 1. 調整 `docker-compose.yml`

## 2. 新增 `.env` 檔案

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