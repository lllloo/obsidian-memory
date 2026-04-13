---
title: "Claude Code vs Lovable：沒人說破的真正差異"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-27
source: https://youtu.be/wbzFyDJhruc
---

## 影片描述

從零開始用 Lovable 建立全端應用程式，對比 Lovable 與 Claude Code 等終端機型 AI 工具的本質差異，並說明各自適用的場景。

## 重點摘要

### Lovable 是什麼

- 瀏覽器中的 AI 全端開發平台（[lovable.dev](https://lovable.dev)）
- 輸入一段自然語言描述，自動生成前端、後端、資料庫、認證、部署一套完整應用
- 整個流程在 Lovable 的雲端環境中運行，本機完全不需設定

### 實際示範流程

1. 用一段 prompt 描述需求（SaaS dashboard + 認證 + 月收益圖表 + 客戶管理表）
2. 等待幾分鐘，取得可互動的預覽頁面
3. 可直接在瀏覽器中閱覽並修改生成的程式碼
4. 連接 GitHub 後可持續 push 並切換到本地 VS Code 繼續開發
5. 用 chat 追加功能（例如：新增 Stripe 訂閱系統與定價頁面）
6. 點擊「Publish」即完成部署，附帶 HTTPS

### 與 Claude Code 的關鍵差異

| 面向 | Lovable | Claude Code |
|------|---------|-------------|
| 環境設定 | 全部在雲端自動處理 | 需在本機安裝相依套件、設定環境變數 |
| 部署 | 一鍵部署，SSL 已配置 | 需另外設定 Vercel、AWS 等 |
| 程式碼所有權 | 可同步到 GitHub 取回完整程式碼 | 原本就在本地 repo |
| 適合對象 | 非技術創辦人、設計師、快速原型驗證 | 有技術背景的開發者 |

### 適合使用 Lovable 的情境

- 非技術背景創辦人驗證 MVP 想法
- 設計師或 PM 需要可互動 demo 而非靜態 Figma
- 開發者想跳過重複性的 boilerplate 工作（認證、CRUD、管理介面）
- 需要快速從想法到上線 URL 的工作流程

### Plan Mode

- 對於較大的變更，可先用 plan mode 讓 AI 提出修改方案
- 確認後才執行，避免意外變更
