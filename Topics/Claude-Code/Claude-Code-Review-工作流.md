---
title: Claude Code Review 工作流
created: 2026-04-26
updated: 2026-05-29
tags:
  - claude-code
  - code-review
---

PR 規模分層跑不同 review 工具，避免「每次都 ultra」浪費 token、也避免「只跑 review」漏掉安全或大型重構。

## 分層策略

| 規模 | 流程 |
|---|---|
| 一般 PR | 本地測試 → `/code-review`（找 bug）→ `/security-review` |
| 大型 / 關鍵 PR（>500 行）| 加 `/simplify`（清理）+ `/code-review ultra`（雲端深審，合併前） |
| 基礎設施變更（DB migration、auth、permission） | 全跑 + 人工最終確認 |

## 各指令的角色

- **`/code-review`**（每個 PR 主力）：本地審當前 diff，找 correctness bug + 重用 / 簡化 / 效率 cleanup。`--fix` 把修正套進 working tree、`--comment` 貼成 PR inline comment。effort 越高涵蓋越廣（也可能含不確定 finding）
- **`/review`**：通用 PR 審查，session 內較深的一遍（read-only）
- **`/simplify`**（近期改為**純清理**）：4 個平行 agent 找重用 / 簡化 / 效率 / 抽象層級問題後自動修，**不再找 bug**——找 bug 改用 `/code-review`。此指令早期即現在的 `/code-review`，後被改名分家
- **`/security-review`**：聚焦當前 branch 待提交變更的安全漏洞（OWASP Top 10、注入、認證 / 授權、權限提升）
- **`/code-review ultra`**（舊名 `/ultrareview`，現為 alias）：把 branch 交給雲端 specialist agent 群（安全 / 架構 / 正確性 / 風格 / 測試）平行審、各自 reproduce finding 再合併。耗時最久（平均約 20 分、$15–25），留給大型 / 關鍵 PR 合併前最後關卡——無參數審本地 diff、加 PR ref 審指定 PR

## 立場：自動 review 不能取代人工 finding 確認

每個 finding 都該人工判斷「真該修嗎」。LLM review 常見偏差：

- 把 stylistic preference 當 critical issue
- 對 generated code / vendor code 給意見
- 重複指出同一問題多種包裝

全自動修是 `/simplify`（純清理）與 `/code-review --fix` 的能力（範圍受限），其他模式產出的 finding 應視為「待審核 hint」而非「TODO list」。

## 跨模型 review 補同模型盲點

Claude review 自己生成的 code 時，思路往往跟生成時類似——同樣的判斷、同樣的盲點，跑兩次 `/review` 看不出多少新東西。關鍵 PR 引入 [[bookmark-codex-plugin-cc-Codex整合外掛|codex-plugin-cc]] 讓 Codex 從不同訓練分佈、不同推理路徑切入，比同模型重跑更可能抓到漏掉的盲點。
