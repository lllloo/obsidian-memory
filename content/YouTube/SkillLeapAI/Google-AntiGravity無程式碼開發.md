---
title: 24 分鐘掌握 Google AntiGravity 80% 核心功能
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-28
source: https://www.youtube.com/watch?v=E9enKu1BFhg
---

## 平台概覽

- AntiGravity 是 Google 推出的桌面 App，支援 Mac 與 PC，目前完全免費（含付費進階方案）
- 定位：同時面向開發者（競爭對手：Cursor、Windsurf）與 vibe coding 新手
- 網址：anti-gravity.google

## 三個主要介面

- **IDE**：傳統程式碼編輯器，適合開發者直接操作或從 GitHub 匯入程式碼
- **Agent Manager**：以自然語言 prompt 建立 app，是本影片重點
- **Chrome 瀏覽器**：在本地執行 app 並自動測試（agent 會自行點擊、填表、驗證功能）

## 初始設定

- 安裝時選擇控制層級：
  - **自動執行（推薦新手）**：agent 完全自主，不詢問確認
  - **手動確認（作者選擇）**：每個重要步驟需批准才繼續

## Agent Manager 工作流程

1. **Playground（原型）**：快速測試想法，不可部署；滿意後可移入 Workspace 成為正式專案
2. **Workspace（正式專案）**：與電腦資料夾連結，所有程式碼儲存在本機，可透過 GitHub 部署
3. 建議開啟「Planning 模式」先查看計畫再執行
4. 可選 AI 模型：Gemini 3 Pro（多種推理等級）、Claude Opus 4.5、GPT OSS（開源）

## 自動生成的 Artifacts

- **Implementation Plan**：專案目標與步驟清單
- **Task Plan**：每個步驟的細節
- **Walkthrough**：完成後的影片示範，展示 app 在瀏覽器中的操作

## 示範案例一：習慣追蹤 App

- Prompt：簡單的習慣追蹤 app，用戶可新增習慣、標記完成，儲存在本機
- AntiGravity 自行開啟瀏覽器測試（點擊、新增習慣、標記完成），全程無需人工介入
- 結果：功能完整，符合 prompt 要求

## 示範案例二：AI 提案生成器（Briefly）

- Prompt 由 Gemini 生成（描述需求後請 Gemini 產出詳細 prompt，直接複製貼入）
- 目的：貼入品牌的粗略 email，自動轉成專業的創作者簡報
- 第一版：基本功能可用，但視覺不夠精緻
- 第二版（追加 prompt 後）：完整 dashboard、歷史頁、核心功能正常
- 評估：AntiGravity 的 vibe coding 體驗約完成 90%，發布流程較技術性

## 部署流程（較技術性）

1. 將本機資料夾上傳至 GitHub（限 100 個檔案/次）
2. 在 Vercel 連接 GitHub repo
3. 按下部署取得公開網址

此流程較複雜，不適合純 vibe coding 新手。

## 替代方案比較

| 工具 | 易用程度 | 發布難度 | 備註 |
|------|---------|---------|------|
| AntiGravity | 中（有 IDE） | 較複雜（需 GitHub） | 適合想保留開發者彈性者 |
| Google AI Studio | 高 | 簡單（內建發布） | 功能較少但更易上手 |
| Lovable | 高（作者最愛） | 簡單 | 功能完整，支援 backend |
| Base 44 / Emergent / Hostinger Horizons | 高 | 簡單 | 各有特色 |

## 市場研究建議

- 使用 Product Hunt 週排行榜尋找有市場的新 app 想法
- 使用 Similar Web 確認目標網站的實際流量、來源管道、廣告投放策略，再決定是否開發

## AntiGravity 的核心優勢

- 適合在公司內部自動化工具（不需要公開部署）
- 整合 IDE，開發者可直接接手做最後 10% 調整
- 本機執行，成本控制佳
