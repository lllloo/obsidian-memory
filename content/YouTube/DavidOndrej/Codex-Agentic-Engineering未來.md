---
title: Codex 是 Agentic Engineering 的未來
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-16
source: https://www.youtube.com/watch?v=nUxuCoqJzlA
---

## 概覽

- OpenAI 將最強模型 GPT-5.3 Codex 打包成 Codex App，這也是 Peter Steinberger 用來建構 OpenClaw 的模型。
- 本影片示範如何使用新版 Codex App、比較其與 Opus 4.6 的差異，並從零打造一個開源專案。

## Codex App 基本設定

- 前往 openai.com/codex 下載 Mac OS 版本，可用現有 ChatGPT 帳號登入。
- App 特色：不是完整 IDE，但有終端機、Chat 界面與右側檔案差異視圖。
- 可切換模型：
  - **GPT-5.3 Codex**（主力模型）
  - **Spark**（Cerebras 晶片驅動，約 1000 tokens/sec，速度極快但能力略弱）
- 推理力選項：Low、Medium、High、Extra High，一般使用 Medium 即可；難題才切換 High 或 Extra High。

## 多執行緒並行開發（Threads）

- Codex App 的核心功能：同時管理多個 AI Agent，每個負責不同任務。
- 一個 Agent 跑幾十分鐘也沒問題，直接再開新執行緒。
- 結合 **Git Worktrees** 可讓多個 Agent 在同一專案的不同分支上並行工作，互不干擾。
- 預設支援非常低的授權摩擦，可設定 Auto Accept Policy 讓 Agent 自動執行指令。

## 實作：Open Dash 開源專案

### 專案願景

- 建立一個中央協作儀表板，讓團隊成員和 AI Agent 都能透過 Skills 推送與拉取 Markdown 檔案。
- 解決問題：目前沒有乾淨的方式讓人類與 AI 同時使用、共享 prompt 模板與文件。

### 開發流程

1. 建立 `spec.md` 描述專案架構與功能。
2. 建立 GitHub 公開 repo（MIT 授權），讓任何人都能使用。
3. 使用 Codex 建立 Next.js + Supabase 後端。
4. 同時開啟多個 Thread：主 Agent 建後端，前端 Agent 改 UI，另一 Agent 修 bug。
5. 使用截圖作為上下文：在 Codex 中直接貼上 Supabase 設定截圖，讓 Agent 判斷選項。
6. 每 10–15 分鐘 commit 一次——使用 AI 開發時的好習慣。

### 技術棧

- 前端：Next.js（自動生成）
- 資料庫：Supabase（PostgreSQL + Row Level Security）
- 身份驗證：Supabase Auth
- 模型：GPT-5.3 Codex + Spark（快速前端修改）

### UI 演進

- 第一版：基本功能可用，但 UI 簡陋。
- 加入 Slack 風格工作區設計（深炭黑色）。
- 引入「資料夾」概念取代「部門」，支援新增、重新命名、刪除。
- Markdown 渲染、檔案上傳、搜尋功能逐步完善。
- 去除多餘的側欄元件，精簡布局。

## 關鍵開發技巧

- **提示中使用 XML 標籤**：讓 AI 更清楚不同段落的邊界，例如 `<build_idea>...</build_idea>`。
- **截圖作為 context**：直接截圖 Supabase 設定頁面貼入 Codex，精準引導 AI。
- **訊息佇列（Queued Messages）**：可在 Agent 回應前預先送出下一條指令，自動排隊執行。
- **善用 rate limit 檢視器**：在 Codex 左側查看剩餘配額（$200/月方案幾乎不會達到上限）。

## Opus 4.6 vs GPT-5.3 Codex 比較

- **GPT-5.3 Codex 優勢**：
  - 除錯能力更強，更不懶惰
  - Spark 模式速度極快（適合小型前端修改）
  - 多執行緒協作體驗更流暢
- **Opus 4.6 優勢**：
  - 複雜架構設計更有深度
  - 長 context 理解更穩定
  - 解釋能力更佳

## 結語

- 2026 年只要有點子並能用英文描述，就能建出任何軟體。
- Codex App 讓多 Agent 並行開發成為日常工作流，而不只是實驗性功能。
- 該開源專案（Open Dash）已上傳 GitHub，歡迎任何人使用或貢獻。
