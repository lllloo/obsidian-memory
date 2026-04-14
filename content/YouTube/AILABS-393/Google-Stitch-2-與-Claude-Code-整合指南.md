---
title: Google Stitch 2.0 與 Claude Code 的 4 種整合方式
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: 2026-03-28
source: https://www.youtube.com/watch?v=b0lwCDNOFUY
---

## 核心問題：AI 設計過於相似

- 所有模型訓練資料相近，導致 AI 生成的設計收斂到相同風格
- Claude 也需要特殊 prompt 才能避免這個問題
- Google Stitch 是專為設計打造的工具，可直接接入 Claude Code 工作流程

## 方式一：Design System 與 design.md 檔案

**design.md 的作用：**
- 記錄完整設計系統：顏色、主題、字型等
- 可在不同 agent 之間轉移設計風格
- Stitch 2.0 在每次建構前自動產出 design.md，即使沒有明確要求

**自訂 design.md 的步驟：**
1. 從 Google 官方 Stitch skills repo 取得 design.md 模板（針對 Stitch 優化的結構）
2. 在任意 agent 中提供想要的網站風格 + 模板，讓 agent 生成 design.md
3. 將 design.md 貼入 Stitch 的「建立新設計系統」的 design.md 欄位
4. 點儲存後 Stitch 自動視覺化設計系統
5. 基於這個設計系統持續建立多個頁面，保持風格一致性

**匯出既有 Stitch 專案的 design.md：**
- 使用 Google 提供的 design.md skill，自動轉換現有 Stitch 專案成標準 design.md

## 方式二：Redesign Feature（從既有網站借用設計語言）

**與舊做法的差異：**
- 舊做法：提供截圖 → AI 複製整個設計
- 新做法：提供截圖 → Stitch 提取設計語言和元件排版邏輯，應用到自己的網站

**操作步驟：**
1. 用 GoFullPage 等擴充功能截取目標網站的完整頁面截圖
2. 上傳給 Stitch，選擇 redesign 功能
3. Stitch 提取設計模式，生成相似但原創的 UI

**其他匯入方式：**
- 提供網址 → Stitch 爬取網站，提取設計系統生成 design.md
- 上傳手繪草稿或線框圖 + 指定設計主題 → Stitch 精確匹配視覺風格
- 用標注工具修改不滿意的部分

## 方式三：Claude Code + Stitch Skills 自動化工作流程

Google 提供多個 Stitch skills 可安裝：

**Enhanced Prompt Skill（最重要）：**
- 將模糊 prompt 轉換成 Stitch 優化的 prompt
- Stitch 用形容詞識別設計情境，此 skill 含關鍵詞參考

**Stitch Loop Skill：**
- 用自主循環模式從 Stitch 迭代建構完整網站
- 整合 Chrome DevTools，維護 prompt 追蹤，在各階段間傳遞

**前置需求：**
- 必須先連接 Stitch MCP（Stitch 在底層使用此 MCP 建構和取得設計）

**完整自動化流程（在 CLAUDE.md 中定義）：**
```
1. Enhanced Prompt Skill → 將原始 prompt 優化成 Stitch 格式
2. 取得用戶確認
3. Stitch Loop Skill → 透過 Stitch MCP 建立專案、生成設計系統、生成設計
4. React Component Skill → 將 Stitch 輸出的 HTML 轉換成模組化 React 元件
```

## 方式四：搭配 UI Library（Shadcn UI）

**為什麼要用 UI Library：**
- 純 React 元件太靜態，缺乏互動效果和動畫
- UI library 內建互動功能，讓 UI 更生動

**Shadcn UI Skill（Google 提供）：**
- 指導 agent 將 Stitch 設計轉換成 Shadcn 元件
- 支援連接多個 component registry（如 glassmorphism、motion primitives 等）

**設置步驟：**
1. 提前安裝 Shadcn MCP
2. 在 CLAUDE.md 加入指示：使用 Stitch MCP 時自動觸發 Shadcn skill 進行元件轉換
3. 在 CLAUDE.md 中列出要使用的 registry（依專案選擇）

**執行後：**
- 指定 Stitch 專案名稱
- Agent 自動 fetch 設計、載入 Shadcn skill、透過 MCP 和 registry 實作完整 app
- 結果：外觀與 Stitch 設計完全一致，但元件具備豐富的互動效果

## React Component Skill

- 用途：將 Stitch 匯出的龐大 HTML 檔案轉換成模組化元件結構
- 問題背景：Stitch 匯出的 HTML 是一個大檔案，對 React 專案是負擔
- 使用腳本驗證和 fetch 設計，讓元件可以清楚對應
