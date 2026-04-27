---
title: Best GitHub repos for Claude Code
created: 2026-04-27
updated: 2026-04-27
source: https://www.reddit.com/r/ClaudeCode/comments/1ssimaz/best_github_repos_for_claude_code/
published: 2026-04-22
tags:
  - reddit
  - claude-code
  - ai-tools
---

> **繁中摘要**：作者試過 40+ skills/plugins/helpers，列出真正留下來的 4 個主力 + 5 個書籤；涵蓋 skill marketplace、repo 打包、parallel session 編排、token 消耗追蹤。

---

## 原文重點

**真正留下的（每天用）：**

- **awesome-claude-skills**（ComposioHQ，55.5k stars）— 規範性的 Claude Skills 清單，包含 PDF/Word/Excel/PPT、CSV 分析、brand voice、Composio 後端的 SaaS 整合，作者大部分要裝的 skill 都從這裡找
- **Repomix**（yamadashy，23.7k stars）— 把整個 repo 打包成單一檔案餵給 Claude，取代「複製貼上 15 個檔案」工作流
- **agent-orchestrator**（ComposioHQ，6.4k stars）— 跨 git worktree 跑 parallel Claude Code session，一個 agent 一個 feature branch，CI 自動接管
- **ccusage**（ryoppippi，13.2k stars）— CLI 印出每個 session 的 token 消耗，作者觀察「Claude 很貴」抱怨多半是沒看自己用量

**書籤（偶爾用）：**

- awesome-claude-code（40k）— 比 skills 清單更廣
- SuperClaude_Framework（22.4k）
- context-mode（8.8k）— 處理 MCP token 膨脹
- claude-code-system-prompts（9.3k）— 反向工程出來的 system prompts
- awesome-claude-plugins（ComposioHQ，1.4k）

## 社群討論亮點

- **OpenWolf**（`github.com/cytostack/openwolf`）— 6 個 hooks 提供 file index、learning memory、token ledger。Claude 不再重讀已開過的檔案、跨 session 記住使用者糾正、可看 token 流向。留言者表示是唯一真正降低觸頂速度的工具
- 也有人補充 Superpowers、gstack 沒被列入但討論度很高
