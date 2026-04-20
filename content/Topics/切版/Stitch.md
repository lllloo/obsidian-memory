---
title: Google Stitch
created: 2026-04-20
updated: 2026-04-20
tags:
  - design
  - claude-code
  - mcp
---

> Google 推出的免費 AI 設計工具，由 Gemini 3 系列驅動，專為解決 Claude Code 前端設計「AI slop」問題而設計，並提供與 Claude Code 工作流深度整合的多種路徑。

## 為什麼需要 Stitch

Claude Code 在 agentic coding 表現卓越，但前端設計是弱項：所有模型訓練資料相近，AI 生成的設計收斂到相同風格（俗稱 AI slop）。Claude 本身也需特殊 prompt 才能避免這個問題。

Stitch 2.0 的核心價值：

- 專為設計打造的工具，可直接接入 Claude Code 工作流程
- 提供無限畫布，快速看到多個 prototype
- 可一次生成 2–3–4 個設計變體並比較
- 完全免費，Stitch 端不消耗 Claude token
- 最終可將設計匯出為程式碼交給 Claude Code 實作

市場反應：Stitch 2.0（2026-03-18 / 19 發布）推出當日 Figma 股價下跌約 8–8.8%（CNBC 單日報導最高達 12%），次日再跌 4%。

## 核心特性

### 模型與生成方式

| 項目 | 說明 |
|------|------|
| 可選模型（官方） | Gemini 3.0 Pro / 3.0 Flash / 2.5 Pro / 2.5 Flash |
| Pro vs Flash | Pro 品質較高，Flash 迭代較快 |
| MCP 場景 | 底層使用 Gemini 3 Flash 生成 |
| 預設行為 | landing page 各 section 送獨立 prompt 生成（整合時可能斷層） |
| 解法 | 明確要求生成一個完整長頁面，保留各 section 想法 |

> 註：部分 YouTube 轉述稱「Gemini 3.1 Pro」，官方目前並無 3.1，實為 Gemini 3.0 Pro。

### Design System（`DESIGN.md`）

Stitch 2.0 每次建構前自動產出 `DESIGN.md`（官方大寫），無需明確要求。內容包含：

- 主色、副色、中性色
- 字型、按鈕、搜尋列等元件規範
- 創意方向（具體說明如何避免 AI slop）

**用途**：可在不同 agent 間轉移設計風格，是跨專案維持一致性的核心檔案。AI agent（如 Claude Code）讀取 `DESIGN.md` 以產生風格一致的 UI。

## 基本工作流（入門）

**步驟一：找靈感**

- [Dribbble](https://dribbble.com/)（三個 B）
- [godly.website](https://godly.website/)
- Pinterest（搜尋 `landing page design` 效果佳）

**步驟二：在 Stitch 生成**

1. 前往 Stitch（Google 搜尋「Google Stitch」）
2. 選擇 Web App
3. 選擇模型（推薦 Gemini 3.1 Pro）
4. 上傳截圖或貼入網址作為靈感
5. 給出提示，例如：`Create a landing page for my AI agency in the style of the screenshot`

**步驟三：迭代**

| 操作 | 方式 |
|------|------|
| 重新生成 | 右鍵 → Regenerate |
| 變體探索 | 右鍵 → Variants（layout / color scheme / images 等維度） |
| 個別元件編輯 | 點鉛筆圖示 |
| 即時對話修改 | Live mode — Stitch 即時觀看螢幕，可用語音或文字對談 |

**步驟四：匯出到 Claude Code**

達到 80–90% 滿意度後：

1. 點選設計 → More → Export → Code to Clipboard
2. 切換到 Claude Code
3. Prompt：`Create a landing page for [用途]. Here's the front-end code: [貼上]`
4. Claude Code 約 60 秒完成前端頁面

## 四種 Claude Code 整合方式

### 方式一：`DESIGN.md` 跨 agent 轉移設計風格

1. 從 Google 官方 Stitch skills repo（<https://github.com/google-labs-code/stitch-skills>）取得 `design-md` skill
2. 在任意 agent 提供「想要的網站風格 + 模板」，讓 agent 生成 `DESIGN.md`
3. 將 `DESIGN.md` 貼入 Stitch 的「建立新設計系統」欄位
4. 點儲存後 Stitch 自動視覺化設計系統
5. 基於此設計系統持續建立多個頁面，保持風格一致

**匯出既有 Stitch 專案的 `DESIGN.md`**：使用官方 `design-md` skill，透過 Stitch MCP 拉取專案畫面、擷取設計 token（顏色 / 字型 / 間距 / 元件模式）、翻譯為自然語言的 `DESIGN.md`。

**安裝 skill**：

```bash
npx add-skill google-labs-code/stitch-skills --skill design-md
npx add-skill google-labs-code/stitch-skills --skill react-components
```

### 方式二：Redesign Feature（從既有網站借用設計語言）

與舊做法的差異：

| 做法 | 結果 |
|------|------|
| 舊：提供截圖 → AI 複製整個設計 | 視覺抄襲 |
| 新：提供截圖 → Stitch 提取設計語言、元件排版邏輯 | 相似但原創的 UI |

操作步驟：

1. 用 GoFullPage 等擴充功能截取目標網站完整頁面
2. 上傳給 Stitch，選擇 redesign 功能
3. Stitch 提取設計模式，生成相似但原創的 UI

其他匯入方式：

- 提供網址 → Stitch 爬取網站，提取設計系統生成 `design.md`
- 上傳手繪草稿或線框圖 + 指定設計主題 → Stitch 精確匹配視覺風格
- 用標注工具修改不滿意的部分

### 方式三：Claude Code + Stitch Skills 自動化

Google 提供多個 Stitch skills 可安裝：

| Skill | 用途 |
|-------|------|
| **Enhanced Prompt Skill（最重要）** | 將模糊 prompt 轉換成 Stitch 優化的 prompt，含關鍵詞參考 |
| **Stitch Loop Skill** | 自主循環模式從 Stitch 迭代建構完整網站，整合 Chrome DevTools，維護 prompt 追蹤 |
| **React Component Skill** | 將 Stitch 匯出的 HTML 轉換成模組化 React 元件 |

**前置需求**：必須先連接 Stitch MCP（Stitch 在底層使用此 MCP 建構和取得設計）。

**完整自動化流程**（在 `CLAUDE.md` 中定義）：

```
1. Enhanced Prompt Skill → 將原始 prompt 優化成 Stitch 格式
2. 取得用戶確認
3. Stitch Loop Skill → 透過 Stitch MCP 建立專案、生成設計系統、生成設計
4. React Component Skill → 將 Stitch 輸出的 HTML 轉換成模組化 React 元件
```

### 方式四：搭配 UI Library（Shadcn UI）

**為什麼**：純 React 元件太靜態，缺乏互動效果和動畫；UI library 內建互動功能讓 UI 更生動。

**Shadcn UI Skill（Google 提供）**：

- 指導 agent 將 Stitch 設計轉換成 Shadcn 元件
- 支援連接多個 component registry（如 glassmorphism、motion primitives 等）

**設置步驟**：

1. 提前安裝 Shadcn MCP
2. 在 `CLAUDE.md` 加入指示：使用 Stitch MCP 時自動觸發 Shadcn skill 進行元件轉換
3. 在 `CLAUDE.md` 中列出要使用的 registry（依專案選擇）

**執行結果**：指定 Stitch 專案名稱 → Agent 自動 fetch 設計、載入 Shadcn skill、透過 MCP 與 registry 實作完整 app。外觀與 Stitch 設計完全一致，但元件具備豐富互動效果。

## Stitch MCP 整合（讓 Claude Code 驅動 Stitch）

MCP 整合後，agent 可直接建立並管理 Stitch 專案。

**主要功能**：

- 專案管理：建立新專案、取得所有活躍專案
- 列出畫面、取得專案和畫面
- 從 text prompt 生成新設計

**安裝需求**（官方 docs：<https://stitch.withgoogle.com/docs/mcp/setup/>）：

1. 安裝 Google Cloud SDK（`gcloud`）
2. `gcloud auth login`（用戶身分）
3. `gcloud config set project YOUR_PROJECT_ID`
4. `gcloud auth application-default set-quota-project YOUR_PROJECT_ID`（應用程式身分）
5. 啟用 Stitch API
6. 在 MCP client config 加入：
   ```json
   {
     "mcpServers": {
       "stitch": {
         "command": "npx",
         "args": ["@_davideast/stitch-mcp", "proxy"]
       }
     }
   }
   ```

**社群簡化腳本**：`npx @_davideast/stitch-mcp init`（davideast 維護，非 Google 官方，但為 Stitch 官方 docs 推薦的安裝途徑）— 一鍵處理 gcloud 檢查、登入、專案設定、API 啟用、MCP client 設定。

**支援的 MCP client**：VS Code、Cursor、Claude Code、Gemini CLI、Codex、OpenCode。

### 搭配 Claude Code Plan Mode

無論建構什麼，實作前規劃都是必要步驟。以模擬技術面試 app 為例：

1. 使用 Claude Code 的 plan mode 規劃 app，針對每個面向反覆迭代，產出詳細文件
2. 特別要求 UI 設計不要看起來像一般的 AI 生成設計
3. 仔細閱讀計畫並多次修改，直到完全滿意
4. 讓 Claude 取用計畫，透過 Stitch MCP 建立新專案並生成設計

### 將設計整合到 Next.js 專案

1. 請 Claude 使用 Stitch MCP 取得完整 landing page 的程式碼
2. 系統用 `get screen` 工具取得畫面，回傳可下載的連結
3. Claude 用 `curl` 指令提取程式碼
4. 取得 HTML 後整合到 Next.js 專案

**常見問題**：Claude 可能把所有程式碼都倒進 `page.tsx` 單一檔案，不遵循 React 元件結構慣例。

**解決方式**：要求 Claude 使用適當的元件結構重構，整理成結構清晰的 UI 元件與頁面集合。

## 測試與驗證：Vercel Agent Browser

Vercel 推出的 agent browser 已超越 Claude 的 Chrome extension，成為 Stitch 工作流推薦的瀏覽器測試工具。

| 工具 | 方式 | 速度 |
|------|------|------|
| Claude Chrome extension | 截圖 → 像素對應 → 導覽 | 較慢 |
| Playwright / Puppeteer | headless 瀏覽器 | 中等 |
| Vercel Agent Browser | accessibility tree + selector | 最快 |

**特性**：

- CLI 工具，以 Rust 和 Node.js 建構
- 以**快照**（snapshot，頁面的 accessibility tree）而非截圖運作，附有識別各元件的 selector
- Agent 使用 selector 有效率地導覽頁面
- 不與既有瀏覽器共用 session，在獨立瀏覽器中執行
- 目前僅支援 Chromium 系瀏覽器

**實際測試結果**：4 分鐘完成整個測試流程，識別出程式碼編輯器需要可編輯，立即實作修正並再次截取快照驗證。

**設定建議**：在 `CLAUDE.md` 中指定：所有測試一律使用 agent browser 工具，若不熟悉指令則先用 `help` 指令查詢。

## 實務建議總結

| 場景 | 推薦做法 |
|------|----------|
| 新專案、單次設計 | 基本工作流：找靈感 → Stitch 生成 → 匯出 code |
| 跨 agent / 跨專案維持風格 | 方式一：`design.md` |
| 借用既有網站設計語言 | 方式二：Redesign Feature |
| 端對端自動化工作流 | 方式三：Skills + MCP |
| 需要豐富互動的 UI | 方式四：Shadcn UI Skill |
| 需要 Claude Code 原生驅動 | MCP 整合 + Plan Mode |
| E2E 驗證 | Vercel Agent Browser |

## 相關前端設計筆記

Stitch 在以下筆記被當作前端設計工具鏈的一環被提及：

- [[Claude-Design快速上手]]
- [[Claude-Design-Masterclass指南]]
- [[Claude-Code前端設計七層級]]
- [[Claude-Code前端設計技巧與工具Top10]]

## 外部來源

### 影片摘要（本 MOC 整合來源）

- Chase H AI《Claude Code 搭配 Stitch 2.0 進行網頁設計》（2026-03-19）— <https://www.youtube.com/watch?v=qqcpiDXPCvY>
- AILABS-393《現在我這樣用 Google Stitch 設計》（2026-01-25）— <https://www.youtube.com/watch?v=VNx9Gy5pHZI>
- AILABS-393《Google Stitch 2.0 與 Claude Code 的 4 種整合方式》（2026-03-28）— <https://www.youtube.com/watch?v=b0lwCDNOFUY>

### 官方資源

- Google Stitch 官網：<https://stitch.withgoogle.com>
- Stitch MCP 安裝 docs：<https://stitch.withgoogle.com/docs/mcp/setup/>
- 官方 Skills repo：<https://github.com/google-labs-code/stitch-skills>
- Stitch MCP 社群實作（davideast）：<https://github.com/davideast/stitch-mcp>
- Google Blog 介紹：<https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/>

### 事實校正相關報導

- CNBC《Figma stock drops 12% after Google releases vibe design product Stitch》— <https://www.cnbc.com/2026/03/19/figma-stock-drops-11percent-after-google-releases-vibe-design-product-stitch.html>
- Parameter《Figma (FIG) Stock Tumbles 8% as Google Unveils Enhanced Stitch》— <https://parameter.io/figma-fig-stock-tumbles-8-as-google-unveils-enhanced-stitch-ai-design-platform/>
