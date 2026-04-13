---
title: "Obsidian + Claude Code：真正有效的第二大腦設定"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-06
status: done
source: https://youtu.be/Y2rpFa43jTo
---

EricWTech 示範如何結合 Obsidian 與 Claude Code 打造真正運作的「第二大腦」，以 GitHub 為版控後端，並透過 Obsidian skills 讓 AI 自動整理與查詢筆記。

## 影片描述

作者以實際工作流程示範如何用 Claude Code 管理 Obsidian 筆記、自動匯入專案資料（Gmail、本地檔案），並讓 AI 擔任個人助理來回答任何關於筆記庫的問題。

## 重點摘要

### GitHub 版控設定
- Obsidian 免費版不支援雲端同步，使用 GitHub 作為替代方案
- 建立私有 GitHub repository，將 Obsidian vault 存放其中
- 建議非工程師使用 **GitHub Desktop** 管理版控
- 安裝 Obsidian 社群外掛 **Git**，啟用自動 commit 功能
  - 設定停止編輯後 1 分鐘自動 commit
  - 啟用「pull on startup」，確保多裝置同步

### Obsidian CLI 設定
- 在 Obsidian 設定 → General → Advanced → Command Line Interface 啟用 CLI
- 安裝 Obsidian skills（透過 marketplace 或 mpx skills 指令）
- Skills 讓 Claude Code 可操作 Obsidian 的 markdown、base、JSON、canvas 等功能

### 核心功能：onboard projects 技能
一個自動將外部資料整理進 Obsidian 的技能，流程如下：

1. **資料來源收集**：Gmail 郵件、本地檔案（PDF、合約等）、貼上文字或截圖
2. **專案資料夾結構**：
   - `overview.md`：專案概覽、技術棧、階段說明
   - `conversation-log.md`：按時間順序整理的所有溝通摘要
   - `links.md`：外部資源連結
   - `documents/`：靜態文件（NDA、合約等，不摘要）
   - `projects.base`：所有專案的狀態追蹤表
3. **Gmail 整合**：需設定 Google Cloud Console OAuth 憑證，儲存於 `.gmail-credentials/` 資料夾

### 實際使用情境
- 觸發技能後自動建立專案結構，不需手動整理
- 可直接問 Claude Code「這個專案目前狀態如何？」並獲得準確回答
- 結合 Google Workspace CLI 可讓 Claude Code 直接回覆 Gmail，無需手動複製貼上

### 適用場景
- 專案管理（作者的主要用途）
- 學習與研究整理
- 結合 Notebook LM 進行深度研究自動化

## 補充說明

影片中提到的工具為「Clockwise」，實際上是 Claude Code 的別稱（影片可能為早期版本或口誤）。
