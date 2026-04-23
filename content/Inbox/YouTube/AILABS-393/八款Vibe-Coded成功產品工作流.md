---
title: 八款 Vibe Coded 成功產品的共通工作流
created: 2026-04-22
updated: 2026-04-22
source: https://www.youtube.com/watch?v=zNOunnM1jTs
published: 2026-04-20
parent: "[[01.index]]"
tags:
  - youtube
  - ai-coding
  - vibe-coding
  - indie-hacker
  - product-building
---

## 影片核心觀點

AI 讓不會寫程式的人也能做出年營收百萬美金的產品，這些團隊的工作流其實不特別，只是更簡單、更聰明：
- 不是靠單一工具 all-in，而是**為每個任務挑最擅長的模型**
- 不是一次要 AI 把整個 app 寫出來，而是**拆成小塊逐步迭代**
- 不是從零打造所有元件，而是**把依賴當服務用**（外包藥局、諮詢、金流等）
- 真正的技能是**判斷力**：做什麼、用什麼工具組合、何時停手

## 案例一：Medvy（醫療平台）

- 創辦人 Matthew Gallagher 無程式背景，獨自用 AI 工具端到端打造
- 首年營收 $401M，本年有望達獨角獸（billion-dollar）估值
- 活躍用戶超過 500,000
- 工具組合（按強項分工）：
  - **Claude / Grok**：主力 coding
  - **ChatGPT**：次要 debugging
  - **Midjourney**：圖片生成
  - **Eleven Labs**：語音通話（完全取代人工客服）
- 關鍵策略：**所有依賴當服務用**，不自建藥局與物流，外包專業諮詢
- 教訓：獨自經營有風險，曾在他外出時 production 掛掉、一小時流失 200 名客戶；後來聘兩名工程師當 safety net，而非 scale

## 案例二：Cal AI（AI 卡路里追蹤）

- 兩名高中生打造（後擴編）
- 8 個月破 500 萬下載，單月營收超過 $2M
- 30% 留存率（遠勝多數 app），App Store / Play Store 雙平台 4.8 分
- 產品差異化：
  - 傳入食物照片即自動換算卡路里並更新資料庫，取代手動輸入
  - 依賴大型開源食物資料庫，搭配 Anthropic 與 OpenAI 模型，準確度約 90%
- 成長主要靠 **fitness 影響者推廣**，而非廣告投放

## 案例三：Wave AI（AI 會議筆記）

- 創辦人完全非開發者，獨自完成
- 營收約 $7M
- 市場已擁擠，但仍脫穎而出因為解決了真實痛點：會議中重要細節容易漏掉
- 推出順序：iOS → Android → 全平台
- 工作流：
  - 主要工具是 **ChatGPT**
  - **不要 AI 一次把整個 app 寫出來**，而是把應用拆成小塊逐一產生
  - 基礎設施大量用 third-party，專注在 UX

## 案例四：Flypedia（瀏覽器飛行模擬器）

- 起初只是 hobby project，後來月營收達 $500,000
- 被 Elon Musk 親自 endorse，撐過網路攻擊
- 建置速度：**Cursor 3 小時完成 80%**，首版 30 分鐘就上線
- 迭代工作流：
  - 第一個 prompt 開始 → 觀察產出 → 下一個 prompt 補 feature 或修 bug
  - 每次迭代只加一個功能或修一個問題
- 多人連線的故事：
  - 單人模式沒問題，多人連線卡關
  - Beta List 創辦人幫忙加 WebRTC，但只適用兩人
  - **Cursor 創辦人親自聯絡**，改用 WebSockets 才真正解決 real-time multiplayer
- 商業模式：免費版 + $29 特定飛機
- Stack：Cursor + Grok 3（後端模型）+ Claude Sonnet 3.7 + ChatGPT（debug）

## 案例五：TrendFeed（內容創作者行銷工具）

- 4 週營收約 $12,000，launch 當天賺 £5,500
- 創辦人非技術背景
- 建置流程：
  1. 仔細分析 UI 並做深度競品研究（用 AI 拆解競品）
  2. 用 Cursor 或 Claude 設計 data structure / schema
  3. 從 design 開始、搭核心結構、onboarding、主框架、重複 design patterns
  4. 拆成 modular components 讓 AI 分別建置再合併
- Stack：Next.js、React、Shadcn、Supabase、Vercel（AI 工具最熟的組合）
- 行銷零預算，全靠 TikTok、Instagram、YouTube
- 工具組合：Claude Code + Cursor（Sonnet 為主模型）

## 案例六：Aura（設計 template 站）

- 創辦人 Meng To 獨自完成
- 單月 MRR $15,000，一個月累積 21,700 名用戶
- 核心觀點：
  - 「不只要 vibe code，還要 **vibe design**」，否則 AI 只會產出基礎 UI
  - 給 AI 引導性 template，搭配現有 library（如 21.dev）提升設計多樣性
  - **不只用單一模型**：先用 Claude（coding 最強），失敗再切 Gemini 或 GPT
  - 採漸進式 incremental changes，把 app 拆成小塊迭代
  - **Prompt 保持在三句以內**，讓 AI 保持專注
  - 不要把所有文件塞給 AI，**只給最小但正確的 context**
- 已從 Figma 轉到 Cursor 做設計

## 案例七：Sleek（prompt 轉網站）

- 6 週達 MRR $10,000
- 行銷零支出
- 成功關鍵：**Day 1 就定義清楚 ICP（Ideal Customer Profile）**
  - 知道目標客群是誰，就能針對性打造產品
  - 「建 app 時先定義 ICP，才是讓成功 app 和僅止於 impressive 的 app 的分水嶺」
- 非從零開始：把團隊過往做過的設計工具重新組合成這個產品
- Stack：Next.js + Supabase + Vercel
- 獲客管道：X 平台 algorithm + early access 發佈

## 案例八：Sideshore（AI 引用驗證）

- 解決 AI agent 常幻覺出不存在的引用、citation、來源的問題
- 使用者輸入 citation，系統驗證其真實性
- MRR 約 $10,000，後被 **Jenny AI 收購**（同領域平台）
- 證明「解決一個簡單但關鍵的問題」就能變成有價值的產品

## 共通 Pattern 總結

### 工具與模型選用
- 多模型分工：Claude / Grok 做 coding、ChatGPT 做 debug、Midjourney 出圖、Eleven Labs 出聲
- 模型優先順序建議：Claude 優先 → 失敗再切 Gemini / GPT
- 技術棧偏好：Next.js + Supabase + Vercel + Shadcn + React（AI 最熟悉的組合）

### Prompt 工程原則
- Prompt 控制在三句內
- 最小但正確的 context，不要把整份文件塞進去
- 把 app 拆成小 module，一次只建一塊

### 產品策略
- 先定 ICP（ideal customer profile）再動工
- 依賴當服務用，不要從零建 everything
- 模組化設計，重複 design patterns 讓 AI 易於擴展
- 影響者 / 社群媒體（TikTok、Instagram、YouTube、X）是零預算獲客關鍵

### 獨立經營的風險
- 一人運營存在 outage 風險（Medvy 一小時流失 200 名客戶）
- 聘人不是為了 scale，而是當 safety net
