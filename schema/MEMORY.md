---
title: Agent Memory
created: 2026-07-09
updated: 2026-07-17
tags:
  - meta
---

# Agent 跨 Session 記憶

有界、凍結快照式檔案，記錄 agent 跨 session 該延續的**操作狀態**——不是 wiki 內容（陳述性知識），也不是治理規則（那是 CLAUDE.md／SYSTEM-DESIGN.md 的事）。**決策理由也不寫這裡**：settled 決策的 why 進 commit message 與相關 wiki/schema 頁就地記錄（`git log --grep` 可回溯）；本檔只留仍在約束當下行為的活狀態（勿重複提議的拍板、未實作項的重開觸發、排程/routine 的操作參照），不累積歷史沿革——反覆有損壓縮沿革正是記憶漂移的頭號來源。

存在理由是**可攜性**：agent 自身的 harness 記憶（如 Claude Code 的全域 memory）是工具專屬、不進 repo，換到別的 AI 工具打開這個 vault 就失憶；本檔 checked-in 進 repo，任何 agent、任何工具打開 vault 都讀得到，是這裡**唯一跨工具可攜的操作記憶載體**。由 `CLAUDE.md` `@` 匯入，session 開始自動載入。

**有界、不自動摘要精簡**：40 行上限是唯一防線，寫爆時當場合併／刪除過時條目，逼自己維持精簡而非無限累積。**agent 自主、逐回合即時寫**——當下發現值得跨 session 延續的操作狀態就直接寫，不用等明確檢查點，不逐次拍板。

## 上限

正文（不含本節與 frontmatter）**不超過 40 行**。超過時先合併/刪除過時條目，不是加大上限。

## Skill 升級訊號候選

判準見 [`SYSTEM-DESIGN.md`](SYSTEM-DESIGN.md) 的「Skill 升級訊號」一節：候選滿 3 次時，**主動提議使用者要不要寫成 skill，不擅自動筆**；使用者點頭才動手拆 `SKILL.md`／`references/*.md`。

- ~~Lint checklist~~——2026-07-10 已 codify 成 `vault-lint` skill（使用者主動提出，非滿 3 次觸發；`.base` 誤判排除已寫進掃描腳本 BASEIDX 邏輯），候選收掉
- ~~deep-research 回存流程~~——2026-07-10 第 4 次（repo 方向研究）結案：主體流程與 CLAUDE.md Ingest 重合，**不開 skill**；特有的「強度標註」寫法已 codify 進 CLAUDE.md 寫入慣例第 6 條（使用者核可）。重開條件：回存變每週例行、或流程長出 CLAUDE.md 沒有的專屬結構。價值判準沿用：先評該輪產出值不值得存
- ~~貼 URL ingest 全流程~~——2026-07-17 退場（使用者核可）：手動 ingest 無具名入口可累積次數，結構上永遠踩不到「滿 3 次」；fetch 段已由全域 `defuddle` 覆蓋，其餘與 CLAUDE.md Ingest 重合。重開條件：日後真的要做網頁版 ingest skill 時另起

## 待追蹤的開放問題

- 待辦：後續新增資料夾時路徑一律全小寫；目前不新增資料夾。
- **勿重複提議**（已拍板不動）：`.gitignore` 不補 `.env`/金鑰規則、`.obsidian/plugins/obsidian-git/` bundle 維持 tracked（換機開箱即用優先）。
- **勿再提議**為 lint/BACKLOG 加「上次執行／心跳」欄（已拍板移除）：與「安靜的一輪零變更、不開雜訊 PR」天生不相容；routine 存活靠 claude.ai 執行紀錄判斷，不靠 in-repo 紀錄。
- `vault-lint` 語意層已改**全面自動修**（2026-07-17 使用者拍板：agent 自主修、真需使用者的決策才進 BACKLOG）。**勿再提議**加獨立 refuter 對抗驗證——選項已擺出，使用者選了不加，review 靠排程端 PR diff。
- `vault-lint` **skill 本身不碰 git**；排程走雲端 routine（`trig_018QPWmi5K8hiV7ghMvKnTU9`，每天台北 05:00，claude-sonnet-5），其 prompt 自帶 commit+push+開 PR 且不依賴 Skill 工具（改讀 `SKILL.md`）——此即使用者對該 routine push 的明確同意（憲法唯一守門不因此鬆動）。
- `vault-updates-daily` 雲端 routine **已由使用者自行排定**（2026-07-17 告知，agent 未經手、無 trigger id）；**勿再提議排程**。其 starred 同步在本 vault 刻意停用（純雲端 atom 遭 proxy 擋），`starred-repos.txt` 快照留著但不靠它跑。
