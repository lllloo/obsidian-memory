---
title: Claude Code 很強大…直到它刪掉 Production：Damage Control 防護系統
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 
source: https://www.youtube.com/watch?v=VqDs46A8pqE
parent: "[[01.index]]"
---

## 問題背景

Agent 在 production codebase 上運行時，只需一次 hallucination 就可能執行毀滅性指令（刪除 DB、rm 整個 git repo 等）。本影片展示用 Claude Code Hooks 建立「Damage Control」防護系統。

## 四種 Hook 防護機制

### 1. PreToolUse Prompt Hook（AI 智慧攔截）

- 對**所有** Bash 指令執行 LLM 判斷：是否為危險指令？
- 可攔截「從未見過的危險指令」（不依賴硬編碼規則）
- 缺點：每次 Bash 呼叫都會變慢
- 定位：最後一道防線；一旦找到某危險指令，立即轉為確定性規則

### 2. PreToolUse Deterministic Hook（確定性阻擋）

- 以 `patterns.yaml` 管理禁止指令的 regex 清單
- 設定方式：

```yaml
# patterns.yaml
blocked_commands:
  - "rm -rf"
  - "DROP TABLE"
  - "git push --force"
ask_patterns:
  - pattern: "DELETE FROM"
    ask: true
zero_access_paths:
  - ".ssh/"
read_only_paths:
  - ".bashrc"
no_delete_paths:
  - ".claude/hooks/"
  - ".claude/commands/"
```

### 3. PreToolUse Ask（詢問確認）

- 設定 `ask: true` → agent 執行前會先問你是否同意
- 可回答 skip 跳過或確認執行

### 4. 路徑存取保護

三個層級：
- **zero_access_paths**：完全禁止任何讀寫存取（如 `.ssh/`）
- **read_only_paths**：可讀不可寫（如 `.bashrc`）
- **no_delete_paths**：可讀寫但不可刪除（如 `.claude/hooks/`）

## Damage Control Skill 結構

```
claude-code-damage-control/
  skill/
    cookbook.md          # 安裝 agentic workflow
    patterns.yaml        # 危險指令與路徑規則
    bash-tool-damage-control.py   # PreToolUse 腳本
    write-tool-damage-control.py  # Write 工具保護
    edit-tool-damage-control.py   # Edit 工具保護
```

安裝方式：

```bash
git clone <repo>
cd <codebase>
# 複製 skill 目錄進來，或
claude code  # 然後 /install
```

`/install` 流程：
1. 詢問安裝層級（global / project / personal）
2. 詢問語言（Python / TypeScript/Bun）
3. 偵測既有 settings.json → merge 或 override
4. 寫入 hooks 設定

## Hook 層級（Claude Code 架構）

優先順序（高到低）：
1. Enterprise level
2. User level（Global）
3. Project level（`.claude/settings.json`）
4. Local level（`.claude/settings.local.json`）

**建議**：至少設定 global + project 兩層，確保任何 codebase 都有基礎防護。

## 核心原則

- Agent sandboxes 可完全「延後信任」問題（讓 agent 跑自己的機器）
- Hooks = 不需要信任的信任機制
- Prompt hook 比 deterministic hook 慢，但能攔截未知危險指令
- 100,000 次 tool calls 裡只需一次 hallucination 就能毀掉一切
