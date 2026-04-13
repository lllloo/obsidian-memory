---
title: "Claude 全新顧問模式：效果更好，還更便宜"
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
published: 2026-04-09
source: https://youtu.be/hGYfsvlQ5Ok
---

**影片描述**：Anthropic 發布 Advisor Strategy，讓 Opus 擔任顧問角色、Sonnet 或 Haiku 擔任執行者，透過動態雙向互動達到更佳效果，且成本比單獨使用 Opus 低許多。此功能透過 API 自動運作，適合在 Claude Code 以外使用 Anthropic API 的應用程式。

**重點摘要：**
- Advisor Strategy 與 Claude Code Plan Mode 最大差異在於它是「持續動態」的：Sonnet 遇到無法解決的問題時會自動回頭請教 Opus，而非一次性規劃後就自行執行。
- Opus 全程保有完整 shared context，但不執行任何 tool call，所有工具操作都由 Sonnet 或 Haiku 執行，以此控制成本。
- 效能測試顯示，Sonnet 4.6 High + Opus Advisor 在 SWE-Bench 達 74.8（vs 單獨 72.1），成本約 $0.96/任務（vs 單獨 $19），效能更好且更便宜。
- 相同的優勢在 BrowseComp（60.4 vs 58.1）和 Terminal Bench 均獲得驗證，且每次都更便宜。
- 這填補了「想要比 Sonnet 更強但 Opus 又太貴」的需求缺口，提供介於兩者之間的效能，卻以低於正常 Sonnet 的成本達成。
- 使用方式：調整 API 呼叫，指定 `type: advisor` 與 `max_uses`（Opus 最多被諮詢的次數上限）。
- 此功能是 API 層級的功能，不是 Claude Code 的原生功能；適合用於有 Anthropic API 整合的自製 web 應用或 agent 系統。
