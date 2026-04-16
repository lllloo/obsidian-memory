---
title: Claude Code Multi-Agent 編排：Opus 4.6、Tmux 與 Agent Sandboxes
tags:
  - youtube
  - claude-code
  - multi-agent
created: 2026-04-13
updated: 2026-04-13
published: 2026-02-09
source: https://www.youtube.com/watch?v=RpUTF_U4kiw
parent: "[[01.index]]"
---

## 核心三元素

1. **Multi-Agent Orchestration**：Claude Code 新的 agent team 功能
2. **Multi-Agent Observability**：即時追蹤所有 agent 的行為
3. **Agent Sandboxes**：安全、可擴展的 agent 執行環境（E2B）

> 「模型已不再是限制。真正的限制是你和我——我們 prompt engineering 和 context engineering 的能力。」

## 啟用 Multi-Agent 功能

```bash
# 確認 claude 路徑
which claude

# 啟用 experimental agent teams 功能
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 在 Tmux 中啟動 Claude Code
tmux new-session
claude
```

**Tmux 的關鍵作用**：primary agent 創建 sub-agents 時，會自動開啟新的 **Tmux panes**，每個 agent 有獨立視窗，讓工程師可視覺化看到所有 agent 並行工作。

## Multi-Agent Observability 系統

在新的 Claude Code session 啟動時，hook 系統捕捉所有事件：

- `session:start` → 🚀 顯示新 session 開啟
- `session:end` → 顯示 session 結束
- Tool call 事件 → 記錄每個工具呼叫
- Task 相關事件 → 追蹤 task 建立、更新、完成

查看 observability dashboard：可過濾 swim lane，依 agent 追蹤工具呼叫序列。

## 實際操作流程

### 步驟 1：建立第一個 Agent Team

```
# 提示 primary agent
Build a new agent team for each codebase in this directory.
Have an agent summarize and how to set it up.
```

Primary agent 自動：
1. 建立 task list
2. 為每個 codebase 建立一個 sub-agent（Haiku 模型）
3. 每個 sub-agent 在獨立 Tmux pane 中執行
4. 完成後回報給 primary agent

結果：8 個 full-stack 應用的摘要，primary agent 只用了 **31% context window**（其他 context 分散在 sub-agents）。

### 步驟 2：Agent Sandbox 部署（E2B）

使用 Agent Sandbox skill 將應用部署到 E2B：

```
Build a new agent team using agent sandboxes.
Use the backslash reboot command.
Mount sandbox directories 1 through 4.
```

架構：
- Primary agent（Opus 4.6）負責編排
- 4 個 sub-agents（Opus 4.6）各自處理一個 sandbox
- 每個 agent 獨立 context window，執行 E2B setup、安裝依賴、啟動服務

### 步驟 3：兩組並行 Teams

同時在**兩個 Tmux session**中運行：
- Team 1：處理 sandbox 1-4
- Team 2：處理 sandbox 5-8
- 共 24 個 sandbox 環境同時運行

```bash
# 查看所有運行中的 sandboxes
claude + agent-sandbox skill
# "list all running sandboxes"
# 結果：24 個 sandbox 環境
```

## 新 Task System 工具

| 工具 | 說明 |
|------|------|
| `task` | 傳統 sub-agent 啟動工具（一直有） |
| `task_create` | 建立新任務（含依賴關係） |
| `task_list` | 列出所有任務與狀態 |
| `task_get` | 取得特定任務詳情 |
| `task_update` | 更新任務狀態，sub-agent 用此通知 primary |
| `team_create` | 建立 agent team |
| `team_delete` | 解散 team（強制 context reset） |
| `send_message` | agents 之間的通訊 |

**Task 依賴關係**：可設定任務 A 必須在任務 B 完成後才能開始執行，取代 `bash sleep` 輪詢。

## Multi-Agent Workflow 完整流程

```
1. 建立 team（team_create）
2. 建立 task list（含依賴關係）
3. Spawn agents（task tool）
4. Agents 並行工作
5. 完成後 send_message 通知 primary
6. Primary 接收事件，編排後續工作
7. 解散 team（team_delete，強制 context reset）
```

**為何要 team_delete**：強迫每輪工作重置 context，避免 context 污染，保持每個 agent 的專注度。

## Tmux 操作速查

```bash
# 進入 scroll mode
Ctrl+B [

# 上下滾動
↑ / ↓

# 退出 scroll mode
Escape

# 切換 pane（left）
Ctrl+B ←
```

## 關鍵結論

三個能力組合起來的威力：
- **Multi-Agent Orchestration** → 並行執行，規模化
- **Multi-Agent Observability** → 知道 agent 在做什麼，才是真工程師
- **Agent Sandboxes** → 安全執行，不影響本機

> 「Scale your compute to scale your impact。」
