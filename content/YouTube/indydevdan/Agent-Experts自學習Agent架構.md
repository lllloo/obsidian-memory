---
title: Agent Experts：終於出現了真正會學習的 Agents
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 
source: https://www.youtube.com/watch?v=zTcDwqopvKE
---

## 核心問題：Agents 會忘記

當前 agents 的最大問題：**執行後遺忘，不會自動學習**。

現有解法的缺陷：
- Memory files：全域強制載入的靜態 context，需手動更新
- Prime prompts、sub agents、skills：同樣需手動維護

## Agent Expert 的定義

| 一般 Agent | Agent Expert |
|-----------|-------------|
| 執行後遺忘 | 執行後學習 |
| 每次需重新 boot | 累積並管理自己的專業知識 |
| 手動更新 memory | 自動在 runtime 更新心智模型 |

**Agent Expert** = 能自動將行動轉化為專業知識並複用的 self-improving meta-prompt。

## Meta-Agentics（基礎）

三種 meta 工具（會建造工具的工具）：

- **Meta Prompt**：寫 prompts 的 prompt（生成 question prompt、plan prompt 等）
- **Meta Agent**：建造 agents 的 agent（生成新 sub agent）
- **Meta Skill**：建造 skills 的 skill（生成 orchestrator skill）

注意：Meta-agentics 本身不是 Agent Expert，因為它們**不會自動學習**——需手動觸發。

每個 codebase 都應該有 meta-agentics。

## Expertise 檔案（心智模型）

```yaml
# .claude/experts/database/expertise.yaml
# Agent Expert 的「心智模型」
# 不是 source of truth（source of truth = 程式碼）
# 而是 working memory —— 隨 codebase 演化的動態理解
entity_relationships:
  ...
information_flow_patterns:
  ...
```

Agent Expert 的工作流程：
1. 先讀取 `expertise.yaml`（自己的心智模型）
2. 對照程式碼驗證假設
3. 執行任務
4. 執行 `self-improve` 步驟，更新 expertise 檔案

## 三步驟工作流（Agent Expert 版）

```
/plan → build → self-improve
```

1. **Plan**：根據 expertise 制定計畫（~80K tokens，由 sub agent 處理）
2. **Build**：執行計畫（sub agent，context 隔離）
3. **Self-Improve**：讀取 git diff，更新 expertise 檔案反映變化

Top-level orchestrator 的 context 始終受保護（只傳 plan/diff，不傳整個歷史）。

## 並行 Agent Experts

```
/question --agents=3 --domain=websocket "what websocket events exist?"
```

- 3 個 WebSocket Expert 並行回答同一問題
- 即使某個 agent 失敗，其他完成的結果可互補
- 組合結果 → 比單一 agent 更高信心

61K tokens，41 tool uses 完成功能開發 + expertise 更新。

## 核心洞見

- Agent Expert 使 agents 能「一次設定，持續學習」
- 心智模型（expertise YAML）≠ source of truth；是 working memory
- 一切仍回歸 Core Four：Context × Model × Prompt × Tools
- 三次重複 = 一個模式 → 移入自動化（meta-expert 生成 experts）
