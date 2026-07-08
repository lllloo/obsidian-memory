---
name: vault-wiki-build
description: 把散落 raw（整個 raw）綜合壓縮成 wiki 候選頁。偵測 ≥N 篇共享同主題的散落原料 → 提議 → 使用者同意才產頁到 wiki/，全 draft、可丟可重生。壓縮硬閘（跨 ≥2 來源才產、鏡射單源則拒）、單向 wikilink 指回 raw。使用時機：使用者說「建 wiki 候選」、「綜合散落 raw」、「掃 raw 找可綜合的主題」、「wiki build」，或直接呼叫 /vault-wiki-build。
---

# vault-wiki-build — raw → wiki 候選層

掃 raw 找共享主題 → 列 cluster 提議 → 使用者挑 → subagent 綜合成 wiki 候選頁。

## 定位

- **raw = 整個 `raw/`**：永久留存的原料，本 skill 只讀不改。
- **wiki = AI 候選層**：把散落 raw 壓縮成的候選頁，全 `draft: true`、可丟可重生。給人看為主。
- **流向**：`raw →（本 skill 綜合）→ wiki(候選) →（人內化）→ Card → Topic`。wiki→Card 匯出由使用者挑選、機制另定，不在本 skill。

**提議制**：偵測到 cluster 只是「有這個可綜合」，不等於要產。一律先列提議、等使用者挑哪幾個才產——只持久化使用者說「會回來看」的。

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
3. `cluster_count` 為 0 → 回報「無 ≥N 篇共享主題的散落 raw，暫無候選」，停止。
4. **提議**：把每個 cluster 列成一行——主題 tag、篇數（`count`／其中未綜合 `new_count`）、成員標題。問使用者「要綜合哪幾個成 wiki 候選頁？」。**不要全部自動產**；使用者沒挑就不動。
   - cluster 過寬（成員數很大、主題發散，如把整個 `claude-code` 混在一起）時，主動建議縮小切角或拆成子主題，別硬綜成一頁大雜燴。
5. 對每個**使用者選中**的 cluster：
   - Read 成員 raw 筆記全文。
   - 可用 `Agent` 工具時：`subagent_type: "general-purpose"`，prompt = `references/synthesizer.md` 全文 + 主題 tag + 成員路徑與全文 + 今日日期（`YYYY-MM-DD`）。無 Agent 工具時主 agent 直接 Read `references/synthesizer.md` 照走。
   - subagent 依**壓縮硬閘**判斷：跨 ≥2 來源、綜合出原文沒有的結論才產頁到 `wiki/<主題>.md`；只是鏡射單源就拒絕、回報原因，不產垃圾頁。
6. wiki 頁由 `wiki/清單.base` 自動列出，不需手動維護 `wiki/01.index.md` 目錄。

## 固定回覆

完成後回覆：

- 偵測到的 cluster 數 / 使用者選中數 / 實際產出頁數
- 各產出頁路徑與涵蓋來源
- 被壓縮硬閘拒絕的 cluster 與原因
- 提醒：wiki 頁為 `draft` 候選；要升 Card 由使用者挑選、機制另定
