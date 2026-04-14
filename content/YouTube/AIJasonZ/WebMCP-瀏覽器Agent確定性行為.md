---
title: WebMCP 瀏覽器 Agent 確定性行為
tags:
  - youtube
  - ai-agent
  - mcp
  - chrome
created: 2026-04-14
updated: 2026-04-14
published: 2026-02-15
source: https://www.youtube.com/watch?v=xQAYZBDV5jg
---

## 核心問題

現有 browser use agent 的痛點：
- 傳統方式：擷取整頁 HTML 清理後給 LLM → 非確定性行為多、噪音大
- 自建 MCP server：需要每個 agent 都預先安裝，不實際

## WebMCP 的解法

Google 為 Chrome 設計的新規範：在網頁程式碼中宣告 MCP 工具，agent 瀏覽到該頁時自動取得對應工具。

每個頁面可針對其內容暴露不同工具集：
- 首頁：search products、get categories
- 商品頁：add to cart、get similar products

Agent 透過 MCP tool 執行操作，確定性等同直接呼叫 API。

## 兩種設定方式

### 宣告式（Declarative）— 靜態 HTML

在 HTML 元素上加屬性：
```html
<form tool-name="book-table" tool-description="Book a restaurant table">
  <input type="text" tool-param-description="Customer name" />
</form>
```

Chrome 自動將這些屬性轉換為 MCP tool schema。

### 命令式（Imperative）— JS/React 應用

```js
navigator.registerTool(toolSchema, handler)
navigator.unregisterTool(toolName)
```

在 React component mount/unmount 時自動 register/unregister，讓工具隨頁面內容 contextual 載入。

## 啟用需求

- 安裝 Chrome Beta
- 在 `chrome://flags` 啟用 Web MCP flag
- 安裝 Chrome extension：Model Context Tool Inspector

## 與現有方案的比較

| 方案 | Token 效率 | 確定性 | 適用場景 |
|--|--|--|--|
| Browser use（HTML 擷取） | 低 | 差 | 一般爬取 |
| 預載 MCP | 高確定性但 context 消耗固定 | 好 | 固定工具集 |
| Skill + CLI | 高效率 | 中 | 長尾功能 |
| WebMCP | 高（contextual 載入） | 好 | 任意網站 |

WebMCP 將 contextual MCP loading 的概念帶到瀏覽器，被視為未來方向。
