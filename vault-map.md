---
title: Vault Map
created: 2026-04-15
updated: 2026-05-27
tags:
  - index
---


## 資料夾索引

> 路徑以 repo root 為基準（即 vault root）。

```
.
├── Inbox/         — 待消化暫存（理想為空，消化完刪除）
│   ├── YouTube/   — 影片摘要暫存，依頻道分組；消化後刪原篇，各頻道留 01.index.md + .base（含 last_sync_id checkpoint）
│   │   ├── AIJasonZ/              — Claude 設計工作流、Skills、Agent 記憶體管理
│   │   ├── AILABS-393/            — Claude Code 進階技巧、RAG
│   │   ├── AgentcrewAcademy/      — Claude Code Windows 安裝、MCP 整合、Sub-Agent 與新手教學
│   │   ├── Chase-H-AI/            — Claude Code 實戰、RAG、Obsidian 整合
│   │   └── daveebbelaar/          — Python、LLM Evals、API 整合
│   ├── Clippings/ — 網頁剪貼暫存（消化後清空）
│   └── Updates/   — 日常更新彙整（vault-updates-daily skill 產出）
├── Cards/         — 未歸屬或待補事實審查的完整概念 Cards
└── Topics/        — 已歸檔主題（子目錄如下）
  ├── AI-Agent-工作流/ — Harness、frameworks、multi-agent workflow
  ├── Claude-Code/    — Skills、permissions、agent packages、日常操作
  ├── Obsidian/       — CLI 整合、Skills、Quartz 部署
  ├── UI設計/         — 設計工具、DESIGN.md 系統、視覺靈感
  ├── 前端技術/       — CSS、動效、捲動互動實作
  └── 部署/           — 上版工作流、本機環境、CI/CD 踩坑
```

## Tag 查詢指南

| 主題 | Tags | 位置 |
|------|------|------|
| Claude Code 實作 | `claude-code` | `Topics/Claude-Code/` + `Cards/` + `Inbox/YouTube/` |
| AI Agent 工作流 | `ai-agent` `agent-framework` `harness` | `Topics/AI-Agent-工作流/` + `Cards/` |
| Agent 協作 / 長任務 | `advisor` `agentic` `codex` `harness` | `Cards/` + `Topics/Claude-Code/` |
| RAG / 知識庫 | `rag` `agentic-rag` `hybrid-search` | `Cards/`（Production-RAG-架構） |
| LLM Evals / 評估 | `eval` | `Cards/`（LLM-Evals-方法論） |
| 記憶系統 / Context | `memory` `context-engineering` | `Cards/` |
| MCP | `mcp` | `Cards/` |
| 內容自動化 | `content-automation` | `Cards/` |
| 安全 | `security` `python` | `Cards/` |
| AI 職涯 / 商業 | `career` | `Cards/` |
| Obsidian 操作 | `obsidian` `cli` | `Topics/Obsidian/` + `Cards/` |
| UI 設計 / 設計工作流 | `design` `design-system` `frontend` | `Topics/UI設計/` + `Cards/` |
| 前端 / CSS / 動效實作 | `css` `flexbox` `animation` | `Topics/前端技術/` + `Cards/` |
| Docker / Laradock / CI3 | `docker` `laradock` `codeigniter` `本機環境` `sop` | `Cards/` |
| Windows / Git / CLI 工具 | `windows` `git` `cli` `workflow` | `Cards/` |
| 上版 / 部署 | `deploy` `quartz` | `Topics/部署/` + `Cards/` |
