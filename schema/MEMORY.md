---
title: Agent Memory
created: 2026-07-09
updated: 2026-07-13
tags:
  - meta
---

# Agent 跨 Session 記憶

有界、凍結快照式檔案，記錄 agent 跨 session 該延續的**操作狀態**——不是 wiki 內容（陳述性知識），也不是治理規則（那是 CLAUDE.md／SYSTEM-DESIGN.md 的事）。

存在理由是**可攜性**：agent 自身的 harness 記憶（如 Claude Code 的全域 memory）是工具專屬、不進 repo，換到別的 AI 工具打開這個 vault 就失憶；本檔 checked-in 進 repo，任何 agent、任何工具打開 vault 都讀得到，是這裡**唯一跨工具可攜的操作記憶載體**。由 `CLAUDE.md` `@` 匯入，session 開始自動載入。

**有界、不自動摘要精簡**：40 行上限是唯一防線，寫爆時當場合併／刪除過時條目，逼自己維持精簡而非無限累積。**agent 自主、逐回合即時寫**——當下發現值得跨 session 延續的操作狀態就直接寫，不用等明確檢查點，不逐次拍板。

## 上限

正文（不含本節與 frontmatter）**不超過 40 行**。超過時先合併/刪除過時條目，不是加大上限。

## Skill 升級訊號候選

判準見 [`SYSTEM-DESIGN.md`](SYSTEM-DESIGN.md) 的「Skill 升級訊號」一節：候選滿 3 次時，**主動提議使用者要不要寫成 skill，不擅自動筆**；使用者點頭才動手拆 `SKILL.md`／`references/*.md`。

- ~~Lint checklist~~——2026-07-10 已 codify 成 `vault-lint` skill（使用者主動提出，非滿 3 次觸發；`.base` 誤判排除已寫進掃描腳本 BASEIDX 邏輯），候選收掉
- ~~deep-research 回存流程~~——2026-07-10 第 4 次（repo 方向研究）結案：主體流程與 CLAUDE.md Ingest 重合，**不開 skill**；特有的「強度標註」寫法已 codify 進 CLAUDE.md 寫入慣例第 6 條（使用者核可）。重開條件：回存變每週例行、或流程長出 CLAUDE.md 沒有的專屬結構。價值判準沿用：先評該輪產出值不值得存
- **貼 URL ingest 全流程**（抓內容→存 raw/fetched→寫 wiki→更新 index→交叉引用→收尾 lint）——2026-07-10 schema 落地（raw write-once），目前 0 次手動執行；滿 3 次時評估 codify 成 skill（類 youtube-sync 的網頁版）

## 待追蹤的開放問題

- 待辦：後續新增資料夾時，路徑一律採全小寫；目前不新增資料夾。
- 成長面 Lint 自動化（SYSTEM-DESIGN.md「不做自動成長掃描」）：2026-07-10 已採**限縮版**——結構性 lint 綁進 ingest 收尾、只檢當輪動到的頁（見 CLAUDE.md Ingest 第 5 步），由 Karpathy 社群生產經驗（漂移是頭號失敗模式）佐證。更重的**背景全庫成長掃描**仍不做（7/9 決定不變，token 成本不成比例）。
- 2026-07-10 七線全面審核結案（含第二輪複審通過）：批次 A（README）、B（強度標註/措辭）、D（複審殘留三項）已修；**倉庫衛生兩項使用者拍板不動、勿重複提議**——`.gitignore` 不補 `.env`/金鑰類規則、`.obsidian/plugins/obsidian-git/` bundle 維持 tracked（換機開箱即用優先）。
- YouTube 自動產物位於 `feeds/youtube/`，是系統外、只供使用者瀏覽的內容，不進 raw 或 wiki。`raw/Archive/` 已於 2026-07-11 整個移除（原地說明「永久留存供回查」與治理規則的「不主動刪除」互相矛盾，經使用者拍板刪除並同步改掉 README/SYSTEM-DESIGN/vault-map/lint skill 的相關敘述）。
- 2026-07-13 lint skill 改制：以持久 `schema/BACKLOG.md`（待你決定／已婉拒兩區、去重、解決即移除、熔斷）取代每日快照報告，機械可修自動修、**語意仍只報告**。放 schema/ 而非 feeds/：它是 agent 每輪讀回來約束自身行為的操作狀態（feeds/ 規則是 agent 不讀，放那裡自相矛盾）；`feeds/lint/` 已整個移除。寫入該檔頁面引用一律反引號、不用 wikilink（schema 在死連結掃描範圍內）。此為「第一段 MVP」。**第二段**（語意自動修＋獨立 refuter 對抗驗證＋暫存修法經 merge 把關，經 5 輪對抗式分析定稿）**刻意未實作**：觸發＝使用者主動 felt-need（待你決定語意項堆積且想交給 AI）＋簽署治理位移（語意只報告→暫存修法，接受不可根除的殘留汙染風險）。定稿 spec 僅在當時 scratchpad（易失），未存進 repo。
- 2026-07-13 `vault-lint-daily` → **改名 `vault-lint`**（它不專為排程而生，手動隨時可跑）＋**skill 本身完全不碰 git**（不 commit/push/PR/建分支），手動與排程共用同一條流程、無模式分支。**推論**：git 動作移到呼叫端——排程若走雲端 routine（拋棄式環境），該 routine 的 prompt **必須自帶 commit+push+開 PR**，否則 BACKLOG 寫入隨環境蒸發、跨輪去重與「已婉拒」全失效；那句 prompt 即使用者對 push 的明確同意（憲法唯一守門不因此鬆動）。**雲端 routine 已建立**（每天台北 05:00，`trig_018QPWmi5K8hiV7ghMvKnTU9`，claude-sonnet-5；prompt 不依賴 Skill 工具，改叫它讀 `SKILL.md` 照做）。
- 2026-07-13 **BACKLOG 移除「執行狀態／心跳」區**（使用者拍板）：心跳持久化與「安靜的日子不開 PR」在雲端拋棄式環境**天生不相容**——心跳保證每輪有 diff，等於天天開一個「今天沒事」的雜訊 PR。「上次何時跑過」是排程器的營運狀態、非 vault 知識，不該進 BACKLOG。故 skill 改為**無發現時零檔案變更**，`scan-error` 改進「待你決定」（它本來就是該讓人看到的「有事」）。**已知代價、勿再提議修**：失去 in-repo 的「上次執行」紀錄，routine 若靜默死亡看不出來（安靜的日子同樣沒 PR），要靠 claude.ai 的 routine 執行紀錄判斷存活。
