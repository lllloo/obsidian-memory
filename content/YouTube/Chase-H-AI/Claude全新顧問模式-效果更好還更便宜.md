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

Anthropic 發布 Advisor Strategy，讓 Opus 擔任顧問、Sonnet/Haiku 執行，達到更佳效果且成本更低。

## 影片重點摘要

### 運作方式
- **Opus 擔任 Advisor**：負責規劃與指導
- **Sonnet 或 Haiku 擔任 Executor**：執行所有工作（包含 tool calls）
- 非一次性規劃，而是持續來回互動：Sonnet 遇到無法解決的決策時自動回頭請教 Opus
- Opus 全程保有完整 shared context，但不執行任何 tool call

### 效能對比（Sonnet 4.6 High + Opus Advisor vs 單純 Sonnet 4.6 High）
| 指標 | 有 Advisor | 無 Advisor |
|------|-----------|-----------|
| SWE-Bench | 74.8 | 72.1 |
| BrowseComp | 60.4 | 58.1 |
| 成本/任務 | ~$0.96 | ~$19 |

### 適用情境
- 使用 Anthropic API 的應用程式（非 Claude Code 原生功能）
- 需要介於 Sonnet 與 Opus 效能之間的場景
- API 呼叫需指定 `type: advisor` 及 `max_uses`（最多諮詢 Opus 的次數）

### 與 Claude Code Plan Mode 的差異
- Claude Code 的 plan mode 是一次性：Opus 規劃 → Sonnet 執行
- Advisor Strategy 是持續動態的雙向互動
- Advisor Strategy 透過 API 自動運作，不需手動切換
