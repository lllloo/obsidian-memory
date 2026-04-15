---
title: Claude Code 入門完整指南
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-19
source: https://www.youtube.com/watch?v=WCuwYLVE6j8
---

## 什麼是 Claude Code

- 不是聊天機器人，是「AI 建構器」：能在電腦上建立與編輯檔案
- 支援建立網站、app、內部工具、資料視覺化儀表板、自動化流程
- 無需寫程式，只需用英文 prompt 指令
- 內建 vibe coding，但比其他 vibe coding 工具更直接來自源頭（Anthropic）

## 安裝方式

- **桌面 App**（推薦）：Mac / Windows 均可，同時包含 Claude Chat 與 Co-work
- VS Code 擴充：適合進階用戶，可看到資料夾結構與程式碼
- 網頁版：類似 claude.ai 聊天介面操作
- 需要 Pro Plan（$17/月年繳）以上才能使用 Claude Code 與 Co-work

## 基本操作流程

1. 為每個專案建立獨立資料夾，選擇「Select Folder」
2. 選擇模型：複雜任務用 Opus；修改與迭代用 Sonnet
3. 設定 permission 模式：Auto Accept（推薦）或 Plan Mode（先產生計畫再執行）
4. 輸入 prompt，Claude Code 自動撰寫程式並測試輸出
5. 用 Preview 預覽結果，選取特定元素做局部修改

## Prompt 結構（5 要素）

1. **要建什麼** — 網站、app、工具
2. **給誰用** — 目標受眾
3. **要做什麼** — 核心功能
4. **長什麼樣** — 設計風格、參考截圖
5. **下一步改什麼** — 迭代修改方向

## CLAUDE.md 業務上下文

- 在專案資料夾放 `CLAUDE.md`（Markdown 格式文字檔），給 Claude Code 業務背景
- 建立方式：用 ChatGPT / Gemini 訪談自己的業務後匯出文件，或讓 Claude 訪談後產生
- 每個專案可有各自的 CLAUDE.md，也可放在帳戶層級跨專案共用

## Skills 與 MCPs

- **Skills**：Markdown 格式自訂指令，可安裝至專案或帳戶層級；社群市集有現成 skills 可複製貼上
- **Plugins**：Anthropic 官方現成工作流，如 frontend-design（提升 UI/UX 品質）
- **Connectors**：串接 Slack、Google Drive、Figma 等，讓 Claude Code 取得外部資料

## 發布上線流程

1. Customize → Connectors 連接 GitHub（需先有帳號）
2. 要求 Claude Code 推送至 GitHub → 取得 repo 連結
3. 至 vercel.com → 貼上 GitHub 連結 → Deploy → 取得公開網址

## 迭代原則

- 第一個 prompt 不需完美，預期需要多次迭代
- 用 Preview 右上角選取元素功能，針對局部修改
- 複雜任務或第一次 prompt 用 Opus；後續修改換 Sonnet 省 credits
- Plan Mode 適合不確定輸出方向時使用
