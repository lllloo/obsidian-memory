---
title: Vault Lint Backlog
created: 2026-07-13
updated: 2026-07-17
tags:
  - meta
  - lint
---

# Vault Lint Backlog

vault 健檢的**待處理清單**,由 `vault-lint` skill 每輪讀寫(手動或排程觸發皆同)。findings 去重後留在此,解決即移除;你的決定(婉拒)留在此,約束 agent 之後的行為。

放 `schema/` 而非 `feeds/`:這不是「給人瀏覽的自動產物」,而是 **agent 每輪讀回來、用來約束自己行為的跨 session 操作狀態**——與 [`MEMORY.md`](MEMORY.md) 同層。`feeds/` 的規則是 agent 不讀,把行為約束放進去會自相矛盾,別的工具打開 vault 也看不到你的決定。

- 機械可修項(路徑錯的死連結、缺欄位、有 `description` 的 index 漏登)由 skill **自動修**,不進本清單。
- 需判斷 / 語意項進 `待你決定`;你退回的修法進 `已婉拒`,skill 之後不再重提。
- **agent 自己判維持現狀／待觸發的**進 `Agent 已判`——不每輪浮上來問你,除非有新資料或被再次引用才重開。
- **頁面引用一律用反引號**(如 `` `wiki/某頁.md` ``),**不得用 wikilink**——`schema/` 在死連結掃描範圍內,用 wikilink 會被自己的 lint 掃成死連結。
- **沒有「上次執行」欄位,無發現的一輪本檔零變更**——那是排程器的營運狀態,不是 vault 的知識;記在這裡會讓每輪都產生 diff、天天開一個「今天沒事」的 PR。排程是否還活著,去排程器的執行紀錄看。

## 設定

- `semantic_days: 7` — 語意層只審近 N 天有 git 變動的 wiki 頁
- `semantic_page_cap: 10` — 語意層單次最多審幾頁,超過取最近變動者並標注截斷

## 待你決定(真正需要使用者,其餘見 `Agent 已判`)

這三件因 push 授權／治理決定／repo「改 skill 一律先問」硬規則而卡在使用者,不由 agent 自主:

- [中] SKILL | `vault-updates-daily` 雲端 routine 未排 | 該 skill 的 `starred-repos.txt` snapshot fallback 存在的唯一理由就是雲端 token-free 排程跑,基建做好卻只有 vault-lint 一支 routine。**卡點**:須先本機 `--snapshot-starred` 一次並授權推送(排 routine 會 push 遠端,憲法唯一守門)——無使用者不能動
- [中] SKILL | MEMORY「貼 URL ingest 全流程」候選計數退場 | 手動 ingest 無具名入口累積次數,結構上永遠踩不到「滿 3 次」門檻、無限期卡在 0 次;fetch 段已被全域 `defuddle` 覆蓋。**這是使用者的 `MEMORY.md` 升級訊號治理決定**:退場(agent 建議),或保留「日後做網頁版 ingest skill」的種子改用時間／成長訊號
- [低] SKILL | 兩個一行文件補丁(可批) | 皆只記錄既有行為、零行為改變,但按 repo「改 skill 一律先問」需點頭:(1) 跨工具可攜縫——`AGENTS.md` 加一句「非 Claude Code 工具請先 Read `schema/MEMORY.md`、`schema/BACKLOG.md`」(`@import` 為 Claude Code 專屬,Codex／Cursor／opencode 不解析);(2) `ask-vault` 在 `SKILL.md` 補一行 `OBSIDIAN_VAULT` 逃生口說明(腳本已支援、文件沒提)

## Agent 已判(維持現狀／待觸發,不再每輪問)

**新頁候選——agent 判暫不開,待觸發**(反過度工程判斷屬 wiki 全權;有新料或被再次引用才重開):

- NEWPAGE | OpenClaw | 記憶六層與 Hermes 頁點名「值得日後專門對照」,橫跨兩簇的樞紐;inline 提及暫足夠,待被更多次引用再開(使用者 2026-07-17 亦「先不開」)
- NEWPAGE | SDD 工具橫向對照(Spec Kit／Kiro／Tessl／BMAD／OpenSpec) | AI-自主頁聚焦「效果證據」、對照頁聚焦「工具功能」切面不同,BMAD 當初刻意折進;非急件(使用者 2026-07-17 亦「先不開」)
- NEWPAGE | route B 記憶(Cline Memory Bank) | route A 有 `wiki/LLM-Wiki-生態實作比較.md` 撐,route B 與相鄰 Letta MemFS 只有 inline;待再被引用再開

**frontmatter／一致性——agent 判維持現狀**(動既有 raw 反違反 write-once;此註記為錨點,防機械層重複洗版):

- FRONTMATTER | `sha256`(白名單外,見兩個 `raw/fetched/` cookbook 檔)、fetched 檔 `tags: clippings`(語意與資料夾矛盾)、clippings 回連不對稱(6 clippings 僅 1 有 wiki 回連)——三者同受 raw write-once 約束,正解是接受現狀;唯 `sha256` 若要正式納 `CLAUDE.md` 白名單(當內容指紋)才需使用者動憲法檔,不納亦無妨

**其餘 agent 判斷不動**:

- STALE | `wiki/LLM-方案定價與-coding-agent-比較.md` | 孤立已修(補 2 條反鏈);定價數字仍為 2026-05~07 快照,頁面已標「回官網查」,agent 判**不值得例行 re-fetch**(11+ 廠商即時價、月月再過期)——要新快照再指示
- STALE | `wiki/第二大腦方法論比較.md` | Hermes 雙軸類比未提 `wiki/Hermes-Agent.md` 2026-07-14 新增的 Kanban board 子系統;屬 enrichment 非錯誤,待再動該頁順手補
- RAWGAP | `raw/clippings/` | 現存 clippings 全數判定已消化、無待 ingest(機械層仍逐篇 flag 因未加 wikilink;此為判斷錨點);首見 2026-07-13,最後結清 2026-07-16
- 待回查 | `wiki/第二大腦整合的現成工具與做法.md`↔`wiki/LLM-Wiki-生態實作比較.md` | 兩輪不同主題 deep-research 的統計數字(22 來源、25 主張)完全相同,需使用者當初原始記錄才能核實,agent 無解、留 watch-flag
- 維持現狀:vault-lint 第二段語意自動修(刻意延遲、重開條件明確)、無 in-vault 全文搜尋(21 頁 Grep 夠用)、evals 覆蓋不均(邊際價值低)

## 本輪語意層截斷(下輪續審)

- 2026-07-17(手動,近 10 頁):19 頁 `CHANGED` 依 `semantic_page_cap: 10` 只審 10 頁;略過 9 頁待下輪——`wiki/LLM-Wiki-生態實作比較.md`、`wiki/Claude-Code-記憶系統六層比較.md`、`wiki/Building-Effective-Agents-Anthropic.md`、`wiki/Agent-記憶兩大路線-知識庫與-memory-bank.md`、`wiki/第二大腦實踐與本-vault-優化.md`、`wiki/Context-優先與多-agent-的適用邊界.md`、`wiki/Agent-Harness-Engineering-框架綜述.md`、`wiki/Hermes-Agent.md`、`wiki/OKF-與本-vault-的相容性.md`

## 已修退場紀錄(精簡,細節見 git log)

- _(2026-07-16 全專案改進審視語意層 13 項——2 過時、9 交叉引用缺口、2 低優先群組——經「全都修」指示全數落地退場。)_
- _(2026-07-17「修問題」批次:全專案改進審視的 3 條 XREF、07-16 語意層的 3 矛盾 + 6 XREF + 4 過時、07-17 的 4 條低信心新發現,均已修補落地;`feeds/watch/` 漏登已補進 `schema/vault-map.md`、`schema/SYSTEM-DESIGN.md`;`published` 空值統一為 `""`。低信心「AI-自主 相關頁 pi-workflow 措辭」與「OpenSpec 31 工具」覆核後判定原敘述已足、退場。)_

## 已婉拒

_(目前無項目)_
