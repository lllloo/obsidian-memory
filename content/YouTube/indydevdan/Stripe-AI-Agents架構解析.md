---
title: 研究 Stripe 的 AI Agents 架構：Vibe Coding 已死
tags:
  - youtube
  - claude-code
  - agentic-engineering
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-02
source: https://www.youtube.com/watch?v=V5A1IU8VVp4
parent: "[[01.index]]"
---

## 核心對比：Vibe Coding vs Agentic Engineering

- **Agentic Engineering**：知道系統會發生什麼，不需要盯著看
- **Vibe Coding**：不知道、也不看
- Stripe 每週合併 1,300 個 PR，零行人工寫的程式碼——這是 Agentic Engineering

## Stripe Minions 系統概覽

Stripe 自研的 end-to-end coding agents，稱為 **Minions**：

- 從 Slack 訊息觸發，到生產就緒的 PR 全程無人值守
- 操作含數百萬行 Ruby 程式碼的 monorepo（含 Stripe 自研 library，LLM 不認識）
- 工程師可同時啟動多個 Minion 並行解決不同問題

為何要自建而非用 Claude Code？因為 Stripe 的程式碼庫規模、複雜度和合規要求，通用工具無法滿足。**Specialization is the advantage。**

## 七大關鍵架構元件

### 1. API Layer（多入口）
三種觸發方式：CLI、Web UI、Slack。Web UI 左側顯示工具呼叫與思考過程，右側顯示修改的檔案。

### 2. Warm Devbox Pool（Agent Sandbox）
- 基於 AWS EC2，與工程師開發環境完全相同
- 10 秒內 spin up，預先暖機
- 每位工程師可同時開 6 個以上
- 隔離環境讓 Minion 不需要人工權限確認
- 思路：**要讓 agent 表現如你，就給它你有的工具和環境**

### 3. Agent Harness（fork 自 Goose）
- fork Block 的開源工具 [Goose](https://github.com/block/goose)
- 客製化 orchestration flow，**交錯 agent loop 與 deterministic code**
- 強制執行 Stripe 特定步驟（linters、測試）
- 核心原則：**agents + code > agents alone > code alone**

### 4. Blueprint Engine（最關鍵）
- **Blueprint** = workflow as code + agent 彈性的組合
- 每個 Blueprint 是一系列 agent skill 與 deterministic code 交織的步驟
- 確定性步驟（linter、git commit、測試）不調用 LLM
- 非確定性步驟（理解需求、修改邏輯）交給 agent
- 讓 sub-agents 在特定步驟中擁有受限的工具與 system prompt → **專業化**

### 5. Rules File（Context Engineering）
- 使用類似 cursor rules 的格式（MDC），加上 frontmatter glob pattern
- 規則**按子目錄條件觸發**，不是全域載入
- 解決大型 codebase 的 context 爆炸問題

### 6. Tool Shed（Meta-Agentics）
- 集中式內部 MCP server，管理近 500 個 MCP tools
- 提供一個「選工具的工具」給 agents 動態發現可用工具
- 工程師可輕鬆新增工具，系統自動可被發現

### 7. CI 驗證層 + GitHub PR
- 3,000,000+ 測試，push 時選擇性執行相關子集
- Minion 最多跑 **2 輪 CI feedback**（作者認為限制過少）
- GitHub PR 供工程師 review

## In-Loop vs Out-Loop Agentic Coding

| 模式 | 說明 | 適用場景 |
|------|------|----------|
| **In-Loop** | 工程師在場，來回 prompt | 構建 agent 系統本身 |
| **Out-Loop** | 全自動，工程師只在開頭與結尾參與 | 規模化生產任務 |

建議：**50% 以上的時間用於構建 agent 系統**，而非直接寫應用程式碼。

## 作者對 Stripe 系統的評分與建議

- 評分：**8/10**
- 建議 1：CI feedback 僅限 2 輪過於保守，應增加輪數以獲得更多學習
- 建議 2：目前系統仍有「人工 review」步驟，真正的目標是 **ZTE（Zero Touch Engineering）**——從 prompt 到 production 無需人工介入

## 關鍵結論

> 「它不是關於什麼模型贏了，而是你如何建構讓 agent 在其中運行的系統。」

specialization 必須貫穿整個技術棧：prompt → skill → agent → harness → infrastructure。
