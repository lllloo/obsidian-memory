---
title: GStack 框架
created: 2026-04-20
updated: 2026-04-25
tags:
  - claude-code
  - agent-framework
  - planning
---

GStack 是 Garry Tan 開源的 workflow pack：把 planning、design、QA、deployment 這些常見階段整理成一套可安裝到 agent host 的技能 / 指令組。它不是單一「神 agent」，而是一個偏 **虛擬軟體團隊 operating system** 的工具箱。

## 核心概念

GStack 的重點不是只有 `CLAUDE.md`，而是整組 workflow：

- planning pipeline
- design pipeline
- QA / ship pipeline
- browser / runtime 輔助工具

它支援 Claude Code，也支援多個其他 agent host；README 目前列出的整合對象已不只「其他七個」。

另外，**telemetry 不是完全沒有**：官方 README 目前是 **opt-in telemetry，預設關閉**。這點很容易被說反。

## 最有代表性的兩段流程

### 1. Planning pipeline

常見組合：

- `office-hours`
- `plan-ceo-review`
- `plan-eng-review`
- `plan-design-review`
- `plan-devex-review`

核心思路是：

1. 先把問題定義清楚
2. 主動 challenge 前提
3. 從 CEO / Engineering / Design / DevEx 等不同 persona 看同一方案
4. 最後再收斂成可執行 spec

這讓 GStack 特別適合 **brownfield 專案加功能**、**有商業取捨的產品決策**，而不只是「寫 code」。

### 2. Design pipeline

常見組合：

- `design-consultation`
- `design-shotgun`
- `design-html`
- `design-review`

其中 `design-shotgun` 的代表性很高：先生成多個方向，再讓人類從中挑、給 feedback、再迭代，而不是一開始就逼 agent 猜唯一正解。

## 它和 GSD / Superpowers 的差異

| 面向 | GStack | Superpowers | GSD |
|---|---|---|---|
| 最強點 | 規劃、設計、QA、發佈 | 實作、TDD gate、debugging | orchestration、fresh context、roadmap 管理 |
| 約束重心 | 多 persona / 多視角審查 | 流程與品質門檻 | context 與狀態機 |
| 最適合的問題 | 功能收斂、產品決策、UI / QA | 嚴謹實作與修 bug | 長任務拆解與續跑 |

## 安裝與形態

GStack 不是 SaaS；通常是把 repo / workflow assets 安裝到本地 agent 環境，再依 README 做 setup。也就是說：

- 你可以 fork / 客製
- 沒有強制 vendor lock-in
- 但它不是「只有幾個 markdown 檔」那麼簡單，還會帶入瀏覽器與輔助 runtime 能力

## 何時適合用

- 需求發散、需要先做產品收斂
- 你想在動工前就讓多個 persona 先挑方案毛病
- UI / UX / QA / ship 也想納入同一套工作流

## 常見陷阱

**只用了 planning，不做 handoff**
- 結果：spec 寫完後無法順利交棒給實作框架

**把 persona 當成口號，不是真的隔離視角**
- 結果：每個 reviewer 都講一樣的話

**忽略實作成本**
- 結果：規劃很完整，但落地還要接 [[Superpowers框架]]、原生 Claude Code 或其他 execution flow

## 相關

- [[Superpowers框架]] — 若要接 TDD / implementation gates
- [[GSD框架]] — 若要接 long-running orchestration

## 來源

- [garrytan/gstack](https://github.com/garrytan/gstack)
- [gstacks.org](https://gstacks.org/)