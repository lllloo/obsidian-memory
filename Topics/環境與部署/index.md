---
title: 環境與部署
description: 從本機把專案跑起來到上版發佈的整條鏈：Laradock 開發環境、Quartz 靜態站發佈、GitHub Actions CI/CD 與踩坑
created: 2026-05-08
updated: 2026-06-26
tags:
  - deploy
  - docker
  - laradock
  - sop
---

從「本機把專案跑起來」到「上線發佈」整條工程交付鏈的 SOP 與踩坑筆記。以目的地分組：先讓程式碼在本機跑起來（Docker / Laradock 開發環境），再走上版、發佈與 CI/CD。

## 開發工具與設定

- [[Git-設定]] — 常用 `git config`、alias（含 `git lg` graph log）、`core.autocrlf` 換行轉換與暫存區重設
- [[npm-套件更新與檢查]] — `npm outdated`／`update` 的 semver 範圍行為，與 npm-check-updates（ncu）拉高版本範圍
- [[Volta-使用教學]] — Node.js 版本管理：`install`／`pin` 專案綁定版本與 `package.json` volta 欄位

## 本機開發環境

- [[bookmark-Laradock-Docker開發環境|Laradock]] — 基於 Docker 的完整 PHP 開發環境（nginx / php-fpm / DB / Redis…），本組各筆記的工具底座
- [[Laradock-多專案架構]] — 一份 laradock 靠 `APP_CODE_PATH_HOST=../`（掛父目錄）+ 每專案一份 nginx conf 服務多專案；加專案動什麼、PHP 版本共用限制
- [[Laradock-CI3-本機啟動模板]] — CodeIgniter 3.x 去識別化啟動範本，填空清單照抄；含 CI nginx rewrite 與 `CI_ENV` 白屏坑
- [[laradock-初始化要改的東西]] — clone 完 laradock 不是 just works：`.env` 必改三處、自訂 vhost、Laravel `.env` 只改 5 處連線設定
- [[Docker-Compose-Laravel-啟動步驟]] — 非 Laradock 的 Docker Compose 流程，Laravel artisan migrate/seed

## 上版 / 發佈

- [[git-archive-打包異動檔]] — 把 commit 之間的異動打包成 zip 交付給沒 Git 的環境
- [[Quartz-部署筆記]] — 把本 vault 以 Quartz 發佈成靜態站的設定與踩坑

## CI/CD（GitHub Actions）

- [[GitHub-Actions-Secrets-與-Variables]] — Secrets/Variables × Repository/Environment 四象限與 fork PR 信任邊界
- [[環境變數-Secret-命名規範]] — `<服務>_<資源>_<型別>` UPPER_SNAKE_CASE 命名慣例
- [[GitHub-Actions-PR-merge-Discord-通知]] — PR merge 觸發 Discord 通知，含 script injection 防護
- [[bookmark-Discord-Webhook-CI通知用|Discord Webhook]] — Webhook 通知原理與設定（書籤）
- [[bookmark-actions-status-discord-CI狀態通知Action|actions-status-discord]] — 現成的 CI 狀態 Discord 通知 Action（書籤）
