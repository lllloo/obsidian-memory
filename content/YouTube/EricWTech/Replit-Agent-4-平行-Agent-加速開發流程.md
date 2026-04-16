---
title: Replit Agent 4 平行 Agent 能否加速你的開發框架
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-13
source: https://www.youtube.com/watch?v=TdJwBiv3zS0
parent: "[[01.index]]"
---

## 核心定位

Replit Agent 4 是「**創意優先**」的建構 agent，不是單純的程式碼生成工具。

核心主張：多數 AI coding 工具只擅長工作流的一個環節——設計在一個工具、程式碼在另一個、文件又在別處。Agent 4 嘗試把這些全部放在同一個環境。

## 四大主軸

### 1. Design Freely（自由設計）

- **無限畫布**：可生成多個 UI 方向並排比較，選定後套用回 app
- **視覺編輯器**（canvas + live preview 雙模式）：直接點擊介面修改文字、間距、顏色、版面、圖片
  - 簡單修改 → source code 直接更新
  - 複雜變更 → 交給 agent 處理
- 解決設計到程式碼的來回循環（Figma → code → feedback → 再實作），全部留在同一個地方

### 2. Move Faster（更快推進）

- **Path System**：大任務自動拆成離散子任務，可視化追蹤每個任務狀態（計劃中 / 執行中 / 待審查 / 完成）
- **平行執行**（Pro 方案）：各任務跑在獨立 thread
  - Thread A：後端工作
  - Thread B：前端修改
  - Thread C：設計路徑探索
  - 完成後 review 並 merge 回主專案
- 對 Pro 方案使用者：大幅壓縮 build 時間

### 3. Ship Anything（任何產品都能發）

同一個專案可建構多種 artifact：
- Web app、Mobile app（透過 Expo Go 預覽）
- 投影片、數據應用、動畫

**連接外部服務：** Notion、Slack、BigQuery、Linear — agent 可讀取這些工具的 context 並對它們執行操作（建立 ticket、回答文件問題、處理外部資料）。

**General Agent：** 無需預先設定技術棧，從自然語言出發，agent 自動處理環境設定。

### 4. Build Together（協作開發）

- 多人可在同一個專案內建立各自的 thread，互不干擾
- Core 方案：任務依序執行；Pro 方案：任務平行執行
- 設計師、PM、工程師可同時推進，agent 在背景處理協調工作

## 對現有 Replit 用戶的改變

- **Stack Selector 退場**：不需要預先選技術棧，直接描述想要什麼
- **General Agent** 取代原本的結構化設定流程（planning + building 合而為一）
- 現有專案可直接導入 Agent 4，不需遷移

## 核心論點

Agent 4 不是「更快的程式碼生成」，而是**壓縮設計→規劃→實作→測試→發布之間的摩擦**：
- 減少工具切換
- 讓工作流程可視化（知道 agent 在做什麼）
- 保持人在迴圈中（你決定方向，agent 處理執行細節）

作者評價：Agent 3 主打自主性，Agent 4 主打**創意控制**——你在重要的地方保持參與，系統負責重複性的協調工作。

