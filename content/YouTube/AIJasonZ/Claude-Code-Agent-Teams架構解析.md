---
title: Claude Code Agent Teams 架構解析
tags:
  - youtube
  - claude-code
  - ai-agent
created: 2026-04-14
updated: 2026-04-14
published: 2026-02-07
source: https://www.youtube.com/watch?v=S2WTTMXYcYY
parent: "[[01.index]]"
---

## 與舊 Sub-agent 的差異

舊版 task tool：spin up sub-agent → 完成後 session 終止，只回傳摘要。

新版 Agent Teams：多個 Claude Code instance 協作，可互傳訊息、共享 task list、互相更新進度。

## 啟用方式

1. 更新 Claude Code 到 2.1.32+
2. 在 `settings.json` 加入：`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
3. 建議搭配 tmux/iTerm2 使用 split view：`claude --teammate --mode`

## 運作機制（新工具集）

### 建立流程

1. `team_create`：建立 team config，存在 `.claude/teams/`
2. `task_create`：建立任務清單（每個任務一個 JSON，含 subject、description、status、blocked_by）
3. `task_tool`（升級版）：帶 `team_name` 和 `name` 參數，不再只 spin up sub-agent，而是建立新的 Claude Code session

### 通訊機制

- 每個 agent 有 inbox（`.claude/teams/<id>/inbox/`）
- `send_message` 工具：
  - `message`：一對一訊息
  - `broadcast`：廣播給所有 agent
  - `shutdown_request`：team lead 終止特定 teammate
- 訊息以新 user message 形式注入對方 conversation history

### 任務管理

Sub-agent 可：
- `task_update`：更新任務狀態（pending/in_progress/complete/deleted）
- 新增 blocks/blocked_by 依賴關係
- 建立新任務（不限於接受原始 task list）

## 調試工具建議

使用 LangFuse（Anthropic 的 Claude Trace 已無法追蹤最新版）：
- 透過 Claude Code stop hook 自動將 session 資料同步到 LangFuse
- 可追蹤每次 LLM call 的 system prompt、工具、完整對話

## 應用場景範例

**多方向 Debug**：
- 對單一 bug，spin up 5 個 agent 各探索不同假設
- Agent 互相分享發現、挑戰彼此理論（科學辯論模式）
- 最終共識整理成 documentation
