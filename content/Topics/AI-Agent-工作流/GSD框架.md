---
title: GSD 框架（Get Shit Done）
created: 2026-04-20
updated: 2026-04-25
tags:
  - claude-code
  - agent-framework
  - context-management
---

GSD（Get Shit Done）是一條以 **fresh session / state machine / 狀態持久化** 為核心的 agent orchestration 流派。它目前其實分成兩條線：

- **v1：`gsd-build/get-shit-done`** — 注入 Claude Code / 多 runtime 的 workflow pack，資料多落在 `.planning/`
- **v2：`gsd-build/gsd-2`** — 基於 Pi SDK 的 standalone CLI，資料落在 `.gsd/`

本文以 **GSD-2** 為主，並明確標示 v1 差異，避免把兩代命令混寫。

## 核心概念

GSD 的中心思想是：**不要讓單一對話一路拖到爛掉**。與其讓 agent 在同一條超長對話裡硬撐，不如把工作切成可完成的單位，由狀態機驅動新 session 接力。

GSD-2 常見做法：

- 每個 task / slice 在 **fresh context** 執行
- 關鍵狀態寫回 `.gsd/`
- 由 state machine 決定下一步，而不是讓 agent 自己無限 loop
- 任務層級通常是 **Milestone → Slice → Task**
- 任務結束後提煉 learnings / decisions，供後續 session 讀取

## GSD-2 的實際工作流

### 啟動

```bash
npm install -g gsd-pi@latest
gsd
```

第一次啟動會進設定精靈，之後主要有兩種節奏：

- **Step mode**：一步一步走，適合想保留掌控感
- **Auto mode**：`/gsd auto`，適合已經認可 plan、讓它自己往前跑

### 典型迴圈

1. 探索現有 codebase / 問題定義
2. 形成 milestone / roadmap
3. 把 milestone 拆成 slice / task
4. 在 fresh session 執行單個 task
5. 驗證、記錄學習、更新 state
6. 回頭看 roadmap，決定下一個 slice

這種模式最強的地方不是「比較聰明」，而是**比較不會把髒 context 一路累積下去**。

## v1 與 v2 別混

### v1：`get-shit-done`

- 比較像注入 Claude Code 的 workflow / prompt framework
- 常見資料夾：`.planning/`
- 常見命令：`/gsd-new-project`、`/gsd-plan-phase` 這一代的 slash commands

### v2：`gsd-2`

- 是獨立 CLI，不只是 Claude Code 的一層 prompt
- 常見資料夾：`.gsd/`
- 主要入口是 `gsd` 與 `/gsd` 狀態機工作流

如果你看到某篇筆記同時把 `.planning/`、`/new-project`、`.gsd/`、`/gsd auto` 全寫在同一個流程裡，八成就是把兩代混在一起了。

## 認證與費用：別把 OAuth 當穩定合法路徑

GSD-2 README 與 Anthropic 官方 legal / compliance 文件的方向一致：

- **第三方工具 / 服務** 不應把 Claude Free / Pro / Max 的 OAuth 認證當成穩定合法路徑
- 比較穩妥的做法是 **API key**

所以如果你把 GSD-2 當成第三方 orchestration CLI 來用，實務上應該預設走 API key，不要把 Max plan 當成萬用燃料桶。

## 它在三框架裡的位置

| 面向 | GSD | Superpowers | GStack |
|---|---|---|---|
| 約束重點 | 環境 / context | 流程 / TDD | 視角 / planning / QA |
| 最強階段 | 長任務 orchestration、roadmap、slice 管理 | 實作與測試 gates | 規劃、設計、QA、發佈 |
| 核心問題 | context rot、長任務續跑 | 開發品質、測試紀律 | 決策收斂、多人視角審查 |

## 何時適合用

- 長任務、多里程碑、要保留進度狀態
- 你不信任單一長對話能穩穩跑完
- 你願意用更多 orchestration 換更乾淨的執行邊界

## 何時不適合

- 很小、很快就能做完的 side project
- 成本極度敏感、無法接受 orchestration 開銷
- 需求已很清楚，只差乾淨落地實作 —— 這時 [[Superpowers框架]] 或原生 Claude Code 可能更直覺

## 常見陷阱

**把 v1 / v2 命令混寫**
- 解法：先確認你現在講的是 `get-shit-done` 還是 `gsd-2`

**規劃本身就燒太多 token**
- 解法：小專案不要把 GSD 當預設；先估算值不值得開 orchestration

**Auto mode 放著跑太久**
- 解法：設預算、設檢查點、必要時人工接管

## 來源

- [gsd-build/gsd-2](https://github.com/gsd-build/gsd-2)
- [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)
- [Claude Code legal and compliance](https://code.claude.com/docs/en/legal-and-compliance)