---
title: Claude Code 開工前 SOP
created: 2026-04-24
updated: 2026-04-24
tags:
  - claude-code
  - workflow
  - planning
---

Claude Code 專案最重要的前置步驟——**規劃**，無論模型多強都需要花時間。

**不建議直接用 Claude Code 內建的 plan mode 開工**：它偏技術面、缺乏產品視角。改用 planner agent + PRD 模板，以下是完整流程。

## 推薦流程

1. **Planner agent + PRD 模板**：建立專屬 planner agent，持續追問直到完整理解需求；產出 PRD 含所有需求細節、分階段實作計畫、關鍵設計決策
2. **文件四件組**（放專案根或 `docs/`）：
   - `PRD.md`：需求與範圍
   - `architecture.md`：資料格式、檔案結構、API 設計
   - `decision.md`：所有決策記錄，供後續回溯
   - `feature.json`：token-efficient 的功能清單，含完成標準與 `passes` 追蹤欄位
3. **CLAUDE.md 寫法**（細節見 [[Context-Engineering]]）：連結 PRD、只寫 agent **不知道**的事、不要 `claude init` 自動生成
4. **Skills / Agents / MCP 在開工前全部設置好**
   - Skills：可重複執行、需要參考資料的工作流
   - Agents：需要獨立 context window 的任務
   - Path-specific rules：為 `src/api`、`src/components` 等特定路徑設專屬規則
5. **Negative constraints 清單**：放 `docs/` 並在 CLAUDE.md 連結，列出具體禁止事項（「不要使用預設紫色或藍白配色」），彌補 agent 正面指示留下的隱性空白
6. **`progress.md` + `learnings.md` 持續更新**
   - `progress.md`：功能完成度，避免 agent 重讀整個 codebase 判斷進度
   - `learnings.md`：錯誤、原因、解法，避免重複踩坑
7. **先寫測試再實作**：參照 PRD 反推測試，給明確測試範圍（不要「測試這個 app」這種開放式指令）
8. **Issue tracking 從第一天建**：技術團隊用 GitHub Issues + conventional commit；非技術成員接 Trello / Notion MCP
9. **生產擴展性**：告知 agent 預期用戶量、撰寫壓測（K6 等）、規劃優雅降級

## Plan Mode 搭配四要素（若仍要用內建 plan mode）

1. **目標導向**：說「為什麼建這個」，不只「建什麼」
2. **提供範例**：截圖或 GitHub repo 連結優於文字描述（截圖可直接拖入）
3. **開放性問題**：「這領域的專家會問什麼？」「我沒想到什麼？」「有什麼非預期後果？」——逼出 plan mode 預設之外的深度思考
4. **技術選擇不要跳過**：看到不懂的選項要問到理解為止；不需會寫程式，但需理解軟體工程基本概念

## 相關主題

- [[Claude-Code-效率技巧與設定]] — 開工完成後的日常操作技巧與 Hub MOC
- [[Context-Engineering]] — CLAUDE.md 精簡原則與 context 管理策略
- [[Claude-Code-Skills]] — Skills 機制與建立方式
