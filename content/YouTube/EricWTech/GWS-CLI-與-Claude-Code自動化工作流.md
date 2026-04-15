---
title: 用 Google GWS CLI 與 Claude Code 自動化工作流程
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-13
source: https://www.youtube.com/watch?v=P-PA4YSX-qQ
---

## 什麼是 GWS CLI

Google Workspace CLI，讓 AI agent 可以直接操作 Gmail、Google Drive、Google Sheets、Google Calendar 等 Google 工具。搭配 Claude Code 可以自動化日常工作流程。

## 安裝

```bash
npm install -g @google/gws-cli
gws version  # 驗證安裝
```

需要 Node.js 環境。

## Google Cloud 設定步驟

1. 前往 Google Cloud Console → 建立新專案（如 `gws-cli-project`）
2. API & Services → OAuth consent screen → Get Started，填入 App 名稱與 support email
3. Audience 設定後 → Publish App（避免每 7 天重新驗證）
4. Credentials → Create Credentials → OAuth Client ID → Desktop Application → 下載 JSON
5. 將下載的檔案重新命名為 `client_secret.json`，放到指定目錄：
   - macOS：`~/.gws/client_secret.json`
   - Windows：對應路徑
6. 啟用所需的 Google APIs：Gmail API、Google Drive API、Google Calendar API、Google Sheets API

## 認證登入

```bash
gws login
```

複製輸出的 URL 到瀏覽器 → 授權 OAuth scope → 認證成功後測試：

```bash
gws drive list --limit 2
```

## Skills 系統

GWS CLI 有 100+ 個 agent skills，結構分三層：

| 層級 | 說明 | 範例 |
|------|------|------|
| Helper Skills | 最小單元操作 | 發送郵件、回覆郵件、轉發 |
| Service Skills | 整合同一服務的 helpers | Gmail skill（含所有郵件操作）|
| Persona Skills | 多個 Service skills 組合 | Executive Assistant、Project Manager |

安裝全部 skills：
```bash
npx skill install --all
```

安裝單一 skill：
```bash
npx skill add <skill-name>
```

用 Claude Code 安裝特定 persona 的完整 skill stack（自動識別依賴關係）：提供 persona 連結與 skills index URL，讓 Claude Code 在 plan mode 分析並安裝所有相關 service skill 和 helper skill。

## Model Armor（安全防護層）

GWS CLI 整合 Google Cloud Model Armor，在 AI 處理前掃描內容，防止：
- Prompt injection
- Jailbreak 嘗試
- 敏感資料洩漏

設定步驟：
1. Google Cloud Console → 搜尋「Model Armor API」→ Enable（需啟用 Billing）
2. 免費額度：2M tokens/月，超出後 $0.1/1M tokens
3. 用 Claude Code 建立 template：`create a model armor template with jailbreak presets`，提供 project ID、location（如 `us-central1`）、template ID

4. 設定環境變數讓所有 GWS 指令自動通過 Model Armor：
   - Warn mode：標記但不阻擋
   - Block mode：完全阻擋不安全內容

## 實際案例：YouTube 贊助商郵件 Pipeline

連接 Gmail + Google Sheets，自動處理贊助商來信：

**子操作：**
- `analyze`：理解郵件內容，用 Model Armor 掃描安全性，用 Firecrawl 爬取相關資訊，輸出 deal context 物件
- `draft response`：依郵件模板草擬回覆
- `sync to spreadsheet`：將對話資料同步到 Google Sheets

**主操作：**
- `process_one_email`：處理單封郵件 → 分析 → 加星標 → 移至標籤 → 草擬回覆 → 更新 Sheets
- `sync_all`：掃描指定 label（如 inbox）中所有郵件，批次執行完整流程，輸出摘要報告

執行方式：在 Claude Code 中使用自訂 slash command，如 `/yt-sponsor-pipeline sync-all`，選擇要處理的 Gmail label。
