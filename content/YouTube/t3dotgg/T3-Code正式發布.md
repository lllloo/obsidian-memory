---
title: T3 Code 正式發布
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-06
source: https://www.youtube.com/watch?v=hDn8-fK3XaU
---

## 什麼是 T3 Code

- 開源的 agentic coding 桌面應用 + web app，由 Theo 與 Julius 建造
- 靈感來自 Codeex app，但修正了效能問題、工作樹實作不足、以及被鎖定在單一模型的問題
- 完全免費開源，目前 alpha 版

## 核心設計理念：不建自己的 harness

- 直接呼叫各 lab 的官方 CLI（Codex CLI、Claude Code、Cursor CLI 等）
- 不自建 agent harness，因為 lab 的 harness 有大量迭代，模型在自己的 harness 中表現最好
- 使用者已有的訂閱（Codex、Claude Code 等）在 T3 Code 內直接可用
- 對比：Open Code 等工具建了自己的 harness，讓 T3 Code 更靈活

## 主要功能

- **多執行緒並行**：可在同一專案跑多個 agent 執行緒，也可多專案並行
- **Work tree 工作流**：每個執行緒在獨立 work tree 中執行，互不干擾
- **一鍵 PR**：點按即可 commit、push、建立 PR
- **Command Shift O**：切換到另一個 work tree 繼續其他任務
- **Command J**：開啟該 work tree 的 terminal

## 技術選擇

- 桌面應用採用 **Electron**（反對聲音很多，但 Theo 認為效能實際測試是最好的）
- 也可用 `npx t3@alpha` 不安裝直接跑 web 版本

## 版本狀態

- 目前 alpha，優先補齊與現有工具的功能差距，不損耗效能
- **暫不接受 PR**，但歡迎提 issue 並附上建議 prompt 和截圖
- 將陸續支援：Claude Code、Cursor、Open Code、Gemini、遠端執行（Mac Mini / 雲端）
- 支援 Windows（含 WSL）、macOS、Linux（目前 AppImage）

## Julius 的貢獻

- Theo 最初是用好奇心和對效能問題的挫折感開始建這個工具
- Julius 接手後短時間內達到「用 T3 Code 建 T3 Code」的程度
- Macroscope 顯示 Julius 某週被計算出 1,200+ 小時的 coding 時間
