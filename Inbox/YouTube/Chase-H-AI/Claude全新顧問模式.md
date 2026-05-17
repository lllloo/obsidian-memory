---
title: Claude 全新顧問模式：效果更好還更便宜
created: 2026-04-13
updated: 2026-04-13
source: https://www.youtube.com/watch?v=hGYfsvlQ5Ok
published: 2026-04-09
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
---

## 核心概念

Anthropic 發布 Advisor Strategy（顧問策略）：Opus 擔任顧問，Sonnet 或 Haiku 擔任執行者。

- Opus 負責規劃與指導，不執行任何工具呼叫
- Sonnet/Haiku 負責所有實際工具呼叫，並保有完整的共享上下文
- 透過 API 自動運作，適合 Claude Code 生態系以外的應用

## 與 Claude Code Plan Mode 的差異

Plan Mode 是「Opus 一次性規劃 → Sonnet 執行」的單向流程。Advisor Strategy 是**持續性雙向溝通**：

- Sonnet 遇到無法自行解決的決策時，自動回頭諮詢 Opus
- Opus 始終保有執行者的完整上下文
- 這個顧問↔執行者的關係持續整個任務過程，而非只發生一次

## 效能數據

| 指標 | Sonnet + Opus Advisor | 純 Sonnet |
|------|----------------------|-----------|
| SWE-bench | 74.8 | 72.1 |
| BrowseComp | 60.4 | 58.1 |
| TerminalBench | 更高 | 基準 |
| 每任務成本 | ~$0.96 | ~$19 |

效能介於 Sonnet 與 Opus 之間，但成本比正常 Sonnet 更低。

## 使用方式

這是 **API 層級**功能，需修改程式碼中的 API 呼叫：

```python
# 需指定兩個參數
type: "advisor"          # 啟用 advisor 模式
max_uses: <數字>         # Opus 被諮詢的最大次數
```

適用對象：在自己的 Web 應用中直接呼叫 Anthropic API 的開發者。不需要 Claude Code，任何使用 Anthropic API 的專案都能直接套用。

## 適用場景

- 需要比 Sonnet 更好效果，但 Opus 又太貴的情境
- 填補了 Sonnet 與 Opus 之間沒有中間模型的空缺
- 若本來就在用 Anthropic API 開發應用，幾乎是無腦升級
