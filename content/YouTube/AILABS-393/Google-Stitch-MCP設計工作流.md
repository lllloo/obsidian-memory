---
title: 現在我這樣用 Google Stitch 設計
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-25
source: https://www.youtube.com/watch?v=VNx9Gy5pHZI
---

## Google Stitch MCP 整合

好的設計不來自依賴單一工具，而是工具與資源的正確組合。Google Stitch（AI 設計工具）現在可作為 MCP 連接 AI agent，讓 agent 能夠建立與管理專案，以及從 text prompt 生成設計。

主要功能：
- 專案管理：建立新專案、取得所有活躍專案
- 透過列出畫面與取得專案和畫面來管理
- 從 text prompt 生成新設計

**安裝說明：**
- 需安裝 Google Cloud SDK，登入兩次（一次作為用戶，一次作為應用程式）
- 需連接 Google Cloud 內的專案並啟用 Stitch API
- 社群也提供非官方的簡化安裝腳本，可自動處理從 Google Cloud 安裝到專案設定的整個流程

## 以 Plan Mode 規劃 UI

無論建構什麼，實作前規劃都是必要步驟。以模擬技術面試 app 為例：

- 使用 Claude Code 的 plan mode 規劃 app，讓它針對每個面向反覆迭代，產出詳細文件
- 特別要求 UI 設計不要看起來像一般的 AI 生成設計
- 仔細閱讀計畫並多次修改，直到完全滿意

設計規劃確定後，讓 Claude 取用剛生成的計畫，透過 Stitch MCP 建立新專案並生成設計。

## 生成設計的注意事項

- Stitch 使用 Gemini 3 Flash 生成設計
- 預設行為：分別為 landing page 的各 section 送獨立 prompt，而非整頁一次生成
- 這可能在整合時造成問題
- 解法：明確要求 Claude 生成一個完整的長頁面設計，保留各 section 的所有想法

生成的設計包含：流暢的 hover 效果、RWD 響應式設計、開發者終端機美學風格。

## 將設計整合到 Next.js 專案

1. 請 Claude 使用 Stitch MCP 取得完整 landing page 的程式碼
2. 系統用 `get screen` 工具取得畫面，回傳可下載的連結
3. Claude 用 `curl` 指令提取程式碼
4. 取得 HTML 後整合到 Next.js 專案

**常見問題**：Claude 可能把所有程式碼都倒進 `page.tsx` 單一檔案，不遵循 React 的元件結構慣例。

**解決方式**：要求 Claude 使用適當的元件結構重構，整理成結構清晰的 UI 元件和頁面集合。

## Vercel Agent Browser 測試

Vercel 推出的 agent browser 已超越 Claude 的 Chrome extension，成為首選的瀏覽器測試工具：

- **CLI 工具**，以 Rust 和 Node.js 建構，速度遠快於傳統瀏覽器自動化工具
- 以**快照**（snapshot，頁面的 accessibility tree）而非截圖運作，附有識別各元件的 selector
- Agent 使用 selector 有效率地導覽頁面
- 不與既有瀏覽器共用 session，在獨立瀏覽器中執行
- 目前僅支援 Chromium 系瀏覽器

**與其他工具的比較：**

| 工具 | 方式 | 速度 |
|------|------|------|
| Claude Chrome extension | 截圖 → 像素對應 → 導覽 | 較慢 |
| Playwright / Puppeteer | headless 瀏覽器 | 中等 |
| Vercel Agent Browser | accessibility tree + selector | 最快 |

**實際測試結果**：4 分鐘完成整個測試流程，識別出程式碼編輯器需要可編輯，立即實作修正並再次截取快照驗證。

在 `CLAUDE.md` 中設定：所有測試一律使用 agent browser 工具，若不熟悉指令則先用 `help` 指令查詢。
