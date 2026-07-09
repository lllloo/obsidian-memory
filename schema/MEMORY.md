---
title: Agent Memory
created: 2026-07-09
updated: 2026-07-09
tags:
  - meta
---

# Agent 跨 Session 記憶

有界、凍結快照式檔案，記錄 agent 跨 session 該延續的**操作狀態**——不是 wiki 內容（陳述性知識），也不是治理規則（那是 CLAUDE.md／SYSTEM-DESIGN.md 的事）。設計借鑑 [[Hermes-Agent]] 的 `MEMORY.md`／`USER.md`：**有上限、不自動摘要精簡**，寫爆時手動整理過時條目，逼自己維持精簡而非無限累積。由 `CLAUDE.md` `@` 匯入，session 開始自動載入；只在明確檢查點（如健檢、研究回存）更新，不逐句隨對話碎片化改動。

## 上限

正文（不含本節與 frontmatter）**不超過 40 行**。超過時先合併/刪除過時條目，不是加大上限。

## Skill 升級訊號候選

判準見 [`SYSTEM-DESIGN.md`](SYSTEM-DESIGN.md) 的「Skill 升級訊號」一節：候選滿 3 次時，**主動提議使用者要不要寫成 skill，不擅自動筆**；使用者點頭才動手拆 `SKILL.md`／`references/*.md`。

- **Lint checklist**（孤立頁比對、raw-index `.base` 動態查詢誤判排除、tag 表同步）——出現 1 次（2026-07-09 健檢對話）
- **deep-research 回存流程**（建頁→更新 index→補雙向交叉引用→同步 tag 表）——第 3 次出現已於 2026-07-09（跨專案協作機制研究）觸發提議，**使用者判定該輪查證結果沒有回存價值而回絕**；純出現次數不是自動觸發依據，下次候選需一併評估該輪產出是否值得回存，不要只看次數重提

## 待追蹤的開放問題

- Hermes 自主 skill 生成的品質把關機制未查證（已知有背景 skill-review agent 產生非預期副作用的案例）——借鑑其「免拍板」模式前需先確認失敗模式，見 [[第二大腦方法論比較]]
- skill 自動生成若引入免拍板機制，透明作法定為「事後可見（如 commit 訊息標記），而非逐次拍板」——目前只有原則共識，尚無實作
