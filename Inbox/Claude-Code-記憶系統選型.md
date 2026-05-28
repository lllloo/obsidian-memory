---
title: Claude Code 記憶系統選型
created: 2026-05-27
updated: 2026-05-28
source: https://www.youtube.com/watch?v=UHVFcUzAGlM
published: 2026-04-24
tags:
  - claude-code
  - memory
  - context-engineering
---

搜尋「最佳 Claude Code 記憶系統」會被 Mem0、memsearch、ClaudeMem、MemPalace、LLM Wiki、OpenBrain 等淹沒。關鍵認知：**這些不是在競爭，是針對不同情境的不同解。** 每一套都回答同一個問題——給 Claude 任務時，如何在對的時機取得對的 context。

差異只有兩軸：

- **儲存在哪**：markdown vs vector database；本地 vs 雲端。
- **如何召回**：自動複製進 context vs 放 database 需要時才搜。

不要一開始就裝重的系統。從 L1 起步，遇到具體痛點才往上爬；L1–L3 可疊加共用，資料夾結構相近。

## 六層光譜與升級觸發

| 層 | 方案 | 機制 | 何時升上來 |
|---|---|---|---|
| **L1** 原生內建 | `CLAUDE.md` + automemory（`memory.md`） | session 啟動載入；automemory 背景記錄、以索引組織檔案 | 預設就用。CLAUDE.md ≤ 200 行當索引，大段內容（品牌語調等）拆外部檔引用，避免 context rot |
| **L2** 強制召回 | session start hook 自動注入記憶索引 | hook 在每次開 session / 子 agent 時把 `memory.md` 索引塞進 context，不靠 Claude 自己想起來去讀 | 常重複告訴 Claude 它早該知道的事。**多數人停在這層** |
| **L3** 語意搜尋 | memsearch（移植 openclaw）；替代：ClaudeMem | 內容分塊成語意向量，UserPromptSubmit hook 自動注入 top-N 語意匹配；markdown 優先、可讀可移植 | 用超過一個月、檔案多到關鍵字搜尋開始失效 |
| **L4** 逐字召回 | MemPalace（本地 RAG，記憶宮殿索引） | 逐字儲存不摘要，符號化索引讓模型一次掃過數千「抽屜」；session end / pre-compaction hook 背景索引 | 想找「當時到底決定了什麼」的**確切原文**，而非摘要 |
| **L5** 互聯知識庫 | Karpathy LLM Wiki；代管替代：Recall；企業級：LightRAG | `raw`（只讀來源）+ `wiki`（Claude 維護、人不寫）兩資料夾，純 markdown 建知識圖譜 | 定期消化要長期保存與連結的資訊（文章、影片、podcast），想建第二大腦。只隨意消化不回查就跳過 |
| **L6** 跨工具大腦 | OpenBrain（自有 Postgres）；Mem0 | MCP server 接 Postgres，ChatGPT / Claude / Cursor 共用同一記憶；面向未來可移植 | 要在多個 AI 工具間自由切換且共用記憶。單機只用 Claude Code 可跳過 |

## 選型 trade-off 軸

- **所有權**：本地 markdown（可讀、可移植、自己擁有）↔ 雲端代管（省設定，但租而非擁有，資料活在別人伺服器）。
- **召回方式**：自動注入（memsearch / MemPalace，免主動要求）↔ MCP 主動查詢（ClaudeMem，Claude 得自己決定呼叫工具，有延遲）。
- **可讀性**：markdown 隨時看得懂 ↔ vector / 逐字索引取回快但不能直接讀。

**本 vault 走的是 L5（Karpathy LLM Wiki）路線**——但做了吸收型調整，消化完刪原料，見 [[vault-model]]。

### L5 落地經驗

實作 L5（Obsidian + Claude Code）的兩條心得：

- **知識庫慢慢長出來、不一次到位**：從最小結構起步（如 projects + 連到生涯主線的 pillars），再按需求逐步加 decisions、日誌、週報、insight。
- **wikilink 由 AI 按語義代建、人不手動維護**：請 agent「按語義判斷哪些檔案有關係並加雙向連線」，連線夠密，AI 讀任一檔時就能沿連結跨讀相關內容——在恰好的時刻讀到恰好的 context，正是 L5 對抗 context rot 的方式。

## 相關

- [[Context-Engineering]] — context rot 與 auto memory 的底層概念
- [[vault-model]] — L5 LLM Wiki 的吸收型實作
