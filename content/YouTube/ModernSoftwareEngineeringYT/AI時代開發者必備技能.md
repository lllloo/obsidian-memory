---
title: AI 時代開發者必備技能
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-13
source: https://www.youtube.com/watch?v=06kr0DiDAlU
---

Dave Farley 與 Gene Kim 對談，探討 Vibe Coding 普及後開發者需要什麼技能，以及架構設計與團隊結構的未來。

## 架構設計是否還重要？

Gene Kim 的疑問：若 LLM 能在幾分鐘內從零重寫系統，架構設計、延遲決策、模組化這些技能還重要嗎？

Dave Farley 的回應：**比以前更重要**，原因：
- 就算重寫成本降低，小改動仍應有小成本
- 良好架構讓你能快速取得回饋而不必全部重寫
- 「從頭重寫」是比以前好的 worst case，但不應是 default

## 把架構偏好餵給 LLM

Gene Kim 的實踐：把個人的架構品味寫成規則讓 LLM 遵守，例如：
- 後端 web server 要有 view 層、database 查詢集中在一個地方
- 不散落 SQL 字串
- 使用 closure-like 資料結構
- HTMX endpoint 要有固定的結構

關鍵概念：**LLM onboarding**——就像新人入職需要架構文件，AI 也需要。用 CLAUDE.md 或 README 描述「道路規則」，讓 LLM 不用讀完整個 codebase 就能遵守設計慣例。

（DORA AI 研究也確認：onboarding 文件對 AI 和人類都有效。）

## 初階開發者如何學習？

Dave Farley 的擔憂：快速迭代的 AI 輔助開發，junior 開發者能從噪音中找到訊號學到設計思維嗎？

Gene Kim 的看法：
- 教學內容需要改變——整學期的資料結構課可能不再必要
- 更需要的是：如何建立 **option-rich systems**（保留彈性的系統）
- 如何設計快速 feedback loop
- 引用 Merton（諾貝爾經濟學獎）：不確定性越高，越需要保留選項

## 團隊規模的轉變

- 傳統敏捷小組：6 個開發者 + PM + UX = 8 人
- AI 輔助後：可能 2 人就能走得比 8 人更快更遠
- 極端案例：部分前沿工程師規定「每個 repo 一個開發者」，因協作成本（merge conflict）超過收益

Kent Beck 說的模型：「有問題的人」直接與「能解決問題的人」合作，中間由 LLM 橋接。

## 核心結論

在快速變化的時代：
- **模組化架構**、**快速 feedback loop** 是讓系統保持安全的核心
- 這些原則在 AI 時代不是過時，而是更加關鍵
