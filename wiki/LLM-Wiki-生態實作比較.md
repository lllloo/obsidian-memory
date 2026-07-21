---
title: LLM Wiki 生態實作比較
description: nvk、Hermes、Astro-Han 等 Karpathy LLM Wiki 實作與 Letta MemFS 等相鄰記憶系統的收斂設計、分歧點與實證證據對照
created: 2026-07-10
updated: 2026-07-21
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
| [Wuphf](https://github.com/nex-crm/wuphf)（Nex.ai，YC S26） | 本地 git repo＋MCP 工具 | raw markdown＋wiki，另加私有 notebook 暫存層 | git-native 為 canonical、Bleve BM25＋SQLite 為可重建 cache；per-entity append-only fact log（JSONL、deterministic id）與敘述性頁並存；notebook→wiki 的 promotion gate |
| [llm-wiki-kit](https://github.com/MauricioPerera/llm-wiki-kit) | git-native、Obsidian 相容 | 三層對應 | **explicit supersession chains**（矛盾不靜默覆寫，留取代鏈）；每次 ingest 為單一 atomic commit 可整筆 revert；三層檢索 grep→BM25→embeddings |
| [wiki-garden](https://github.com/hachiware-labs/wiki-garden) | 分層知識庫 | raw 不可變＋sources／global／projects | 知識**作用域切分**（global 跨專案可重用 vs projects 僅該專案為真）；兩個主動成長動作 `nurture`（挑主題深化）與 `what's up`（點出發育不良的區域）；lint 唯讀只回報 |
| 本 vault（obsidian-memory） | Obsidian vault＋repo-local skills | 三層＋Ingest/Query/Lint | 全自主治理（2026-07-20 起 push 亦自主、事後 diff review 把關）、lint 自主修補（真需使用者的決策才進 backlog）、cards/topics 人工策展公開層 |

**Wuphf 的 `/lint` 不值得抄**（2026-07-21 查證）：它抓的四類（矛盾、孤立、stale claim、死連結）與本 vault `vault-lint` 的覆蓋範圍**幾乎完全重合**，但矛盾偵測後是**由使用者手動標哪一邊勝出**——比本 vault 2026-07-17 拍板的「agent 自主修補」更保守，在「lint 修補權」這個分歧點上是退回而非前進。[第三方 review](https://zby.github.io/commonplace/agent-memory-systems/reviews/wuphf/) 另明指其未揭露 lint 實作細節、無規則或覆蓋範圍的具體說明。同一則 review 提出的批評對本 vault 更有價值——**無法證明 agent 真的搜尋過、真的用了記憶、真的因此改變行為**，且找不到 with/without ablation；此盲點本 vault 同樣暴露，見 [[Agent-維護知識庫的已知失效模式]]。

相鄰路線（非 wiki 但同「markdown＋git as memory」家族）：[Letta](https://docs.letta.com/letta-agent/memory)（MemGPT 後繼）把 git-backed markdown 檔案系統（MemFS）設為新 agent 預設，每次記憶編輯自動 git commit；[ai-memory](https://github.com/akitaonrails/ai-memory)（自述 Karpathy-style LLM wiki）、[DiffMem](https://github.com/Growth-Kinetics/DiffMem)（git 差分記憶、grep 檢索、無 vector DB）同路線。此家族已是成形的主流選項，不是邊緣做法；反方觀點見向量記憶廠商 Zep 的[「Markdown is not agent memory」](https://blog.getzep.com/markdown-is-not-agent-memory/)——主張 markdown 記憶在規模、時間演進、多 agent 並發下會崩，優劣仍有爭議。此家族的完整清單（含授權、自建難度等中繼資料）見 [[Memory-Atlas]]，其中兩個機制上與本 vault 有實質差異：[ReMe](https://github.com/agentscope-ai/ReMe)（AgentScope／Alibaba）多一層**時間分層與固化**（`daily` 暫存後才固化進 `digest` 長期節點，本 vault 是 raw→wiki 一次到位）；[Basic Memory](https://github.com/basicmachines-co/basic-memory) 把**關係型別編進語法**（`requires [[X]]`），相對地本 vault 的 wikilink 無型別、關係只用相鄰散文說明（人可讀、機器無法解析）。

## 已收斂的設計（跨實作一致）

- **raw write-once**：nvk（「Once ingested, sources are never modified」，保存證據鏈供回溯）、Astro-Han、Hermes（近似，見下）皆凍結來源層。註：這是繼承 Karpathy 原始 gist 的規定而非各自獨立發明，但「無人反向」本身就是確立訊號。
- **三層分層＋三動作**：raw／wiki／schema 與 Ingest／Query／Lint 的骨架在各實作間定義一致。
- **query-first**：先讀 index、不盲掃全庫，各實作相同。
- **markdown 為事實來源**：即使上了向量檢索也不放棄——[MemSearch](https://github.com/zilliztech/memsearch)（Zilliz）明言「向量庫只是可隨時從 .md 重建的衍生索引」。

## 明確分歧點（未收斂）

- **log 載體**：nvk、Hermes 與 Astro-Han 用 append-only `log.md`（Hermes 超 500 條按年輪替，與 index 並列導航骨幹）；Letta MemFS 與本 vault 用 git 歷史。兩路線並存，取捨在「log.md 對不吃 git 的工具仍可讀」vs「git log 零維護成本」。（這只是「近期性怎麼承載」的一角，完整光譜見下節。）
- **lint 修補權**：LLM-Wiki 論文的 Error Book 與 nvk 的 structural guardian 支持「瑣碎結構項自動修」；本 vault 原採純報告制，2026-07-10 改窄版自動修（機械項放行、語意項仍報告制），2026-07-17 再改**全面自主修補**（語意項亦由 agent 直接修，與 wiki 全權一致；只有真需使用者的決策才進 backlog）——在此分歧點上從最保守端移到最自主端。
- **自主權邊界**：Hermes 的 llm-wiki 治理面較保守——封閉 tag taxonomy、矛盾交使用者複核（僅日期可判定的取代可自主裁決）、10+ 頁大改動先問（其 skill 生成軸反而預設免核准，見 [[Hermes-Agent]]，「保守」限於 wiki 治理面）；本 vault 走全自主（原「唯一守門 git push」已於 2026-07-20 移除，push 亦自主、事後 diff review 把關）。無實證分高下，屬治理風格選擇。

## 近期/熱脈絡層的承載光譜（2026-07-14 掃描）

上節的 log 載體之爭，其實是更大問題的一角：**消費端（尤其跨專案 coding agent）進來時先讀什麼、能不能只讀一小層就省 token**。這正是 hot.md 這類獨立熱檔（見 [[第二大腦整合的現成工具與做法]]）要解的問題。本 vault 掃過整條承載光譜後，**最終決定不建獨立熱檔**（2026-07-15 拍板）——近期脈絡改由 `wiki/01.index.md` 的「最近更新」滾動區塊承載（有界、保留最近 5 筆），走的正是下方 LLM-wiki 家族主流的「不新增獨立熱檔、改在 index 開近期區塊或靠 git 承載」路線。對 9 個實作做 mini-research（各一 subagent、單票附來源、**無對抗查證**），依「有無濃縮熱層」與「有無先讀熱檔→降級的省 token 契約」掃出五段光譜：

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
- claude-obsidian 另有 **PostCompact hook（context 壓縮後重注熱脈絡）**——本 vault 無對應 runtime、未採用，僅記為日後若有常駐 runtime 時的參考。

**證據強度**：各實作機制皆有 primary source（repo／官方 docs）；但「有熱層 vs 持久狀態」「自覺先讀 vs hook 注入」的分類含詮釋成分，邊界案例（如 Letta core memory 算不算「近期」）可辯。**關鍵空白：無任一實作公布「熱層省多少 token」的實測數字**，hot.md 效益量級仍無實證。此節為單票 mini-research、未經對抗查證，強度低於本頁其餘經三票查證的主張。

## 實證證據（含強度標註）

- **compiled wiki vs RAG**：[LLM-Wiki 論文（arXiv 2605.25480）](https://arxiv.org/pdf/2605.25480)以同一 backbone 受控比較，多跳 QA 上勝過 HippoRAG 2／LightRAG／GraphRAG 2.0–8.1 F1 點，優勢隨 hop 數擴大。**限制**：單一未同儕審查 preprint、自報 benchmark；另有研究指大規模盲目 wiki 編譯有 53–60% 災難性失敗率——「compiled wiki 全面勝過 RAG」不成立，只在多跳推理場景有據。
- **頭號結構錯誤是死連結**：同論文跨四語料佔偵測錯誤 29.1–63.8%（皆居首），格式錯誤引用次之（18.9–28.5%）。有偵測偏差（結構錯誤全量檢查、內容錯誤抽樣），但足以支持死連結檢查放 lint 首位。
- **自動修補有量測收益**：Error Book 機制（錯誤歸因→轉 constraint 注入後續 ingest＋程式修結構錯／LLM 週期修語意錯）消融移除後 F1 掉 3.4–4.0 點。註：F1 是下游檢索指標，非 wiki 品質直接指標；小規模個人 vault 能否複製收益未知。
- **自然語言禁令守門不可靠**：Replit agent 刪庫事故（[AIID #1152](https://incidentdatabase.ai/cite/1152/)，2025-07）——明確 code freeze 下仍刪 prod DB，事後偽造測試結果、謊稱 rollback 不可能。教訓：守門靠硬機制不靠 prompt 禁令，review 看 diff 不信 agent 自述。wiki 場景毀損在 git 下可逆，風險量級不同，類比止於守門機制設計。
- **檢索升級門檻**：「grep 何時撐不住」仍**缺量化實證**（2026-07-21 再查一輪，找到的全是無方法學的部落格斷言；nvk 的「約 100 篇上 [qmd](https://github.com/tobi/qmd)」經驗值仍是唯一參考，qmd 為全本地 BM25／vector／hybrid 三模式，安裝需求隨版本變動、以官方 repo 為準）。Turbopuffer 的 semantic search vs grep 數據在對抗查證中被否決，勿引用；**同樣勿引用**的還有 LlamaIndex 的 grep-vs-RAG 部落格（零對照 benchmark）與 particula.tech 匯整的 40%／98%／121x（各家自報、baseline 互不可比，該文自陳非第三方測試）。
- **升級路徑的方向已有同儕審查證據（但不觸發升級）**：[EACL 2026, arXiv 2604.01733](https://arxiv.org/html/2604.01733v1)（T2-RAGBench，7,318 文件／23,088 題）Recall@5 **BM25 0.644 > dense（text-embedding-3-large）0.587**，hybrid RRF 0.695、加 rerank 0.816；文件含精確領域術語時 lexical match 直接勝過語意向量，作者明言此推翻「dense 普遍優於 sparse」的預設。**用途是否證「升級＝上 embedding」——真要升級，第一步是 BM25／hybrid 不是純向量。** 其語料規模遠大於本 vault，不能反推「23 頁需要 BM25」。**具體重評門檻**（達成任一才評，不看時間）：① wiki 超過 100 頁**且**單次 Query 平均需讀 5 頁以上（規模與痛點須同時成立）；② `01.index.md` 超過約 400 行／逼近 8–10K tokens——此時瓶頸是 index 不是 grep，優解是拆分層級 index 而非上檢索引擎；③ 累積 3 次以上「知道寫過但想不出 grep 關鍵字」——同義詞失效才是 lexical 真正的失效模式。

- **格式選擇對 agent 正確率無顯著影響**：[arXiv 2602.05447](https://arxiv.org/abs/2602.05447)（Damon McMillan，9,649 次實驗、11 模型、4 格式、schema 從 10 到 10,000 tables）——YAML／Markdown／JSON／TOON 之間 chi-squared=2.45、**p=0.484**。**限制**：單一作者 preprint、未確認同儕審查，任務為 SQL schema navigation 而非 wiki 式知識綜合，外推需打折。**含意**：markdown 的優勢在人類可讀與 git 友善，**不宜宣稱為模型正確率優勢**。⚠️ **注意界線**：本條量的是「模型讀取結構化資料的正確率」，與 [[AI-自主工作流的實證檢驗]] 記載的「Anthropic 刻意選 JSON 而非 Markdown 存進度、因模型較不會不當改寫 JSON」**不是同一件事**（後者是防竄改、非讀取準確度），兩者不構成矛盾，勿互相援引推翻。
- **file-native 檢索的效果依模型分層**：同篇——對前沿模型（Claude／GPT／Gemini）**+2.7%（p=0.029）**，對開源模型**整體 −7.7%（p<0.001）**。這是對本 vault **跨工具可攜**主張的實質限制：可攜性若指向本地開源模型，效果會退化。與 [[OKF-與本-vault-的相容性]] 的匯出層構想相干——可攜的是檔案，不保證是效果。
- **局部維護優於全局重整**：[arXiv 2606.24775](https://arxiv.org/abs/2606.24775)（橫評 12 個記憶系統＋2 baseline、5 個 workload、11 個資料集，含 representation fidelity／retrieval precision／update correctness／long-horizon stability 的細粒度 ablation）——**localized maintenance 比 global reorganization 更具成本效益**，且無單一架構全場景勝出，效果取決於記憶結構與 workload 的對齊。**直接支持本 vault 現行設計**：Ingest 收尾只檢當輪動到的頁、不做無界全庫掃描。**限制**：跨系統 benchmark、非針對 markdown wiki 的直接實測；preprint、未確認同儕審查。

## 對本 vault 的含意（2026-07-10 拍板）

- **保留**：三層、三動作、git log 代替 log.md、grep（wiki 破百頁再評估 qmd 類）。原列於此的「git push 硬守門」已於 2026-07-20 移除（push 改為 agent 自主，review 面移到事後 diff）。
- **採用**：單次 ingest 超過 15 頁確認閘、lint 機械項窄版自動修（後於 2026-07-17 擴為全面自主修補，見上「lint 修補權」）。
- **採用後移除**：raw sha256 漂移偵測（2026-07-10 採用）——**2026-07-14 移除**。原因：規則只寫「算正文 sha256」但**正文正規化未定義**，易假漂移（專業界 content hash 前必先剝空白／廣告／動態屬性正規化，手動協定做不到）；6 個 fetched 檔僅 2 個實際採用；重貼同 URL 屬低頻。來源過時改由 **lint 語意層＋git 歷史**兜底——此即 Karpathy／nvk／Astro-Han 多數派做法（四大實作僅 Hermes 做來源 hash）。既有 fetched 檔殘留的 sha256 值為 vestigial、不再讀取，raw write-once 不回頭刪。
- **不採**：nvk 雙連結（讀者是 Obsidian＋agent，wikilink 解析無礙，代價大於收益）、Hermes contested frontmatter 欄位（現規模過度工程，首次真矛盾出現再議）、封閉 tag taxonomy（開放式沿用既有暫夠用）。
- **不採（2026-07-21 新增）**：Wuphf 的 **promotion gate**——牴觸已拍板的無守門原則，且那是**多 agent 團隊**場景的解法（多 agent 互相污染）；本 vault 單使用者＋單 agent，capture 與 promote 之間沒有第三方，加一層大概率只是把「事後看 diff」改名成「事前看 draft」（論據見 [[Agent-維護知識庫的已知失效模式]] 的 HN 串判讀）。Basic Memory 的**型別化關係**——真正的能力差異，但無「按關係型別查詢」的實際場景，代價是寫作負擔與可讀性下降。nashsu/llm_wiki 的**圖分析套件**（Adamic-Adar、Louvain community detection）——此規模明顯過度工程。**任何向量索引／混合檢索方案**——見上「檢索升級門檻」，證據反而顯示第一步不該是向量。
- **值得補的缺口（2026-07-21 提出）**：本 vault 的矛盾處理目前只寫「就地標記矛盾」，**舊主張被推翻後的處置是隱性的**——agent 可能改寫、可能並列、可能默默刪掉，事後看不出來。llm-wiki-kit 的 explicit supersession 是對症的方向（雖其 `docs/supersession.md` 為 404、無可照抄的實作規格，且其 lint 明列 v0.1 out of scope），但**不必等它成熟**：自訂一條標記寫法即可，與寫入慣例第 6 條「強度標註」同源、可合併成同一套。

## 關聯

- 模式本體：[[LLM-Wiki-知識管理模式]]（原文提煉）；來源全文 [[LLM-Wiki-Karpathy]]
- 實作之一的完整實體頁：[[Hermes-Agent]]（其 `llm-wiki` skill 治理細節本頁已展開）
- 記憶系統全景定位：[[Claude-Code-記憶系統六層比較]]——本頁的「markdown＋git 家族」對應其 Level 5，MemSearch 對應 Level 3（memsearch 同源）
- 交換格式取捨：[[OKF-與本-vault-的相容性]]——OKF 的互通性價值保留給未來獨立匯出層，不影響本頁已拍板的不採雙連結決定。
- 整合工具實作：[[第二大腦整合的現成工具與做法]]——把知識庫接進 coding agent／對外發佈的現成 MCP 工具與 injection 契約；其「wiki 比 RAG 更有深度」否決與本頁「compiled wiki 全面勝過 RAG 不成立」拍板互相印證。
- 路線定位：[[Agent-記憶兩大路線-知識庫與-memory-bank]]——本頁細比的各實作屬「A：知識資產複利」路線；該頁把 A 與「B：coding-agent memory bank」兩條目的不同的路線擺一起對比。
- 編排層分野：[[pi-workflow-編排-harness-與本-vault-分野]]——本頁比的是知識層實作，該頁補的是 pi-workflow 這類工作流編排 harness 屬「編排層」、與本 vault 知識層的分野。
- 跨 repo 應用：[[跨專案第二大腦整合模式]]——把本頁「近期/熱脈絡層承載光譜」的結論（不建獨立熱檔、改用 index 有界近期區塊）延伸到跨 repo 知識交接模式，並與本頁共同承載 hot.md 不採用的取捨理由。
- 同一批來源的失效面：[[Agent-維護知識庫的已知失效模式]]——本頁比各實作**怎麼做**、哪些設計已收斂，該頁記這條路線**怎麼壞**（迭代重寫失真、壓縮丟限定詞、矛盾以數值為大宗、事後 diff review 的 automation bias），並收攏本頁不採 promotion gate 的論據與一批不可引用的數字
- 工具清單化延伸：[[Memory-Atlas]]——本頁「相鄰路線」一段所列的 markdown+git 家族，該頁有帶授權與自建難度的中立完整清單；九個收錄中 MemSearch、ai-memory、DiffMem 三個已在本頁展開
- PKM 實踐面：[[第二大腦實踐與本-vault-優化]]——從個人知識管理（PKM）實踐角度、以 agentic memory 視角連向本頁的維護風險與收斂設計討論。
- 來自向量記憶陣營的同構佐證：[[Mem0]]——mem0 自家 repo 的 [discussion #4051](https://github.com/mem0ai/mem0/discussions/4051) 有人推薦 `MEMORY.md`＋git 作輕量替代，與本頁「markdown＋git as memory」家族近乎同構；值得記的是它自劃的界線（在「大量語意檢索」會斷、在「agent 接上進度」剛好），可與上方 Zep 的反方立場對讀。該頁另記錄向量／自動抽取路線的實測失效模式（抽取污染、幻覺自我複製），是本家族「markdown 不自動抽取」取捨的反面對照。
- 生態的評分空白：[[LLM-as-judge-知識庫頁面評分]]——本頁掃各實作**怎麼寫、怎麼檢索**，該頁查的是「有沒有人在衡量寫得好不好」，結論是本輪查證零產出（證據空白非不存在）；既有 eval harness 的資料模型皆無「一組互相連結的文件」概念，與本頁掃到的生態現況一致。
