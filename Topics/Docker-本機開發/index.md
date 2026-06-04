---
title: Docker 本機開發
description: 用 Laradock 在 Windows + Docker Desktop 跑既有專案的本機開發環境，啟動模板與初始化踩坑
created: 2026-06-03
updated: 2026-06-04
tags:
  - docker
  - laradock
  - sop
---

用 Docker（主要是 Laradock）在本機把既有專案跑起來的 SOP 與踩坑筆記。聚焦 Windows + Docker Desktop 情境、container 內部網路接線、CI3 / Laravel 專案的本機差異。

## 工具

- [[bookmark-Laradock-Docker開發環境|Laradock]] — 基於 Docker 的完整 PHP 開發環境（nginx / php-fpm / DB / Redis…），本 Topic 各筆記的工具底座

## 架構

- [[Laradock-多專案架構]] — 一份 laradock 靠 `APP_CODE_PATH_HOST=../`（掛父目錄）+ 每專案一份 nginx conf 服務多專案；加專案動什麼、PHP 版本共用限制

## 啟動 SOP

- [[Laradock-CI3-本機啟動模板]] — CodeIgniter 3.x 去識別化啟動範本，填空清單照抄；含 CI nginx rewrite 與 `CI_ENV` 白屏坑
- [[laradock-初始化要改的東西]] — clone 完 laradock 不是 just works：`.env` 必改三處、自訂 vhost、Laravel `.env` 只改 5 處連線設定

## 相關

- [[Docker-Compose-Laravel-啟動步驟]] — 非 Laradock 的 Docker Compose 流程，Laravel artisan migrate/seed
