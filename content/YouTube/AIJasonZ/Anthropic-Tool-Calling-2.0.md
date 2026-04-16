---
title: Anthropic Tool Calling 2.0
tags:
  - youtube
  - ai-agent
created: 2026-04-14
updated: 2026-04-14
published: 2026-02-22
source: https://www.youtube.com/watch?v=3wglqgskzjQ
parent: "[[01.index]]"
---

## 傳統 Tool Calling 的問題

傳統機制（兩年未變）的核心缺陷：
- Agent 需依序呼叫多個工具，每次都要重新生成參數
- 工具回傳的大量 metadata 全部留在 context window，浪費大量 token
- 複雜任務中非確定性行為明顯

## Anthropic 的四項升級

### 1. Programmatic Tool Calling（最重要）

受「Executable Code Actions」論文啟發：
- 不讓 LLM 當每次工具呼叫的膠水層
- 改為讓 LLM 直接輸出一段程式碼，在沙盒中執行多個工具
- 可在程式碼中使用 for loop、條件判斷，實現更複雜的工作流

啟用方式：在 agent 回應中加入 `code_execution` 工具，並在每個工具定義中加入 `allowed_callers: ["code_execution_20260120"]` 參數。

效果：減少 30-50% token 消耗，大幅減少 LLM 呼叫次數。

### 2. Dynamic Filtering for Web Fetch

- Web fetch 傳統上會把整個 HTML 傾入 context window
- Dynamic filtering 在中間加一層，自動過濾只留相關內容
- 平均減少 24% token 消耗
- 啟用：使用指定版本的 web fetch tool（`2026209`）

### 3. Tool Search（工具搜尋）

- 問題：載入上百個 MCP 工具 schema 的 token 成本高
- 解法：只載入一個 `tool_search` 工具（約 500 token），讓 agent 動態查詢需要的工具
- 可設定 `deferred_loading: true` 讓工具預設不載入
- 效果：最多減少 80% context window 使用

### 4. Tool Use Example

- 對複雜工具（如 `create_ticket` 有很多欄位）提供使用範例
- 在工具定義中加入 `input_examples` 陣列
- 測試：複雜參數處理準確率從 72% → 90%

## 建議使用場景

- Programmatic tool calling：需批次處理大型資料集、有固定呼叫順序的場景
- Dynamic filtering：任何需要 web fetch 的 agent
- Tool search：工具數量超過 10 個的 agent
- Tool use example：有複雜 nested 結構或大量 optional 參數的工具
