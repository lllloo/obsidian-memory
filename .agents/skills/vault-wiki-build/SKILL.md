---
name: vault-wiki-build
description: Ingest——讀散落 raw（整個 raw）綜合維護 wiki 活知識庫。偵測 ≥N 篇共享同主題的散落原料 → 與使用者確認切角 → subagent 綜合成 wiki 概念/綜合頁並更新 index。跨 ≥2 來源綜合出原文沒有的結論、單向 wikilink 指回 raw。使用時機：使用者說「ingest」、「綜合散落 raw」、「掃 raw 找可綜合的主題」、「wiki build」、「更新 wiki」，或直接呼叫 /vault-wiki-build。
---

# vault-wiki-build — Ingest：raw → wiki 活知識庫

掃 raw 找共享主題 → 列可綜合的 cluster、與使用者確認切角 → subagent 綜合成 wiki 頁 → 更新 `wiki/01.index.md`。

## 定位

- **raw = 整個 `raw/`**：不可變原料，本 skill 只讀不改。
- **wiki = 活知識庫**：agent 綜合 raw 維護的頁面（摘要 / 實體 / 概念 / 綜合）。本 skill 負責其中的**跨來源綜合頁**。
- **流向**：`raw →（本 skill 綜合）→ wiki`。使用者自行從 wiki 撿選內容進 Cards/Topics，那不在本 skill、agent 也不碰 Cards/Topics。

agent 自主維護 wiki，不需逐頁拍板；偵測到 cluster 後**列出可綜合的主題群、與使用者確認切角**（尤其 cluster 過寬要拆），再綜合——這是讓使用者導引重點，不是逐步審批。

## 前置條件

用 harness-native `Read vault-map.md` 確認 cwd 是 vault root（不經 shell、跨平台）。讀不到就停止，請使用者 cd 到 vault root（`~/code/obsidian-memory`；三平台一致，cmd.exe 不認 `~` 改用 `%USERPROFILE%\code\obsidian-memory`）。

## 資源

- `scripts/cluster.py`：掃 raw，依既有 tags 找 ≥N 篇共享主題的散落項，輸出 JSON。已被既有 wiki 頁指到的 raw 視為已綜合，整群已綜合的 cluster 不重複提議。
- `references/synthesizer.md`：綜合器 subagent prompt。傳給 Agent subagent 時貼**全文** + 本次主題與成員 raw 全文；不叫 subagent 自己讀。無 Agent 工具時主 agent 直接 Read 全文照走同一流程。

## 主流程

1. 確認 cwd（見前置條件）。
2. 偵測 cluster（門檻預設 3）：

   ```
   python3 .agents/skills/vault-wiki-build/scripts/cluster.py --min 3
   ```

   使用者指定門檻時加 `--min N`。輸出為 JSON：`clusters` 依 `new_count`（未綜合過的成員數）排序。
3. `cluster_count` 為 0 → 回報「無 ≥N 篇共享主題的散落 raw，暫無可綜合主題」，停止。
4. **列出並確認切角**：把每個 cluster 列成一行——主題 tag、篇數（`count`／其中未綜合 `new_count`）、成員標題。與使用者確認要綜合哪些、切角怎麼切。
   - cluster 過寬（成員數很大、主題發散，如把整個 `claude-code` 混在一起）時，主動建議縮小切角或拆成子主題，別硬綜成一頁大雜燴。
5. 對每個選定的 cluster：
   - Read 成員 raw 筆記全文。
   - 可用 `Agent` 工具時：`subagent_type: "general-purpose"`，prompt = `references/synthesizer.md` 全文 + 主題 tag + 成員路徑與全文 + 今日日期（`YYYY-MM-DD`）。無 Agent 工具時主 agent 直接 Read `references/synthesizer.md` 照走。
   - subagent 依**綜合價值判準**：跨 ≥2 來源、綜合出原文沒有的結論才產頁到 `wiki/<主題>.md`；只是鏡射單源就回報原因、不產鏡射頁。
6. **更新 `wiki/01.index.md`**：把新產出的頁登錄進內容目錄對應類別（概念頁 / 實體頁 / 摘要綜合頁），各附一行摘要 + wikilink。

## 固定回覆

完成後回覆：

- 偵測到的 cluster 數 / 選定數 / 實際產出頁數
- 各產出頁路徑與涵蓋來源
- 被綜合價值判準擋下的 cluster 與原因
- `wiki/01.index.md` 已更新的條目
