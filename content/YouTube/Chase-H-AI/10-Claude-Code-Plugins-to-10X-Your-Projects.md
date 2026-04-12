---
title: 10 Claude Code Plugins to 10X Your Projects
tags:
  - youtube
  - claude-code
  - plugins
  - tools
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/OFyECKgWXo8
---

精選 10 個 Claude Code 插件與工具，每個提供：使用理由、使用方式、安裝方式、實際案例。

## CLI vs MCP 重要原則

Claude Code 住在終端機，CLI 工具也在終端機，無中間人開銷。**優先選 CLI，而非 MCP**。

## 10 個工具清單

### 1. Supabase CLI（非 MCP）
- **用途**：資料庫（PostgreSQL）+ 用戶認證
- **安裝**：參考 Supabase 官方文件，依作業系統安裝；或直接叫 Claude Code 安裝
- **重點**：有對應的 Claude Code skill，裝完記得安裝 skill
- **注意**：作者本人也曾長期用 Supabase MCP，後來才發現 CLI 更好，提醒大家「即使是專家也會跟不上」

### 2. Skill Creator（最強大）
- **用途**：建立、修改、評估 custom skills；可做 A/B 測試驗證 skill 效果
- **安裝**：`/plugin` → 搜尋 skill-creator → 安裝
- **使用**：`/skill-creator` 或自然語言

### 3. GSD（Get Stuff Done）Framework
- **用途**：spec 驅動開發的 orchestration layer，適合從零開始的新專案
- **特色**：按階段、功能逐步規劃；每個新階段使用新的 context window，防止 context rot
- **安裝**：GitHub 搜尋 GSD / get-done，一行命令安裝
- **使用**：`/gsd new project`

### 4. NotebookLM CLI/Skill
- **用途**：在 Claude Code 終端機中使用 NotebookLM（研究、分析、製作簡報/播客/閃卡）
- **安裝**：從 NotebookLM-API GitHub 安裝依賴，再執行 `notebooklm skill install`
- **特點**：NotebookLM 無官方 API，此工具繞過限制；幾乎免費

### 5. Obsidian
- **用途**：個人助理情境下管理大量 Markdown 筆記，視覺化連結關係
- **安裝**：下載 Obsidian → 建立 vault 資料夾 → 在該資料夾開啟 Claude Code
- **使用**：告訴 Claude Code「建立 Markdown 時遵循 Obsidian 格式」即可，不需 CLI 或 skill

### 6. Vercel CLI
- **用途**：管理部署，與 GitHub CLI 搭配使用
- **安裝**：一行命令；或叫 Claude Code 安裝；記得安裝對應 skill
- **用例**：搭配 agent loop 自動監控部署狀態

### 7. Playwright CLI
- **用途**：瀏覽器自動化（購物、表單填寫、UI 測試）
- **安裝**：從 Playwright CLI GitHub 複製指令安裝；`playwright-cli install-skills`
- **特色**：`playwright-cli show` 指令可顯示視覺化儀表板，即使 headless 模式也能看

### 8. GitHub CLI
- **用途**：從 Claude Code 終端機完整操作 GitHub（commit、PR、issue 等）
- **安裝**：依作業系統安裝，參考官方 GitHub 頁面
- **備注**：Claude Code 對 Git/GitHub 已高度熟悉，基本不需要額外 skill

### 9. Firecrawl CLI
- **用途**：AI 友善的網頁爬取，輸出專為 AI agent 優化
- **安裝**：一行命令，含 skill 安裝
- **四大指令**：scrape、crawl、map、search
- **用例**：競品研究、文件監控、深度研究

### 10. Excalidraw Diagram Skill
- **作者**：Cole Medin（YouTube 知名創作者）
- **用途**：用自然語言讓 Claude Code 生成圖表
- **安裝**：從 GitHub clone repo → 複製到 project skill 目錄
- **用例**：技術架構圖、簡報圖表，完全不需手動操作 Excalidraw
