---
title: 35 個 Claude Code 概念全解析——非工程師也能懂
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-08
source: https://www.youtube.com/watch?v=UAMAAoSPu8o
---

## 描述

針對非工程師設計的 Claude Code 完整入門指南，涵蓋 35 個核心概念，從基礎安裝到進階 sub-agent 架構，提供清晰的學習路線圖。

## 重點摘要

**Section 1：核心基礎（概念 1–5）**

- **概念 1：Claude.ai vs Claude Code 的差異**
  - 兩者使用相同的 AI 大腦；Claude Code 多了「身體」（可執行工具呼叫、操作電腦）
- **概念 2：安裝**
  - Google 搜尋「Claude Code install」，依作業系統（macOS/Linux/WSL 或 Windows PowerShell）複製對應的單行指令安裝
- **概念 3：在哪裡使用 Claude Code**
  - 選項：原生終端機、VS Code、Claude Code 桌面應用程式、Cursor
  - 建議從終端機（VS Code）開始，體驗最完整的功能
- **概念 4：權限設定**
  - Shift+Tab 切換：預設（每次詢問）→ 自動接受編輯 → 計畫模式
  - `--dangerously-skip-permissions` 旗標可完全略過確認，適合熟練用戶
- **概念 5：Plan Mode**
  - 執行前先規劃步驟並向使用者提問，填補 prompt 的漏洞
  - 取得更好輸出的首要方法

**Section 2：觀念心態與中階技巧（概念 6–？）**

- **概念 6：以協作者心態使用 Claude Code**
  - 不要盲目接受建議，要主動詢問 Claude Code 解釋技術概念
  - Claude Code 是無限耐心的導師，善用它來真正理解底層邏輯

**Section 3：工具箱（Skills、CLI、MCP）**

- **Skills 的本質**：Skills 就是文字 prompt，告訴 Claude Code 以特定方式做特定事情
- **前端設計 Skill**：透過 `/plugin` 市場安裝，解決 Claude Code 前端設計能力不足的問題
- **Skill Marketplace**：官方 plugin 市場，可搜尋並安裝各種 skills
- **Skill Creator Skill**：自訂 skill 並進行 A/B 效能測試
- **呼叫 Skill 的三種方式**：`/skill名稱`、自然語言提及、Claude Code 自動識別情境

**Section 4：進階（Power User）**

- **自訂 slash 指令（Custom Commands）**
  - 可建立多步驟自動化工作流，例如 `/yt-pipeline`（YouTube 研究流程）
  - 可串接多個 sub-skills 與 CLI 工具
- **Hooks**
  - 在特定指令前後觸發動作，例如任務完成時播放聲音、發送 email
  - 建立方式：直接告訴 Claude Code「建立一個任務完成時播放聲音的 hook」
- **Sub-agents 與 Agent 團隊**
  - Claude Code 可自主派生 sub-agents 並行處理任務
  - 每個 sub-agent 擁有獨立的 context window，避免 context rot
