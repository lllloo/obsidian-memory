---
title: Codebase Singularity：「我的 agents 比我更會跑 codebase」
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-12-29
source: https://www.youtube.com/watch?v=fop_yxV-mPo
---

## 核心概念：Agentic Layer

**Agentic Layer** = Codebase 外圍的新環，讓 agents 代表你操作應用程式。

**Codebase Singularity**：當 agentic layer 足夠強大時，工程師會意識到「我的 agents 現在跑 codebase 比我更好」——這是終極目標。

架構：
- 外層（綠色）= Agentic Layer
- 內層（暗色）= Application Layer（DB、前端、後端、腳本、DevOps）

## 三個 Class，多個 Grade

### Class 1

**Grade 1（最薄）**
- CLAUDE.md 記憶檔案 + `/prime` 命令
- 優點：極簡、快速設置、agents 立刻理解 codebase
- 缺點：對大型 codebase 無用，缺少大量 leverage points

**Grade 2**
- 新增：`specs/` 規劃目錄、`ai-docs/` 文件目錄、sub agents（fetch docs agent、test writer）
- 特點：開始並行化工作、收集文件、規劃後再執行
- 仍然：缺少 custom tools

**Grade 3（關鍵跳躍）**
- 新增：Skills、MCP servers、帶 tool access 的 prime commands
- 三者都提供相同東西：增強 agents 的 Core Four 的 custom tools
- MCP 範例：PostgreSQL、Firecrawl、Jira、Notion
- 常見陷阱：太多工具、token 消耗過重、過度工程化
- 核心原則：Skills 和 MCP servers 都可以被一個好的 prompt 取代

**Grade 4（反饋迴路）**
- 新增：Build prompt、Review prompt、Closed Loop prompts
- Closed Loop 模式：Request → Validate → Resolve（不斷循環直到完成）
- 例如：`/test-backend`、`/test-frontend`、`/code-review`
- Agents 開始自我修正工作
- 隨著 codebase 成長，前端/後端 prompts 開始分化

**Grade 5**
- 更大規模的 AI developer workflows
- Orchestrator agent 可控制多個工作流程
- 示範：orchestrator 一個 prompt 觸發 plan-build-review-fix 整個流程

## Orchestrator + AI Developer Workflows（Class 3）

最強版本：
- Orchestrator agent 上層指揮
- 下面跑多個 AI developer workflows 並行
- 工程師只在最外層 prompt 和 review

## 工程師進步路徑

```
Class 1 Grade 1 → Grade 2 → Grade 3 → Grade 4 → Grade 5
         ↓            ↓          ↓          ↓         ↓
    記憶/Prime    Sub agents  Custom     Feedback   Orchestrator
                  + 規劃      tools      loops      + ADWs
```

判斷自己在哪個層級 → 找到下一個 leverage point → 持續擴展 agentic layer。

## 核心原則

- 建立 agentic layer 是 agent 時代投資報酬率最高的行動
- Scale compute = Scale impact
- 一切最終回歸 **Core Four**：Context × Model × Prompt × Tools
