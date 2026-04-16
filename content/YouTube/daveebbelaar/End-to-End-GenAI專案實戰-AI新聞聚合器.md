---
title: 完整 End-to-End GenAI 專案實戰：AI 新聞聚合器
tags:
  - youtube
  - rag
created: 2026-04-13
updated: 2026-04-13
published: 2025-11-15
source: https://www.youtube.com/watch?v=E8zpgNPx8jE
parent: "[[01.index]]"
---

## 專案概覽：AI 新聞聚合器

目標：每天自動寄送一封 email，內含依使用者興趣排序的最新 AI 新聞。

資料來源：
- YouTube 頻道（YouTube Transcript API）
- OpenAI 部落格（RSS feed）
- Anthropic 部落格（第三方 RSS 轉換服務）

技術棧：
- Python + FastAPI
- SQLAlchemy + Docker Compose（PostgreSQL）
- OpenAI Responses API（GPT-5.1）
- Pydantic 資料模型
- Render 部署（Blueprint 方式）

## 開發工作流程與 AI 輔助編碼

作者的開發哲學：
- 先做腦力激盪（speech-to-text 語音輸入），再用 AI 規劃架構
- 使用 Cursor + Claude Code 混合模式（agent mode 建構功能，chat 模式討論設計）
- 先讓系統跑起來、看到具體結果，再逐步完善（不從資料庫模型開始，先建 scraper）
- 遇到問題立即 debug，不要等到最後

## 各模組架構

### Scraper 層

**YouTube Scraper**
- 使用 YouTube 內部 Transcript API 取得影片字幕
- 注意：大量抓取時可能被 YouTube 暫時 IP 封鎖（解法：付費代理服務，約 4-5 USD/月）

**OpenAI Scraper**
- 使用 OpenAI 官方 RSS feed 直接解析，比網頁爬蟲簡單得多

**Anthropic Scraper**
- Anthropic 無官方 RSS，使用第三方 [Old Shanks 的 RSS 轉換 repo](https://github.com/)
- 整合三個 feed：news、engineering、research
- 原本使用 `defuddle` 解析 HTML，因記憶體過大改為輕量 Rust 實作的 `html-to-markdown` 套件

優化：三個 scraper 共用 80% 的 RSS 解析邏輯，後期重構為 `BaseScraper` 基類。

### 資料庫層

```yaml
# docker-compose.yml 結構
services:
  db:
    image: postgres
  app:
    build: .
    depends_on: [db]
```

- SQLAlchemy ORM 定義資料模型
- Repository pattern（每個操作一個函數）
- 環境變數管理：`.env.example` 範本，加入 `.gitignore` 防止 commit 機密

### Pipeline 執行流程

```
daily_runner.py
├── 1. 執行所有 scraper → 儲存文章至 DB
├── 2. 處理文章為 Markdown 格式
├── 3. 產生每篇文章摘要（digest agent）
├── 4. 聚合 Agent 依使用者 profile 排序文章
└── 5. Email Agent 發送每日彙整信
```

### Aggregator Agent（排序）

- 輸入：過去 24 小時的文章摘要 + 使用者 profile
- 使用者 profile：描述興趣、背景（儲存在專案中的設定檔）
- 輸出：有評分與排序的文章清單（Pydantic 模型）
- 使用 OpenAI Responses API + structured output

### Email Agent

- 使用 Python 內建 `smtplib` 搭配 Gmail SMTP（最簡方案，不需付費服務）
- 格式：HTML email，包含個人化問候、排序後的文章清單

## 部署（Render）

使用 **Blueprint** 方式一鍵部署：
1. Render 介面 → New Blueprint → 連接 GitHub repo
2. 設定環境變數（API keys、DB URL、Gmail 帳密）
3. 設定 Cron Job：每天固定時間執行 `daily_runner.py`

遇到的部署問題：
- `defuddle` 套件過重（含本地 OCR 模型），超出 Render 免費方案記憶體限制
- 解法：改用 `html-to-markdown`（Rust 實作，輕量）

## 重複項目去重

問題：24 小時視窗可能有重疊，同一篇文章被寄送兩次。

解法：在資料庫中記錄已寄送的 digest items，每次執行前先查詢排除。

## 開發心得

- 先讓東西跑起來，再重構（例如先用醜陋的 dict，後期改為型別安全的 Pydantic）
- 理解底層流程很重要，才能給 AI coding agent 精準指令（如：「我要 Docker Compose + SQLAlchemy，放在 docker/ 資料夾」）
- 早期就接入追蹤工具（如 Langfuse）以便觀察 agent 行為
- 避免把 `.env` commit 進版本控制（使用完整的 `.gitignore`）
