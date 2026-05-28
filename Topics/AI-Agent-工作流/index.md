---
title: AI Agent 工作流
description: Harness 設計、多 agent 協作、planner/generator/evaluator 三角，與 BMAD/GStack/Spec-Kit 等主流 agent framework 取徑
created: 2026-04-25
updated: 2026-05-28
tags:
  - ai-agent
---

聚焦 harness、multi-agent collaboration、planning / execution / evaluation 迴圈，以及代表性的 agent frameworks。

## 概念入口

- [[Harness-Engineering]] — Planner / Generator / Evaluator 三角 + 立場（Generator 不要自評 / 通用工具優於客製 / 狀態外部化）；連結各框架實作

## 工具書籤

- [[bookmark-Superpowers-Agent開發框架|Superpowers]] — TDD gate / systematic debugging / review loop 為核心的 implementation workflow
- [[bookmark-GStack-Agent開發框架|GStack]] — planning / design / QA / ship 多 persona workflow pack（CEO / Eng / Design / DevEx 審查）
- [[bookmark-BMAD-Agent開發框架|BMAD]] — agile lifecycle 為骨架的多 agent 開發框架（PM / Architect / Developer / UX 等 12+ 軟體角色 persona）；[[BMAD-Method-流程]] 速查指令
- [[Spec-Kit]] — GitHub 出的 Spec-Driven Development toolkit，spec 為 first-class artifact 驅動 agent 生 code（跨 30+ agent host）；[[Spec-Kit-流程]] 速查指令
- [[bookmark-OpenSpec-Spec驅動開發框架|OpenSpec]] — Fission-AI 出品的輕量 spec-driven development 框架，"Actions not phases" 哲學，支援 25+ AI coding agents；[[OpenSpec-流程]] 速查指令

## 後續候選（仍在 Cards/ 待消化）

`Context-Engineering`、`GAN-Style-Harness`、`dotLLM-AI-輔助開發方法論`——改寫消化後再升回 Topic。
