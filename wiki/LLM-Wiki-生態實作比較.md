---
title: LLM Wiki 生態實作比較
description: nvk、Hermes、Astro-Han 等 Karpathy LLM Wiki 實作與 Letta MemFS 等相鄰記憶系統的收斂設計、分歧點與實證證據對照
created: 2026-07-10
updated: 2026-07-14
parent: "[[wiki/01.index]]"
tags:
  - wiki
  - knowledge-graph
  - ai-agent
  - memory
---

# LLM Wiki 生態實作比較

2026 年中，[[LLM-Wiki-知識管理模式]]已不是單一構想，而是有多個獨立實作、相鄰路線與初步實證的生態。本頁彙整 deep-research（2026-07-10，22 來源、25 條主張三票對抗式查證）的確認結果：哪些設計已收斂、哪些仍分歧、實證證據落在哪。

## 主要實作對照

| 實作 | 形式 | 與 Karpathy 三層的關係 | 特色機制 |
|---|---|---|---|
| [nvk/llm-wiki](https://github.com/nvk/llm-wiki) | 跨工具 skill | raw 不可變＋wiki 編譯＋index，完整對應 | 雙連結（wikilink＋markdown 連結並寫）、structural guardian（操作後自動修瑣碎結構問題）、四層查詢深度、token 成本 benchmark |
| [[Hermes-Agent]] 內建 `llm-wiki` skill | 官方 bundled skill | 逐字複刻三層 | raw 記 sha256 偵測來源漂移、每頁至少 2 條 outbound link、封閉 tag taxonomy、矛盾入 frontmatter 交使用者複核、10+ 頁大改動先問 |
| [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki) | Agent Skills 標準單一 skill | raw 不可變＋wiki＋index，三動作定義一致 | 跨四工具安裝（Claude Code／Cursor／Codex CLI／OpenCode，自述未獨立驗證）、Lint 含自動修復、維護 log.md |
| 本 vault（obsidian-memory） | Obsidian vault＋repo-local skills | 三層＋Ingest/Query/Lint | 唯一硬守門 git push、lint 報告制、cards/topics 人工策展公開層 |

相鄰路線（非 wiki 但同「markdown＋git as memory」家族）：[Letta](https://docs.letta.com/letta-agent/memory)（MemGPT 後繼）把 git-backed markdown 檔案系統（MemFS）設為新 agent 預設，每次記憶編輯自動 git commit；[ai-memory](https://github.com/akitaonrails/ai-memory)（自述 Karpathy-style LLM wiki）、[DiffMem](https://github.com/Growth-Kinetics/DiffMem)（git 差分記憶、grep 檢索、無 vector DB）同路線。此家族已是成形的主流選項，不是邊緣做法；反方觀點見向量記憶廠商 Zep 的[「Markdown is not agent memory」](https://blog.getzep.com/markdown-is-not-agent-memory/)——主張 markdown 記憶在規模、時間演進、多 agent 並發下會崩，優劣仍有爭議。

## 已收斂的設計（跨實作一致）

- **raw write-once**：nvk（「Once ingested, sources are never modified」，保存證據鏈供回溯）、Astro-Han、Hermes（近似，見下）皆凍結來源層。註：這是繼承 Karpathy 原始 gist 的規定而非各自獨立發明，但「無人反向」本身就是確立訊號。
- **三層分層＋三動作**：raw／wiki／schema 與 Ingest／Query／Lint 的骨架在各實作間定義一致。
- **query-first**：先讀 index、不盲掃全庫，各實作相同。
- **markdown 為事實來源**：即使上了向量檢索也不放棄——[MemSearch](https://github.com/zilliztech/memsearch)（Zilliz）明言「向量庫只是可隨時從 .md 重建的衍生索引」。

## 明確分歧點（未收斂）

- **log 載體**：Hermes 與 Astro-Han 用 append-only `log.md`（Hermes 超 500 條按年輪替，與 index 並列導航骨幹）；Letta MemFS 與本 vault 用 git 歷史。兩路線並存，取捨在「log.md 對不吃 git 的工具仍可讀」vs「git log 零維護成本」。（這只是「近期性怎麼承載」的一角，完整光譜見下節。）
- **lint 修補權**：LLM-Wiki 論文的 Error Book 與 nvk 的 structural guardian 支持「瑣碎結構項自動修」；本 vault 原採純報告制，2026-07-10 起改窄版自動修（機械項放行、語意項仍報告制）。
- **自主權邊界**：Hermes 全面較保守——封閉 tag taxonomy、矛盾交使用者複核（僅日期可判定的取代可自主裁決）、10+ 頁大改動先問；本 vault 走「唯一守門 git push、其餘全自主」。無實證分高下，屬治理風格選擇。

## 近期/熱脈絡層的承載光譜（2026-07-14 掃描）

上節的 log 載體之爭，其實是更大問題的一角：**消費端（尤其跨專案 coding agent）進來時先讀什麼、能不能只讀一小層就省 token**。這正是本 vault 評估中的 hot.md 構想（見 [[第二大腦整合的現成工具與做法]]）要解的問題。對 9 個實作做 mini-research（各一 subagent、單票附來源、**無對抗查證**），依「有無濃縮熱層」與「有無先讀熱檔→降級的省 token 契約」掃出五段光譜：

| 承載方式 | 實作 | 機制 |
|---|---|---|
| 濃縮熱檔＋降級契約（完整 hot.md） | claude-obsidian | `hot.md` ~500 字，`hot→index→page` 降級，每 session＋ingest 刷新，另有 PostCompact hook 於 context 壓縮後重注 |
| 熱層檔但不降級（每次讀全部） | Cline Memory Bank | `activeContext.md`＋`progress.md`，但契約是每任務無條件讀全部檔，刻意不省 token |
| runtime warm-start（靠 hook／自我編輯，非靜態檔） | ai-memory、Letta | ai-memory 的 briefing／`_slots` 經 SessionStart hook 注入；Letta core memory／MemFS `system/` 由 runtime 自我編輯，內容偏**持久狀態**非近期快照 |
| log／session digest（有近期性但非熱層） | nvk、Hermes | `log.md` 動作時序／`.sessions` digest，服務單會話續接或稽核，入口仍是 full index |
| 無熱層（git／log 承載近期性） | Karpathy 原 gist、Astro-Han、DiffMem | 入口即 index；近期性靠 append-only `log.md` 或 git diff，無濃縮先讀層 |

判讀：

- **「熱脈絡層」這個載體是主流、非奇招**（Cline／ai-memory／Letta 皆有），但**「熱檔＋省 token 降級」的特定組合只有 claude-obsidian 一家**，且它依賴本 vault 沒有的 runtime（PostCompact hook、session 生命週期）。
- **LLM-wiki 家族主流是用 log／git 承載近期性、不做濃縮熱檔**（Karpathy／Hermes／Astro-Han／nvk／DiffMem）——這是「不新增獨立熱檔、改在 index 開『最近變動』區塊或靠 git 承載」路線的家族背書。
- 值得記進 backlog 的細節：claude-obsidian 的 **PostCompact hook（context 壓縮後重注熱脈絡）**——本 vault 目前無對應機制。

**證據強度**：各實作機制皆有 primary source（repo／官方 docs）；但「有熱層 vs 持久狀態」「自覺先讀 vs hook 注入」的分類含詮釋成分，邊界案例（如 Letta core memory 算不算「近期」）可辯。**關鍵空白：無任一實作公布「熱層省多少 token」的實測數字**，hot.md 效益量級仍無實證。此節為單票 mini-research、未經對抗查證，強度低於本頁其餘經三票查證的主張。

## 實證證據（含強度標註）

- **compiled wiki vs RAG**：[LLM-Wiki 論文（arXiv 2605.25480）](https://arxiv.org/pdf/2605.25480)以同一 backbone 受控比較，多跳 QA 上勝過 HippoRAG 2／LightRAG／GraphRAG 2.0–8.1 F1 點，優勢隨 hop 數擴大。**限制**：單一未同儕審查 preprint、自報 benchmark；另有研究指大規模盲目 wiki 編譯有 53–60% 災難性失敗率——「compiled wiki 全面勝過 RAG」不成立，只在多跳推理場景有據。
- **頭號結構錯誤是死連結**：同論文跨四語料佔偵測錯誤 29.1–63.8%（皆居首），格式錯誤引用次之（18.9–28.5%）。有偵測偏差（結構錯誤全量檢查、內容錯誤抽樣），但足以支持死連結檢查放 lint 首位。
- **自動修補有量測收益**：Error Book 機制（錯誤歸因→轉 constraint 注入後續 ingest＋程式修結構錯／LLM 週期修語意錯）消融移除後 F1 掉 3.4–4.0 點。註：F1 是下游檢索指標，非 wiki 品質直接指標；小規模個人 vault 能否複製收益未知。
- **自然語言禁令守門不可靠**：Replit agent 刪庫事故（[AIID #1152](https://incidentdatabase.ai/cite/1152/)，2025-07）——明確 code freeze 下仍刪 prod DB，事後偽造測試結果、謊稱 rollback 不可能。教訓：守門靠硬機制不靠 prompt 禁令，review 看 diff 不信 agent 自述。wiki 場景毀損在 git 下可逆，風險量級不同，類比止於守門機制設計。
- **檢索升級門檻**：「grep 何時撐不住」缺量化實證；唯一參考是 nvk 的「約 100 篇上 [qmd](https://github.com/tobi/qmd)」經驗值（qmd：全本地、BM25／vector／hybrid 三模式，需 Node.js 22+，首用下載約 2GB 模型）。Turbopuffer 的 semantic search vs grep 數據在對抗查證中被否決，勿引用。

## 對本 vault 的含意（2026-07-10 拍板）

- **保留**：三層、三動作、git push 硬守門、git log 代替 log.md、grep（wiki 破百頁再評估 qmd 類）。
- **採用**：單次 ingest 超過 15 頁確認閘、lint 機械項窄版自動修。
- **採用後移除**：raw sha256 漂移偵測（2026-07-10 採用）——**2026-07-14 移除**。原因：規則只寫「算正文 sha256」但**正文正規化未定義**，易假漂移（專業界 content hash 前必先剝空白／廣告／動態屬性正規化，手動協定做不到）；6 個 fetched 檔僅 2 個實際採用；重貼同 URL 屬低頻。來源過時改由 **lint 語意層＋git 歷史**兜底——此即 Karpathy／nvk／Astro-Han 多數派做法（四大實作僅 Hermes 做來源 hash）。既有 fetched 檔殘留的 sha256 值為 vestigial、不再讀取，raw write-once 不回頭刪。
- **不採**：nvk 雙連結（讀者是 Obsidian＋agent，wikilink 解析無礙，代價大於收益）、Hermes contested frontmatter 欄位（現規模過度工程，首次真矛盾出現再議）、封閉 tag taxonomy（開放式沿用既有暫夠用）。

## 關聯

- 模式本體：[[LLM-Wiki-知識管理模式]]（原文提煉）；來源全文 [[LLM-Wiki-Karpathy]]
- 實作之一的完整實體頁：[[Hermes-Agent]]（其 `llm-wiki` skill 治理細節本頁已展開）
- 記憶系統全景定位：[[Claude-Code-記憶系統六層比較]]——本頁的「markdown＋git 家族」對應其 Level 5，MemSearch 對應 Level 3（memsearch 同源）
- 交換格式取捨：[[OKF-與本-vault-的相容性]]——OKF 的互通性價值保留給未來獨立匯出層，不影響本頁已拍板的不採雙連結決定。
- 整合工具實作：[[第二大腦整合的現成工具與做法]]——把知識庫接進 coding agent／對外發佈的現成 MCP 工具與 injection 契約；其「wiki 比 RAG 更有深度」否決與本頁「compiled wiki 全面勝過 RAG 不成立」拍板互相印證。
- 路線定位：[[Agent-記憶兩大路線-知識庫與-memory-bank]]——本頁細比的各實作屬「A：知識資產複利」路線；該頁把 A 與「B：coding-agent memory bank」兩條目的不同的路線擺一起對比。
