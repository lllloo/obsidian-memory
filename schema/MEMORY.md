---
title: Agent Memory
created: 2026-07-09
updated: 2026-07-09
tags:
  - meta
---

# Agent 跨 Session 記憶

有界、凍結快照式檔案，記錄 agent 跨 session 該延續的**操作狀態**——不是 wiki 內容（陳述性知識），也不是治理規則（那是 CLAUDE.md／SYSTEM-DESIGN.md 的事）。設計借鑑 [[Hermes-Agent]] 的 `MEMORY.md`／`USER.md`：**有上限、不自動摘要精簡**，寫爆時手動整理過時條目，逼自己維持精簡而非無限累積。由 `CLAUDE.md` `@` 匯入，session 開始自動載入；比照 Hermes 預設的 `write_approval: false`，**agent 自主、逐回合即時寫**——當下發現值得跨 session 延續的操作狀態就直接寫，不用等明確檢查點，不逐次拍板；40 行上限仍是唯一防線，寫爆時當場合併/刪除過時條目。

## 上限

正文（不含本節與 frontmatter）**不超過 40 行**。超過時先合併/刪除過時條目，不是加大上限。

## Skill 升級訊號候選

判準見 [`SYSTEM-DESIGN.md`](SYSTEM-DESIGN.md) 的「Skill 升級訊號」一節：候選滿 3 次時，**主動提議使用者要不要寫成 skill，不擅自動筆**；使用者點頭才動手拆 `SKILL.md`／`references/*.md`。

- **Lint checklist**（孤立頁比對、raw-index `.base` 動態查詢誤判排除、tag 表同步）——出現 1 次（2026-07-09 健檢對話）
- **deep-research 回存流程**（建頁→更新 index→補雙向交叉引用→同步 tag 表）——第 3 次出現已於 2026-07-09（跨專案協作機制研究）觸發提議，**使用者判定該輪查證結果沒有回存價值而回絕**；純出現次數不是自動觸發依據，下次候選需一併評估該輪產出是否值得回存，不要只看次數重提

## 待追蹤的開放問題

- 成長面 Lint 自動化（SYSTEM-DESIGN.md「不做自動成長掃描」）：曾提案比照 Hermes 背景 self-improvement review，限縮成「每次 ingest/query 結束後順手檢查當輪動到的幾頁」而非全庫掃描（全庫掃描 token 成本不成比例）。**2026-07-09 使用者選擇維持現況**（不做），列為未來可重新評估的待辦，非立即行動項。
