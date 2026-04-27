---
title: GitHub Copilot is not the same product you signed up for, breakdown of everything they changed.
created: 2026-04-27
updated: 2026-04-27
source: https://www.reddit.com/r/GithubCopilot/comments/1srj6xi/github_copilot_is_not_the_same_product_you_signed/
published: 2026-04-21
tags:
  - reddit
  - github-copilot
  - ai-tools
---

> **繁中摘要**：GitHub Copilot 在無預警下對 Pro / Pro+ 方案做出多項變更：暫停新註冊、限縮週 token 上限、移除 Opus 4.6，僅留下 7.5x multiplier 的 Opus 4.7（原 4.6 為 3x），等於同價位用更快被打到牆。

---

## 原文重點

作者為 Pro+（$40/月）使用者，未收到任何 in-app 通知，需自行從 blog post 拼湊變更：

- **新註冊暫停**：Pro / Pro+ / Student 方案目前停止新訂閱（[官方 plans 頁](https://docs.github.com/en/copilot/get-started/plans)）
- **週 token 上限收緊**：在原本的 premium request quota 之上再加上 weekly token cap，可能 request 還沒用完就被限流
- **Claude Opus 從 Pro 方案完全移除**
- **Opus 4.5、4.6 連 Pro+ 也移除**
- 唯一剩下的 Opus 模型是 **Opus 4.7**，multiplier 為 **7.5x**
  - 對照：Opus 4.6 的 multiplier 是 3x
  - 換算：同樣 quota 下消耗速度為原本的 2.5 倍（`7.5 / 3 = 2.5`）

額外問題：

- Auto mode 失效，錯誤訊息：`Auto mode failed: no available model found in known endpoints.`
- 已連續兩天無法正常使用

官方說明連結：[GitHub Blog — Changes to Copilot Individual Plans](https://github.blog/news-insights/company-news/changes-to-github-copilot-individual-plans/)

## 社群討論亮點

- 多數問題集中在 Claude 系列：Student 移除 Claude、Pro 移除 Claude、Claude 成本拉高、rate limit 為 model-specific（針對 Claude），可能根因是 Anthropic 端供給／成本變動，並非單純 Copilot 政策
- 替代方案實測：Claude API 直連用 Sonnet 做 refactor，單一 prompt 吃掉 2M tokens、$3 USD；Copilot Pro+ 仍是「200 個 Opus 4.7 request + 1500 個 Sonnet request」單價較划算
- 有用戶表示 GPT 5.4 對 Opus 4.6 工作流不是好替代（深度推理任務退步明顯）
