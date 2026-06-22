---
title: Vault Map
created: 2026-04-15
updated: 2026-06-18
tags:
  - index
---


## 根層治理檔

| 檔案 | 職責 |
|---|---|
| `CLAUDE.md` | agent 執行規則：寫入前 checklist、frontmatter schema、Cards -> Topics 升級門檻（`AGENTS.md` 為其 symlink） |
| `SYSTEM-DESIGN.md` | 運作總綱：模式血緣、核心賭注、刻意不做的事（給人建立心智模型） |
| `card-quality.md` | 單張 Card 品質標準與反指標 |

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
│   ├── Clippings/ — 網頁剪貼參考庫（agent 不主動消化；使用者明指才處理）
│   ├── Archive/   — 封存區：已內化但保留備查的原料（agent 不主動掃描/消化/刪除；使用者明指才處理）
│   └── Updates/   — 日常更新彙整（vault-updates-daily skill 產出）
├── Cards/         — 未歸屬的完整概念 Cards
└── Topics/        — 已歸檔主題（子目錄如下）
  ├── AI-Agent-工作流/ — Harness、frameworks、multi-agent workflow
  │   ├── Spec-Kit/    — GitHub spec-driven toolkit，spec 驅動生 code
  │   ├── OpenSpec/    — Fission-AI 輕量 spec-driven，"Actions not phases"
  │   ├── BMAD/        — agile lifecycle 多 agent persona（PM／Architect／Dev…）
  │   ├── GStack/      — planning／design／QA／ship 多 persona workflow
  │   └── Superpowers/ — TDD gate／系統化除錯／review loop
  ├── Claude-Code/    — Skills、permissions、agent packages、日常操作
  ├── Obsidian/       — CLI 整合、Skills、Quartz 部署
  ├── UI設計/         — 設計工具、DESIGN.md 系統、視覺靈感
  ├── 前端技術/       — CSS、動效、捲動互動實作
  │   └── issues/      — 跨瀏覽器／裝置的前端疑難（iOS Safari、LINE WebView、EXIF…）
  └── 環境與部署/      — 本機開發環境 → 上版發佈 → CI/CD 整條交付鏈
      ├── 本機開發環境/ — Laradock / Docker Compose 把專案在本機跑起來
      ├── 上版發佈/     — git-archive 交付、靜態站發佈
      └── CI-CD/        — GitHub Actions secrets、Discord CI 通知
```

## Tag 查詢指南

| 主題 | Tags | 位置 |
|------|------|------|
| Claude Code 實作 | `claude-code` | `Topics/Claude-Code/` + `Cards/` + `Inbox/YouTube/` |
| AI Agent 工作流 | `ai-agent` `agent-framework` `harness` | `Topics/AI-Agent-工作流/` + `Cards/` |
| 記憶系統 / Context | `memory` `context-engineering` | `Cards/` |
| MCP | `mcp` | `Topics/UI設計/`（附於 Pencil / Stitch 等 MCP 工具書籤；尚無獨立 MCP 主題筆記） |
| Obsidian 操作 | `obsidian` `cli` `quartz` | `Topics/Obsidian/` + `Cards/` |
| UI 設計 / 設計工作流 | `design` `design-system` `frontend` | `Topics/UI設計/` + `Cards/` |
| 前端 / CSS / 動效實作 | `css` `flexbox` `animation` | `Topics/前端技術/` + `Cards/` |
| Docker / Laradock / CI3 | `docker` `laradock` `codeigniter` `本機環境` `sop` | `Topics/環境與部署/` + `Cards/` |
| Windows / Git / CLI 工具 | `windows` `git` `cli` `workflow` | `Cards/` |
| 上版 / 部署 | `deploy` | `Topics/環境與部署/` + `Cards/` |
| GitHub Actions / CI 通知 | `github-actions` `discord` | `Topics/環境與部署/` |
