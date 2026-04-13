---
title: Claude 全新顧問模式：效果更好還更便宜
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-09
source: https://www.youtube.com/watch?v=hGYfsvlQ5Ok
---

## 描述

Anthropic 發布 Advisor Strategy（顧問策略），以 Opus 作顧問搭配 Sonnet/Haiku 執行，達成更好效果並降低成本。

## 重點摘要

**核心概念**
- Advisor Strategy：Opus 擔任顧問角色，負責規劃與指導；Sonnet 或 Haiku 擔任執行者，負責實際工具呼叫
- 與 Claude Code 的 Plan Mode（Opus 規劃後 Sonnet 執行）類似，但更進一步

**與 Plan Mode 的差異**
- Plan Mode 是一次性規劃後執行；Advisor Strategy 是持續性來回溝通
- 執行者（Sonnet）遇到無法解決的決策時，會自動回頭諮詢顧問（Opus）
- Opus 始終保有完整的共享上下文，但不執行任何工具呼叫

**效能數據**
- SWE-bench：Sonnet + Opus Advisor 得 74.8 分 vs 純 Sonnet 72.1 分
- BrowseComp：60.4 vs 58.1
- 費用：每個 agentic task 約 $0.96 vs 純 Sonnet 約 $19

**適用場景**
- 這是 API 層級的功能，非 Claude Code 原生功能
- 適合任何使用 Anthropic API 的 Web 應用程式
- API 呼叫需指定 `type: advisor` 及 `max_uses`（顧問被諮詢的最大次數）

**優勢**
- 介於 Sonnet 與 Opus 之間的效能，但成本低於正常 Sonnet
- 填補了 Sonnet 與 Opus 之間沒有中間模型的空缺
