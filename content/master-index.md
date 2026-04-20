---
title: Master Index
created: 2026-04-15
updated: 2026-04-20
tags:
  - index
---

## 資料夾索引

```
content/
├── Cards/         — 快速筆記（CSS、Docker、設計工具等）
├── Clippings/     — 網頁剪貼
├── Topics/        — 主題 MOC，3 個子目錄
│   ├── Claude-Code/   — Skills、Agent Packages、Hooks、GAN Harness
│   ├── Obsidian/      — CLI 整合、Skills、Quartz 部署
│   └── 切版/          — Pencil 讀取規則、Flexbox、Border 規則
└── YouTube/       — 92 篇影片摘要，5 個頻道
    ├── AIJasonZ/              — Claude 設計工作流、Skills、Agent 記憶體管理
    ├── AILABS-393/            — Claude Code 進階技巧、OpenClaw、RAG
    ├── Chase-H-AI/            — Claude Code 實戰、RAG、Obsidian 整合
    ├── EricWTech/             — Claude Code 自動化、Skill 系統
    ├── daveebbelaar/          — Python、AI Agent 工程、LLM Evals
```

## Tag 查詢指南

| 主題 | Tags | 篇數 |
|------|------|------|
| Claude Code 實作 | `claude-code` | 29 |
| AI Agent 架構 | `ai-agent` | 7 |
| RAG / 知識庫 | `rag` | 2 |
| MCP | `mcp` | 1 |
| 其他 | `memory` `design` | 1 / 3 |
| Obsidian 操作 | `obsidian` `cli` | Topics/ + Cards/ |
| 前端 / CSS | `css` `flexbox` | Cards/ |

## 查詢策略

- **主題明確** → 先查 `Topics/` 對應子目錄
- **找影片摘要** → 依頻道特性選 `YouTube/<頻道>/`
- **跨主題** → Grep 搜尋 tag（`tags:.*<tag名稱>`）
