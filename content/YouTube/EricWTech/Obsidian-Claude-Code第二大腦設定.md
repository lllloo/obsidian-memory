---
title: "Obsidian + Claude Code：真正有效的第二大腦設定"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-06
source: https://youtu.be/Y2rpFa43jTo
---

**影片描述**：作者以實際工作流程示範如何用 Obsidian + Claude Code 打造真正運作的「第二大腦」，以 GitHub 為免費版控後端，透過 Obsidian CLI Skills 讓 AI 自動整理專案資料（Gmail、本地檔案）並擔任個人助理回答任何關於筆記庫的問題。

**重點摘要：**
- **GitHub 版控取代付費同步**：Obsidian 免費版不支援雲端同步，作者建立私有 GitHub repository 作為替代方案，建議非技術使用者用 **GitHub Desktop** 管理版控（GUI 介面，不需終端機）；將 GitHub repo clone 到本機後，以該資料夾作為 Obsidian vault。
- **自動 commit 設定**：在 Obsidian 社群外掛安裝 **Git 外掛**，啟用「auto commit and sync after stopping file edits」，設定停止編輯後 1 分鐘自動 commit；同時啟用「pull on startup」確保多裝置同步最新版本。
- **Obsidian CLI 啟用**：進入 Obsidian Settings → General → Advanced，啟用 Command Line Interface 選項，讓 Claude Code 能透過 CLI 操作 Obsidian。
- **安裝 Obsidian Skills**：透過 marketplace 或 mpx skills 指令安裝，讓 Claude Code 可操作 Obsidian 的 markdown、base、JSON、canvas 等功能，透過 Slash 指令或自然語言呼叫。
- **核心功能：`onboard projects` 技能**：自動將外部資料整理進 Obsidian。資料來源支援 Gmail 郵件標籤、本地檔案（PDF、合約等）、貼上文字或截圖；自動建立專案資料夾結構，包含 `overview.md`（專案概覽）、`conversation-log.md`（按時間順序的溝通摘要）、`links.md`（外部連結）、`documents/`（靜態文件，不摘要）、`projects.base`（所有專案狀態追蹤表）。
- **Gmail 整合細節**：需在 Google Cloud Console 建立 OAuth 憑證、啟用 Gmail API，下載憑證 JSON 存放於 `.gmail-credentials/` 資料夾，設定完成後 Claude Code 可自動抓取指定 Gmail 標籤中的所有郵件並摘要整理。
- **onboard 完整流程**：觸發技能後輸入專案名稱 → 檢查是否為現有專案（是則更新，否則新建）→ 輸入 Gmail 標籤與本地檔案路徑 → 自動分類（靜態文件/對話/參考資料/關鍵細節）→ 提取 wiki links、行業標籤 → 更新 overview.md → 生成時間軸摘要與關鍵事件報告。
- **實際使用情境**：可直接問 Claude Code「這個專案目前狀態如何？」獲得準確回答；結合 Google Workspace CLI 可讓 Claude Code 直接起草 Gmail 回覆；作者主要用於多專案同時管理，也適合學習研究整理與 NotebookLM 深度研究自動化。
