---
title: Vault Lint Backlog
created: 2026-07-13
updated: 2026-07-16
tags:
  - meta
  - lint
---

# Vault Lint Backlog

vault 健檢的**待處理清單**,由 `vault-lint` skill 每輪讀寫(手動或排程觸發皆同)。findings 去重後留在此,解決即移除;你的決定(婉拒)留在此,約束 agent 之後的行為。

放 `schema/` 而非 `feeds/`:這不是「給人瀏覽的自動產物」,而是 **agent 每輪讀回來、用來約束自己行為的跨 session 操作狀態**——與 [`MEMORY.md`](MEMORY.md) 同層。`feeds/` 的規則是 agent 不讀,把行為約束放進去會自相矛盾,別的工具打開 vault 也看不到你的決定。

- 機械可修項(路徑錯的死連結、缺欄位、有 `description` 的 index 漏登)由 skill **自動修**,不進本清單。
- 需判斷 / 語意項進 `待你決定`;你退回的修法進 `已婉拒`,skill 之後不再重提。
- **頁面引用一律用反引號**(如 `` `wiki/某頁.md` ``),**不得用 wikilink**——`schema/` 在死連結掃描範圍內,用 wikilink 會被自己的 lint 掃成死連結。
- **沒有「上次執行」欄位,無發現的一輪本檔零變更**——那是排程器的營運狀態,不是 vault 的知識;記在這裡會讓每輪都產生 diff、天天開一個「今天沒事」的 PR。排程是否還活著,去排程器的執行紀錄看。

## 設定

- `semantic_days: 7` — 語意層只審近 N 天有 git 變動的 wiki 頁
- `semantic_page_cap: 10` — 語意層單次最多審幾頁,超過取最近變動者並標注截斷

## 待你決定

- [低] RAWGAP | `raw/clippings/` | **現存 clippings 全數判定已消化,無待 ingest**(機械層仍會逐篇 flag,因未加 wikilink;此註記為判斷錨點,防重複洗版)。2026-07-16 結清最後 2 篇:`Claude-Code-Best-Practice-—-Threads-Carousel-Cards`(82 條操作最佳實務)判定**不 ingest**——純操作 cheatsheet、大量版本專屬易過期內容與 wiki 時間抗性相斥,概念層已由 harness/記憶/多-agent/實證四側面 5–7 頁涵蓋,屬使用者自撿進 topics 公開層的料;`The-Official-BMad-Method-Masterclass`(BMAD IDE 工作流示範逐字稿)行銷示範品質撐不起一手實體頁,已將其角色鏈(Analyst→…→QA)＋advanced elicitation＋doc sharding 最小增補進 `wiki/AI-自主工作流的實證檢驗.md` spec-driven 節,不建專頁。原項首見 2026-07-13

_(2026-07-16 語意層 13 項——2 過時、9 交叉引用缺口、2 低優先群組——經使用者「全都修」指示已全數修補落地,退場。)_

## 已婉拒

_(目前無項目)_
