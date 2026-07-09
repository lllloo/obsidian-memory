---
title: Vault Map
created: 2026-04-15
updated: 2026-07-09
tags:
  - index
---


## schema 層治理檔

> `CLAUDE.md`（+ `AGENTS.md` symlink）因 harness 從 repo root 自動載入而留在 root；敘述文件 `SYSTEM-DESIGN.md` 與本檔已移入 `schema/`。CWD 契約的哨兵檔是 `schema/vault-map.md`（本檔）——此路徑只存在於本 vault，能同時擋「不在 root」與「跑錯 repo」。

| 檔案 | 職責 |
|---|---|
| `CLAUDE.md`（root） | schema：agent 維護規則、三層架構、Ingest/Query/Lint、寫入慣例、唯一守門 git push（`AGENTS.md` 為其 symlink） |
| `schema/SYSTEM-DESIGN.md` | 運作總綱：Karpathy LLM Wiki 心智模型、人/AI 分工、刻意不做的事 |
| `schema/vault-map.md` | 本檔：全局導航與 tag 查詢地圖 |

## 資料夾索引

> 路徑以 repo root 為基準（即 vault root）。agent 只維護 `raw/` + `wiki/`；`cards/`、`topics/` 是使用者私人區，agent 不讀不寫不掃。

```
.
├── schema/      — schema 層敘述文件：SYSTEM-DESIGN.md（運作總綱）、vault-map.md（本檔，導航）；CLAUDE.md/AGENTS.md 因 harness 自動載入留 root
├── raw/         — 不可變原始來源。agent 只讀不改，事實來源
│   ├── YouTube/   — 影片摘要，依頻道分組；各頻道 01.index.md + 02.影片清單.base 索引（含 last_sync_id checkpoint）
│   │   ├── AIJasonZ/              — Claude 設計工作流、Skills、Agent 記憶體管理
│   │   ├── AILABS-393/            — Claude Code 進階技巧、RAG
│   │   ├── AgentcrewAcademy/      — Claude Code Windows 安裝、MCP 整合、Sub-Agent 與新手教學
│   │   ├── Chase-H-AI/            — Claude Code 實戰、RAG、Obsidian 整合
│   │   └── daveebbelaar/          — Python、LLM Evals、API 整合
│   ├── Clippings/ — 網頁剪貼參考庫（01.index.md + 清單.base 索引；agent 不主動消化，使用者明指才處理）
│   └── Archive/   — 封存區：保留備查的原料（01.index.md + 清單.base 索引；agent 不主動掃描/消化/刪除）
├── wiki/          — 活知識庫：agent 綜合 raw 維護的摘要/實體/概念/綜合頁（01.index.md 為內容目錄，每次 ingest 更新）
├── updates/       — 【獨立消費層，不屬三層系統】日常工具更新日報（vault-updates-daily 產出，01.index.md 為來源設定；使用者瀏覽用，agent 不 ingest／query／lint）
├── cards/         — 【使用者私人區，agent 不管理】使用者自存文件；Quartz 公開層之一
└── topics/        — 【使用者私人區，agent 不管理】使用者自存主題資料夾；Quartz 公開層之一
```

## Tag 查詢指南

> agent 查詢範圍是 `raw/` + `wiki/`。`cards/`、`topics/` 屬使用者私人區，不在 agent 查詢範圍內。

| 主題 | Tags | 位置 |
|------|------|------|
| Claude Code 實作 | `claude-code` | `raw/` 各區 + `wiki/` |
| AI Agent 工作流 | `ai-agent` `agent-framework` `harness` | `raw/YouTube/` + `raw/Archive/` + `wiki/` |
| 記憶系統 / Context | `memory`（僅 `wiki/`）、`context-engineering` | `raw/YouTube/` + `raw/Archive/` + `wiki/` |
| RAG / 知識圖譜 | `rag` `knowledge-graph` | `raw/YouTube/` + `wiki/` |
| Obsidian 操作 | `obsidian` | `raw/YouTube/` + `wiki/` |
| CLI / 部署類封存 | `cli` `deploy` `github-actions` | `raw/Archive/` |
| Python / LLM 評測 | `python` `llm-eval` `llm-as-a-judge` | `raw/YouTube/daveebbelaar/` |
| LLM 定價 / coding agent | `llm-pricing` `coding-agent` | `wiki/` |
| 日常工具更新 | 見 `updates/01.index.md` | `updates/` |

wiki 尚在成長，新主題頁隨 ingest 補入 `wiki/01.index.md`；查詢先讀該內容目錄再鑽細節。
