---
title: Claude Code 多 Agent 協作
created: 2026-04-24
updated: 2026-04-25
tags:
  - claude-code
  - workflow
---

## Subagent vs Agent Teams vs Forked subagent

| | Subagent | Agent Teams | Forked subagent |
|---|---|---|---|
| Context | 獨立，不繼承主對話 | 各自獨立，可共享 task list / mailbox | 繼承主 session 對話 |
| 互相溝通 | 否，結果回主線 | 是，可彼此傳訊 | 否，最後回主線 |
| 啟動方式 | 自動 delegation 或明確指定 | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | `CLAUDE_CODE_FORK_SUBAGENT=1`（v2.1.117+），或 `/fork <任務>` |
| 適合場景 | 單點研究、單點審查、隔離輸出 | 多人分工、長任務、平行 review/fix | 中途開支線、不想重講背景 |

## `/branch` vs `/fork`

- `/branch` 是主命令（v2.1.77 改名自 `/fork`）；`/fork` 預設為向後相容 alias，兩者等效
- 開啟 `CLAUDE_CODE_FORK_SUBAGENT=1` 後，`/fork` 改為真正 spawn 一個 forked subagent，不再等於 `/branch`

## Git worktrees 平行 Agent

官方支援 worktree isolation：

- `claude --worktree feature-auth`
- subagent frontmatter 可設 `isolation: worktree`

每個 agent 各有自己的 working tree，避免互相覆蓋檔案。**subagent 若沒有留下變更，worktree 會自動清掉。**

## 來源

- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Forked subagents](https://code.claude.com/docs/en/sub-agents#fork-the-current-conversation)
- [Agent Teams](https://code.claude.com/docs/en/agent-teams)
