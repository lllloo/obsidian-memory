---
title: Mirage 虛擬檔案系統取代 MCP 工具
description: Mirage 把 Gmail、Slack、Drive 等服務掛載成 Claude Code / Codex CLI 可直接操作的虛擬資料夾，用模型早已熟練的 file system 語意取代每個 MCP 都要重學的自訂工具。
created: 2026-05-28
updated: 2026-05-28
source: https://www.youtube.com/watch?v=B44bXmzU60s
published: 2026-05-27
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
---

## 核心概念：file system 取代 MCP

MCP 工具要求 model 現學每組 tool description、規劃呼叫順序，光是「了解工具」就先吃掉一輪 token，每新增一個 tool 就重來一次。

file system 是 LLM 在訓練語料中見過億次的介面，Unix 已經精煉 50 年，是唯一一個讓 AI agent 跨服務操作而不需要重新學習的抽象層。Mirage 的核心做法就是把外部服務（Gmail、Slack、Notion、Drive 等）掛載成虛擬資料夾，emails、訊息、檔案都變成 model 可以直接 `read`、`cp`、`grep` 的檔案。

## Mirage 的實際運作

在 Mirage workspace 啟動 Claude Code 後，掛載的服務會顯示為目錄。Gmail 例子中：

- 每個 Gmail label / category 各自是一個 directory
- 每封 email 是檔案，Claude 用讀 markdown 的方式讀 email
- email 附件可以直接讀取，不像 MCP 只能看到檔名

預設支援的連接器：Gmail、整套 Google Suite、Notion、Slack、Telegram、各種儲存系統與資料庫。掛載後全部變成 Claude 目錄裡的資料夾。

## 解決 Google Drive MCP 的下載瓶頸

Google Drive MCP 的下載邏輯是：抓檔案內容成字串 → decode → 寫回本機檔案系統。

- 2 MB 檔案下載要花約 4 分鐘，並且 bloat context
- 100 MB 檔案會直接撞到 response limit

Mirage 直接用 bash `cp` 指令把 drive 上的檔案複製到本機資料夾，不過 model 的 context window，速度與成本都贏。

## Bash pipeline 即 code mode

Mirage 配合 bash 指令天然就是 code mode：把不同服務的內容用 pipeline 串起來，內容不需要進入 model 的 context window。

範例：找 inbox 裡提到 sponsors 的 email、列出前 3 名（贊助金額最高的）、寫進 Notion 頁面。整個流程是 bash 指令的 pipeline，model 只負責寫 script，不需要把 email 內容都載入 context。

## 自訂服務也能轉成檔案系統

Mirage 後端用的就是各 MCP server 用的同一套 API，只是把它包裝成 file system。任何有 API 的服務都可以做：

- Figma 設計稿列成檔案
- Google Chat 把 spaces 與訊息掛成資料夾

只要叫 Claude 讀 Mirage repo source code，給它跑幾輪 feedback loop，就能把任何 service 接成虛擬檔案系統。

## 安裝與認證

```bash
# 推薦做法：直接 clone repo，讓 Claude 自己讀 source 帶你裝
git clone <mirage-repo>
cd mirage
claude
```

macOS 額外要裝 macFUSE（macOS 才支援第三方 file system），需要重啟系統並改安全性設定。重啟前先 `/rename` 當前 chat 或讓 Claude 從歷史 chat 還原 context（Claude Code chat 都存在本機）。

認證不像 Claude connectors 有自動 OAuth，每個服務要自己掛憑證：

1. Mirage 會 mount 一個 TypeScript 檔案，把該服務加到 workspace 的目錄
2. 你提供該服務的 credentials（Google 服務要進 Google Cloud Console 開 API、取 credentials）
3. Claude 會引導你跑 mount command，要在獨立 terminal 保持開啟（或叫 Claude 跑成 background process）

## Persistent workspace 與遠端 host

cache 與 index 是 workspace 持久化的關鍵，process restart 就會清空。Mirage 用 daemon 模式把它變成常駐 background server：

- 支援多個具名 workspace 同時跑
- 每個 workspace 可以指定啟動模式
- 因為是標準 HTTP server，可以 host 在任何機器上，跨機器切換時直接連過去
