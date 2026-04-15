---
title: Anthropic Claude Code 7 小時課程精華
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-20
source: https://www.youtube.com/watch?v=XuSFUvUdvQA
---

## 課程概覽

- 作者花 7 小時研讀 Anthropic 官方 Claude Code 課程，並整合超過 500 小時的個人使用心得。
- 課程分四大部分：什麼是程式碼助手、為什麼選 Claude Code、如何與 Claude Code 協作、如何最大化使用效果。

## 什麼是程式碼助手

- 語言模型 + 工具集 = 程式碼助手。
- 運作三步驟：蒐集上下文 → 制定計畫 → 採取行動，不斷循環直到任務完成。
- 蒐集上下文與採取行動都需要與外部環境互動，僅靠模型推理無法完成。
- Claude Code 擁有豐富的內建工具：啟動子 Agent、執行 bash 指令、編輯檔案等。

## Claude Code 的強大能力（官方案例）

- **效能最佳化**：對 chalk 函式庫跑 benchmark，找出根因並修復，在週下載量近 4 億次的函式庫中發現 3.9 倍效能提升。
- **資料分析**：讀取串流平台 CSV 資料，在 Jupyter Notebook 中生成視覺化圖表與流失分析。
- **UI 設計**：搭配 Playwright MCP 控制瀏覽器，截圖確認效果，像前端工程師一樣迭代改善界面。
- **CI/CD 整合**：自動審查每一個 GitHub Pull Request。

## 安裝與啟動

- 搜尋「Claude Code」找到官方連結，複製 curl 指令，在終端機執行即可安裝。
- 安裝後直接在終端機輸入 `claude` 啟動。
- 建議在特定專案資料夾下執行，避免 Claude 誤動到其他目錄。

## 初始化專案

- 在新專案或既有 codebase 執行 `/init`，Claude 會分析整個 codebase 並生成 `claude.md`。
- `claude.md` 作為系統提示，包含架構摘要、關鍵檔案、慣例等，每次請求都會帶入。

## 加入上下文

- 用 `@` 標記特定檔案（如 `@schema.prisma`）加入上下文。
- 用 `/memory` 指令編輯專案記憶或使用者記憶，讓 Claude 記住特定偏好（例如「永遠使用 TypeScript」）。
- 最佳實踐：在 `claude.md` 中明確提及所有關鍵檔案路徑，讓每個 Claude Code 實例都知道。

## 計畫模式與思考模式

- **計畫模式**（Plan Mode，按 Shift+Tab 切換）：Claude 做大量研究、規劃，不動任何程式碼。
- **思考模式**：有四個強度——think、think hard、think harder、ultra think。
- 注意：最新版 Claude Code 已預設使用最大推理力（ultra think 預設開啟），不再需要手動指定。
- 按 Escape 可隨時中斷 Claude，提供更多上下文後重新開始。
- `/compact` 指令：壓縮整段對話以釋放 context window，適合長工作階段使用。

## 自訂指令

- 在 `.claude/commands/` 目錄建立 Markdown 檔案即可建立自訂 slash 指令。
- 使用 `$ARGUMENTS` 變數傳入執行時參數（例如：`/review PR-123`）。
- 找出重複使用的 prompt 並轉成自訂指令，大幅提升生產力。

## MCP 伺服器

- MCP 伺服器讓 Claude Code 擁有更多工具能力，可本地或遠端運行。
- 範例：
  - **Playwright MCP**：讓 Claude 控制瀏覽器，可截圖、點擊、測試 UI
  - **N8N MCP**：提供所有 N8N 節點的最新文件，讓 Claude 自動生成 N8N 自動化流程

## GitHub 整合

- 執行 `/install-github-app`，讓 Claude Code 整合到你的 GitHub repo。
- 整合後可在 Pull Request 或 Issue 中 `@Claude` 指派任務，Claude 可直接推送 commit、開 PR、回應 review 留言。

## Hooks

- **Pre-tool hook**：在 Claude 使用工具前觸發，可用來防止讀取敏感檔案（如 .env）或修改特定檔案。
- **Post-tool hook**：工具執行後觸發，例如：自動執行 TypeScript 型別檢查（`tsc --no-emit`），提早發現型別錯誤。
- **重要**：hooks 中的路徑必須使用絕對路徑（可用 `$PWD` 佔位符搭配腳本替換）。

## Claude Code SDK

- Claude Code 提供 CLI 及 TypeScript/Python 函式庫的程式化介面（Agent SDK）。
- 允許開發者建立自訂 AI Agent，擁有與 Claude Code 相似的工具能力，但針對特定領域最佳化。
- 注意：Claude Code 本身不是開源的，SDK 僅公開部分能力。

## 官方課程小測驗答案

1. 語言模型的根本限制：**只能處理文字輸入，無法與外部系統互動**（選 D）
2. GitHub Actions 整合 MCP 所需權限：允許 Claude 讀寫 repo 內容
3. 計畫模式 vs 思考模式：計畫模式處理廣度（研究不動程式碼），思考模式處理深度
4. `claude.md` 的三種類型：全域、專案級、使用者級
5. 建立帶參數的自訂指令：使用 `$ARGUMENTS` 變數
6. 可防止工具執行的 hook 類型：**Pre-tool-use hook**
7. 防止讀取 .env 的 hook：Pre-tool-use hook，匹配 Read 與 Grep 工具
8. Hooks 的主要用途：**在 Claude 執行工具前後運行自訂腳本**
