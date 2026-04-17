---
title: TOP 2% Engineering：2026 年成為頂尖 Agentic 工程師的計畫
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-16
published: 2025-12-22
source: https://www.youtube.com/watch?v=u-SQ0Jsv4mI
parent: "[[01.index]]"
---

## 核心主題：2026 是「信任之年」

**Trust → Speed → Iteration → Impact**

模型已不再是瓶頸。限制在於你和 agent 之間的信任程度——你能讓 agent 跑多長、多遠、多自主？

信任的量化指標：agent 能連續正確執行的 tool calls 長度。

## 10 個 Big Bets（2026 年預測）

### Bet 1：Anthropic 成為主導者
- Claude Code 是 agentic coding 的領導工具
- Sonnet 3.5、Claude Code、Sub agents、Opus 4.5 的發展軌跡顯示一致執行力
- 投注 Anthropic = 減少與工具搏鬥的時間，更多時間 ship

### Bet 2：Tool Calling 是最大機會
- 截至報告時，只有 15% 的 output tokens 是 tool calls（Open Router 數據）
- Tool call ≈ agent 代你採取的行動 ≈ 直接影響力
- Reasoning models 已占超過一半的 LLM 用量
- Claude Opus 最適合長鏈 tool calls

### Bet 3：Custom Agents 最重要
- 50 行程式碼 + 3 個 tools + 150 行 system prompt = 自動化數千小時工作
- 使用 agent coding 工具是 baseline，下一步是用 SDK 建 custom agents
- 每個大 AI lab 都有 agent SDK，選一個綁定

### Bet 4：Multi-Agent Orchestration
- 「1 agent 不夠」—— 跑 3、5、10、甚至數百個 agents
- 多 agent 互相驗證 → 更高信心
- Cross-validation 技術：多個 agents 同時分析問題，4/5 給出相同答案 = 高置信度

### Bet 5：Agent Sandboxes
- 讓 agent 在自己的電腦上跑（defer trust）
- 就像 dev/staging 環境——agent 在裡面搞爛沒關係
- Best-of-N 模式：同時跑 10 個 agent，看誰贏

### Bet 6：In-Loop vs Out-Loop Agentic Coding
- **In-Loop**：工程師在 terminal 旁邊監控（大多數人現在在做）
- **Out-Loop**：從外部系統（Slack、Discord、GitHub）觸發，agent 完成後提交 PR
- 頂尖工程師兩者都用

### Bet 7：Agentic Coding 2.0
- 2024 = AI coding（寫程式）
- 2025 = Agentic coding（Core Four：Context + Model + Prompt + Tools）
- 2026 = 下一個範式（超越 agent coding）

### Bet 8：Benchmark 崩解
- 公開 benchmark 趨於飽和，所有模型都逼近 100%
- 未來唯一有效的測試：在你的真實工作中實際跑 agent

### Bets 9-11：邊緣預測
- Bet 11：第一個「端對端 agentic 工程師」公開出現（系統建造系統）

## 過往預測準確率
- 2023：24 個預測，16 個正確
- 2024：41 個預測，36 個正確
- 2025：15 個預測，13 個正確（準確率持續上升）

## 成為 Top 2% 的路徑

1. 在 Anthropic 工具鏈上深入投資
2. 最大化 tool calls 長度（= 最大化信任 = 最大化影響力）
3. 建自己的 custom agents（Agent SDK）
4. 跑多個 agents 並行（不要只跑一個）
5. 用 agent sandboxes 處理高風險工作
6. 同時使用 in-loop 和 out-loop 模式
