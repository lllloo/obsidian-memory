---
title: Agent 記憶的兩大路線：知識庫與 memory bank
description: 比較編譯式知識庫與 coding-agent memory bank 的目的、組織、讀取契約、維護方式及適用邊界
created: 2026-07-14
updated: 2026-07-17
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - memory
  - knowledge-graph
  - coding-agent
  - rag
---

# Agent 記憶的兩大路線：知識庫與 memory bank

同樣是「用 markdown 給 agent 記憶」，實務上分兩條目的不同的路線：**A 知識資產複利** vs **B 專案工作記憶**。分清楚這兩條，才好判斷哪些內容該進本 vault、哪些該留在各專案本地。

**與既有頁分工**（本頁不重述）：A 路線內部各實作的收斂/分歧/實證細比在 [[LLM-Wiki-生態實作比較]]；各種記憶外掛按「儲存位置／召回機制」的技術光譜在 [[Claude-Code-記憶系統六層比較]]。本頁補的是前兩頁都沒正面收的角度——把 A、B 兩條路線的**目的與取捨**擺在一起對比，並收進 coding-agent memory bank 這條線。

## 路線 A：LLM-wiki／編譯式知識庫

**目的**：把知識**編譯一次、持續維護**成互聯 markdown wiki，取代 RAG 每次重檢索——「累積並複利」。三層（raw 只讀／wiki LLM 全權／schema）＋三動作（Ingest／Query／Lint），query-first、raw write-once、markdown 為事實來源。代表：Karpathy 原 gist、nvk、[[Hermes-Agent]] 官方內建的 llm-wiki skill（把 Karpathy 模式複刻成產品化實例）、Astro-Han、本 vault。

細節見 [[LLM-Wiki-知識管理模式]]（原型）與 [[LLM-Wiki-生態實作比較]]（各實作＋實證與風險：多跳 QA 對 RAG 有 preprint 級優勢、但大規模盲目編譯有 53–60% 災難失敗率、錯誤複利是核心風險）。

## 路線 B：coding-agent memory bank

**目的**：解決 coding agent 跨 session **失憶**——每次對話或 context reset 後，靠讀一組 markdown 檔**完全重建**專案脈絡。Cline 的定位原話是「memory reset 後我完全依賴這些檔」。

主流結構與 A 明顯不同：

- **固定角色檔**：一組職責固定的 markdown。以 [Cline Memory Bank](https://docs.cline.bot/features/memory-bank) 為代表六檔——`projectbrief`（基底）→`productContext`/`systemPatterns`/`techContext`→`activeContext`/`progress`，有階層依賴。（Roo Code、Cursor 生態有同構變體。）
- **讀取契約相反**：每次任務開始**無條件讀全部**（Cline 明言 not optional），而非 A 的 query-first 省讀。賣點就是「不靠記憶、靠重讀全部檔恢復」。
- **維護**：agent 在重大變更後自更新檔；使用者可下 `update memory bank` 強制全檔覆核。

**進階變體（維護自動化）**：[ai-memory](https://github.com/akitaonrails/ai-memory)、[Letta](https://docs.letta.com/letta-agent/memory) 把維護從「agent 自覺」變成 **runtime hook／自我編輯**——DB/SQLite-backed、SessionStart/SessionEnd hook 自動注入，Letta 甚至有 sleep-time「反思」子代理把教訓寫回並自動 git commit。

**定位**：服務**單一專案**的 agent 連續性，是「工作記憶」，不做跨來源知識累積。

## 根本差別

| 維度 | A：LLM-wiki 知識庫 | B：memory bank |
|---|---|---|
| 目的 | 知識資產複利（跨來源/跨專案） | 專案工作記憶（單專案續作） |
| 組織 | 按概念/實體/主題，互聯成網 | 按固定角色檔（brief/context/progress） |
| 讀取契約 | query-first，先 index 再鑽 | 每次讀全部，或 hook 自動注入 |
| 來源層 | raw write-once，保留證據鏈 | 無獨立來源層，檔即事實 |
| 維護動作 | Ingest／Query／Lint | 變更後自更新＋使用者強制覆核 |
| 過期處理 | lint＋矛盾標記＋git 歷史 | 每次重讀全部，天然反映現況 |

## 交集傘與反方

- **同屬「markdown + git as memory」大家族**：[Letta MemFS](https://docs.letta.com/letta-code/memfs)、[DiffMem](https://github.com/Growth-Kinetics/DiffMem) 橫跨兩條路線（git-backed markdown、每次編輯自動 commit），顯示兩路線在載體層收斂。
- **反方觀點**：向量記憶廠商 Zep 主張「[Markdown is not agent memory](https://blog.getzep.com/markdown-is-not-agent-memory/)」——markdown 記憶在**規模、時間演進、多 agent 並發**下會崩。優劣仍有爭議、非定論（且屬廠商立場）。

## 對本 vault 的含意：什麼進 vault、什麼留專案

這兩條路線正對應 [[跨專案第二大腦整合模式]] 的「知識／行動單向交接」邊界：

- **本 vault 走純 A 路線**（Level 5 知識庫，見 [[Claude-Code-記憶系統六層比較]]）：收**跨來源、可泛化、複利**的研究知識。
- **B 路線的內容留在各專案本地**：專案當前焦點、進度、決策 log（`activeContext`/`progress` 那類）屬單專案工作記憶，不進 vault；需要時由使用者把可泛化的結論明確餵回 raw/wiki。
- **agent 自身的跨 session 操作狀態**（本 vault 的 `schema/MEMORY.md`）概念上更接近 B 的工作記憶，而非 A 的知識頁——兩者刻意分層，別混。

## 證據強度

- 兩路線的結構與讀取契約皆有 primary source（各 repo／官方 docs），可信度高。
- A vs RAG 的效果優勢是 preprint 級（單一未同儕審查、自報 benchmark）；Zep 的批評是廠商立場——兩者都非中立實證，引用時標明。
- [[Claude-Code-記憶系統六層比較]] 的各方案機制出自單一影片、未獨立查證，引用其細節前宜回查官方文件。

## 關聯

- [[LLM-Wiki-生態實作比較]] — A 路線內部各實作（nvk／Hermes／Astro-Han）與橫跨兩路線的相鄰系統（Letta／DiffMem）的收斂、分歧與實證細比；本頁只給 A 的定位，細節在該頁。
- [[Claude-Code-記憶系統六層比較]] — 記憶方案按「儲存／召回」的技術光譜（Mem0／MemPalace／OpenBrain…）；與本頁按「目的」切的兩路線互補、切軸不同。
- [[Mem0]] — 本頁 A／B 分野在單一工具上的落地案例：拍板讓 mem0 只當 B 路線的「隨手記收件匣」、A 路線的嚴謹知識仍留 vault；其失效模式（抽取污染、幻覺自我複製）正是「什麼不該交給自動抽取」的反面教材。
- [[LLM-Wiki-知識管理模式]] — A 路線的原型定義（raw/wiki/schema 三層與三動作）。
- [[跨專案第二大腦整合模式]] — 本頁「什麼進 vault、什麼留專案」的邊界，正是該頁知識／行動單向交接的展開。
- [[第二大腦整合的現成工具與做法]] — B 路線「近期熱脈絡層」（hot.md）承載方式的現成工具與拍板在該頁；memory bank 六檔（如 activeContext）的結構細節見本頁「路線 B」節，非本連結頁涵蓋。
