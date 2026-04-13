---
title: 十大 Claude Code 技能、外掛與 CLI 工具（2026 年 4 月）
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-09
source: https://www.youtube.com/watch?v=KjEFy5wjFQg
---

## 描述

2026 年 4 月推薦的 10 個 Claude Code skills、plugins 與 CLI 工具，從程式碼審查到瀏覽器自動化一應俱全。

## 重點摘要

**1. Codex Plugin**
- 將 OpenAI Codex 接入 Claude Code，專門用於程式碼 review 與對抗式審查（adversarial review）
- 指令：`codeex adversarial review`、`codeex rescue`
- 需要 OpenAI 帳號（ChatGPT 付費方案即可）

**2. Obsidian + Obsidian Skills**
- Obsidian 作為 markdown 組織工具，與 Claude Code 結合成輕量 RAG 系統
- 由 Obsidian CEO 提供的官方 skills，教 Claude Code 如何最佳化使用 Obsidian
- 適合大型且持續成長的 markdown 文件庫

**3. Auto Research**
- 自動化機器學習實驗工具，持續優化目標程式或 skill
- 自動拋棄不進步的變更、提交有改善的變更，無需人工介入

**4. Awesome Design（awesome.design.md）**
- 參考 Google Stitch 設計理念，將熱門網站轉為設計 markdown 模板
- 提供按鈕、顏色、字型等完整前端設計規格，解決 Claude Code 前端設計能力不足的問題
- 釋出首週已達 38,000 stars

**5. Firecrawl CLI + Skill**
- 支援繞過反爬蟲防護的網頁抓取工具，回傳 LLM 友好的結構化格式
- 有付費 API 版（完整防爬功能）與免費開源版兩種選項

**6. Playwright CLI**
- 最新版 Playwright，比 Playwright MCP 更有效且更便宜
- 透過可及性樹（accessibility tree）操作網頁，而非截圖，速度與準確度更高
- 可讓 Claude Code 自動開啟 Chrome 實例並執行測試、表單送出等操作

**7. NotebookLM Pine CLI + Skill**
- 透過 CLI 讓 Claude Code 連接 NotebookLM（本身無 API）
- 可批次下載、修改投影片、完整文字存取、程式化分享等
- Google 伺服器負責分析，大幅節省 Claude Code token 消耗

**8. Skill Creator Skill**
- 官方 plugin，可建立、測試、優化自訂 skills
- 內建 A/B 測試與效能基準，提供量化數據判斷 skill 改善幅度

**9. LightRAG**
- 開源 Graph RAG 系統，適合超過 Obsidian 規模時使用
- 比 Microsoft GraphRAG 輕量且免費，適合大型客戶專案

**10. GWS（Google Workspace CLI）**
- 由 Google 團隊開發，連接 Claude Code 與 Gmail、Docs、Calendar
- 提供大量預建工作流 skills（重新排程會議、整理雲端硬碟等）
- 初始設定需透過 Google Cloud 開啟相關權限，較繁瑣
