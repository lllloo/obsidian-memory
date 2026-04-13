---
title: "這個 NotebookLM + Claude Code 工作流程強得誇張"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-26
source: https://youtu.be/fV17ZkPBlAc
---

## 影片描述

示範如何結合 NotebookLM 與 Claude Code，透過開源工具 `notebooklm-py` 讓 AI agent 能程式化存取 NotebookLM 的功能，並以競品分析為實際應用案例。

## 重點摘要

### 為什麼結合這兩個工具

- **Claude Code** 擅長執行（execution）：寫程式、呼叫工具、執行指令
- **NotebookLM** 擅長理解（grounded understanding）：將雜亂文件、研究資料整理成結構化知識
- 組合後：先用 NotebookLM 建立知識庫，再將理解結果傳給 Claude Code 執行

### notebooklm-py 工具

- 開源 Python 函式庫，提供完整的 NotebookLM CLI 與 Python API
- 支援的功能：
  - 建立、列出、重新命名、刪除 Notebook
  - 插入來源（網頁、文件等）
  - 擷取問答歷史、設定 persona
  - 切換深度/快速研究模式
  - 下載生成內容（音訊、影片、投影片）
- 安裝：`pip install notebooklm-py[browser-login]`
- 認證：透過瀏覽器 Google 登入，憑證儲存在根目錄

### 整合到 Claude Code 的方式

兩種安裝 Skill 的方式（效果相同）：
1. `notebooklm install-skill`（CLI 方式）
2. `npx <open-skill-ecosystem-command>`（MPX 方式）

安裝後，Claude Code 可透過 Slash 指令或自然語言呼叫 NotebookLM 功能。

### 實際案例：BookZero.ai 競品分析

**架構設計：**
- 35 個 AI 財務競品，分為三個 tier
- Notebook 1：直接競品（Tier 1 + Tier 2），約 250 個來源
- Notebook 2：市場概況（Tier 3），約 136 個來源
- 輸出：競品分析報告（MD）、心智圖、投影片（PPT）

**執行流程：**
1. Tier 1（8 個核心競品）：深度研究（deep queries）
2. Tier 2（40 個競品）：快速查詢（fast queries）
3. Claude Code 自動建立 Notebook、插入來源、執行研究、下載成果

**問答示例：**
- 問：「基於競品分析，BookZero 的賣點是什麼？」
- NotebookLM 回答：超快速 AI 收據提取與比對、三步驟極簡流程（上傳→匯入→比對）
- 產品方向建議：從收據比對延伸至即時帳務對帳與自動化財務洞察

### 其他應用場景

- 技術決策：分析 Jira 票券 + 知識庫，決定功能方向
- 內容行銷：結合 SEO skill 與競品知識庫，生成比較型部落格文章
