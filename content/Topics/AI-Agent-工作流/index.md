---
title: AI Agent 工作流
created: 2026-04-25
updated: 2026-04-25
tags:
  - ai-agent
  - moc
---

聚焦 harness、multi-agent collaboration、planning / execution / evaluation 迴圈，以及代表性的 agent frameworks。

## Harness 與方法論

- [[Agent-Harness]] — 長任務 agent 的外部執行殼層、三角核心與多 agent 拓撲
- [[GAN-Style-Harness]] — Planner / Generator / Evaluator 對抗式循環的具體實作

## 代表框架

- [[GSD框架]] — 以 fresh session / state machine 驅動的 orchestration 流派
- [[GStack框架]] — 規劃、設計、QA、部署一條龍的 workflow pack
- [[Superpowers框架]] — 以 TDD gate 與 systematic debugging 為核心的實作流派

## 大型案例

- [[dotLLM-AI-輔助開發方法論]] — systems-level 專案如何靠文件、review 與 skills 放大 AI 生產力

## Context 與記憶體管理

- [[Context-Engineering]] — 聚焦 context engineering、memory、session 管理；仍需持續補證據與清洗舊 heuristics