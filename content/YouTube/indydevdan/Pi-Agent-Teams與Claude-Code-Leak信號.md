---
title: Pi Agent Teams、Claude Code 洩漏信號與 Harness Engineering
tags:
  - youtube
  - claude-code
  - agent-harness
  - multi-agent
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-06
source: https://www.youtube.com/watch?v=RairMJflUSA
---

## Claude Code 洩漏的真正信號

Claude Code 從零到十億 ARR 僅花 6 個月。洩漏的系統提示揭示一件事：**Agent Harness 至關重要**。Harness 提供 agentic 成果所需的一切：

- 確定性代碼（Deterministic code）
- Token caching
- Agent 編排
- Prompts、Skills、模型控制

沒有 Agent Harness，就沒有 agents，也沒有 agentic coding。

## Harness Engineering 的核心概念

- Claude Code 已成主流，要超越它，下一步是學習 **Harness Engineering**
- 可用 Pi coding agent 等工具建立專屬 domain 的 agent harness
- 擁有 harness 就能控制 Core 4：**Context、Model、Prompt、Tools**
- 可加入模型輪換系統：若某模型失效，自動切換

## 無限 UI Agent 系統架構

三層架構：
- **Orchestrator**（最高層）：只思考、規劃、委派，不直接執行
- **Team Leads**：接收任務後再向下委派，也不直接寫檔案
- **Workers**：超專精執行單一任務（UI 生成、驗證、品牌分析等）

這個系統用來產生無限數量、品牌一致的 UI 原型，以 Aegis（代理安全指揮中心）品牌為示範案例。

## 多模型並行團隊設計

- A、B、C 三個 UI 生成團隊並行運作
- Team C：Claude Sonnet（可靠）
- Team A/B：Minimax 2.7 + Step 3.5 Flash（開源模型，本次示範中出現問題）
- 失敗時 Team Lead 自行接手執行，確保任務完成（till done list）

## Agent 記憶與專業化（Agent Experts）

每個 agent 都有自己的 **expertise 檔案**（mental model），持續追蹤：

- 已完成的工作
- 設計模式與偏好
- Ideas 與改進方向
- 內容約 7K tokens，完全由 agent 自主管理

Agent 設定檔（前置 frontmatter）的關鍵欄位：
```yaml
expertise_file: path/to/expertise.md
max_lines: 10000
skills:
  - mental_model
  - conversational_response
domain:
  read: ["**/*"]
  write: ["frontend/**"]
```

## Multi-Team 設定檔結構

```yaml
# multi-team-config.yaml
orchestrator:
  prompt: path/to/orchestrator.md
  model: claude-sonnet-4-6
teams:
  - name: ui_generation_a
    lead: path/to/lead_a.md
    members:
      - worker_view_generator
      - worker_animation_specialist
  - name: ui_generation_b
    ...
```

- 隨時可新增或移除 team（只改 config 即可）
- Orchestrator 知道如何 prompt 各 team（教會 orchestrator prompt engineering）

## 關鍵原則與 2026 主題

- **Solve problem classes, not tasks**：建立能解決一整類問題的系統，而非單次任務
- **Meta builder 思維**：80% 時間用 Claude Code 建立「建系統的系統」，20% 用專屬系統執行
- **Trust + Scale**：增加對 agents 的信任，才能擴展規模
- **一個 Orchestrator 對應多個 Teams**，認知投入不隨 agent 數量增加

## Agentic Security 商機

結合 Agents 與安全性將是未來幾年的巨大機會：
- Black hat agents 可造成嚴重破壞
- Agent security command center 類型的產品具有高商業價值
- 推薦工程師關注 agentic security 領域
