---
title: Claude Tasks 的 Agent Swarm 升級令人難以置信
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-27
source: https://www.youtube.com/watch?v=li8bIt-mjbA
---

## 重點摘要

- Anthropic 更新引入 agent swarm 到 Claude Code，支援自動任務分解與平行執行
- 主協調器建立 dependency graph，生成 Claude Code subagents 同時處理工作
- 每個 subagent 擁有獨立的 200K context window，解決複雜專案中 context 流失問題
- 實測：原本需要 16 個循序步驟的工作縮減為 1 個平行步驟
- 可設定 CLI flags 讓 session 在終端重啟後保持
- 介紹 Cowork 工具：基於 Claude Code 的 task 系統，但面向非技術用戶
- 影片對比了 claude code vs cursor 與 opencode vs claude code 的適用場景
