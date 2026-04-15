---
title: BIG 3 超級 Agent：Gemini 2.5 Computer Use、OpenAI Realtime API、Claude Code
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-10-13
source: https://www.youtube.com/watch?v=Ur3TJm0BckQ
---

## 核心理念：不要單一工具忠誠度

技術業想讓你選一個工具、一個供應商、一個模型——那是他們的商業策略，不是你的最大化策略。

**正確思維**：用 AND，不用 OR。同時使用 Gemini、OpenAI、Claude，組合出能力最強的系統。

## BIG 3 Super Agent 架構

### 系統三層結構

```
輸入層 (Input Layer)
  └─ 工程師（文字/語音）
  └─ Agent（自我閉環）

系統層 (System Layer)
  └─ OpenAI Realtime API（語音 Orchestrator Agent）
      ├─ 工具：list_agents、create_agent、command_agent
      └─ 命令 Claude Code agents（Builder agents）
          └─ 工具包含：Gemini 2.5 Computer Use（瀏覽器驗證 agent）

輸出層 (Output Layer)
  └─ 音訊、文字、檔案、副作用
  └─ 回饋到 Multi-agent Observability
  └─ 再循環回輸入層
```

### 三大技術角色

1. **OpenAI Realtime API**：語音介面 Orchestrator，管理 Claude Code agents 的 CRUD
2. **Claude Code agents**（Sonnet 4.5）：實際建構前後端的 Builder agents
3. **Gemini 2.5 Computer Use**：瀏覽器 agent，自動截圖、測試 UI、驗證功能

## 實際執行流程

**情境**：用語音命令建構 OpenAI Sora 影片生成器

1. 用語音建立兩個 Claude Code agents：Sony（後端）、Blink（前端）
2. 命令 Sony 讀取 AI docs，用 `/plan` slash command 規劃 Sora API 整合
3. 命令 Blink 處理前端 UI（黑字白底、Play 字型）
4. Blink 完成後，Gemini 2.5 Computer Use 自動截圖驗證 UI 變更
5. 用語音指令協調前後端分工，Sony 建後端 API，Blink 建前端元件
6. 建立獨立 browser use agent 測試生成功能（自動填表單、點按鈕、等待生成）

**Multi-agent Observability**：即時看到每個 agent 的所有 tool calls 和高層摘要（用 Haiku 4.5 快速摘要）

## 關鍵設計原則

**Orchestrator 要薄（Thin Orchestration Layer）**：
- 只有 CRUD 操作（create、list、command、delete agent）
- 不綁定特定 agent 類型，任何工具/模型都可以插入
- 未來新模型（Opus、Gemini 3）可直接接入

**閉環結構（Closed Loop）**：
- Claude Code agent 有 Computer Use 工具 → 自動驗證自己的工作
- Browser agent 的截圖回饋給 agent → 再決策修正
- 系統輸出循環回到輸入 → agent 可以自我糾錯

**Agent 邊界問題（教訓）**：
- Sony 和 Blink 同時對前端動手，造成衝突
- 解決：在 prompt 和 plan 中明確指定「Sony 只做後端」
- 清晰的 agent 責任邊界是 multi-agent 系統穩定的關鍵

## 實用洞見

- Slash commands 在 agent 間可以直接引用（orchestrator 可以命令 builder 執行 `/plan`、`/build`）
- 語音介面只是多一種輸入方式；底層文字 workflow 更可靠且可被 agent 調用
- 系統崩潰後恢復：重啟 → `list all agents` → agent 從 log 繼續工作
- 核心：讓系統同時服務工程師、團隊、和 agent 三種使用者
