---
title: 統治所有 Agent 的唯一 Agent：進階多智能體編排
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-11-03
source: https://www.youtube.com/watch?v=p0mrXfwAbCg
---

## Agentic Scaling Framework

每個工程師目前處於以下其中一個層次：

1. **Base agents**：基本 agent 使用
2. **Better agents**：優化 context 與 prompt engineering
3. **More agents**：多個 agent 並行
4. **Custom agents**：針對特定問題的專屬 agent
5. **Orchestrator agent**（下一層）：管理整個 agent 艦隊的統一介面

核心原則：**Scale your compute to scale your impact**

## Orchestrator Agent 的三大支柱

整個 multi-agent orchestration 系統由三個核心組成：

1. **Orchestrator agent**：統一介面，管理所有 agent（Single Interface Pattern）
2. **CRUD for agents**：能建立、命令、查詢、刪除 agent
3. **Observability**：即時監控每個 agent 的效能、成本、結果

缺少 observability 就無法擴展：「If you can't measure it, you can't improve it. If you can't measure it, you can't scale it.」

## Orchestrator 的運作模式

**工作流程（以 Scout + Builder 模式為例）：**
1. Orchestrator 接收高層需求，透過思考分解成具體任務
2. 建立 Scout agent：收集程式碼現況、找到需要修改的位置
3. Scout 完成 → 輸出 produced assets（markdown 文件、diff 等）
4. Orchestrator 撰寫詳細 prompt 給 Builder agent
5. Builder 根據 Scout 的結果執行修改
6. Orchestrator 每 15 秒 check agent status，在 loop 中 sleep → wake → check
7. Reviewer agent 確認工作完成
8. 工作結束 → 刪除所有 agents（`delete all agents`）

**核心設計原則：**
- Orchestrator 不直接執行工作，只負責協調
- 每個 agent 有**專一任務**（focused, one-purpose agent）
- 保護 Orchestrator 的 context window：不讓它讀取所有 agent 的詳細 logs
- Agent 必須產出具體結果（produced assets），而非只是對話

## Agent 的核心四元素

任何 agent 層面的關鍵資訊：`context + model + prompt + tools`

透過 observability UI 可以即時看到每個 agent 的：
- 名稱、狀態
- Context window 使用量
- Response messages、tool calls、hooks、reasoning
- Consumed assets vs. produced assets
- 成本

## 關鍵洞見

**Agent 應視為「可刪除的臨時資源」：**
- 單一目的，完成後刪除
- 不要讓 agent context switch（就像不讓員工同時做太多事）
- 即使有 200K context window，也應該讓 agent 聚焦，不是塞更多工作

**Human-in-the-loop 決策點：**
- 系統設計上，agent 主動問你問題（而不只是你問 agent）
- 在正確的時機點介入審核

**Out-of-loop vs. In-loop：**
- 大部分工作可以 out-of-loop，讓 agent 自主執行
- 需要時仍可 in-loop（在 terminal 直接操作）
- 優秀的系統讓你能在兩種模式間切換

## 架構實作要求

建構 multi-agent orchestration 系統的成本：
- 時間投入：管理 orchestration agent、plumbing、database、WebSocket 連線
- 值得投入嗎？答案是肯定的——這讓你能部署 domain-specific 專屬解決方案

**出發點**：先有出迴圈（out-loop）的 agentic coding 系統，再根據需求擴展成 orchestrator 架構。
