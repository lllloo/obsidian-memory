---
title: LLM Wiki 知識管理模式
description: Karpathy 提出的個人知識庫模式：LLM 漸進維護一套互聯 markdown wiki，把知識編譯一次後持續維護，與每次查詢重新檢索的 RAG 形成對比
created: 2026-07-08
updated: 2026-07-16
parent: "[[wiki/01.index]]"
tags:
  - wiki
  - knowledge-graph
  - obsidian
  - rag
---

# LLM Wiki 知識管理模式

Andrej Karpathy 提出的個人知識庫 pattern：不是每次查詢才臨時檢索原始文件，而是讓 LLM **漸進建立並持續維護一套互聯的 markdown wiki**，夾在使用者與原始來源之間。知識被編譯一次後持續更新，是會複利累積的資產。來源見 [[LLM-Wiki-Karpathy]]。

> 本 vault（obsidian-memory）就是這個 pattern 的實作。以下是原文提煉；本 repo 的具體規範見根目錄 schema 文件。

## 與 RAG 的核心差異

一般 RAG（NotebookLM、ChatGPT 檔案上傳等）在每次提問時從原始 chunk 重新檢索、重新拼湊答案——知識**不累積**，每個問題都從零重新發現。需要綜合五份文件的細膩問題，每次都得重新找、重新拼。

LLM Wiki 相反：新來源進來時，LLM 讀它、抽取重點、**整合進既有 wiki**——更新實體頁、改寫主題摘要、標記新資料與舊主張的矛盾、強化或挑戰演進中的綜合。價值在於 wiki 是**持續、複利的產物**：交叉引用早已就位、矛盾早已標記、綜合已反映讀過的一切。

分工：使用者負責選料、探索、問對問題；LLM 負責摘要、交叉引用、歸檔、簿記等所有雜活。原文比喻——**Obsidian 是 IDE，LLM 是程式設計師，wiki 是 codebase**。

## 三層架構

| 層 | 角色 | 誰維護 |
|---|---|---|
| **Raw sources** | 精選的原始文件（文章、論文、圖、資料），事實來源 | 不可變，LLM 只讀 |
| **The wiki** | LLM 生成的 markdown：摘要、實體頁、概念頁、比較、綜合 | LLM 全權掌管 |
| **The schema** | 告訴 LLM wiki 怎麼組織、慣例為何、各流程怎麼跑的設定檔（如 CLAUDE.md／AGENTS.md） | 使用者與 LLM 共同演進 |

schema 是關鍵設定：它讓 LLM 成為**有紀律的 wiki 維護者**，而非泛用聊天機器人。

## 三個動作

- **Ingest（擷取）**：新來源進 raw → LLM 讀、與使用者討論重點 → 寫摘要頁、更新索引、更新相關實體／概念頁、附一筆 log。單一來源可牽動 10–15 頁。可一次一源緊盯，也可批次擷取少監督。
- **Query（查詢）**：向 wiki 提問 → LLM 找相關頁、讀、**附引用**綜合答案。答案形式可為 markdown 頁、比較表、Marp 投影片、圖表、canvas。關鍵洞見：**好答案可回存成新 wiki 頁**，讓探索跟來源一樣複利累積，不消失在對話裡。
- **Lint（健檢）**：定期健檢——矛盾、被新來源取代的過時主張、無入連的孤立頁、被提到卻缺專屬頁的概念、缺交叉引用、可用網搜補的資料空缺。LLM 擅長提出新問題與新來源方向。

## 索引與日誌

- **index.md**（內容導向）：wiki 內容目錄，每頁一連結＋一行摘要，按類別分組，每次 ingest 更新；查詢先讀它找頁再鑽細節。在中等規模（約 100 來源、數百頁）意外好用，免掉 embedding RAG 基建。
- **log.md**（時序導向）：append-only 記錄 ingest／query／lint。若每筆用一致前綴（如 `## [YYYY-MM-DD] ingest | 標題`），可用 `grep`／`tail` 等 unix 工具解析。

> 本 vault 保留了 `index.md`，但依自身治理選擇省略 `log.md`；差異屬實作決定，非模式本體。

## 為何有效

維護知識庫真正累的不是讀或想，而是**簿記**：更新交叉引用、保持摘要即時、標記新舊矛盾、跨數十頁維持一致。人類棄坑是因為維護負擔漲得比價值快。LLM 不會膩、不會忘記更新某條交叉引用、一次可改 15 個檔——**維護成本趨近於零**，wiki 才能持續被維護。

淵源上呼應 Vannevar Bush 的 **Memex（1945）**：私人、主動策展、文件間的關聯與文件本身同等重要的知識庫。Bush 解不了「誰來維護」，LLM 補上了這塊。

## 已被獨立產品化

2026 年中，Nous Research 的 [[Hermes-Agent]] 官方內建 `llm-wiki` skill，文件明言「Based on Andrej Karpathy's LLM Wiki pattern」，逐字複刻 raw／wiki／schema 三層架構——證明這套模式不是本 vault 的孤例，已被獨立的 AI agent 產品採用。其後生態進一步展開（nvk/llm-wiki、Astro-Han 等多個獨立實作，加上多跳 QA 的受控實證），各實作的收斂與分歧見 [[LLM-Wiki-生態實作比較]]。差別在 Hermes 把它定位為「外接圖書館」，疊在自己的**有界核心記憶**（`MEMORY.md`／`USER.md`，session 級快照）之下，形成雙層結構；本 vault 現也有對應的有界核心記憶層（[[MEMORY]]，40 行上限、agent 逐回合即時寫），但份量遠小於 Hermes 的雙系統，仍以 wiki 為主要複利資產——兩者對照見 [[Hermes-Agent]] 任務管理一節。

## 選配工具

- 規模變大時可加 wiki 專屬搜尋引擎（原文舉例 [qmd](https://github.com/tobi/qmd)：本地 markdown 搜尋，混合 BM25／向量＋LLM re-rank，含 CLI 與 MCP server）；小規模下 index 檔已足夠。
- Obsidian Web Clipper 快速把網頁轉 markdown 進 raw；graph view 看 wiki 形狀（樞紐與孤立頁）；Marp 出投影片；Dataview 對 frontmatter 跑動態查詢。整套皆**選配且模組化**，按需取用。

## 關聯

- 來源全文：[[LLM-Wiki-Karpathy]]
- 生態全景：[[LLM-Wiki-生態實作比較]]——各實作（nvk、Hermes skill、Astro-Han）的收斂設計、分歧點與實證證據，以及本 vault 的採用取捨。
- 同源哲學的另一實作：[[Hermes-Agent]]——把「複利資產」用在 agent 自策展的 **skill 庫**，可與本頁「維護 markdown wiki」對照兩種複利路徑。
- 架構定位：[[Claude-Code-記憶系統六層比較]] 把本 pattern 列為 **Level 5（自組織知識庫）**，並與其餘五層（原生 CLAUDE.md、hook 召回、語意搜尋、逐字宮殿、跨工具共腦）對照取捨。
- 人類 PKM 方法論對照：[[第二大腦方法論比較]]——BASB、Zettelkasten 等人類第二大腦方法論同樣在解「擷取後如何維護」，差異在維護者是人還是 LLM。
- 放進 PKM 光譜的本 vault 實踐：[[第二大腦實踐與本-vault-優化]]——把本頁的 Karpathy LLM Wiki 模式放進人類 PKM 方法論光譜對照，據此提出本 vault 的優化方向。
- Agent 記憶路線定位：[[Agent-記憶兩大路線-知識庫與-memory-bank]]——以本頁模式作為知識庫路線（路線 A）的代表原型，與 memory-bank 路線對照。
- harness 工程脈絡：[[Agent-Harness-Engineering-框架綜述]]——本 pattern 屬該頁 context engineering 三技術中的 structured note-taking／agentic memory 路線（筆記持久化到 context window 外再拉回）。
- 實證檢驗：[[AI-自主工作流的實證檢驗]]——本 pattern 對應「沉澱回知識庫」那一步；該頁盤點整條自主工作流各環節的證據強度與已知失效模式。
