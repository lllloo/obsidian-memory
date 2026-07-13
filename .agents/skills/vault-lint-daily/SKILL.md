---
name: vault-lint-daily
description: 每日 vault 健檢:掃 wiki+raw 的死連結、孤立頁、frontmatter 缺欄、tag 漂移、raw 消化缺口(機械層),加近期變動頁的矛盾／過時／交叉引用缺口審查(語意層)。機械可修項(可唯一對應的死連結、index 漏登)自動修;需判斷與語意項去重後進 feeds/lint/BACKLOG.md 待處理清單(語意項只報告,修補由使用者另行指示)。取代舊的每日快照報告,同一問題不重複洗版。使用時機:使用者要求「vault 健檢」「lint 報告」「每日健檢」「掃一下 wiki」「檢查 vault 健康」,或直接呼叫 /vault-lint-daily。
---

# Vault Lint Daily

維護一份 wiki+raw 健檢的**待處理清單** `feeds/lint/BACKLOG.md`。**機械可修項自動修、語意項只報告**——對 `wiki/` 的寫入僅限下方「機械修補」明列的類別;`raw/` 零寫入;清單寫入 `feeds/lint/`,整個 `feeds/` 不納入掃描。

## 產出

- 待處理清單:`feeds/lint/BACKLOG.md`(單一持久檔,去重後留未解決項,解決即移除)。**不再產每日快照報告檔。**
- 設定:`feeds/lint/01.index.md`(語意層掃描天數等)。
- 清單存於 `feeds/lint/`,是使用者瞄一眼的消費性 feed;不屬三層系統,不進 raw 或 wiki。

`BACKLOG.md` 結構:

- frontmatter:`title / created / updated / tags:[lint]`。
- 正文頂一行心跳:`> **上次執行**:<YYYY-MM-DD> · **狀態**:ok | scan-error | no-op`。
- `## 待你決定` — 需判斷的機械項 + 語意報告項,逐條一行(帶頁面、一句話、首見日)。
- `## 已婉拒` — 使用者退回的項;每條記所在段落錨,之後不重提。

## 主流程

1. 用 harness-native `Read schema/vault-map.md` 確認 cwd 是 vault root;讀不到就停止,請使用者 cd 到 vault root(`~/code/obsidian-memory`;cmd.exe 用 `%USERPROFILE%\code\obsidian-memory`)。
2. `Read feeds/lint/01.index.md` 取設定(`semantic_days`、`semantic_page_cap`);讀不到用預設(7 天、10 頁)。`Read feeds/lint/BACKLOG.md` 取既有清單(含 `已婉拒`)。
3. 執行機械層掃描:

```
python3 .agents/skills/vault-lint-daily/scripts/lint_scan.py --days <semantic_days>
```

4. **熔斷檢查**:掃描輸出**有任何 `ERROR:` 行、或缺 `SCAN:complete` 行** → 本輪視為掃描異常:**只新增、不退場**(不移除 BACKLOG 既有項),心跳狀態記 `scan-error`。正常則往下。
5. 機械修補(僅限以下兩類可**唯一對應**者,自動修並記錄;其餘一律不修):
   - `DEADLINK`:目標檔實際存在、只是名稱或路徑寫錯且**可唯一對應**(漏資料夾限定、大小寫差異)→ 直接修 wikilink。**目標不存在、多候選、或目標在 `feeds/` 等範圍外(wiki 不得引用 feeds)→ 不修,當「需判斷」項進 BACKLOG**。
   - `INDEXGAP`:wiki 頁存在但未登錄 `wiki/01.index.md`,且該頁 frontmatter **有 `description` 可複製** → 補一行登錄。無 `description` 需生摘要 → 不自動修,進 BACKLOG。
   - 修補動到的頁同步 `updated` 為今日。
6. **對 BACKLOG「待你決定」做 reconcile**(去重 + 退場):
   - **去重**:新掃出的每一項,跟 BACKLOG 既有項比對(同頁 + 同目標/同議題)→ 已在清單就不重複加。比對用讀進 context 的兩份短文本判斷,不算 hash。
   - **退場**(熔斷未觸發時):BACKLOG 既有機械項若本輪掃描不再輸出 → 移除。語意項僅當**該頁本輪在 `CHANGED` 內被重審且未重現**才移除;該頁未變動 → 保留。
   - **已婉拒**:`已婉拒` 清單中的項,本輪一律**跳過不重提**;唯該項所在段落實際變動時,才移回「待你決定」標「基礎已變,重新評估」。
7. 整理機械層「需判斷」項寫入 `待你決定`:
   - 未自動修的 `DEADLINK`／`INDEXGAP`、全部 `ORPHAN`／`FM`(FM 缺 `updated` 等可視為機械可修者可直接補值,同步 `updated`)。
   - `TAG` 盤點由主 agent 判讀**同義異寫漂移**,只列疑似漂移對。
   - `RAWGAP`:`raw/clippings/` 只彙總數量;`raw/fetched/` 未被引用時逐條列;`feeds/` 不列。
8. 語意層:取 `CHANGED` 清單,超過 `semantic_page_cap` 時取最近變動前幾頁並標注截斷。每頁備妥「目標頁全文 + 鄰接頁全文(wikilink 指到的頁與連入它的頁,各至多 5 頁)」**加上該頁在 BACKLOG 的既有語意項**(供去重)。可用 `Agent` 工具時以 `subagent_type: "general-purpose"` 平行審查,prompt = `references/semantic-review.md` 全文 + 該頁與鄰接頁內容 + 既有語意項(不要叫 subagent 自己讀檔);無 Agent 工具時主 agent 直接照該 reference 逐頁審查。語意發現去重後寫入 `待你決定`。
9. 更新心跳行(`updated`、上次執行日期、狀態 `ok`/`no-op`)。寫回 `BACKLOG.md`。
10. **開 PR**:本輪 BACKLOG 或 wiki 有變動 → commit 並開一個 per-run PR(分區:機械修補略讀、待你決定細看);全無變動 → 心跳仍更新但可不開 PR。**不 push/merge 到保護分支**(需使用者明確同意)。
11. 機械修補以外不執行任何修補。語意項使用者要修時另行指示,屆時才動 wiki。

## 資源

- `references/semantic-review.md`:語意層審查 prompt(含去重指示)。傳給 subagent 時貼全文。
- `scripts/lint_scan.py`:機械層掃描,輸出 machine-readable lines + `SCAN:complete`(格式見腳本 docstring)。

## 固定回覆

完成後回覆:

- 本輪:自動修 N 機械項、新增 M 待決項、退場 K 項、BACKLOG 現存 open 數。
- 心跳狀態(ok / scan-error / no-op)。
- `待你決定` 前 3 條(高嚴重度優先)。
- 語意層有截斷時明講掃了幾頁、略過幾頁。
