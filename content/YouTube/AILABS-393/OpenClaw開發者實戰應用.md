---
title: OpenClaw 開發者實戰應用
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-22
source: https://www.youtube.com/watch?v=hp7n45JqvIw
parent: "[[01.index]]"
---

## 依賴管理自動化

建立 dependency maintenance cron job，每 12 小時執行：

- 檢查 repo 依賴與安全漏洞
- 執行 lock file refresh（更新至最新穩定版）
- 回報需要人工處理的項目（linting、testing）到 Discord
- 通過後自動 push patch 到 GitHub

## 每日技術研究報告

在 Mac Mini 上架設 OpenClaw 作為內部伺服器，建立 cron job：

- 每天自動研究指定來源的新工具與 releases
- 提供多個影片角度切入點與說明
- 包含各新聞的來源連結
- 結果彙整至 Discord 專屬頻道，供團隊每日 briefing

## API 費用監控

建立 API cost watchdog skill：

- 監控 cloud provider CLI 工具回報的 API 使用量
- 使用量異常（如過去 60 分鐘翻倍）時發送 Discord/WhatsApp 警報
- 提供立即可執行的降低費用建議

## 已部署應用監控

**Uptime + 安全 heartbeat：**
- 監控網站 uptime 與 response time
- 掃描 server logs 檢查 XSS、SQL injection
- 定期傳送健康報告到 Discord
- 提供安全強化建議（如加入 security headers）

**SEO heartbeat：**
- 定期檢查 indexability、robots.txt、sitemap 可達性
- 回報 SEO 問題與修復建議

## 完整應用自主開發

提供 PRD，讓 OpenClaw 全程自主處理：

- 結合 Codex 與 Gemini 3 各自優勢
- 自動建立 app、push 到 GitHub、部署到 Vercel
- 回傳部署連結與執行摘要

注意：OpenClaw 無法自行回應 Claude Code 的權限提示，需在 `.claude/settings.json` 預設權限，或使用 `--dangerously-skip-permissions` flag。

## Claude Code + Nano Banana 圖片整合

OpenClaw 協調 Claude Code（實作）與 NanoBananaPro skill（AI 圖片生成）：

- Claude Code 提供 prompts 與檔案名稱
- Nano Banana 平行生成多張圖片放入 public 目錄
- Claude Code 自動偵測並整合圖片到網站

## 冷郵件外展自動化

每天早上 9:00 自動：

- 從 GitHub trending 頁面爬取目標用戶資料（公開 email）
- 儲存到 documents 資料夾
- 依指定風格（輕鬆對話、soft CTA）產生草稿存入 Gmail（不自動發送）

整合方式：使用 `gog` CLI（OpenClaw 內建），從 Google Cloud Console 取得 API credentials。

## 遠端存取 Claude Code

出門在外透過 WhatsApp/Discord 讓 OpenClaw 遠端執行 Claude Code：

- 指定目錄讓 OpenClaw 開啟 Claude Code
- 預設必要權限或使用 `--dangerously-skip-permissions`
- 可遠端 push 變更、review PR、修復 production 錯誤
