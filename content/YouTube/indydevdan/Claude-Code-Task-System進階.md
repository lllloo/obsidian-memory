---
title: Claude Code Task System：Anti-Hype 進階 Agentic Coding
tags:
  - youtube
  - claude-code
  - ai-agent
  - multi-agent
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-13
source: https://www.youtube.com/watch?v=4_2j5wgt_ds
parent: "[[01.index]]"
---

## 背景：為何值得關注

Claude Code Task System 因為被 Claw/Maltbot 熱潮掩蓋而沒有受到足夠重視，但它才是真正讓 agent 協作進化的核心功能。

核心進步：從「ad hoc sub-agents 沒有共同使命」升級為「有任務依賴、有通訊機制、有共同目標的 agent teams」。

## Task System 四個核心工具

| 工具 | 作用 |
|------|------|
| `task_create` | 建立任務，可設定依賴其他任務 |
| `task_list` | 列出所有任務與狀態 |
| `task_get` | 取得特定任務詳情 |
| `task_update` | **最重要**：sub-agent 用此回報工作完成，觸發 primary agent 響應 |

**關鍵改進**：Sub-agent 完成工作後 `task_update`，primary agent 即時收到事件，不需要 `bash sleep` 輪詢等待。任務有依賴關係（Task A 完成才能解鎖 Task B）。

## Template Meta-Prompt：`/plan-with-team`

這個 prompt 有三個核心能力：

### 1. Self-Validation（自我驗證）

Frontmatter 中定義 stop hooks，agent 完成後自動執行：

```bash
# validate-new-file：確認在正確目錄建立了正確類型的檔案
# validate-file-contains：確認檔案包含特定內容段落
```

如果驗證失敗，hook 會將錯誤訊息回饋給 agent，要求重試。

### 2. Agent Orchestration（team 組成）

Prompt 中 `team_orchestration` 區塊指導 primary agent 如何建立 team：

```markdown
## Team Orchestration
<!-- primary agent 讀取 .claude/agents/team/ 目錄下的可用 agents -->
<!-- 每個 team member 指定：name、role、agent_type、resume_on_failure -->
```

可用 agent 組合（最基礎的配對）：
- **Builder**：專注執行一個任務並回報
- **Validator**：確認 builder 的工作是否正確完成

作者實作：每個 hook 都有一對 builder + validator，例如：
- `session-end-builder` → `session-end-validator`
- `permission-request-builder` → `permission-request-validator`

Builder 自帶 micro-validation：`post_tool_use` hook 在寫入 Python 檔案後自動執行 `ruff` 和 `mypy`。

### 3. Templating（生成可執行的 plan）

Meta-prompt 不只建立計畫，而是**生成包含嵌入式 prompt 的計畫**：

```markdown
# 生成的 plan 格式（specs/hooks-update-with-team.md）：
- task_name: 任務名稱
- task_description: 任務描述（agent 填入）
- team_orchestration:
    members:
      - name: session-end-builder
        role: builder
        agent_type: builder
        resume_on_failure: true
      - name: session-end-validator
        role: validator
        ...
- step_by_step_tasks:
    - step 1: build（可並行）
    - step 2: build（可並行）
    - step 7: validate（依賴 steps 1-6 完成）
```

**Template Meta-Prompt 的意義**：生成另一個 prompt，且格式經過嚴格定義。Stop hook 確保生成的 plan 包含所有必要的段落，否則強制重試。

## 實際執行流程

```bash
# Step 1：用 meta-prompt 生成計畫
/plan          # 填入 user_prompt + orchestration_prompt

# user_prompt: "Update documentation and code for claude-code-hooks-mastery"
# orchestration_prompt: "create groups of agents for each hook, one builder and one validator"

# Step 2：執行計畫
/bu           # 載入生成的 plan，建立 task list，spawn agent team
```

執行結果：
- 6 個 builder tasks（並行）
- 6 個 validator tasks（依賴對應 builder 完成）
- 2 個文件更新 tasks

最終：新增 hooks 程式碼、更新 README、建立 JSON 設定檔。

## 架構升級路徑

```
Base Agent
  → Context + Prompt Engineering（更好地使用單個 agent）
  → 新增更多 Agents
  → 客製化 Agents（Self-Validation、Specialization）
  → Orchestrator Agent（使用 Task System 編排 team）
```

## 何時使用 Task System

**適合場景**：
- 需要並行執行多個獨立任務（如多個 hook 的建立）
- 任務之間有明確依賴關係
- 需要 build + validate 配對確保品質
- 希望 agent 完成後自動通知，不需人工輪詢

**錯誤的假設**：給更多 agents = 更好結果。正確的是：**組織良好、目標明確的 agents** > 數量多但混亂的 agents。

## 核心理念

> 「不要外包學習。如果你連 primitives 都不懂，當工具換掉時你什麼都不剩。」

Multi-agent orchestration 的本質仍是 **core four**：Context、Model、Prompt、Tools。
Maltbot/Cloudbot 等工具是這些 primitives 的包裝，理解底層才能在工具迭代中保持競爭力。
