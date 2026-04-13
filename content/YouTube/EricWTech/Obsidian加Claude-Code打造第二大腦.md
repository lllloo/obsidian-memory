---
title: Obsidian + Claude Code 打造真正有效的第二大腦
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-06
source: https://www.youtube.com/watch?v=Y2rpFa43jTo
---

## 重點摘要

- 用 Obsidian + GitHub 實現免費雲端備份與版本控制：安裝 GitHub Desktop，clone repo 後在 Obsidian 開啟為 Vault，使用 Git 社群插件設定自動 commit（每 1 分鐘）與 pull on startup
- 啟用 Obsidian CLI：設定 → General → Advanced → Command Line Interface 開啟，讓 Claude Code 可透過 CLI 操作筆記
- 安裝 Obsidian Skill：透過 marketplace 或 `npx skills` 安裝，賦予 Claude Code 操作 Markdown、Base、JSON、Canvas 的能力
- 建立「onboard projects」Skill：整合 Gmail（OAuth2 憑證）與本地文件，自動在 Obsidian 建立專案資料夾結構，包含 overview、conversation log、links、documents、projects.base
- 專案資料夾結構：
  - `overview.md`：專案概述、tech stack、scope
  - `conversation-log.md`：按時序彙整所有對話紀錄
  - `links.md`：外部連結
  - `documents/`：靜態文件（NDA、合約等，不摘要）
  - `projects.base`：所有專案狀態看板
- 可查詢 Obsidian 筆記讓 Claude Code 回答「目前專案狀態」、「如何草擬回信」等問題，作為 AI 輔助的專案管理中心
