---
title: Claude Code + NotebookLM 整合：用 AI Agent 做競品研究與知識庫查詢
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-26
source: https://www.youtube.com/watch?v=fV17ZkPBlAc
---

## 核心概念

- **Claude Code**：擅長執行（execution）
- **NotebookLM**：擅長將雜亂文件、研究資料轉化為有條理的知識庫
- **notebooklm-py**：開源函式庫，將 NotebookLM 包裝成 CLI，讓 AI agent 可程式化呼叫

## 安裝與設定

```bash
# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate

# 安裝（含瀏覽器登入支援）
pip install notebooklm-py[browser]

# 驗證安裝
notebooklm --version

# 首次登入（開啟瀏覽器用 Google 帳號認證）
notebooklm login --browser
# 認證後 credentials 存於 root directory
```

## CLI 功能

- 建立/列出/重新命名/刪除 notebook
- 插入來源（最多 300 個/本 notebook）
- 提取問答、對話歷史
- 設定 persona
- 設定研究模式（deep / fast）
- 下載生成物（音訊、影片、投影片）

## 安裝 NotebookLM Skill 到 Claude Code

```bash
# 方法 1：CLI 安裝（安裝到 root directory，所有專案可用）
notebooklm install-skill

# 方法 2：open skill ecosystem
npx notebooklm install-skill
```

安裝後在 Claude Code 中用 `/` slash command 或自然語言呼叫 NotebookLM skills。

## 實際案例：35 個競品深度分析

**目標**：為 BookZero.ai 分析 AI 財務競品市場，輸出報告 + 心智圖 + 投影片。

**架構設計**：
- Notebook 1（直接競品）：深度研究 8 個核心競品（deep queries × 8）+ 快速研究 40 個二線競品（fast queries × 10）= ~250 個來源
- Notebook 2（市場概覽）：快速研究 17 個競品 = ~136 個來源

**輸出**：5 個可下載檔案（PPT、MD、JSON）存於 `docs/marketing-comparative-analysis/`

## 應用場景

**產品開發決策**：
基於競品研究回答「下一步該聚焦什麼」，結合 Jira tickets 和現有程式碼庫，生成具體產品方向建議。

**內容行銷**：
整合競品知識庫 + SEO skill，自動生成比較型部落格文章。

**查詢示範**：
「Based on the BookZero product, what is our selling point, how is it unique, and what should we focus on for product vision?」

→ NotebookLM 查閱 300+ 來源後回答：核心賣點是超快速高準確度收據提取；建議聚焦從收據配對擴展到即時帳務對帳，提供自動化財務洞察。

## 設定回應格式

在 NotebookLM 設定中調整 configuration（如選 "learning guide" 模式 + 保持簡短），避免冗長回應。
