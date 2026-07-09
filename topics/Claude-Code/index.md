---
title: Claude Code
description: Claude Code 本體能力的長期筆記：規則系統、權限、skills、多 agent 協作與日常操作慣例
created: 2026-04-25
updated: 2026-06-22
tags:
  - claude-code
---

以 Claude Code 本體能力、skills、agents、permissions 與日常工作流為主的筆記集合。

## 核心能力與日常操作

- [[Claude-Code-規則系統設計]] — CLAUDE.md / Rules / Hooks 三層機制與升級路徑
- [[Claude-Code-雙帳號設定]] — 用 `CLAUDE_CONFIG_DIR` 在同機切換多帳號
- [[Claude-Code-CLI-優先]] — 工具整合優先選 CLI 退而選 MCP（架構 / Token / 生態三層論述）
- [[Claude-Code-Dangerously-Skip-Permissions]] — `--dangerously-skip-permissions` 該用 / 不該用 / 替代決策
- [[Claude-Code-完成提示-Windows-方案比較]] — 多視窗時用 OSC 9;4 工作列進度條 inline 在 hooks，及 OSC 2／OSC 9 等備選方案比較
- [[Claude-Code-Skill-Command-命名]] — kebab-case + 同家族前綴 + 動名詞偏好
- [[Claude-Code-Review-工作流]] — PR 規模分層跑 review 工具的決策表
- [[Claude-Code-多-Agent-協作]] — Subagent / Agent Teams / Forked subagent / worktrees 該怎麼選
- [[Claude-Code-Skills]] — Skill 概念定位、立場（vs MCP / token 是 bonus / 不是所有重複都該包）、陷阱

## 工具書籤

- [[bookmark-codex-plugin-cc-Codex整合外掛|codex-plugin-cc]] — OpenAI 出的 Claude Code plugin，做跨模型 review / task delegation
- [[Skills-跨工具安裝]] — vercel-labs/skills：一份 skill 經 symlink 多工具共用（Claude Code／Copilot／OpenCode），暫放 cards 待累積
