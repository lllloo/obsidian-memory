---
title: Anthropic 設計主管談 AI 時代的新開發流程
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: ""
source: https://www.youtube.com/watch?v=X4vAlWtsJD4
parent: "[[01.index]]"
---

## 舊流程為什麼存在

Anthropic Claude 設計主管 Jenny Wen（前 Figma 設計總監）在 Lenny's Podcast 訪談中指出：

舊流程（需求 → Figma 設計稿 → 前端實作 → 後端平行開發 → 整合）的每個步驟，都是為了降低「走錯方向」的代價。因為在沒有 AI 的時代，一個方向錯誤代表數個月的工程時間浪費，所以需要研究、personas、wireframe、spec 等每一道保護。

## 什麼改變了

- **工程速度先改變**：多個 agent 平行執行，瓶頸從工程轉移到設計
- 設計師花在 mockup 和 prototype 的時間從 60-70% 降到 30-40%
- **Vision 時間軸縮短**：從 2-5 年縮短到 3-6 個月，交付物從 deck 變成可互動的 prototype
- **Figma 翻譯層消失**：agent 直接從需求文件生成可執行的前端，不再需要 Figma 作中間橋接

## 新流程：從需求到可運作 Prototype

### Step 1：定義 PRD（用訪談式 prompt）

重點：PRD 不包含技術規格，只需要足以讓人點頭說「對，就是這個」的資訊。

訪談過程聚焦三個問題：

**Actors（使用者角色）**
- 定義與系統互動的具體人物與目標
- 不同 actor = 不同介面與第一個畫面
- 範例：「提交內容者」和「審核者」是兩套不同介面

**View 分岔點**
- 找出同一個 URL 下不同 actor 看到完全不同東西的位置
- Admin 看管理面板，一般用戶看個人 dashboard

**Constraints（限制條件）**
- 告訴 agent 什麼不能做、成本上限是多少
- 不要告訴 agent 用什麼技術棧（讓 constraints 引導技術選型）

### Step 2：生成前端架構

用「layer prompt」讓 agent 讀取 PRD，產出：

- **Pages + Modals 清單**：所有需要實作的頁面和彈窗
- **User Flows**：每個 actor 的操作路徑、互動狀態、導覽邏輯

結果：`architecture.md`，包含 pages、modals 和 user flows。

### Step 3：實作前端 Prototype

```bash
# 用 Next.js + Supabase 快速建立框架
# 使用 Anthropic 提供的 general-purpose frontend skill 提升 UI 品質
# 建議存成 slash command 或 skill，讓 agent 使用
```

Prototype 特性：
- 使用 mock data，不接 database
- 功能完整呈現（導覽、互動狀態）
- 可以直接給客戶看、取得 yes/no 回饋
- 修改成本極低（幾分鐘 vs 舊流程的幾天）

`architecture.md` 讓 agent 能建立精確的 task list，避免幻覺。

### Step 4：API Spec + Backend

確認 Prototype 被批准後：

1. 讓 agent 讀取前端程式碼 + PRD + architecture.md，**寫出 API spec**
2. 用 API spec + Supabase MCP 自動建立 schema、執行 migration

```
# 用 Supabase MCP 省去手動設定步驟
# MCP 自動建立專案、執行 SQL、跑 migration，不需要手動貼 query
```

3. 前端直接與 database 溝通（Next.js + Supabase 整合）
4. 需要進階功能時（付款、通知、rate limiting、analytics）才建立獨立後端 API layer

### 何時需要獨立後端

- 需要 Python 獨有的 library
- 需要複雜的背景任務編排
- 一般情況下 Next.js 後端已足夠

## 關鍵結論

需求分析仍然重要——跳過這步直接到 spec 是錯誤的。

AI 改變的不是需求的重要性，而是讓走錯方向的代價極度降低，因此可以更快進入可見的 prototype 來驗證需求是否正確。
