---
title: Vault Lint Backlog
created: 2026-07-13
updated: 2026-07-15
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

- [高] SCAN-BUG | `.agents/skills/vault-lint/scripts/lint_scan.py` | CHANGED 偵測用 `git log --name-only` 抓近 N 天變動的 wiki 頁,但呼叫時未設 `core.quotepath=false`;git 預設會把非 ASCII 檔名輸出成 quoted-octal 逃逸字串(如 `"wiki/\350...\346..."`),導致腳本的 `line.strip().startswith("wiki/")` 過濾對幾乎所有中文檔名頁面失效。本輪(2026-07-15)機械掃描只驗出 2 頁(`wiki/Building-Effective-Agents-Anthropic.md`、`wiki/Hermes-Agent.md`),但手動加 `-c core.quotepath=false` 重跑同一 `git log --since` 查詢,實際近 7 天內有 18 頁 wiki 異動。熔斷機制(`ERROR:`/`SCAN:complete`)偵測不到此問題——腳本本身不報錯,只是靜默漏抓,語意層長期只審到一小部分頁面。建議修法:在該 subprocess 呼叫加 `-c`、`["git", "-c", "core.quotepath=false", "log", ...]`。本輪已手動補做語意審查以涵蓋真實 18 頁清單(見下兩項發現),但腳本本身的 bug 建議優先修,否則往後每輪都會複發同樣的隱性漏審。首見日 2026-07-15
- [中] 過時 | `wiki/第二大腦整合的現成工具與做法.md` | hot.md 一節仍稱「尚未拍板採用,列為可評估項」,但同批動到的 `wiki/跨專案第二大腦整合模式.md` 與 `wiki/01.index.md`「最近更新」已記錄 2026-07-15 拍板「方案 A」(index 最近更新區塊承載近期性、刻意不建獨立 hot.md)。建議把該節措辭更新為已拍板結果(不採用 hot.md),並回連決定出處。首見日 2026-07-15
- [低] 引用缺口 | `wiki/Agent-記憶兩大路線-知識庫與-memory-bank.md` | 關聯區塊稱 memory bank 檔(如 activeContext)細節「在該頁(`wiki/第二大腦整合的現成工具與做法.md`)與 `wiki/LLM-Wiki-生態實作比較.md`」,但前者實際未涵蓋 activeContext/Cline 六檔細節(只有後者的「近期熱脈絡層承載光譜」節有)。建議修正該指向,只留 `wiki/LLM-Wiki-生態實作比較.md`。首見日 2026-07-15
- [低] RAWGAP | `raw/clippings/` | 剩 2 篇真未消化新料待 ingest:`Claude-Code-Best-Practice-—-Threads-Carousel-Cards`(82 條最佳實務,參考型清單)、`The-Official-BMad-Method-Masterclass`(BMAD 完整 IDE 工作流;主題部分已散見 `wiki/AI-自主工作流的實證檢驗.md` 的 spec-driven 一節,ingest 前先評增量)。2026-07-15 已處理原 5 篇中 3 篇:`AI-做的設計` ingest 成 `wiki/設計品質的可量化檢測.md`;`Every-Claude-Code-Memory-System`(→`wiki/Claude-Code-記憶系統六層比較.md`)、`Harness-Engineering`(→`wiki/Agent-Harness-Engineering-框架綜述.md`)、`Copilot...spec-kit`(→`wiki/AI-自主工作流的實證檢驗.md` spec-driven 節)三篇主題已由一手來源頁深涵蓋、二次中文導讀無新主張,判定已消化不重 ingest。原項首見 2026-07-13

## 已婉拒

_(目前無項目)_
