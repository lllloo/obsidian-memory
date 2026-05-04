---
title: You have to use Harness Engineering with GPT 5.5 to quit burning tokens
created: 2026-05-04
updated: 2026-05-04
source: https://www.reddit.com/r/codex/comments/1sx5q94/you_have_to_use_harness_engineering_with_gpt_55/
published: 2026-04-27
tags:
  - reddit
  - codex
  - workflow
  - best-practices
---

> **繁中摘要**：在大型 codebase 用 GPT-5.5 時，把 OpenAI Harness Engineering 文件貼進 chat 讓它對齊專案結構、再用 subagents 依規則維護「地圖式」上下文，比丟一坨 instructions 快、token 也省；同樣原則適用 skill 編排（main → sub skill map）與 model routing。

---

## 原文重點

- **核心做法**：把 [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/) 文件直接貼進 chat 讓 GPT-5.5 自我對齊專案，明顯加速大型 codebase 操作。
- **本質**：給 model 的不是「一條條指令」，而是「一組地圖」（map of project structure / module relationships）。
- **維護方式**：規則化要求 subagents 持續更新這份 map，避免地圖過期。

## 社群討論亮點

- **Skill 結構應為 map 不為 list**：90% GitHub 上的 `AGENTS.md` 是扁平 12389+ skill 列表，正確做法是 `main skill → sub skill` 樹狀地圖；agent 準確度與效率會大幅提升。
- **Governance 細項**：以 lanes、instructions、routing 治理 agent 行為；目的不是省 token，而是避免 context 被淹沒、品質才上去。已迭代到第 7 版 governance。
- **Model routing 原則**：planning skill 路由到 high-reasoning（如 GPT-5.5 high），implementation skill 路由到 medium / low；不要把 xhigh 浪費在 file edits。
- **GPT-5.5-low / medium 比 5.4 更省 token**：實測 token burn 較低、效率較高。
