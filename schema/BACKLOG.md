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
- **頁面引用一律用反引號**(如 `` `wiki/某頁.md` ``),**不得用 wikilink**——`schema/` 在死連結掃描範圍內,用 wikilink 會被自己的 lint 掃成死連結。
- **沒有「上次執行」欄位,無發現的一輪本檔零變更**——那是排程器的營運狀態,不是 vault 的知識;記在這裡會讓每輪都產生 diff、天天開一個「今天沒事」的 PR。排程是否還活著,去排程器的執行紀錄看。

## 設定

- `semantic_days: 7` — 語意層只審近 N 天有 git 變動的 wiki 頁
- `semantic_page_cap: 10` — 語意層單次最多審幾頁,超過取最近變動者並標注截斷

## 待你決定

### 覆蓋缺口 / 可延伸新頁(需先確認不觸犯反過度工程)

- [中] NEWPAGE | OpenClaw | `wiki/Claude-Code-記憶系統六層比較.md` 第 52 行自我點名「Hermes 與 OpenClaw 同血緣,值得日後專門對照」;OpenClaw 另在 memsearch 移植、`hermes claw migrate` 多次被提卻無實體頁。橫跨記憶六層與 Hermes 兩簇的樞紐
- [低] NEWPAGE | SDD 工具橫向對照 | Spec Kit／Kiro／Tessl／BMAD／OpenSpec 散在 `wiki/AI-自主工作流的實證檢驗.md` 第 54 行 prose + 獨立 OpenSpec 頁,而平行的 wiki 工具簇已有 `wiki/LLM-Wiki-生態實作比較.md` 對照表。**權衡**:AI-自主聚焦「效果證據」、對照頁聚焦「工具功能」,切面不同不算重複,但 BMAD 當初刻意折進而非開頁——非急件
- [低] NEWPAGE | route B 記憶實作 | `wiki/Agent-記憶兩大路線-知識庫與-memory-bank.md` 的 route A 有 `wiki/LLM-Wiki-生態實作比較.md` 撐實作細節,route B(Cline Memory Bank)與相鄰 Letta MemFS 只有 inline 描述、無對等實作頁。可待再被引用時再開

### skill／系統層(改 agent 行為,依 repo 規則須逐項拍板)

- [中] SKILL | `vault-updates-daily` 雲端 routine 未排 | 該 skill 的 `starred-repos.txt` snapshot fallback 存在的唯一理由就是雲端 token-free 排程跑,基建做好卻只有 vault-lint 一支 routine。前置:須先本機 `--snapshot-starred` 一次並授權推送
- [中] SKILL | MEMORY「貼 URL ingest 全流程」候選計數失效 | 手動 ingest 無具名入口累積次數,結構上永遠踩不到「滿 3 次」門檻、無限期卡在 0 次;fetch 段已被全域 `defuddle` 覆蓋。建議做決策:退場 or 改用「時間／成長」訊號
- [低] SKILL | 跨工具可攜縫 | `schema/MEMORY.md` 自稱唯一跨工具可攜操作記憶,但靠 `CLAUDE.md` 的 `@schema/MEMORY.md` 自動載入,而 `@import` 為 Claude Code 專屬;Codex／Cursor／opencode 讀 `AGENTS.md` 不解析。可在 `AGENTS.md` 正文加一句「非 Claude Code 工具請先 Read `schema/MEMORY.md`、`schema/BACKLOG.md`」
- [低] SKILL | `ask-vault` 缺 `OBSIDIAN_VAULT` 逃生口說明 | 腳本支援該環境變數覆寫 vault 路徑,但 `SKILL.md` 沒提;非預設路徑時 agent 只會拿到「工具未就緒」。補一行

### frontmatter／一致性(注意 `raw/` write-once 約束)

- [低] FRONTMATTER | `sha256` 為白名單外欄位 | 只在 `raw/fetched/Anthropic-Cookbook-Research-Prompts.md`、`raw/fetched/Anthropic-Multi-Agent-Research-System.md` 出現,同資料夾其餘 3 檔沒有。**注意**:移除會改既有 raw、違反 write-once;現實解是納入 CLAUDE.md 白名單(當內容指紋)或接受現狀
- [低] FRONTMATTER | fetched 檔全掛 `tags: clippings` | 語意與資料夾矛盾(fetched 是 agent 貼 URL、clippings 是 Web Clipper);跨資料夾 tag 查詢會混淆。同受 raw write-once 約束,傾向接受或改慣例、不回改既有檔
- [低] FRONTMATTER | clippings 回連紀律不對稱 | 6 個 fetched 全有 wiki 回連,6 個 clippings 僅 1 個有——正是機械層每輪 flag clippings 的根因。立慣例「clipping 種子某 wiki 頁時在該頁補 `[[clipping]]` 回連」可讓 linter 自動消 flag

### 待回查 / 低信心(需原始記錄或跨頁核對)

- [低] RAWGAP | `raw/clippings/` | **現存 clippings 全數判定已消化,無待 ingest**(機械層仍會逐篇 flag,因未加 wikilink;此註記為判斷錨點,防重複洗版)。原項首見 2026-07-13,最後結清 2026-07-16(2 篇判定不 ingest／最小增補,見 git log)
- [低][低信心] STALE | `wiki/LLM-方案定價與-coding-agent-比較.md` | 孤立(入連太少)已修——補了 `wiki/Context-優先與多-agent-的適用邊界.md`、`wiki/AI-自主工作流的實證檢驗.md` 兩條反鏈。**殘留**:定價數字仍為 2026-05~07 快照(頁面已標「回官網查」),真要刷新須逐一 re-fetch 11+ 廠商即時價、且月月會再過期——屬「值不值得例行 re-ingest」的決策,非機械修
- [低][低信心] STALE/疑慮 | `wiki/第二大腦整合的現成工具與做法.md`↔`wiki/LLM-Wiki-生態實作比較.md` | 兩輪日期主題皆不同的 deep-research,統計數字(22 來源、25 條主張)完全相同,不排除巧合,亦可能複製前次框架未更新;建議之後回查原始記錄核實
- [低][低信心] STALE | `wiki/第二大腦方法論比較.md` | Hermes 雙軸類比(2026-07-09 驗證)未提及 `wiki/Hermes-Agent.md` 2026-07-14 新增的 Kanban board 任務佇列子系統;屬可補充的 enrichment、非錯誤,待再動該頁時順手

**審視後判斷維持現狀(不動)**:vault-lint 第二段語意自動修(刻意延遲、重開條件明確)、無 in-vault 全文搜尋(21 頁 Grep 夠用)、evals 覆蓋不均(機械掃描與外部 API 相依 skill 補 eval 邊際價值低)。

## 本輪語意層截斷(下輪續審)

- 2026-07-17(手動,近 10 頁):19 頁 `CHANGED` 依 `semantic_page_cap: 10` 只審 10 頁;略過 9 頁待下輪——`wiki/LLM-Wiki-生態實作比較.md`、`wiki/Claude-Code-記憶系統六層比較.md`、`wiki/Building-Effective-Agents-Anthropic.md`、`wiki/Agent-記憶兩大路線-知識庫與-memory-bank.md`、`wiki/第二大腦實踐與本-vault-優化.md`、`wiki/Context-優先與多-agent-的適用邊界.md`、`wiki/Agent-Harness-Engineering-框架綜述.md`、`wiki/Hermes-Agent.md`、`wiki/OKF-與本-vault-的相容性.md`

## 已修退場紀錄(精簡,細節見 git log)

- _(2026-07-16 全專案改進審視語意層 13 項——2 過時、9 交叉引用缺口、2 低優先群組——經「全都修」指示全數落地退場。)_
- _(2026-07-17「修問題」批次:全專案改進審視的 3 條 XREF(跨專案↔OKF、OpenSpec↔Agent-Harness、設計品質↔AI-生成流程圖)、07-16 語意層例行審查的 3 矛盾 + 6 XREF + 4 過時、07-17 例行審查的 4 條低信心新發現,均已修補落地;`feeds/watch/` 漏登已補進 `schema/vault-map.md`、`schema/SYSTEM-DESIGN.md`;`published` 空值寫法已統一為 `""`。低信心 XREF「AI-自主工作流 相關頁 pi-workflow 措辭」與過時「OpenSpec 31 工具」覆核後判定原敘述已足、退場。)_

## 已婉拒

_(目前無項目)_
