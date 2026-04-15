---
title: Claude Code vs Lovable：瀏覽器 AI 開發與本地 Terminal 工具的真正差異
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-27
source: https://www.youtube.com/watch?v=wbzFyDJhruc
---

## 核心問題

本地 terminal AI 工具（Cursor、Claude Code）很強大，但有固定開銷：安裝依賴、管理 API key、建立資料庫、設定環境變數、部署到另一個 hosting provider。Lovable 的定位是保留 AI agent 工作流（用英文描述功能、用 AI 迭代），但跳過整個 terminal 設定過程。

## Lovable 實際示範

**初始 Prompt**：「Build a SaaS dashboard with real user authentication, a monthly revenue chart, and a customer management table, all with a database. Use a clean modern UI.」

**幾分鐘後產出：**
- 完整 login/signup 流程
- Revenue chart
- Customer table（已連接資料庫）
- 前後端、資料庫 schema、auth flow 全部在雲端環境中執行
- 本機完全不動

## 核心差異對比

| 面向 | Claude Code（Terminal） | Lovable（Browser） |
|------|----------------------|-------------------|
| 起點 | 本機 repo | 雲端 |
| 環境設定 | 自行處理 | 平台負責 |
| 程式碼所有權 | 完整 | 可 sync 到 GitHub |
| 部署 | 需另外設定 | 點 Publish 即完成 |
| 客製化程度 | 高 | 可拉回本機繼續 |

## 加入 Stripe 訂閱（迭代示範）

輸入 Prompt：「Add a Stripe subscription system with a pricing page. Include a basic monthly and yearly plan.」

Lovable 自動：加入 pricing page、設定 payment flow、建立 backend 邏輯、整合進現有 auth system。過程中會要求輸入 Stripe API key 和確認訂閱設定細節。

## Plan Mode（大型修改前的安全機制）

先詢問方向而非直接套用：例如「What's the best way to structure role-based access?」它會先提出計劃（DB layer、RLS policies 等），用戶確認後再執行。適合不想要意外修改的重大變更。

## 部署流程

只需按 Publish：Lovable 自動處理 hosting、backend、資料庫連線、SSL 設定，並給出 live URL。

## 適用對象

- **非技術創辦人**：從概念到可運作產品，不需後端知識
- **設計師/PM**：不再只是 Figma mockup，可測試真實 auth 和資料儲存
- **開發者**：處理重複性基礎建設（auth、admin dashboard、CRUD、內部工具），專注差異化部分

## 關鍵優勢

GitHub sync 讓你不會被鎖定：可隨時把程式碼拉回本地 editor 繼續用傳統工作流開發。
