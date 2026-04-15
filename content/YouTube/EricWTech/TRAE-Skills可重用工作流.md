---
title: TRAE Skills：Cursor 沒有的遊戲規則改變者
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-09
source: https://www.youtube.com/watch?v=5CeLK6N0F4k
---

## 什麼是 TRAE

一個兼具傳統 IDE 和 AI 助理的編碼工具，兩種模式可隨時切換：

- **IDE mode**：像一般 IDE — 編輯檔案、執行指令、管理版本控制、debug
- **Solo mode**：AI 主導 — 描述功能或工作流，Solo 規劃步驟、生成程式碼、執行測試、準備部署

## Skills 核心概念

TRAE 最大差異化特色。大多數 AI 編碼工具很強，但**會忘記你的標準**。每個新專案都要重複輸入：資料夾結構、命名規則、測試 pattern、API 格式。

Skills 把這些重複的指示和工作流封裝成**可重用的 building blocks**，跨專案和 agent 使用。

## 建立 Skill

兩種方式：
1. **手動定義**：直接撰寫指示
2. **AI 互動式**：展示你的工作方式，讓 AI 從中學習建立

範例：永遠以特定方式建立 React component → 建立一個 skill，之後每次生成 component 都完全符合你的風格，不需要每次試錯。

## Skills 的三個層次

Skills 可以組合使用：

| 情境 | 組合方式 |
|------|----------|
| 全端 App | backend API skill + frontend component skill + testing skill |
| Dashboard | API scaffold skill + UI card skill + validation logic skill |
| 文件 | README skill + API doc skill + usage guide skill |

組合後，TRAE 以一致的方式執行整個工作流，節省數小時重複工作。

## Skills 與 Agents 整合

TRAE agents 是針對特定任務的 AI 助理，skills 與 agents 整合後：
- 一個 agent 執行 skill 生成程式碼
- 另一個 agent 執行 skill 測試
- 第三個 agent 執行 skill 寫文件

Agents 感知專案 context，skills 可以在沒有重複解釋的情況下順暢執行。

## IDE / Solo 模式中的 Skills

- **IDE mode 中**：作為智能助理，建議程式碼並執行工作流，但你保持控制
- **Solo mode 中**：讓 AI 自主處理複雜專案，不需要持續監督

Q（TRAE 的程式碼預測功能）與 skills 搭配使用，能預測多行編輯、跨專案更新引用、自動加 import。

## 團隊優勢

- Skills 確保一致性：所有開發者生成相同風格的程式碼
- 降低心理負擔：只需觸發 skill，TRAE 處理細節
- 可共享：整個團隊使用同一套 skills，新人上手更快
- 框架改變時，更新 skill 一次，套用到所有未來專案

## 注意事項

- Skills 的品質取決於你定義的指示品質
- 不要建立太多超細節的 skills，會讓工作空間雜亂
- 最佳做法：建立模組化、可重用的 skills，視需要組合
