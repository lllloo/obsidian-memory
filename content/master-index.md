---
title: Master Index
created: 2026-04-15
updated: 2026-04-24
tags:
  - index
---


## 資料夾索引

```
content/
├── Inbox/         — 待消化暫存（理想為空，消化完刪除）
│   ├── YouTube/   — 影片摘要，依頻道分組
│   │   ├── AIJasonZ/              — Claude 設計工作流、Skills、Agent 記憶體管理
│   │   ├── AILABS-393/            — Claude Code 進階技巧、OpenClaw、RAG
│   │   ├── Chase-H-AI/            — Claude Code 實戰、RAG、Obsidian 整合
│   │   └── daveebbelaar/          — Python、LLM Evals、API 整合
│   └── Clippings/ — 網頁剪貼
├── Cards/         — 未歸屬的完整概念 Cards（工作區）
└── Topics/        — 已歸檔主題，3 個子目錄
    ├── Claude-Code/   — Skills、Agent Packages、Hooks、GAN Harness
    ├── Obsidian/      — CLI 整合、Skills、Quartz 部署
    └── 前端設計/      — 工作流、Stitch、動效、設計系統、切版規則
```

## Tag 查詢指南

| 主題 | Tags | 位置 |
|------|------|------|
| Claude Code 實作 | `claude-code` | `Topics/Claude-Code/` + `Inbox/YouTube/` |
| RAG / 知識庫 | `rag` | `Inbox/YouTube/daveebbelaar/` |
| MCP | `mcp` | `Topics/前端設計/` |
| Obsidian 操作 | `obsidian` `cli` | `Topics/Obsidian/` + `Cards/` |
| 前端 / 設計 | `design` `css` `flexbox` | `Topics/前端設計/` + `Cards/` |
| 記憶系統 | `memory` | `Cards/` |
| Docker / Laradock / CI3 | `docker` `laradock` `codeigniter` `本機環境` `sop` | `Cards/` |

## 查詢策略

- **主題明確** → 先查 `Topics/` 對應子目錄
- **找影片摘要** → 依頻道特性選 `Inbox/YouTube/<頻道>/`
- **跨主題** → Grep 搜尋 tag（`tags:.*<tag名稱>`）
