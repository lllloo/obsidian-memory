---
title: /routines 徹底改變 Claude Code 排程任務的方式
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-04-14
source: https://www.youtube.com/watch?v=Hd4Ck1BS4Kw
parent: "[[01.index]]"
---

## 什麼是 Routines

Anthropic 為 Claude Code 新增的排程任務功能，讓 Claude 能在雲端自動執行任務，不再受限於 session-based 的迴圈或排程，也不需要電腦保持開啟。

三種觸發方式：
- **Schedule**：固定排程（如每天早上 9:00 執行 cron job）
- **API call**：按需觸發（on demand）
- **Event-based**：事件驅動（如 GitHub repo 的特定事件）

限制：
- Max plan 用戶每 24 小時最多 15 次執行
- 適合單一使用者的小規模自動化，非大量批次（如 N8N 的數百個自動化）

## 設定方式

**透過 Claude Code CLI：**
```
/schedule
```

**透過 Claude Code 桌面應用：**
左側選單 → Scheduled → New Task → New Remote Task

建立任務需填寫：
- 任務名稱
- 任務說明（prompt）
- 連結的 GitHub repository（執行結果會推送到此）
- 雲端環境（Ultra plan 用戶通常已自動建立）
- 觸發方式（排程 / API / GitHub 事件）

**前置條件：**
- GitHub 整合需在 claude.ai 的 Settings → Connectors 完成授權
- 使用 GitHub webhook 時需安裝 Claude GitHub App

## 實際範例

每天自動抓取 GitHub 上 AI 領域熱門 repo：
- Top 10（過去 7 天）
- Top 5（過去 30 天）
- 附帶 AI 分析的 editor's take

執行後 Claude 會將 Markdown 報告推送至指定 GitHub repo，可在執行頁面即時觀看進度。

## API 與 GitHub 事件觸發

- **API trigger**：只能透過 Web UI 設定（`claude.ai/code/routines`），CLI 不支援
- **GitHub event trigger**：同樣只能透過 Web UI 設定
- Claude Code Docs 有完整支援的 GitHub 事件清單

## 使用建議

- 使用 Claude Code（另一個 session）幫你撰寫 routines 的 prompt，結構更完整
- 模型選 Sonnet 即可，不需要 Opus
- 每日配額有限（15 次），需規劃好 API trigger 的使用頻率
