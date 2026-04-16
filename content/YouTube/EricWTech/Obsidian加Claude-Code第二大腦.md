---
title: Obsidian + Claude Code 打造真正有效的第二大腦
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-06
source: https://www.youtube.com/watch?v=Y2rpFa43jTo
parent: "[[01.index]]"
---

## 核心架構

**GitHub 作為免費雲端同步**（因 Obsidian 免費版不含同步）：

- 建立 GitHub private repo → GitHub Desktop clone 到本機 → Obsidian 以 Vault 方式開啟該資料夾
- 安裝 Obsidian **Git 社群插件**，設定 `auto commit and sync`（建議 1 分鐘間隔）+ `pull on startup`
- 結果：多裝置自動同步，版本控制全免費

## Obsidian CLI 設定

Settings → General → Advanced → **Command Line Interface** → 開啟

啟用後 Claude Code 可透過 CLI 直接操作 Vault（建立筆記、查詢、Base、Canvas 等）

## 核心技巧：Obsidian Skills

安裝一組 Obsidian CLI skills，讓 Claude Code 學會操作 Vault 的所有能力（markdown、base、JSON、canvas）。

## 實際案例：`onboard-projects` Skill

**功能**：將外部資料（Gmail、本機文件、截圖）自動整理進 Obsidian 專案結構

**資料來源**：
- Gmail label（需 Google OAuth credentials）
- 本機檔案（PDF、合約、文件）
- 貼上的文字或截圖

**自動產生的專案結構**：

```
Projects/<專案名>/
├── overview.md         # 專案概覽、技術棧、階段
├── conversation-log.md # 時間軸對話摘要
├── links.md            # 外部連結
├── documents/          # NDA、合約等靜態文件
└── projects.base       # 所有專案狀態儀表板
```

**處理邏輯**：
- 若專案已存在 → 偵測重複、更新資料
- 若新專案 → 分類（靜態文件 vs 對話摘要）→ 自動萃取 wiki links、產業標籤、更新 overview

## 實際使用方式

觸發 `onboard-projects` → 輸入專案名稱 → 提供 Gmail label + 本機路徑 → Claude Code 自動整理一切，最後可直接問：

> 「這個專案目前狀態如何？幫我草擬一封回信給客戶」

Claude Code 結合 Google Workspace CLI，可直接操作 Gmail 發信，不需手動切換 app。
