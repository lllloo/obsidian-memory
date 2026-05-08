---
title: Claude Code Review 工作流
created: 2026-04-26
updated: 2026-05-08
tags:
  - claude-code
  - code-review
---

PR 規模分層跑不同 review 工具，避免「每次都 ultra」浪費 token、也避免「只跑 review」漏掉安全或大型重構。

## 分層策略

| 規模 | 流程 |
|---|---|
| 一般 PR | 本地測試 → `/review` → `/security-review` |
| 大型 / 關鍵 PR（>500 行）| 加 `/simplify`（前）+ `/ultrareview`（後） |
| 基礎設施變更（DB migration、auth、permission） | 全跑 + 人工最終確認 |

## 各指令的角色

- **`/review`**：通用 PR 審查，每個 PR 都跑
- **`/simplify`**：多 review agent 平行找重用 / 品質 / 效率問題後**自動修**——所以放最前，省得後面 review 還在針對被它修掉的東西
- **`/security-review`**：聚焦當前 branch 待提交變更的安全漏洞（OWASP Top 10、注入、認證 / 授權、權限提升）
- **`/ultrareview`**：把 branch 交給雲端 specialist agent 群（安全 / 架構 / 正確性 / 風格 / 測試）合併報告。耗時最久，留給大型 / 關鍵 PR 合併前最後關卡——無參數審本地 branch、`/ultrareview <PR#>` 審指定 GitHub PR

## 立場：自動 review 不能取代人工 finding 確認

每個 finding 都該人工判斷「真該修嗎」。LLM review 常見偏差：

- 把 stylistic preference 當 critical issue
- 對 generated code / vendor code 給意見
- 重複指出同一問題多種包裝

讓 review agent 全自動修是 `/simplify` 的特權（且範圍受限），其他模式產出的 finding 應視為「待審核 hint」而非「TODO list」。

## 跨模型 review 補同模型盲點

Claude review 自己生成的 code 時，思路往往跟生成時類似——同樣的判斷、同樣的盲點，跑兩次 `/review` 看不出多少新東西。關鍵 PR 引入 [[codex-plugin-cc]] 讓 Codex 從不同訓練分佈、不同推理路徑切入，比同模型重跑更可能抓到漏掉的盲點。
