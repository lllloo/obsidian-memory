---
title: Vault Map
created: 2026-04-15
updated: 2026-07-17
tags:
  - index
---


## schema 層治理檔

> `CLAUDE.md`（+ `AGENTS.md` symlink）因 harness 從 repo root 自動載入而留在 root；敘述文件 `SYSTEM-DESIGN.md` 與本檔已移入 `schema/`。CWD 契約的哨兵檔是 `schema/vault-map.md`（本檔）——此路徑只存在於本 vault，能同時擋「不在 root」與「跑錯 repo」。
>
> **本表是 schema 各檔職責的單一權威清單。** 新增／移除 schema 檔只改這裡；`CLAUDE.md`、`SYSTEM-DESIGN.md` 概念性提及即可，不重列檔案清單（避免像過去 `BACKLOG.md` 那樣一處新增、他處漏同步的漂移）。

| 檔案 | 職責 |
|---|---|
| `CLAUDE.md`（root） | schema：agent 維護規則、三層架構、Ingest/Query/Lint、寫入慣例、唯一守門 git push（`AGENTS.md` 為其 symlink）；`@` 匯入 `MEMORY.md` |
| `schema/SYSTEM-DESIGN.md` | 運作總綱：Karpathy LLM Wiki 心智模型、人/AI 分工、刻意不做的事、skill 升級判準 |
| `schema/vault-map.md` | 本檔：全局導航與 tag 查詢地圖 |
| `schema/MEMORY.md` | 有界跨 session 操作記憶：skill 升級訊號追蹤、待辦開放問題（非治理規則、非 wiki 內容；checked-in 進 repo，是 vault 唯一跨工具可攜的操作記憶載體） |
| `schema/BACKLOG.md` | `vault-lint` 待處理清單：只收真需使用者的決策（待你決定／Agent 已判／已婉拒三區），agent 每輪讀回來約束自身行為（去重、解決即移除；頁面引用一律反引號、不用 wikilink） |

## 資料夾索引

> 路徑以 repo root 為基準（即 vault root）。agent 維護 `raw/` + `wiki/`，指定 skills 維護 `feeds/`；`cards/`、`topics/` 是使用者私人區，agent 不讀不寫不掃。

```
.
├── schema/      — schema 層：SYSTEM-DESIGN.md（運作總綱）、vault-map.md（本檔，導航）、MEMORY.md（跨 session 操作記憶）、BACKLOG.md（lint 待處理清單，agent 每輪讀回來約束自身行為）；CLAUDE.md/AGENTS.md 因 harness 自動載入留 root
├── raw/         — 原始來源，write-once。agent 可新增、不可修改，事實來源
│   ├── clippings/ — 使用者以 Web Clipper 或手動放入的來源（01.index.md + 清單.base 索引；agent 不主動消化，使用者明指才處理）
│   └── fetched/   — agent 依使用者提供 URL 擷取的來源（01.index.md + 清單.base 索引；落地後直接 ingest）
├── wiki/          — 活知識庫：agent 綜合 raw 維護的摘要/實體/概念/綜合頁（01.index.md 為內容目錄，每次 ingest 更新）
├── feeds/         — 【自動產物層，不屬三層系統】只供使用者瀏覽，不進 raw／wiki／ingest／query／lint
│   ├── youtube/   — YouTube 自動同步筆記；各頻道含 01.index.md + 02.影片清單.base，只供使用者瀏覽
│   ├── updates/   — 日常工具更新日報（vault-updates-daily 產出，01.index.md 為來源設定）
│   └── watch/     — GitHub issue/PR 追蹤看板與變更 digest（vault-watch 產出，01.index.md 為追蹤清單）
├── cards/         — 【使用者私人區，agent 不管理】使用者自存文件；Quartz 公開層之一
└── topics/        — 【使用者私人區，agent 不管理】使用者自存主題資料夾；Quartz 公開層之一
```

## Tag 查詢指南

> agent 查詢範圍只限 `raw/` + `wiki/`；`feeds/`、`cards/`、`topics/` 不在 agent 查詢範圍內。

| 主題 | Tags | 位置 |
|------|------|------|
| Claude Code 實作 | `claude-code` | `raw/` + `wiki/` |
| AI Agent 工作流 | `ai-agent` `agent-framework` `harness` | `wiki/` |
| 記憶系統 / Context | `memory`（僅 `wiki/`）、`context-engineering` | `wiki/` |
| RAG / 知識圖譜 | `rag` `knowledge-graph` | `wiki/` |
| Obsidian 操作 | `obsidian` | `wiki/` |
| LLM 定價 / coding agent | `llm-pricing` `coding-agent` | `wiki/` |
| 人類 PKM 方法論 | `pkm` `second-brain` | `wiki/` |

wiki 尚在成長，新主題頁隨 ingest 補入 `wiki/01.index.md`；查詢先讀該內容目錄再鑽細節。
