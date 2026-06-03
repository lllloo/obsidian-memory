---
title: Laradock
created: 2026-06-03
updated: 2026-06-03
source: "https://laradock.io/"
tags:
  - laradock
  - docker
---

Laradock 是基於 Docker 的完整 PHP 本機開發環境，預先打包 nginx、php-fpm、MySQL / MariaDB、Redis、phpMyAdmin 等 70+ 服務，用 docker-compose 選用啟動。把 laradock 與專案資料夾並列同層、設 `APP_CODE_PATH_HOST=../`，一份環境即可服務多個專案；雖以 Laravel 為名，純 PHP / CodeIgniter 等專案同樣適用。

## 連結

- 官網 / 文件：<https://laradock.io/>
- Repo：<https://github.com/laradock/laradock>

## 相關

- [[Laradock-多專案架構]] — 一份 laradock 服務多專案的機制與限制
- [[Laradock-CI3-本機啟動模板]] — CodeIgniter 3.x 啟動填空模板
- [[laradock-初始化要改的東西]] — clone 完的初始化清單
