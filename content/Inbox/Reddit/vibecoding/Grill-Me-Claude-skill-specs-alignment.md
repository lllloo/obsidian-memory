---
title: Viral 'Grill Me' Claude skill proves specs-to-code is vibe coding, 13K+ stars
created: 2026-04-28
updated: 2026-04-28
source: https://www.reddit.com/r/vibecoding/comments/1swyadr/viral_grill_me_claude_skill_proves_specstocode_is/
published: 2026-04-27
tags:
  - reddit
  - vibecoding
  - ai-tools
  - best-practices
---

> **繁中摘要**：Matt Pocock 的 `grill-me` Claude skill 翻轉了「寫 spec 餵 AI 生 code」的預設流程——改由 AI 反問你 40–100 題（需求、邊界、UX、資料模型、失敗模式）直到對齊心智模型才開始寫 code，PO 實測重寫時間下降 80%。

---

## 原文重點

- **問題**：標準的 spec-only workflow 本質是 vibe coding 的偽裝，AI 從未真正共享你對專案的 mental model，每輪迭代輸出反而劣化。
- **做法翻轉**：不是你解釋給 AI，而是 AI 用 40–100 題的問卷面試你，題目涵蓋 requirements / edge cases / user experience / data models / failure modes，**全部對齊完才寫第一行 code**。
- **效果**：PO 一週內在非 trivial 專案上實測，「alignment 步驟」讓重寫時間下降 80%。
- **核心主張**：alignment beats speed——對重要的工作，先求對齊，再求速度。

## Skill 內容（Top comment 提供）

```yaml
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---
Interview me relentlessly about every aspect of this plan until
we reach a shared understanding. Walk down each branch of the design
tree resolving dependencies between decisions one by one.
If a...
```

> 留言區只貼出片段；完整內容指向 Matt Pocock 的 GitHub repo（13K+ stars）。

## 社群討論亮點

- **延伸做法 — `deep-discovery` skill**（37 分）：另一個自我審問框架，用 100 道循序問題（每題基於前一題答案）窮盡探索一主題；作者拿來給 Codex 用。Repo：<https://github.com/forsonny/deep-discovery>。形式相近、目標相同（強制對齊）。
- **批評視角**（16 分）：對 99% 場景過度設計；真正有用的形態應該是 LLM-to-LLM 自循環——LLM1 提問 → LLM2 研究 codebase + web search → 回 LLM1，**只在很複雜的功能才值得**。提醒這套不該無腦套用到所有 ticket。
- **諷刺留言**（144 分）：「我會用我的 agents 來回答這 100 題」——點出風險：若把問卷外包給另一隻 LLM，alignment 就破功了，必須由人類回答才有意義。
