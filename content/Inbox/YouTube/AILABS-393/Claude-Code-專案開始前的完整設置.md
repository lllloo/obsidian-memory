---
title: Claude Code 專案開始前的完整設置指南
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-10
source: https://www.youtube.com/watch?v=ywIhw15za9Y
parent: "[[01.index]]"
---

## 規劃需求（Plan Requirements）

- 規劃是最重要的前置步驟，無論模型多強都需要花時間
- 不建議用 Claude Code 的 planning mode，因為它太偏技術面，缺乏產品視角
- 建議建立專屬的 **planner agent**，搭配 PRD 模板，持續追問直到完整理解需求
- Planner agent 完成後產出 PRD 文件，存入專案資料夾，包含：所有需求細節、分階段實作計畫、關鍵設計決策

## CLAUDE.md 設置

- 連結 PRD 文件，避免重複說明需求
- 只寫 agent **不知道**的事，不要寫它本來就會的事（如專案結構、框架基礎用法）
- 包含內容：最佳實踐、coding conventions、風格規範
- **不包含**：可從檔案結構自行推導的內容
- 此檔案不是一次設定就好，開發過程中持續補充
- 建議自己手寫，不要用 `claude init` 自動生成（它只反映現有程式碼，不反映真正需求）

## Skills、Agents 與 MCP 設置

在開始實作前全部設置好：

**Agents 配置範例：**
- `planner agent`：規劃 PRD
- `commit agent`：提交、執行 pre-checks、遵守 conventional commit 格式
- `refactoring agent`：重構與優化效能
- `verification agent`：用 Playwright MCP 驗證 UI 和用戶流程

**Skills vs Agents 的分工原則：**
- Skills：可重複執行、需要參考資料的工作流程（如前端開發 skill）
- Agents：需要獨立 context window 的任務

**Path-specific rules：**
- 為特定路徑設置專屬規則（如 `/src/api`、`/src/components`）
- 在 CLAUDE.md 中連結這些規則，讓 agent 知道它們的存在

## Negative Constraints（禁止項目清單）

- Agent 天生偏向行動，正面指示留有隱性空白
- 建立一份禁止項目文件放在 `docs/` 資料夾，並在 CLAUDE.md 連結
- 列出每一項你**不想要** agent 做的事，包含具體細節（如：「不要使用預設的紫色或藍白配色」）

## Progress 與 Learnings 文件

**progress.md：**
- 記錄哪些功能已實作、哪些尚未完成
- 避免 agent 花時間重新讀程式碼來判斷進度

**learnings.md：**
- 記錄錯誤、原因、解決方式
- 讓 agent 在遇到相似問題時不重複犯錯

在 CLAUDE.md 明確指示 agent 在開發過程中持續更新這兩份文件。

## 先寫測試再實作

- 開發完才寫測試會導致測試只針對「已實作的樣子」優化，而非「規格要求的樣子」
- 正確做法：讓 agent 參照 PRD 推導功能應有的行為，從規格反推測試案例
- 不要給開放式指令（「測試這個 app」），要給明確的測試範圍
- 測試完成後在開發結束時執行，交叉驗證實作是否符合需求

## Issue Tracking

- 從一開始就建立問題追蹤機制，避免問題無記錄堆積

**技術團隊：**
- 使用 GitHub Issues + 結構化的 git commit 訊息
- 配置 agent 在每次實作後自動 commit，訊息含足夠細節
- 可用 git worktree 做實驗性測試，降低風險

**非技術成員：**
- 連接 Trello 或 Notion MCP
- 在 CLAUDE.md 指示 agent 使用指定工具記錄 bug 和問題

## 生產環境擴展性準備

- AI 生成的程式碼不天然支援多人並發，需事先規劃
- 告知 agent 預期用戶量，讓它撰寫壓力測試案例（可用 K6 等工具）
- 用 Claude plan mode 規劃多種擴展方案，從多角度澄清潛在問題
- 目標：app 在出現問題時能優雅降級，不至於完全崩潰
