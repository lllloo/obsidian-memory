---
name: vault-updates-daily
description: 每天彙整高信任 developer tooling 更新成一篇 Obsidian daily updates briefing。使用官方 changelog / release notes、GitHub releases、GitHub discussions，含 authenticated user 的 starred repo releases；專注 coding agent、CLI、API、model、connector、developer workflow 相關變更。追蹤來源只讀 `Inbox/Updates/01.index.md`，不硬編碼工具清單。使用時機：使用者要求「同步 changelog」、「release notes 更新」、「官方變更同步」、「daily updates」、查最近工具更新，或直接呼叫 /vault-updates-daily。
---

# Vault Updates Daily

同步高信任 developer tooling 更新到 Obsidian，產出可回查、可消化的 Inbox briefing。重點是 high precision：少收但可用，不把 changelog 當全文剪藏。

## 產出

- 日報：`Inbox/Updates/<YYYY-MM-DD>-daily-updates.md`
- 來源設定：`Inbox/Updates/01.index.md`
- 日報進 Inbox，代表「高信任待消化來源」；不要直接整理進 `Cards/` 或 `Topics/`。
- 同日多次同步時追加新內容，不覆蓋舊日報；不要把日報 wikilink 追加回 index。

日報 frontmatter：

```yaml
---
title: "<YYYY-MM-DD> Daily Updates"
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags:
  - updates
  - <本次涵蓋的工具 tag，取自 01.index.md>
---
```

正文按工具分 `## <工具名>` section；每筆 entry 保留繁中摘要與 3-6 條重點，避免逐條搬運原文。

## 資源

- `references/daily-runbook.md`：執行細節。真正同步前必須先讀全文。
- `references/item-analyzer.md`：候選分析 prompt。分析前讀全文；傳給 Agent subagent 時貼全文，不叫 subagent 自己讀檔。
- `scripts/fetch_updates.py`：從 index 抓候選，輸出 machine-readable lines。
- `scripts/dedup_check.py`：寫入前查重，避免跨日重報。

## 主流程

1. 用 harness-native `Read vault-map.md` 確認 cwd 是 vault root；讀不到就停止，請使用者 `cd C:\code\obsidian-memory`。
2. 讀 `Inbox/Updates/01.index.md`。不存在或三個來源段皆空時停止，請使用者先補來源；單段為空只略過該來源類型。
3. 讀 `references/daily-runbook.md`，照 runbook 解析 index、抓候選、處理 `OFFICIAL:`、去重、分析與組裝。
4. 預設同步最近 7 天；使用者指定日期時用該日期到今天。
5. 執行抓取：

```
python3 .agents/skills/vault-updates-daily/scripts/fetch_updates.py
```

指定日期時加 `--since YYYY-MM-DD`；自訂 index 時加 `--index <path>`。

6. 對 `OFFICIAL:` 行使用 Defuddle 或 WebFetch 讀取官方頁，依 runbook 擷取近期 changelog section 成候選。
7. 粗篩只保留會影響 workflow / CLI / API / model / connector / billing-quota / deprecation / breaking change / security posture 的項目；跳過 dependency bump、alpha noise、無使用者可見變更、非 developer workflow 內容。
8. 寫入前每筆先跑 `dedup_check.py`；命中 `DUP:` 就跳過，不傳分析。
9. 去重後最多送 24 筆進分析。可用 `Agent` 工具時每批 8-10 筆平行分析，`subagent_type: "general-purpose"`；無 Agent 工具時主 agent 直接照 `references/item-analyzer.md` 分析。
10. 依 `TOOL:` 分組組裝日報，合併本次 tags 到 frontmatter，更新 `updated`。

## 固定回覆

完成後回覆：

- 各來源抓取數 / 粗篩通過數 / 已寫入數
- 日報路徑
- 跳過原因分布
- 需要人工追蹤但未建檔的候選，最多 5 筆

若來源抓取接近 runbook 記載的上限，明確標注可能截斷。
