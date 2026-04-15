---
title: Cursor 搭配 Playwright MCP 實現自動測試
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-05-07
source: https://www.youtube.com/watch?v=3tYBbH_nFcE
---

## Playwright MCP 的兩大用途

1. **UI 自我迭代**：讓 Cursor 看到瀏覽器畫面 → 識別 UI 問題 → 自動修正，直到符合預期
2. **自動化測試**：讓 Cursor 模擬真實使用者操作，生成可重複執行的測試腳本

## 安裝設定

在 Cursor MCP 設定中加入：

```json
{
  "playwright": {
    "command": "npx",
    "args": ["@playwright/mcp@0.0.2"]
  },
  "playwright-test": {
    "command": "npx",
    "args": ["@playwright/mcp@0.0.2", "--config", "./playwright.config.ts"]
  }
}
```

注意：目前穩定版本為 `0.0.2`，最新版有問題。

**建議建立兩個 MCP 設定：**
- 含 vision 模式：適合 UI 迭代（`--vision` flag），能看到畫面截圖
- 不含 vision 模式：適合測試（vision 對定位 UI 元素較弱）

**Playwright 設定檔（`playwright.config.ts`）可設定：**
- 使用哪種瀏覽器
- 模擬的裝置
- User agent（用於繞過反爬蟲）
- 初始化腳本

## 使用場景一：UI 自我迭代

開啟含 vision 的 MCP，給 Cursor 這樣的提示：

```
Please use Playwright MCP to view the UI. 
Identify areas to improve for UI and iterate until it looks perfect.
Make sure the width of the browser in MCP is 700 pixels.
```

Cursor 會：
1. 開啟瀏覽器並截圖
2. 分析 UI 問題（spacing、alignment 等）
3. 修改程式碼
4. 再截圖驗證，反覆迭代

## 使用場景二：AI 驅動測試

切換到不含 vision 的 MCP，給 Cursor 測試指令，例如：

```
We have a simple to-do app set up in Next.js. 
Let's test the application using Playwright MCP.
First test if login works, then test if users can successfully add to-dos and mark as completed.
```

Cursor 會自動：
- 開啟瀏覽器
- 填入帳號密碼、點擊按鈕
- 驗證操作結果

## 將 AI 測試轉為可重複執行的腳本

完成 AI 測試流程後，要求 Cursor 生成正式測試腳本：

```
Now create a reusable Playwright UI test based on the flow above so I can run it as automated tests.
```

Cursor 會：
1. 安裝 `@playwright/test`
2. 建立 `playwright.config.ts`
3. 撰寫測試腳本（登入、新增任務、標記完成等）
4. 自行執行測試並修復失敗的 case
5. 建立 GitHub Actions workflow（PR 前自動執行測試）

執行測試：`npm run test:e2e`
