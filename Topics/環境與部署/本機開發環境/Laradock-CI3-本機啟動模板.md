---
title: Laradock + CodeIgniter 3.x 本機啟動模板
created: 2026-04-24
updated: 2026-06-16
tags:
  - docker
  - laradock
  - codeigniter
  - sop
---

# Laradock + CodeIgniter 3.x 本機啟動模板

去識別化範本，下個專案照抄，把填空清單的值換掉即可。

> 假設：Windows + Docker Desktop + Laradock clone 在 `C:\code\laradock`，專案放 `C:\code\<PROJECT_DIR>\` 同層。

## 架構：多專案

這張是 Laradock multiple projects 模式下的**單一專案啟動流程**——laradock 與各專案在 `C:\code\` 同層，`APP_CODE_PATH_HOST=../` 讓每個專案都掛進 `/var/www/<PROJECT_DIR>`。為什麼一份 laradock 能服務多專案、加第 N 個專案動什麼、PHP 版本共用限制，見 [[Laradock-多專案架構]]。下面填空清單的 `<PROJECT_DIR>` / `<LOCAL_DOMAIN>` / `<LOG_PREFIX>` 就是各專案的分流鍵。

## 填空清單

| 占位符 | 範例 | 說明 |
|---|---|---|
| `<PROJECT_DIR>` | `my-project` | 專案資料夾，對應 container 內 `/var/www/<PROJECT_DIR>` |
| `<LOCAL_DOMAIN>` | `myapp.test` | 本機開發網址，加到 hosts（TLD 用 `.test`，別用 `.dev` / `.local`，原因見 [[Laradock-多專案架構]]） |
| `<SITE_CONF>` | `myapp.conf` | nginx site 設定檔名 |
| `<DB_NAME>` | `myapp_dev` | DB 名（沿用開發站方便匯 dump） |
| `<LOG_PREFIX>` | `myapp` | nginx log 檔名前綴 |
| `<PROD_HOST_IN_INDEX_PHP>` | `myapp.com` | 若 `index.php` 有 HTTP_HOST 判定才填，沒有跳過 §3 的 CI_ENV |

## 1. 啟動 Laradock

Laradock `.env` 關鍵值（不需改）：`APP_CODE_PATH_HOST=../`、`PHP_VERSION=7.4`。對應後 `C:\code\<PROJECT_DIR>` ↔ container `/var/www/<PROJECT_DIR>`。

```bash
cd C:\code\laradock
docker-compose up -d nginx mariadb php-fpm phpmyadmin workspace
```

workspace 是開發用容器，內含 PHP CLI / Composer / Node.js——`docker-compose exec workspace bash` 進去跑 composer / npm 等指令。

## 2. 取得程式碼

```bash
cd C:\code
git clone <repo-url> <PROJECT_DIR>
```

## 2.5 安裝 Composer 依賴（接 Eloquent 的 CI3 才需要）

專案 `composer.json` 若 `require` 含 `illuminate/database`（接了 Laravel Eloquent），`application/third_party/eloquent.php` 會 `require vendor/autoload.php`；clone 後沒裝依賴就缺 `vendor/`，開首頁直接 Fatal error（非框架白屏）：

```
require(.../vendor/autoload.php): failed to open stream: No such file or directory
```

必須在 **workspace 容器內**跑（依賴要對應容器 PHP 版本，不是 Windows 本機）：

```bash
docker-compose exec workspace bash -c "cd /var/www/<PROJECT_DIR> && composer install"
```

驗證 `vendor/autoload.php` 出現即可。沒接 Eloquent（純 CI3）跳過此節。

## 3. 建立 nginx site 設定

新增 `C:\code\laradock\nginx\sites\<SITE_CONF>`：

```nginx
server {
    listen 80;
    listen [::]:80;

    server_name <LOCAL_DOMAIN>;
    root /var/www/<PROJECT_DIR>;
    index index.php index.html index.htm;

    location / {
        try_files $uri $uri/ /index.php?/$request_uri;
    }

    location ~ \.php$ {
        try_files $uri /index.php =404;
        fastcgi_pass php-upstream;
        fastcgi_index index.php;
        fastcgi_buffers 16 16k;
        fastcgi_buffer_size 32k;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param CI_ENV development;   # 見下方 §3.2
        fastcgi_read_timeout 600;
        include fastcgi_params;
    }

    location ~ /\.ht { deny all; }

    error_log /var/log/nginx/<LOG_PREFIX>_error.log;
    access_log /var/log/nginx/<LOG_PREFIX>_access.log;
}
```

- **URL rewrite 必用 `/index.php?/$request_uri`**（CI 版），別套 Laradock 範本的 `$is_args$args`（Laravel 版），會 404
- **`fastcgi_param CI_ENV development;`**：專案 `index.php` 有 `HTTP_HOST` 判定才進 development 時必加，否則本機會被當 production 白屏；沒這種判定可省略

## 4. 重啟 nginx + 設 hosts

```bash
docker-compose restart nginx
```

修改 Nginx 設定後，不需重啟容器，直接 reload 即可：

```bash
docker exec -it laradock-nginx-1 nginx -s reload
```

> 容器名稱依實際環境而定，可用 `docker ps` 查看正確名稱。

以系統管理員編輯 `C:\Windows\System32\drivers\etc\hosts`：

```
127.0.0.1   <LOCAL_DOMAIN>
```

## 5. 建立資料庫並匯入 dump

CI 3.x 多半沒 migration，從開發站撈 dump。phpMyAdmin：`http://localhost:8088`（root / root）。

1. 建 DB `<DB_NAME>`，collation `utf8mb4_general_ci`
2. 開發站 phpMyAdmin → 匯出 SQL
3. 本機 phpMyAdmin → 選 DB → 匯入

## 6. 建立 `database.php`（最關鍵）

CI 3.x 慣例：`application/config/database.php` 被 `.gitignore` 排除。範本通常在 `remote/database.develop.php` 之類的位置。

```bash
cd C:\code\<PROJECT_DIR>
copy remote\database.develop.php application\config\database.php
```

編輯改成 container 內位址：

```php
'hostname' => 'mariadb',    // ← docker-compose 服務名，不是 localhost / 127.0.0.1
'username' => 'root',
'password' => 'root',
'database' => '<DB_NAME>',
'dbdriver' => 'mysqli',
'char_set' => 'utf8mb4',
'dbcollat' => 'utf8mb4_general_ci',
```

## 7. 驗證

開 `http://<LOCAL_DOMAIN>/`：

- **首頁正常** → 成功
- **Error 1146 Table doesn't exist** → nginx / php-fpm / DB 都通，只是 dump 沒匯完，回 §5
- **白屏 + Fatal `vendor/autoload.php` failed to open** → 沒裝 Composer 依賴，回 §2.5
- **白屏 / 502 / Database Error** → 看 log：`application/logs/log-YYYY-MM-DD.php`、`docker-compose logs -f nginx php-fpm`

## 相關筆記

- [[Docker-Compose-Laravel-啟動步驟]] — Laravel/Artisan 流程，同為 Docker 本機開發情境
