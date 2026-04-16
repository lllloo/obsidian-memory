---
title: Pencil.dev AI 設計工作流
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-28
source: https://www.youtube.com/watch?v=sdxJEd7nqiQ
parent: "[[01.index]]"
---

## Pencil.dev 介紹

Pencil.dev 是設計與程式碼之間的雙向橋接工具，連接 Figma 風格設計畫布與 Claude Code、Codex 等 AI 開發工具。設計檔以 `.pen`（JSON-based）格式儲存，可用 git 版本控制。安裝桌面 app 後自動配置 MCP，所有 tools 立即出現在 Claude Code 中。

現實限制：雙向同步並非自動，每次設計修改後需手動 prompt 觸發同步。

## 自動同步腳本

針對反覆手動同步的問題，建立監控 `.pen` 檔案的 script：

- 使用 JavaScript 監控 `.pen` 檔案變更
- 加入 cooldown 防止連續小修改觸發 Claude 重複呼叫
- 儲存時自動呼叫 Claude CLI 並帶入同步 prompt
- 執行方式：`npm run sync`

前置條件：在 `.claude/settings.json` 預設所有需要的 read/write 與 MCP tool call 權限，否則 Claude 會卡在權限提示無法繼續。

## 多 Agent 平行實作

搭配 Claude Code 多 agent 系統平行處理多頁面：

- 每個 agent 負責一個頁面
- 共用 PRD 與 UI guide 等 context 文件確保一致性
- 五頁網站由五個 agents 同時建立
- 完成後按下 Cmd+S，自動同步腳本接手實作

## GSAP 動畫整合

使用 XML 結構化 prompt 加入捲動動畫（Claude 模型針對 XML 優化，解析更準確）：

- Prompt 包含：任務描述、所有依賴、每個 section 的具體動畫行為
- GSAP 控制「捲動時發生什麼」
- Lenis 控制「捲動本身的手感」（平滑捲動 library）
- 兩者互補：Lenis 讓 GSAP 動畫觸發更自然

## UX Audit Skill

建立 UX 稽核 skill，包含：

- 九點 UX checklist 評分
- Python scripts 程式化偵測人眼難以發現的問題
- 多個 phase：收集 context → 分析 → 報告
- 提供具體修改清單並直接實作

實際效果：網站評分從 C 提升至 B，確保 WCAG 無障礙合規。
