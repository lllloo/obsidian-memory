---
title: Claude Code 資深工程師常忽略的 Hooks 功能：專門化自我驗證 Agent
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 
source: https://www.youtube.com/watch?v=u5GkG71PkR0
---

## 核心概念

Claude Code 新功能：可在 custom slash commands、sub agents、skills 的 frontmatter 中直接宣告 hooks，讓 agent 在每次 tool use 後自動執行驗證腳本——即「專門化自我驗證」。

驗證可信度 = 節省時間，信任是工程資源中最貴重的。

## Hook 類型

- `preToolUse`：工具呼叫前執行
- `postToolUse`：工具呼叫後執行（最常用）
- `stop`：agent 完成後執行

支援於：custom slash commands、sub agents、skills

## Prompt/Slash Command 中宣告 Hook

在 `.claude/commands/csv-edit.md` 的 frontmatter 加入：

```yaml
---
# ... 其他設定 ...
hooks:
  postToolUse:
    - match: [Read, Write, Edit]
      command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/csv-single-validator.py"
---
```

- 省略 `once: true` → 每次 tool use 後都執行（持續自我驗證）
- Validator 腳本輸出 log 檔，供 agent 讀取錯誤並自動修正

## 驗證腳本設計

```python
# csv-single-validator.py
import pandas as pd
# 驗證 CSV 格式
# 若有錯誤，輸出: "Resolve this CSV error in <path>: <errors>"
```

關鍵：validator 的回傳訊息要直接指示 agent 如何修復（not just "error found"，而是「去修正這個路徑的這個問題」）。

## Sub Agent 中的 Hooks

Sub agents 在 `.claude/agents/` 中定義，hook 格式相同。

Sub agents 額外優勢：
- **平行化**：同時部署多個 agent 處理不同檔案
- **Context 隔離**：每個 agent 有獨立的 context window

範例：4 個 CSV edit agents 並行執行，各自在完成後自我驗證。

## 目錄結構建議

```
.claude/
  commands/
  agents/
  skills/
  hooks/
    validators/
      csv-single-validator.py
      html-validator.py
      ...
```

## 完整 Agent Pipeline 範例（Finance Review）

多層 agent 鏈，每層都帶自己的 validator：

- `categorize-csv-agent` → CSV validator
- `generative-ui-agent` → HTML validator
- `merge-accounts-agent` → CSV validator
- `normalize-csv-agent` → 兩個 validators

Stop hook 策略：在 stop 時執行全域驗證，掃描 codebase 所有目標檔案。

## 核心原則

- 專注型 agent（單一職責）遠優於通才型 agent
- Agents + Code > Agents alone
- Hooks 保證驗證一定執行，不依賴 prompt 引導
- 用 `--p settings.json` flag 可在 primary agent 啟動時注入完整 settings（含 hooks）

> 不要把學習外包給 agent——理解底層機制才能正確教會 agent 做驗證。
