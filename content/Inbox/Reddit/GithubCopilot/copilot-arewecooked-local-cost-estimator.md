---
title: Copilot-arewecooked - Know your AI credit cost before June 1st
created: 2026-05-04
updated: 2026-05-04
source: https://www.reddit.com/r/GithubCopilot/comments/1sz1ynw/copilotarewecooked_know_your_ai_credit_cost/
published: 2026-04-29
tags:
  - reddit
  - github-copilot
  - ai-tools
  - workflow
---

> **繁中摘要**：開源工具 `copilot-arewecooked` 在本機讀取 GHCP 客戶端 session log，套用官方 per-token 公開定價，產出 HTML 報表預估 6/1 切換後的費用；對照 Pro / Pro+ / Business / Enterprise 各方案 limit，是目前少數能在官方 estimator 出來前自查的方法。

---

## 原文重點

- Repo：[`PanAchy/copilot-arewecooked`](https://github.com/PanAchy/copilot-arewecooked)
- 6/1 起 GHCP 切到 per-token AI credit billing；本工具用於切換前預估
- 工作方式：完全本地執行，讀取本機 session log → 套官方 per-token 定價 → 產 HTML report
- 比對對象：Pro / Pro+ / Business / Enterprise 方案 limit
- 涵蓋客戶端：VS Code、Copilot CLI、OpenCode、Pi
- **資料精度差異（重要 caveat）**：
  - **VS Code**：input / cache token 沒被持久化 → input/cache 是估的，**output 精確**
  - **Copilot CLI**（normal chat）：只暴露 output token → input 是估的；compaction event 有精確值
  - **OpenCode / Pi**：暴露完整 token breakdown → 結果精確

## 社群討論亮點

- **替代品**：留言提到 [Copilot-Usage 擴充](https://marketplace.visualstudio.com/items?itemName=emagin8.copilot-usage)（VS Code marketplace）也有類似估算
- **Windows bug**：實際試用者回報 Windows 下有 build 不能跑的 bug；建議把 repo 餵給 agent 修
- **session 漏抓問題**：parser 預設找不到所有 session；agent 修過 parser/data path 後能多撈到一些，但仍有遺漏 → 建議先檢查實際 session 數是否合理再相信數字
- **GitHub 官方 estimator 預計 5 月推出**，可作為交叉驗證
