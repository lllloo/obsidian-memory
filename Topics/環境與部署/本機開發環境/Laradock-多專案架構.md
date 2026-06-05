---
title: Laradock 多專案架構
created: 2026-06-03
updated: 2026-06-03
tags:
  - laradock
  - docker
  - sop
---

一份 laradock 同時服務多個專案的關鍵，是 `.env` 的 `APP_CODE_PATH_HOST=../`——掛載的是 laradock 的**父目錄**，不是某個專案資料夾。把 laradock 與各專案放在同一層，父目錄底下每個專案就都被掛進 container 的 `/var/www/<專案名>`。

```
C:\code\
├── laradock\     # 一份，所有專案共用
├── project-1\    # → /var/www/project-1
└── project-2\    # → /var/www/project-2
```

## 為什麼這樣就能多專案並存

laradock 容器（nginx / php-fpm / db…）只起一組，多專案**不是靠多開容器，而是靠 nginx 分流**：每個專案一份 `nginx/sites/<專案>.conf`，各自不同的 `server_name`（本機網域）+ `root /var/www/<專案名>` + log 前綴。request 進來，nginx 依 `server_name` 命中對應 conf，導到該專案目錄。本機網域（`server_name` + hosts）的 TLD 別用 `.dev`（Chrome 63+ 透過 HSTS preload 強制 HTTPS、連不上 http）或 `.local`（與 mDNS / Bonjour 衝突），用官方建議的 `.test` / `.localhost` 這類保留測試後綴最穩。

所以「加專案」加的是 conf 與該專案的 DB / hosts，不是再開一份 laradock。

## 加第 N 個專案動什麼、不動什麼

| 動 | 不動 |
|---|---|
| clone 專案到 `C:\code\<專案>\` | laradock 容器（已起，不重來） |
| 加 `nginx/sites/<專案>.conf` | laradock `.env`（`APP_CODE_PATH_HOST=../` 已對） |
| 重啟 nginx、加 hosts | php-fpm / workspace 等共用服務 |
| 建該專案 DB、接 DB 設定檔 | 其他專案的 DB / 網域 / log（彼此獨立） |

## 限制：共用同一組 container

各專案的 DB、網域、log 互不干擾，但**共用同一組容器與同一個 `PHP_VERSION`**。多專案的 PHP 版本需求衝突時（例如一個要 7.4、一個要 8.x），這套單一 laradock 就不適用——得各自獨立 laradock，或切換 `PHP_VERSION` 重啟（無法同時跑）。

## 相關

- [[Laradock-CI3-本機啟動模板]] — CodeIgniter 3.x 在這套架構下的完整啟動填空模板
- [[laradock-初始化要改的東西]] — clone 完 laradock 的初始化清單（含 `PHP_VERSION` 等 `.env` 必改項）
