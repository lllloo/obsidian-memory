---
title: Master Index
created: 2026-04-15
updated: 2026-04-29
tags:
  - index
---


## 資料夾索引

```
content/
├── Inbox/         — 待消化暫存（理想為空，消化完刪除）
│   ├── YouTube/   — 影片摘要，依頻道分組
│   │   ├── AIJasonZ/              — Claude 設計工作流、Skills、Agent 記憶體管理
│   │   ├── AILABS-393/            — Claude Code 進階技巧、RAG
│   │   ├── Chase-H-AI/            — Claude Code 實戰、RAG、Obsidian 整合
│   │   └── daveebbelaar/          — Python、LLM Evals、API 整合
│   └── Clippings/ — 網頁剪貼
├── Cards/         — 未歸屬或待補事實審查的完整概念 Cards
└── Topics/        — 已歸檔主題，5 個子目錄
  ├── AI-Agent-工作流/ — Harness、frameworks、multi-agent workflow
  ├── Claude-Code/    — Skills、permissions、agent packages、日常操作
  ├── Obsidian/       — CLI 整合、Skills、Quartz 部署
  ├── UI設計/         — 設計工具、DESIGN.md 系統、視覺靈感
  └── 前端技術/       — CSS、動效、捲動互動實作
```

## Tag 查詢指南

| 主題 | Tags | 位置 |
|------|------|------|
| Claude Code 實作 | `claude-code` | `Topics/Claude-Code/` + `Cards/` + `Inbox/YouTube/` |
| AI Agent 工作流 | `ai-agent` `agent-framework` `harness` | `Topics/AI-Agent-工作流/` + `Cards/` |
| RAG / 知識庫 | `rag` | `Inbox/YouTube/daveebbelaar/` |
| MCP | `mcp` | `Cards/` |
| Obsidian 操作 | `obsidian` `cli` | `Topics/Obsidian/` + `Cards/` |
| UI 設計 / 設計工作流 | `design` `design-system` `frontend` | `Topics/UI設計/` + `Cards/` |
| 前端 / CSS / 動效實作 | `css` `flexbox` `animation` | `Topics/前端技術/` + `Cards/` |
| 記憶系統 | `memory` | `Cards/` |
| Docker / Laradock / CI3 | `docker` `laradock` `codeigniter` `本機環境` `sop` | `Cards/` |

## 查詢策略

- **主題明確** → 先查 `Topics/` 對應子目錄
- **Agent / workflow 問題** → 先查 `Topics/AI-Agent-工作流/`
- **找影片摘要** → 依頻道特性選 `Inbox/YouTube/<頻道>/`
- **跨主題** → Grep 搜尋 tag（`tags:.*<tag名稱>`）
