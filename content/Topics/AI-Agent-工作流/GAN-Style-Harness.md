---
title: GAN Style Harness
created: 2026-04-02
updated: 2026-04-25
tags:
  - claude-code
  - ai-tools
  - ai-agent
  - harness
---

模仿 GAN（生成對抗網路）概念的多 agent 協作系統：三個 agent 透過對抗式循環反覆提升產出品質。這個 pattern 來自 `everything-claude-code` 的 `gan-style-harness` skill / agents，靈感可對應到 Anthropic 的 planner / generator / evaluator 三角。

## 三個角色

| Agent | 角色 | 主要任務 |
|---|---|---|
| `gan-planner` | PM / Spec writer | 把一句需求展開成規格、sprint、驗收 rubric |
| `gan-generator` | Builder | 按 spec 實作，讀 evaluator 回饋逐輪修正 |
| `gan-evaluator` | QA / Critic | 透過 Playwright 與 rubric 對實際成果打分 |

> `gan-planner` / `gan-generator` / `gan-evaluator` 這些名稱是 **agent pack 裡的命名**，不是 Claude Code 官方內建代理名稱。

## 工作流程

```text
一句話需求
  ↓
gan-planner → spec.md + eval-rubric.md
  ↓
gan-generator → 實作 + 啟動 app
  ↓
gan-evaluator → Playwright 測試 + feedback.md + score
  ↓
未過門檻 → 回 generator 修正
通過門檻 → 結束
```

這個設計最有價值的地方，不是 agent 名稱很酷，而是它把「自我感覺良好」拆成兩個獨立人格：**做的人**與**挑毛病的人**。

## 評分標準

常見四維度加權：

- **Design Quality**（0.3）
- **Craft**（0.3）
- **Originality**（0.2）
- **Functionality**（0.2）

門檻常設在 **7.0 / 10**：不是「勉強能動」就算過，而是至少要有可交付水準。

## 什麼時候特別適合

- **UI / landing page / dashboard** 這類主觀品質占比高的任務
- 你想避免 agent 一次生成後就草草收工
- 你需要把「不好看」或「不夠細」轉成更可執行的評語

## 使用方式

最穩定的方式是：

1. 先安裝提供這組 skill / agents 的 package
2. 直接在 Claude Code 裡用自然語言要求「用 GAN harness 做一個…」
3. 讓 skill 自己去調用對應 agents

如果你要手動拆跑，也要依 **你安裝的 agent pack** 實際名稱來呼叫，不要把 `gan-planner` 這些名稱當成官方固定介面。

## 常見陷阱

**只有 generator，沒有 evaluator**
- 結果：第一版就被誤當成完成版

**評分太抽象**
- 結果：evaluator 只會說「再更好看一點」
- 解法：先定 rubric、配權重、定門檻

**拿來做超客觀的後端任務**
- 結果：收益不如 TDD / tests
- 解法：UI / UX 類任務用 GAN；純邏輯類任務多半用測試更直接

## 相關

- [[Agent-Harness]] — 三角結構的上位概念
- [[Superpowers框架]] — 另一種把 evaluator 內建到流程裡的做法（TDD gate）

## 來源

- [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)