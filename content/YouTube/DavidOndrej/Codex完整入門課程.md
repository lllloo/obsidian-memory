---
title: Codex 完整入門課程：從零到部署
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-04-11
source: https://www.youtube.com/watch?v=hoCWD1aI60Y
---

## 安裝與設定

- 一行指令完成 Codex 安裝
- 需先安裝 Node.js（若缺少會有錯誤提示）
- 帳號驗證流程：訂閱方案選擇（影響可用模型）
- 啟動方式：在特定專案資料夾下執行 Codex CLI

## Agents.md 系統提示設定

- 在專案根目錄建立 `agents.md` 作為系統提示文件
- 此文件定義 AI 的行為規則、專案脈絡與限制
- 作者的 agents.md 範本：gist.github.com/davidondrej

## 模型與效能設定

- 可在 CLI 中切換不同 AI 模型（包含 Google Nano Banana 2）
- Reasoning Effort 設定影響回應品質與速度
- Fast Mode 可將速度提升約兩倍
- YOLO Mode：自動核准所有操作權限，適合信任度高的任務

## 實際開發流程

- 用圖片輸入提供 UI 設計稿作為上下文（提升準確度）
- Web Search Tool：讓 Codex 在開發時自動搜尋最新文件
- One-Shot MVP：一次提示生成完整 Web App 骨架
- 安裝 Cursor IDE 整合 Codex VS Code Extension

## Git 與版本控制

- 內建 GitHub 整合，支援 commit/push 工作流
- 進階 Debugging 與 Prompt Engineering 技巧

## 部署

- 部署到 Vercel：完整操作示範
- Sandbox Mode 與 Approval Policy 設定說明

## Codex Desktop App 進階功能

- Multi-Agent 管理介面
- Skills 與 Plugins 擴充
- Cron Jobs：排程自動化任務
- Sub-Agents（Worker）派遣機制
