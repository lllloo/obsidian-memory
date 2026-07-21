---
title: Memory Atlas
description: 廠商中立的 agent memory 框架目錄，每條事實附來源與日期；本 vault 用它取代重複搜尋同一批 markdown 記憶工具
created: 2026-07-21
updated: 2026-07-21
source: https://www.memoryatlas.dev/families/filesystem-markdown
parent: "[[wiki/01.index]]"
tags:
  - wiki
  - ai-agent
  - memory
---

# Memory Atlas

agent memory 框架的**廠商中立目錄站**，自述規範是「每個事實與數字都附帶來源和日期」，並明言「git history 即 audit log」。收錄本頁的用途很實際：**取代日後重複搜尋同一批工具**——本 vault 已在 2026-07 多輪研究中反覆搜到相同的 markdown 記憶工具群，有一份帶欄位的中立清單可省掉重跑。

**強度**：目錄站、非實測 benchmark；提供的是 star 數、授權、自建難度這類可查證的中繼資料，不是效果比較。頁面標示 `Last verified 2026-06-28`、`vendor-neutral catalog`（2026-07-21 實查確認）。

## filesystem / markdown 家族收錄

九個系統，每條附 GitHub star 數、授權（AGPL-3.0／Apache-2.0／MIT／ELv2 等）、自建部署難度（trivial／moderate／heavy）、付費選項與適用情景：

| 系統 | 出處 | 本 vault 既有涵蓋 |
|---|---|---|
| OpenViking | Volcengine | 未涵蓋 |
| ByteRover | — | 未涵蓋 |
| memU | NevaMind AI | 未涵蓋 |
| EverOS | EverMind AI | 未涵蓋 |
| ReMe | AgentScope／Alibaba | 未涵蓋（形態與本 vault 最接近，見下） |
| Basic Memory | Basic Machines | 未涵蓋 |
| MemSearch | Zilliz／Milvus | 已見於 [[LLM-Wiki-生態實作比較]] |
| ai-memory | AkitaOnRails | 已見於 [[LLM-Wiki-生態實作比較]] |
| DiffMem | Growth Kinetics | 已見於 [[LLM-Wiki-生態實作比較]] |

九個裡有三個本 vault 早已收錄，可反推這份清單與既有研究的重疊度——它補的是另外六個，而非推翻既有認知。

## 兩個值得日後回看的條目

以下機制描述來自各專案官方 README、**無實測**，記錄用途是「日後若真要深挖從哪裡開始」：

- **ReMe**（AgentScope，Alibaba）——這批裡與本 vault 形態最接近的：同樣 wikilink 圖譜、同樣檔案為真相。差異在**時間分層與固化**：`session`／`resource` → `daily`（輕量處理）→ `digest`（長期記憶節點），多了「daily 暫存、之後才固化進長期」的緩衝層，本 vault 則是 raw → wiki 兩層一次到位。是否值得引入，取決於是否真的發生「ingest 當下寫進 wiki 的內容後來發現不該進」——目前無此痛點。
- **Basic Memory**——markdown 檔即 Entity，檔內用**結構化語法**編碼知識圖譜：Observations 帶類別（`[method]`、`[tip]`、`[fact]`）、Relations 帶關係型別（`requires [[Burr Grinder]]`）。相對地本 vault 的 wikilink 是**無型別**的——`CLAUDE.md` 要求用相鄰文字說明關係，但那是給人讀的散文、機器無法解析。型別化關係是真正的能力差異，代價是寫作負擔與可讀性下降；**不建議現在引入**（無「按關係型別查詢」的實際場景），記錄供日後參考。

## 關聯

- 生態實作對照：[[LLM-Wiki-生態實作比較]]——本頁是該頁「相鄰路線」一節的清單化延伸，九個收錄中有三個已在該頁展開
- 失效面：[[Agent-維護知識庫的已知失效模式]]——目錄列的是各系統宣稱做到什麼，該頁記這條路線共同會壞在哪
- 記憶方案全景：[[Claude-Code-記憶系統六層比較]]——本頁九個系統多屬其 Level 5（自組織知識庫）與 Level 3（語意搜尋）之間
