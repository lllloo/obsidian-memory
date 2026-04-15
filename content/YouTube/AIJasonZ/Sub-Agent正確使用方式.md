---
title: Sub-Agent 正確使用方式
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-08-14
source: https://www.youtube.com/watch?v=LCYBVpSB0Wo
---

## 為什麼 Sub-Agent 常讓人失望

- 用 sub-agent 直接做實作，而非只做研究
- 每個 sub-agent session 是孤立的，缺乏跨 agent 的上下文共享
- parent agent 看不到 sub-agent 的內部行動，只看到任務摘要

## Sub-Agent 的正確定位

> Sub-agent 最適合「只做研究並回傳精簡摘要」，不應直接執行實作

- 核心價值：將大量 token 消耗（read file、search file）轉移到獨立 thread
- Parent agent 只接收幾百 token 的摘要，而非數千 token 的原始操作記錄

## 設計原則

### 每個 Sub-Agent 的職責

1. 啟動時：讀取 context 檔案（了解整體計畫）
2. 執行：研究、設計實作計畫，**不直接實作**
3. 完成時：
   - 將研究/計畫寫入 `.claude/doc/` 的 MD 檔
   - 更新 context session 檔（記錄已完成事項）
   - 回傳固定格式：「已建立計畫 `<檔名>`，請先讀取再執行」

### 透過檔案系統共享上下文（Manus 風格）

- 每個功能建立一個 `context-session-N.md` 檔案
- 所有 sub-agent 在開始工作前都讀這個檔案
- 避免 sub-agent 把大量 tool result 塞入 conversation history

## 專屬 Sub-Agent 的設計

### Shadcn UI Agent

- 系統提示中內嵌 MCP 工具使用規則
- 流程：列出可用元件 → 選擇適合的 → 取得範例程式碼 → 取得 UI block 參考
- 目標：生成**設計計畫**，不執行實作

### Vercel AI SDK Agent

- 系統提示包含 Vercel AI SDK v5 完整文件（直接從官網複製）
- 包含 v4 到 v5 的遷移指南
- 同樣只輸出計畫，由 parent agent 執行

## 實際流程示範（ChatGPT 複製品）

1. Parent agent 建立 `context-session-1.md`（記錄任務目標）
2. 觸發 Shadcn agent：傳入 context 檔名 + 任務說明
3. Shadcn agent 讀 context → 使用 MCP 搜尋元件 → 輸出 UI 設計計畫
4. Parent agent 讀設計計畫 → 執行實作
5. 觸發 Vercel AI SDK agent：傳入 context 檔名
6. SDK agent 讀 context → 輸出整合計畫
7. Parent agent 執行整合

## 效果

- Parent agent 始終有完整 context，能有效修復問題
- 實作由單一 thread 完成，無 merge conflict 風險
- Sub-agent 降低研究階段的 token 消耗
