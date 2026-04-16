---
title: 十個讓 Claude Code 如虎添翼的 CLI 工具
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 
source: https://www.youtube.com/watch?v=uULvhQrKB_c
parent: "[[01.index]]"
---

## 為何 CLI 優於 MCP

CLI 工具和 Claude Code 同樣住在 terminal，無額外 overhead，token 消耗更低、效能更高。這是整個 Claude Code 生態系的大趨勢。

## 十個推薦工具

### 1. CLI Anything（HKUST）
Meta 工具：把任何開源專案轉換成 CLI 工具。
- 兩步安裝，一步執行，自動完成分析、測試、文件、發布
- 已驗證：Blender、Inkscape、OBS、Zoom、Notebook LM
- 適用於任何有開源程式碼但沒有 API 的程式

### 2. NotebookLM-PY
讓 Claude Code 透過 terminal 操控 Notebook LM（沒有官方 API）：
- 直接丟 YouTube URL 進 Notebook LM 做分析（tokens 跑在 Google 伺服器）
- 輸出 Notebook LM 所有功能：podcast、slide、infographic、quiz、flashcard
- 需安裝 CLI 工具 + 配套技能（repo 內有一鍵安裝指令）

### 3. Stripe CLI
簡化 Stripe 商品與支付設定流程：
- 略過繁瑣的 Stripe 界面，讓 Claude Code 直接處理商品建立與設定
- 實際付款仍需手動確認測試

### 4. FFmpeg
音訊、影片、字幕操控工具集：
- 切割影片為個別幀（用於滾動動畫）
- 複製影片並反轉後拼接成無縫循環
- 讓 Claude Code 有處理多媒體的能力

### 5. GitHub CLI
最常用的部署工具，幾乎所有程式專案都需要：
- Claude Code 已熟悉 Git 操作，安裝後一句話即可 commit、push、管理 branch
- 安裝指令：直接告訴 Claude Code「幫我安裝 GitHub CLI」

### 6. Vercel CLI
配合 GitHub CLI 建立 CI/CD pipeline：
- 讓 Claude Code 從 terminal 直接控制部署
- Vercel 官方技能頁面有豐富的相關技能可安裝（含瀏覽器自動化、UI 設計等）

### 7. Supabase CLI
後端資料庫與認證一站式管理：
- 開源，可完全本地運行
- 讓 Claude Code 直接建立資料庫結構、設定認證，無需進入 Supabase 界面
- 免費方案慷慨

### 8. Playwright CLI
瀏覽器自動化，讓 Claude Code 啟動 Chrome 實例：
- 自動設計並執行 web app 測試
- `--headed` 模式可視覺化看到瀏覽器操作過程
- 比 Playwright MCP Server 節省約 90,000 tokens（同等任務）
- 安裝包含配套技能，一行指令自動存入 `.claude` 資料夾

### 9. LLMFit
判斷本地機器最適合跑哪個 Ollama 模型：
- Ollama 模型選項繁多且更新頻繁，此工具一鍵分析硬體給出建議

### 10. Google Workspace CLI（GWS）
讓 Claude Code 控制整個 Google 套件（Gmail、Docs、Sheets、Drive）：
- 可沙箱化：只開放特定資料夾或使用 Gmail filter 限制存取範圍
- Google Model Armor 提供 prompt injection 防護
- 技能數量龐大，建議讓 Claude Code clone 此 repo 後先討論哪些技能適合自己

## 安裝通用方法

多數 CLI 工具都適用：
1. 複製 GitHub repo URL
2. 貼入 Claude Code，說「照這個安裝 [工具名] CLI」
3. Claude Code 會自動執行安裝指令，並完成認證流程
