---
title: Claude Code Review 工作流
created: 2026-04-26
updated: 2026-04-26
tags:
  - claude-code
  - code-review
---

## 核心 Review 指令

| 指令 | 說明 | 耗時 |
|------|------|------|
| `/review` | 通用 PR 審查，每次都跑 | ~3–4 分鐘 |
| `/simplify` | 3 agent 平行找重用/品質/效率問題並自動修 | 快 |
| `/security-review` | 安全漏洞掃描（SQL 注入、權限、認證等） | 中 |
| `/ultrareview` | 多 agent 雲端深度審查（v2.1.111，2026/04/16 推出） | ~10–20 分鐘 |

## 建議分層策略

**一般 PR**：
本地測試 → `/review` → `/security-review`

**大型 / 關鍵 PR（>500 行）**：
本地測試 → `/simplify` → `/review` → `/security-review` → `/ultrareview`

**基礎設施變更**（DB migration、auth 等）：
以上全跑 + 人工最終確認

## 補充說明

- `/simplify` 是 3 個 review agent 平行執行，找重用與效率問題後直接自動修正
- `/security-review` 針對當前 branch 的待提交變更，涵蓋 OWASP Top 10、注入向量、認證/授權、權限提升等
- 所有自動 review 應搭配人工確認每個 finding 是否真正需要修

### /ultrareview

`/ultrareview` 於 Claude Code v2.1.111（2026/04/16）正式推出。會將 branch 交給雲端的 specialist agent 群（安全、架構、正確性、風格、測試各有專責），合併成一份完整報告。

使用方式：
- 無參數：審查本地當前 branch
- `/ultrareview <PR#>`：審查指定 GitHub PR

適合大型或關鍵 PR 合併前最後一道關。
