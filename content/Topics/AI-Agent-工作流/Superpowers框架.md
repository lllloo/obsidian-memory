---
title: Superpowers 框架
created: 2026-04-20
updated: 2026-04-25
tags:
  - claude-code
  - agent-framework
  - tdd
---

Superpowers 是以 **TDD gate + systematic debugging + review loop** 為核心的開發框架 / plugin。它不是單純幫你「想計畫」，而是強調：**沒有通過當前品質門檻，就不要進下一步。**

## 核心概念

它最鮮明的特徵是把 TDD 變成 workflow 中的硬閘門：

- 先寫測試，再寫實作
- 測試不對，不准往下
- review 完再 fix，再 merge

相較於 GStack 偏規劃與多 persona、GSD 偏 orchestration，Superpowers 更像是把**落地實作與品質控制**變成主軸。

## 典型流程

1. **Brainstorm**：先問清楚需求與邊界
2. **Spec**：生成文件，把 acceptance criteria 寫明
3. **Implementation plan**：拆成可執行任務
4. **Execution**：依 TDD gate 推進
5. **Code review**：檢查 spec compliance 與 code quality
6. **PR / merge**：收尾、提交、合併

這條線的優點是：agent 不容易邊做邊漂；缺點是：**對小任務可能很重**。

## 安裝與形態

在 Claude Code 生態裡，常見安裝方式是官方 marketplace 的 plugin：

```text
/plugin install superpowers@claude-plugins-official
```

此外，Superpowers 也不只活在 Claude Code；它是可跨多個 agent host 的 methodology / plugin 生態，而不是只能綁單一客戶端。

## 它在三框架裡的位置

| 面向 | Superpowers | GSD | GStack |
|---|---|---|---|
| 核心約束 | 流程 / TDD / debug | context / state machine | 視角 / planning / QA |
| 最強階段 | 實作與修正 | 長任務 orchestrate | 前期收斂與後段 QA / ship |
| 最適合 | 需要可靠測試與品質門檻 | 長任務、多里程碑 | 需要多 persona 收斂方案 |

## 何時適合用

- 錯誤成本高的系統
- 你真的想把 TDD 當流程約束，而不是口號
- 任務夠複雜，值得多一層 spec / review / debug gate

## 何時不適合

- 很小的 UI tweak
- 純探索型原型
- 需求還沒定，你其實更需要的是先收斂方案

## 常見陷阱

**小任務也硬走完整流程**
- 結果：等待時間 > 實作時間

**spec / tests 太重，context 反而爆**
- 結果：框架本來要救品質，最後先拖慢迭代

**把 framework 當萬靈丹**
- 結果：本來原生 Claude Code 20 分鐘能解的事，硬拖成 1 小時

## 相關

- [[GStack框架]] — 如果你需要的是規劃與多 persona challenge
- [[GSD框架]] — 如果你需要的是長任務 orchestration
- [[Agent-Harness]] — 上位概念：為什麼 evaluator / TDD gate 有價值

## 來源

- [obra/superpowers](https://github.com/obra/superpowers)
- [Superpowers plugin page](https://claude.com/plugins/superpowers)