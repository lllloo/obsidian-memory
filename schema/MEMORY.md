---
title: Agent Memory
created: 2026-07-09
updated: 2026-07-11
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

- ~~Lint checklist~~——2026-07-10 已 codify 成 `vault-lint-daily` skill（使用者主動提出，非滿 3 次觸發；`.base` 誤判排除已寫進掃描腳本 BASEIDX 邏輯），候選收掉
- ~~deep-research 回存流程~~——2026-07-10 第 4 次（repo 方向研究）結案：主體流程與 CLAUDE.md Ingest 重合，**不開 skill**；特有的「強度標註」寫法已 codify 進 CLAUDE.md 寫入慣例第 6 條（使用者核可）。重開條件：回存變每週例行、或流程長出 CLAUDE.md 沒有的專屬結構。價值判準沿用：先評該輪產出值不值得存
- **貼 URL ingest 全流程**（抓內容→存 raw/Clippings→寫 wiki→更新 index→交叉引用→收尾 lint）——2026-07-10 schema 落地（raw write-once），目前 0 次手動執行；滿 3 次時評估 codify 成 skill（類 youtube-sync 的網頁版）

## 待追蹤的開放問題

- 成長面 Lint 自動化（SYSTEM-DESIGN.md「不做自動成長掃描」）：2026-07-10 已採**限縮版**——結構性 lint 綁進 ingest 收尾、只檢當輪動到的頁（見 CLAUDE.md Ingest 第 5 步），由 Karpathy 社群生產經驗（漂移是頭號失敗模式）佐證。更重的**背景全庫成長掃描**仍不做（7/9 決定不變，token 成本不成比例）。
- 2026-07-10 七線全面審核結案（含第二輪複審通過）：批次 A（README）、B（強度標註/措辭）、D（複審殘留三項）已修；**倉庫衛生兩項使用者拍板不動、勿重複提議**——`.gitignore` 不補 `.env`/金鑰類規則、`.obsidian/plugins/obsidian-git/` bundle 維持 tracked（換機開箱即用優先）。
- `raw/Archive/` 3 檔是否本就不 ingest 未確認；YouTube 自動產物已移至 `feeds/youtube/`，不再把未沉澱數量視為 raw 消化待辦，只在使用者明確指定主題簇時處理。
