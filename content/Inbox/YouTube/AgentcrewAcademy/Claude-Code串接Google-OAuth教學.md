---
title: Claude Code 怎麼接上 Google？一步步申請 Google OAuth 完整教學
created: 2026-04-27
updated: 2026-04-27
source: https://www.youtube.com/watch?v=RRADpJ8rYNE
published: 2026-04-26
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - google-oauth
  - mcp
---

## 為什麼要設定 OAuth

要讓 Claude Code 存取 Google Workspace（Gmail、Google Drive、Google Sheet、Google Document、Google Calendar、Google Map 等）服務，必須先在 Google Cloud Platform 申請 OAuth 授權，產出一份 `credentials.json` 設定檔，作為工具進入 Google 服務的鑰匙。整套流程只需做一次，未來重複使用。

OAuth 同意畫面（每次首次授權跳出的選擇 Google 帳號畫面）是 Google 在替使用者把關，不是病毒警告。

## 設定流程

### 1. 建立 Google Cloud 專案

- 搜尋「Google 憑證」進到官方指南，點擊「Google API 控制台」連結
- 連到 Google Cloud Platform 後，左上角新建專案（名稱可自訂）
- 載入後選取剛建立的專案

### 2. 設定 OAuth 同意畫面

- 左側選單找到「OAuth 同意畫面」，選擇「開始」
- 填上應用程式名稱（自用可隨意，例：coco）、選擇自己的 Email
- 使用者類型選「外部」（內部選項僅限 Google Workspace 帳號）
- 同意條款後按「繼續 → 建立」

### 3. 啟用所需的 API

- 左側「API 與服務 → 程式庫」搜尋並啟用要對接的 API：
  - Gmail API
  - Google Drive API
  - Google Sheets / Docs / Calendar / Maps API 等
- 不確定要開哪些可以直接問 Claude Code，他會列清單一個一個搜尋
- 漏開沒關係，後續系統會回報錯誤、Claude 會提醒回來補開

### 4. 建立 OAuth 憑證

- 「憑證 → 建立憑證 → OAuth 用戶端 ID」
- 應用程式類型建議選「電腦版應用程式」（Desktop app）
- 名稱可自訂（例：croq）
- 建立後會跳出用戶端 ID、用戶端密碼，這兩個就是 OAuth 的核心

### 5. 下載 credentials.json

- 從建立後的畫面下載 JSON 檔，妥善儲存，不要外傳
- 未來在 Claude Code 第一次設定 Google Workspace MCP 或 CLI 時，會跟你索取此檔
- 拉進終端機交給 Claude Code，他會自動完成設定

## 後續使用

設定好之後，每次 Claude 要對接新的 Google 服務時：

- 已啟用對應 API → 直接走 OAuth 授權即可
- 還沒啟用 → 系統會回報，回到 Cloud Console 對應路徑開通

完成這一次設定後一勞永逸，後續安裝 Google Workspace CLI 或 MCP 時，憑證會自動授權對接。

## 安全提醒

- `credentials.json` 等同帳號鑰匙，不可外傳；外洩需立刻在 Google Cloud Console 撤銷
- 螢幕示範用的憑證使用後應立即刪除作廢
