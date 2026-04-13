---
title: 三大框架讓 Claude Code 無可匹敵：Superpowers、GSD、GStack
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-02
source: https://www.youtube.com/watch?v=bzutStZJ1Ig
---

## 三個框架解決的問題各不同

Claude Code 的精準度問題有三個來源：**流程混亂**、**context 衰減**、**視角單一**。三個框架分別針對這三點：

| 框架 | 約束目標 | 核心機制 |
|------|---------|---------|
| **Superpowers** | 流程（Process） | 強制 AI 遵循軟體開發方法論 |
| **GSD** | 環境（Environment） | context window 永遠低於 50% |
| **GStack** | 視角（Perspective） | 不同專家角色審視不同階段 |

## Superpowers：流程框架

強制 Claude 依序執行：

1. **澄清意圖** — 問清楚要做什麼
2. **確認 Spec** — 這是你要的嗎？
3. **實作計畫** — 完整的執行步驟
4. **TDD（測試先行）** — 先寫測試，定義應用程式預期行為
5. **寫 App Logic** — 讓測試通過
6. **重構** — 循環直到沒有可重構的東西

使用同一個 Orchestrator 貫穿整個對話，配合不同 Sub Agents 分工執行各階段。

## GSD（40K GitHub Stars）：環境框架

**問題：Context Rot**
對話前 20% 精準，到 40%、60%、80% 準確度大幅下降。

**解法：每個階段換新 Orchestrator**

```
Phase 1 → Orchestrator 1 + Sub Agents → 存狀態到本地 MD 檔
Phase 2 → Orchestrator 2（全新）+ Sub Agents → 讀取 MD 繼續
Phase 3 → Orchestrator 3（全新）...
```

- 每個 Orchestrator 自己的 context 也永遠低於 50%
- 狀態持久化到本地 MD 檔，跨 session 不丟失
- 與 Superpowers 最大差異：**Superpowers 用一個 Orchestrator 管到底，GSD 每個階段都換掉**

## GStack（Gary Tang / YC CEO）：視角框架

將單一 agent 拆成多個專家角色，每個角色只看自己職責範圍：

- **CEO lens** — 審視整體架構、專案可行性
- **Engineer Manager** — 執行規劃、技術方向
- **QA Lead** — 測試計畫、使用者流程、Bug 報告

不只是 role prompt，有五層機制確保角色不破壞設定：

1. **Role Focus** — 戴上眼罩，只看自己職責範圍的事（code style 是工程師的事，QA 不管）
2. **Data Flow** — 工作建立在前一階段輸出之上（QA 接收 Reviewer 的結果）
3. **Quality Control** — 各角色完成項目的 checklist
4. **Boil the Lake** — 只做能 100% 完成的事。能燒小湖（職責內），不要去燒大海（職責外）
5. **Keep it Simple** — 結論只說三件事：發現了什麼 / 為何重要 / 下一步是什麼

## 組合使用：Power Stack

三個框架互補，可按開發階段串接：

```
策略規劃 → GStack（CEO/Engineer Manager lens 驗證架構）
執行規劃 → GSD（拆分里程碑，每個里程碑 < 50% context）
實際執行 → Superpowers（TDD，先測試再寫程式）
QA 收尾  → GStack（QA Lead 用 Playwright 做 UI 測試）
```

- GStack 擅長：策略規劃、QA
- GSD 擅長：專案管理、里程碑切分
- Superpowers 擅長：TDD 執行、sub agent 協調
