---
title: Agent Memory
created: 2026-07-09
updated: 2026-10-13
tags:
  - meta
---

# Agent 跨 Session 記憶

只保留跨 session 仍有效的操作狀態、勿重複提議的決定與重開條件，不作例行摘要精簡。決策理由與已結案歷史回查 git；治理規則放 AGENTS.md／SYSTEM-DESIGN.md。此檔進 repo，供各 AI 工具共用；Claude Code 以 `@` 匯入，其餘工具手動讀取。

## 上限

正文（不含本節與 frontmatter）不超過 40 行。agent 發現需延續的狀態即時維護；超過上限時合併或刪除過時條目，不擴大上限。

## Skill 升級訊號候選

判準見 [SYSTEM-DESIGN.md](SYSTEM-DESIGN.md)「Skill 升級訊號」。目前無活躍候選；以下只留重開條件：

- deep-research 回存不另開 skill；僅在回存成為每週例行、或出現 AGENTS.md 未涵蓋的專屬流程時重評。
- 貼 URL ingest 沿用 AGENTS.md 與全域 `defuddle`；日後明確要做網頁版 ingest skill 才重開。

## 操作約束與待追蹤項

- 新增資料夾一律全小寫；目前不新增。
- **勿重複提議**：`.gitignore` 不補 `.env`／金鑰規則；Obsidian Git bundle 維持 tracked，供換機使用。
- **勿再提議**：lint／BACKLOG 不加執行心跳或「上次執行」欄，無發現的一輪零檔案變更；語意層不加獨立 refuter，review 靠事後 GitHub diff。
- `vault-lint` 本身不碰 git；雲端 routine 已停用，目前只手動觸發，由呼叫端 agent commit／push。原 trigger `trig_018QPWmi5K8hiV7ghMvKnTU9` 留作重啟參照。
- **研究結果回存 wiki 由 agent 自行判斷**（2026-10-15 使用者指示）：deep-research／Query 結束後不再問「要不要存」，值得就直接回存並在回覆中告知。
- **跨 repo 的實作回該 repo 做**：本 vault 只存跨專案通用知識，不寫他 repo 的實作細節或專案狀態。
- **playbook**：獨立私人 repo＋`lllloo/skills` 的 `/playbook` skill；查時掃檔名／title／description，不建索引；寫時 AI 開分支送 PR，由使用者審後合。只手動觸發，勿提議全域規範自動查；實作在那兩個 repo，本 vault 無跨專案查詢入口。
- **私人筆記在 Notion**：tmux／git archive 保留原「技術筆記」入口，勿移入新資料庫；不重建 topics/cards。日常流程不讀寫 Notion，只有重新明確指定的 Notion 任務才操作。
- **本 repo 只供 AI 跑核心流程**（2026-10-13）：不重建真人入口、架構讀本或 PR 合併 Discord 通知；保留 raw／wiki、規範、`vault-lint` 與必要設定。歷史入口集中於 `schema/vault-map.md`。
- **勿重建** `feeds/`、`docs/architecture/`、`vault-youtube-sync`、`vault-watch`、`vault-page`、`vault-updates-daily`（含輕量版）。
