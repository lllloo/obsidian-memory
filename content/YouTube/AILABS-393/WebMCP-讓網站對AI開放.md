---
title: WebMCP 讓網站對 AI 開放
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-19
source: https://www.youtube.com/watch?v=uprZUcv0FSc
parent: "[[01.index]]"
---

## 現有瀏覽器 Agent 的根本問題

目前 AI 操作瀏覽器有兩種方式：

- **Vision-based**：截圖 → 標註元素 → 模型猜測要點擊什麼
- **DOM parsing**：解析完整 HTML（inspect element 等級，數千行）

兩種方式都是 non-deterministic，因為整個網際網路是為人眼設計的，沒有給機器讀的結構。

## WebMCP 的解法

Google 與 Microsoft 共同發布 WebMCP：讓網站本身把可用的操作**宣告為 tools**。Agent 進入頁面時不猜測，直接讀取可用 tools 並呼叫。

現況：
- 目前僅限 Chrome Canary 版本（Chrome 146 預計更廣泛支援）
- 官方示範：flight search demo、Marvel context tool inspector extension
- 正式文件尚未釋出，僅有 Google Chrome Labs 的 repository

## 兩種實作方式

**Declarative API（簡單 HTML 表單）：**

在 HTML 表單中宣告三件事：tool name、tool description、tool parameters description。瀏覽器自動讀取，適合靜態表單。

**Imperative API（複雜 SPA）：**

在 React/Next.js 中建立 library 檔案宣告所有 tools。為避免 context 爆炸，採用 **contextual loading**：

```javascript
// 進入頁面時
registerHomeTools()

// 離開頁面時
unregisterHomeTools()
```

每個頁面只載入該頁面的 tools，不同頁面有不同的可用 tools 集合。

## 與 Claude Code 整合的限制

官方設計對象是 Gemini（內建於 Chrome）。搭配 Claude Code 需使用社群開發的 bridge（MCP + Chrome extension）：

- Declarative API：可正常運作
- Imperative API：contextual loading 時 tool switching 不穩定

## 實作建議

- 每頁最多 50 個 tools（聚焦在該頁面的核心操作）
- Tool descriptions 要詳細清楚，Agent 靠這個決定呼叫哪個 tool
- 目前仍是實驗性質，不建議上 production
- 對網站擁有者：實作 WebMCP 讓網站對 AI 友善是趨勢，不管哪個 agent 先受益
