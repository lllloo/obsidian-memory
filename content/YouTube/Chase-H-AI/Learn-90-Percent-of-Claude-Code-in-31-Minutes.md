---
title: Learn 90% of Claude Code in 31 Minutes
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/TwkdDcO4vWQ
---

針對初學者（尤其是非技術背景）的 Claude Code 完整入門指南，涵蓋安裝、使用方式、核心概念到部署，去除過時建議（如 CLAUDE.md、MCPs）。

## 章節結構

### 安裝與使用方式

- 安裝：Google「Claude Code install」，依作業系統執行對應指令（Windows 用 PowerShell）
- 四種使用方式，從「最多控制」到「最簡單」的光譜：
  1. **Terminal**（CLI）：最多控制，最接近 Claude Code 原生體驗
  2. **IDE 內建 Terminal**（VS Code / Cursor / Antigravity）：免費，兼顧控制與可視化；可看到檔案結構
  3. **Claude Code Desktop App**：類似 terminal 但更美觀
  4. **Co-work**：最簡單，但犧牲部分控制權
- 建議大多數人從 VS Code + terminal 開始

### 權限設定

- 預設模式：每次 shell 指令都會詢問確認
- `--dangerously-skip-permissions`：給予 Claude Code 完整電腦存取權，適合熟悉用戶
- 可透過 Shift+Tab 切換不同權限層級

### 提示技巧

- 盡量在初始 prompt 中給出完整需求，減少來回
- 使用截圖輔助視覺描述
- Plan mode 先規劃再執行

### Skills（技能）

- Skills 本質上是「大型文字 prompt」，告訴 Claude Code 如何以特定方式執行任務
- 安裝方式：`/plugin` 開啟插件庫，搜尋並安裝（官方 Anthropic 技能如 frontend-design）
- 呼叫方式（兩種）：
  1. `/<skill-name> <prompt>`：100% 觸發
  2. 自然語言：Claude Code 自動判斷是否需要調用相關 skill
- 技能要明確「呼叫」才會使用，不會自動持續運行

### Context Window 管理

- 越接近 context 上限，輸出品質越差（context rot）
- 超過 20-25% 就應執行 `/clear` 重置
- 搭配狀態列監控 context 使用率

### CLI 工具（取代 MCP）

- CLIs 是現在的趨勢，MCPs 正在被取代
- CLI 工具直接在 terminal 運行，與 Claude Code 同環境，token 開銷低、效率高
- 典型範例：
  - **Supabase CLI**：建立資料庫、身份驗證，無需手動操作 UI
  - **Playwright CLI**：瀏覽器自動化測試，可視化（headed）或背景（headless）執行
- CLI 工具通常在 GitHub 開源，內含安裝指令與配套 skills
- 安裝方式：直接貼 GitHub URL 給 Claude Code，讓它自行安裝

### 部署

- 兩步驟：codebase → GitHub → Vercel（均免費）
- GitHub 儲存程式碼，Vercel 部署上線

## 重點建議

- 不需要 CLAUDE.md（對初學者弊大於利）
- 不需要 MCPs（改用 CLI）
- 不需要記住所有指令，用自然語言即可
