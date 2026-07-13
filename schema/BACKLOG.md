---
title: Vault Lint Backlog
created: 2026-07-13
updated: 2026-07-13
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

## 設定

- `semantic_days: 7` — 語意層只審近 N 天有 git 變動的 wiki 頁
- `semantic_page_cap: 10` — 語意層單次最多審幾頁,超過取最近變動者並標注截斷

## 執行狀態

- **上次執行**:2026-07-13
- **狀態**:ok(死連結 0、孤立頁 0、frontmatter 缺欄 0、index 漏登 0;語意層審 1 頁,新增 3 項低嚴重度發現)

## 待你決定

- [低] RAWGAP | `raw/clippings/` | 5 篇 clipping 尚未消化(依 CLAUDE.md,clippings 由你明指才處理,此處僅告知數量);首見 2026-07-13
- [低] 過時 | `wiki/Hermes-Agent.md` | 「Tools(60+)」「90+ 預裝 skill」「8 個 memory provider 外掛」等數字未比照同頁「2,200/1,375 字元上限」「max turns 150」已採用的「官方文件快照值,隨版本可變」標注方式,隨 Hermes 版本迭代容易過期;建議補上限定語或改寫為行為描述;首見 2026-07-13
- [低] 過時 | `wiki/Hermes-Agent.md` | 「周邊」節 hermes-agent-self-evolution「每次優化約 $2–10」為未標日期的成本數字,隨 API 定價調整可能過時;建議註明查證/取自日期,比照本頁其他數字的快照標註慣例;首見 2026-07-13
- [低][低信心] 矛盾 | `wiki/Hermes-Agent.md` | 「學習迴路」表中「Autonomous skill creation…預設免人工核准即可寫入」與鄰接頁 `wiki/LLM-Wiki-生態實作比較.md`「自主權邊界」一節稱「Hermes 全面較保守」字面上易讓讀者誤讀為互相矛盾(實際指涉不同子系統:前者是一般 skill 生成、後者專指 `llm-wiki` skill 的內容編輯守門);建議加一句釐清範圍;首見 2026-07-13

## 已婉拒

_(目前無項目)_
