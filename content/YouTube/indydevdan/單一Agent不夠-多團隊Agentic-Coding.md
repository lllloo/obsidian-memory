---
title: 單一 Agent 不夠：超越 Claude Code 的多團隊 Agentic Coding
tags:
  - youtube
  - claude-code
  - multi-agent
  - agent-harness
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-30
source: https://www.youtube.com/watch?v=M30gp1315Y4
---

## 核心主張：一個 Agent 不夠

Multi-agent orchestration 是當前前沿。目標是建立**多團隊 agentic coding**——用專精的 agent 團隊超越一般結果的分布。

適合對象：在 mid 到 large 規模 production codebase 工作的工程師，願意為更好結果付出成本。

## 三層架構

```
Orchestrator（最高層）
  └── Team Lead（各領域）
        └── Worker（前端、後端、QA 等）
```

- **Orchestrator**：協調所有 teams，只與使用者對話，再委派給 team leads
- **Team Leads**：協調本 team，不執行工作，只委派給 workers
- **Workers**：執行具體任務（讀取、寫入、測試）

所有對話都通過 Orchestrator，認知投入不隨 agents 數量增加。

## Pi Coding Agent Harness 設定

### multi-team config 結構

```yaml
orchestrator:
  prompt: .pi/agents/orchestrator.md
  model: claude-opus-4-6

teams:
  - name: planning
    lead:
      prompt: agents/planning_lead.md
      model: claude-opus-4-6
    members:
      - name: planner
        prompt: agents/planner.md
        model: claude-sonnet-4-6

  - name: engineering
    lead:
      prompt: agents/eng_lead.md
    members:
      - name: backend_dev
        prompt: agents/backend.md
      - name: frontend_dev
        prompt: agents/frontend.md

  - name: validation
    lead:
      prompt: agents/val_lead.md
    members:
      - name: qa_engineer
      - name: security_reviewer
```

### Domain 鎖定

```yaml
# 前端 agent 的 domain
domain:
  read: ["**/*"]        # 可讀取所有
  write: ["frontend/**"] # 只能寫前端

# 後端 agent 的 domain
domain:
  read: ["**/*"]
  write: ["backend/**", "migrations/**"]
```

### Skill 共享模式

- `zero_micromanagement`：所有 leads 和 orchestrator 共享，強制委派
- `conversational_response`：leads 和 orchestrator 共享，worker 不需要（worker 要詳細輸出）
- `delegate`：orchestrator 和 leads 的主要工具
- `active_listener`：所有 agents 共享，每次回應前重讀對話記錄

## Agent Experts（agent 記憶）

每個 agent 有獨立的 **mental model 檔案**，每次啟動自動載入：

```
agents/
  expertise/
    backend_dev.md    # 5K tokens，持續累積
    frontend_dev.md
    planning_lead.md
```

Mental model 的功用：
- 追蹤 codebase 已知模式與架構
- 記錄過去的決策與原因
- 累積 session 間的知識（不需要每次重新解釋）

## 實際案例：Prompt Routing Classifier

示範任務：在現有 scikit-learn prompt 複雜度分類器上，讓多團隊協作改進。

工作流程指令：
```
plan engineer and validate. Make sure to add just commands to test both models.
```

Orchestrator 自動：
1. 委派 planning lead 建立詳細計畫
2. Engineering lead 委派給 backend dev 實作
3. Validation lead 同時委派 QA 和 security reviewer 驗證

結果觀察：三個 teams 給出一致推薦（LinearSVC），同時各自發現不同問題。

執行測試指令（justfile）：
```bash
j predict summarize this codebase  # 預測複雜度
j prompt-both                       # 同時測試兩個模型
j train-both                        # 訓練兩個模型
```

## 多觀點的優勢

- 三個 teams 各自獨立分析，共識更可信
- 不同 teams 找到不同問題（QA vs Security 視角差異）
- 對話 log 以 JSONL 儲存，所有 agents 都能看到完整對話

## Session 目錄結構

```
sessions/
  <session_id>/
    conversation.jsonl   # 完整對話記錄（含 tool calls）
    system_prompts/      # 啟動時的系統提示快照
    results/             # 產出的檔案與報告
```

## 成本考量

- 示範 session 花費約 $8
- 作者觀點：token 成本持續下降，現在應該「花更多 tokens 做更多事」
- 使用 Claude 1M context 模型：leads 用 Opus，workers 用 Sonnet

## 2026 核心主題

- **信任 + 規模**：增加對 agents 信任，才能交付更大規模的工作
- **Specialization**：專精 > 泛用。每個 agent 應只負責一個 domain
- **Stacking knowledge**：每次執行都讓 agents 更了解你的 codebase
