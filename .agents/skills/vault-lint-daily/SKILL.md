---
name: vault-lint-daily
description: 每日 vault 健檢報告：掃 wiki+raw 的死連結、孤立頁、frontmatter 缺欄、tag 漂移、raw 消化缺口（機械層），加近期變動頁的矛盾／過時／交叉引用缺口審查（語意層），產出一篇報告到 feeds/lint/。機械項（可唯一對應的死連結、index 漏登錄）自動修並在報告記錄；語意項只報告，修補由使用者看報告後另行指示。使用時機：使用者要求「vault 健檢」「lint 報告」「每日健檢」「掃一下 wiki」「檢查 vault 健康」，或直接呼叫 /vault-lint-daily。
---

# Vault Lint Daily

產一份 wiki+raw 健檢日報供使用者瀏覽決策。**機械項自動修、語意項只報告**——對 `wiki/` 的寫入僅限下方「機械修補」明列的兩類；`raw/` 零寫入；報告寫入 `feeds/lint/`，整個 `feeds/` 不納入掃描。

## 產出

- 日報：`feeds/lint/<YYYY-MM-DD>-lint.md`
- 設定：`feeds/lint/01.index.md`（語意層掃描天數等）
- 日報存於 `feeds/lint/`，是使用者瞄一眼的消費性 feed；不屬三層系統、不進 raw、不當 ingest 原料。
- 同日重跑時在當日報告 append 新發現、更新 `updated`，不覆蓋、不另開檔。

日報 frontmatter：

```yaml
---
title: "<YYYY-MM-DD> Vault Lint"
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags:
  - lint
---
```

## 主流程

1. 用 harness-native `Read schema/vault-map.md` 確認 cwd 是 vault root；讀不到就停止，請使用者 cd 到 vault root（`~/code/obsidian-memory`；三平台一致，cmd.exe 不認 `~` 改用 `%USERPROFILE%\code\obsidian-memory`）。
2. `Read feeds/lint/01.index.md` 取設定（`semantic_days`、`semantic_page_cap`）；讀不到就用預設值（7 天、10 頁）並在報告註明。
3. 執行機械層掃描：

```
python3 .agents/skills/vault-lint-daily/scripts/lint_scan.py --days <semantic_days>
```

4. 機械修補（僅限以下兩類，其餘一律只報告）：
   - `DEADLINK`：目標檔實際存在、只是名稱或路徑寫錯且**可唯一對應**（如漏了資料夾限定、大小寫差異）→ 直接修正該 wikilink，報告記「已修」。無法唯一對應（目標真的不存在、或多個候選）→ 不修，列報告待使用者判斷。
   - `INDEXGAP`：wiki 頁存在但未登錄於 `wiki/01.index.md` → 讀該頁 frontmatter `description`（無則讀首段）補一行登錄到對應類別，報告記「已修」。
   - 修補動到的頁同步 `updated` 為今日。
5. 整理機械層發現：
   - 未修的 `DEADLINK`／`INDEXGAP` 與全部 `ORPHAN`／`FM` 逐條列入報告。
   - `TAG` 盤點由主 agent 判讀**同義異寫漂移**（如單複數、連字號變體、語意重疊的 tag 對），只列疑似漂移對，不列全表。
   - `RAWGAP`：`raw/Clippings/` 只彙總數量（agent 不主動消化區，列數字供參考即可）；`feeds/` 不掃描、不列待消化提醒。
   - 任何 `ERROR:` 行原樣寫進報告開頭。
6. 語意層：取 `CHANGED` 清單（近 N 天變動的 wiki 頁），超過 `semantic_page_cap` 時取最近變動的前幾頁並在報告標注截斷。每頁備妥「目標頁全文 + 鄰接頁全文（目標頁 wikilink 指到的頁與連入它的頁，各至多 5 頁）」。可用 `Agent` 工具時以 `subagent_type: "general-purpose"` 平行審查，prompt = `references/semantic-review.md` 全文 + 該頁與鄰接頁內容（不要叫 subagent 自己讀檔）；無 Agent 工具時主 agent 直接照該 reference 逐頁審查。
7. 組裝報告，段落順序：`## 摘要`（各類計數表，含已自動修補數）→ `## 已自動修補`（機械修補逐條：頁面、修了什麼；無則寫「無」）→ `## 機械層發現` → `## 語意層發現` → `## 建議修補清單`（合併兩層、按嚴重度排序，每條一句話 + 指向頁面）。無發現的段落寫「無發現」。
8. 機械修補以外不執行任何修補。語意項使用者要修時由使用者另行指示（如「照今天 lint 報告修」），屆時才動 wiki。

## 資源

- `references/semantic-review.md`：語意層審查 prompt。傳給 subagent 時貼全文。
- `scripts/lint_scan.py`：機械層掃描，輸出 machine-readable lines（格式見腳本 docstring）。

## 固定回覆

完成後回覆：

- 各類發現計數（死連結／孤立頁／frontmatter／tag 漂移疑似／raw 待消化／語意層）與已自動修補數
- 報告路徑
- 建議修補清單的前 3 條（高嚴重度優先）
- 語意層有截斷時明講掃了幾頁、略過幾頁
