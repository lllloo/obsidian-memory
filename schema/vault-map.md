---
title: Vault Map
created: 2026-04-15
updated: 2026-10-13
tags:
  - index
---


## schema 層治理檔

> `AGENTS.md` 因 harness 從 repo root 自動載入而留在 root；敘述文件 `SYSTEM-DESIGN.md` 與本檔已移入 `schema/`。CWD 契約的哨兵檔是 `schema/vault-map.md`（本檔）——此路徑只存在於本 vault，能同時擋「不在 root」與「跑錯 repo」。
>
> **本表是 schema 各檔職責的單一權威清單。** 新增／移除 schema 檔只改這裡；`AGENTS.md`、`SYSTEM-DESIGN.md` 概念性提及即可，不重列檔案清單（避免像過去 `BACKLOG.md` 那樣一處新增、他處漏同步的漂移）。

| 檔案 | 職責 |
|---|---|
| `AGENTS.md`（root） | schema：agent 維護規則、三層架構、Ingest/Query/Lint、寫入慣例；`@` 匯入 `MEMORY.md`。本 repo **刻意不設 `CLAUDE.md`**——Claude Code 自 v2.1.277 起在沒有 `CLAUDE.md` 時原生讀 `AGENTS.md`，而任何位於本目錄或上層的 `CLAUDE.md`／`CLAUDE.local.md` 都會把本檔整份擋掉（2026-09-21 使用者拍板，原 `AGENTS.md`→`CLAUDE.md` symlink 一併移除） |
| `schema/SYSTEM-DESIGN.md` | 運作總綱：Karpathy LLM Wiki 心智模型、人/AI 分工、刻意不做的事、skill 升級判準 |
| `schema/vault-map.md` | 本檔：全局導航與 tag 查詢地圖 |
| `schema/MEMORY.md` | 有界跨 session 操作記憶：skill 升級訊號追蹤、待辦開放問題（非治理規則、非 wiki 內容；checked-in 進 repo，是 vault 唯一跨工具可攜的操作記憶載體） |
| `schema/BACKLOG.md` | `vault-lint` 待處理清單：只收真需使用者的決策（待你決定／Agent 已判／已婉拒三區），agent 每輪讀回來約束自身行為（去重、解決即移除；頁面引用一律反引號、不用 wikilink） |

## 資料夾索引

> 路徑以 repo root 為基準（即 vault root）。agent 維護 `raw/` + `wiki/`，指定 skills 維護 `feeds/`；私人筆記已搬到 Notion，入口見下方「外部私人筆記」。

```
.
├── schema/      — schema 層：SYSTEM-DESIGN.md（運作總綱）、vault-map.md（本檔，導航）、MEMORY.md（跨 session 操作記憶）、BACKLOG.md（lint 待處理清單，agent 每輪讀回來約束自身行為）；AGENTS.md 因 harness 自動載入留 root
├── raw/         — 原始來源，write-once。agent 可新增、不可修改，事實來源
│   ├── clippings/ — 使用者以 Web Clipper 或手動放入的來源（01.index.md + 清單.base 索引；agent 不主動消化，使用者明指才處理）
│   └── fetched/   — agent 依使用者提供 URL 擷取的來源（01.index.md + 清單.base 索引；落地後直接 ingest）
├── wiki/          — 活知識庫：agent 綜合 raw 維護的摘要/實體/概念/綜合頁（01.index.md 為內容目錄，每次 ingest 更新）
├── feeds/         — 【自動產物層，不屬三層系統】只供使用者瀏覽，不進 raw／wiki／ingest／query／lint
│   ├── youtube/   — YouTube 自動同步筆記；各頻道含 01.index.md + 02.影片清單.base，只供使用者瀏覽
│   └── watch/     — GitHub issue/PR 追蹤看板與變更 digest（vault-watch 產出，01.index.md 為追蹤清單）
└── docs/          — 【呈現層，不屬三層系統】
    └── architecture/ — 有長期回看價值的非 markdown 產出（單檔 HTML 圖／報告，01.index.html 為入口），納版控；agent 可自主建立更新，不進 ingest／query／lint，不對外發佈
```

## 外部私人筆記

[Obsidian 搬入筆記](https://app.notion.com/p/3f888d8b63ed818aac70e7035b8ed7c5) 是原 topics/cards 的新家。2026-10-13 完成遷移：topics 87 篇、cards 13 篇，共 100 篇；98 篇新增、2 篇沿用既有頁。共用資料庫，topics/cards 子頁面各自篩選來源；保留原文、標籤與原始 Markdown 附件，入口另附原始路徑與 Notion URL 的遷移對照表。逐篇回讀與附件比對後，本地原檔已刪除。

Notion 私人筆記不參與本 vault 的 Ingest／Query／Lint，不重新建立本地 topics/cards。`feeds/` 與 `docs/architecture/` 的搬離目的地仍待決定，目前維持原處。

## Tag 查詢指南

> agent 查詢範圍只限 `raw/` + `wiki/`；`feeds/` 與 Notion 私人筆記不在 vault Query 範圍內。

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
