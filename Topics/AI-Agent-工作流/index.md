---
title: AI Agent 工作流
description: Harness 設計、多 agent 協作、planner/generator/evaluator 三角，與 BMAD/GStack/Spec-Kit 等主流 agent framework 取徑
created: 2026-04-25
updated: 2026-06-22
tags:
  - ai-agent
---

聚焦 harness、multi-agent collaboration、planning / execution / evaluation 迴圈，以及代表性的 agent frameworks。

## 概念入口

- [[Harness-Engineering]] — Planner / Generator / Evaluator 三角 + 立場（Generator 不要自評 / 通用工具優於客製 / 狀態外部化）；連結各框架實作
- [[GAN-Style-Harness]] — 三角的具體實作：generator / evaluator 分離 + rubric 打分門檻，適合 UI / 主觀品質任務

## 框架速查

依框架聚合，每個框架的書籤＋流程速查放在一起。Spec 驅動取徑（Spec-Kit / OpenSpec）在前，lifecycle / persona 取徑（BMAD / GStack / Superpowers）在後。

**Spec-Kit** — GitHub 出的 Spec-Driven Development toolkit，spec 為 first-class artifact 驅動 agent 生 code（跨 30+ agent host）

- [[bookmark-Spec-Kit-Spec驅動開發框架|書籤]]
- [[Spec-Kit-流程]] — 流程速查指令

**OpenSpec** — Fission-AI 出品的輕量 spec-driven 框架，"Actions not phases" 哲學，支援 25+ AI coding agents

- [[bookmark-OpenSpec-Spec驅動開發框架|書籤]]
- [[OpenSpec-流程]] — 流程速查指令
- [[確認-OpenSpec-狀態]] — 狀態確認指令分工與 `requirements 0` parser 除錯

**BMAD** — agile lifecycle 為骨架的多 agent 開發框架（PM / Architect / Developer / UX 等 12+ 軟體角色 persona）

- [[bookmark-BMAD-Agent開發框架|書籤]]
- [[BMAD-Method-流程]] — 流程速查指令

**GStack** — planning / design / QA / ship 多 persona workflow pack（CEO / Eng / Design / DevEx 審查）

- [[bookmark-GStack-Agent開發框架|書籤]]

**Superpowers** — TDD gate / systematic debugging / review loop 為核心的 implementation workflow

- [[bookmark-Superpowers-Agent開發框架|書籤]]

## 後續候選（仍在 Cards/ 待消化）

- `Context-Engineering`——改寫消化後再升回 Topic。
- [[QA-系統聊天回覆方案]]——RAG / QA 回覆六種方案選型，單篇暫放 Cards，待同主題累積再升 Topic。
