---
title: Claude 全功能總覽
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-27
source: https://www.youtube.com/watch?v=AxRprCFZBU8
---

## 免費功能

- **claude.ai 聊天介面**：Opus / Sonnet / Haiku 三種模型，免費版有用量限制
- **模型選擇**：Opus 最強但最耗 credits；Sonnet 適合日常；Haiku 最快速
- **網路搜尋**：預設開啟，可手動關閉；能取得即時資訊並附來源連結
- **文件與圖片分析**：上傳 PDF、圖片、試算表；可摘要、分析、重製成互動圖表
- **Artifacts**：無需寫程式即可建立互動圖表、小型 app、生產力工具；可發布分享連結
- **寫作輔助**：語氣自然不機械，有時提供多版草稿；可直接匯出至 Gmail

## 進階設定（免費可用）

- **Styles（寫作風格）**：內建 concise / learning 等預設；可上傳個人寫作樣本建立自訂風格
- **Projects（專案）**：將多個對話組織成資料夾；可設定專屬指令、上傳參考文件、設定專案層級記憶
- **Connectors（連接器）**：可接 Google Drive、Gmail、Google Calendar、Asana、Gamma 等；Teams Plan 可共享專案
- **Memory（記憶）**：帳戶層級跨對話記憶，可從 ChatGPT / Gemini 匯入記憶；設定路徑：Settings → Privacy → Memory preference

## 付費功能（Pro $20/月起）

- **Claude Opus**：最強編程能力，適合複雜任務與第一次 prompt 建構
- **Extended Thinking**：開啟後模型在背景推理，解題更深入；建議搭配 Opus 使用
- **Claude Co-work**：指定電腦上的資料夾，給任務後自動建立多份檔案（品牌指南、競品分析、行銷活動素材、整個網站等）；比聊天模式更像「執行者」
- **Claude Code**：建立完整網站或 app，使用 Opus 在指定資料夾寫程式；可結合 CLAUDE.md 給予業務上下文
- **Computer Use**（Max Plan）：可代替使用者在電腦上執行操作，超出資料夾範圍

## Skills 與 Plugins

- **Skills**：Markdown 格式的自訂指令集，擴充 Claude 的特定能力（例如 brainstorming、前端設計）；可從社群市集複製後貼入 Claude Code 安裝，分專案或帳戶層級啟用
- **Plugins**：類似 Skills 的現成工作流，Anthropic 官方提供（如 frontend-design）；與 Skills 互補使用

## 部署與發布

- **GitHub 整合**：在 Customize → Connectors 連接 GitHub，要求 Claude Code 將專案推送至 repo
- **Vercel 部署**：貼上 GitHub 連結至 vercel.com，一鍵部署成公開網址
- **VS Code 擴充**：安裝 Claude Code extension，可在 IDE 內查看資料夾結構並使用 Claude Code
