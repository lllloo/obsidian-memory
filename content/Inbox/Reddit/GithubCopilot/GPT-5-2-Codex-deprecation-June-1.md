---
title: Upcoming deprecation of GPT-5.2 and GPT-5.2-Codex - GitHub Changelog
created: 2026-05-05
updated: 2026-05-05
source: https://www.reddit.com/r/GithubCopilot/comments/1t2vt2d/upcoming_deprecation_of_gpt52_and_gpt52codex/
published: 2026-05-03
tags:
  - reddit
  - github-copilot
  - ai-tools
---

> **繁中摘要**：GitHub 官方公告 6 月 1 日 deprecate GPT-5.2 與 GPT-5.2-Codex，建議遷移到 GPT-5.5 / GPT-5.3-Codex；Copilot Code Review 中 5.2-Codex 仍保留。對 Student / 年費 plan 影響最大（5.2 是部分方案剩下的可用 GPT 模型）。

---

## 原文重點

**Deprecation 時程**：2026-06-01

**影響範圍**：所有 GitHub Copilot 體驗——Copilot Chat、inline edits、ask mode、agent mode、code completions。

**例外**：Copilot Code Review 中 GPT-5.2-Codex 繼續保留。

**建議遷移路徑**：

- GPT-5.2 → GPT-5.5
- GPT-5.2-Codex → GPT-5.3-Codex

**Plan 差異**：官方公告未在 Pro / Pro+ / Student / Business 之間做差別說明；Enterprise admin 可能需在 Copilot model policy 啟用替代模型。

**遷移動作**：使用者需在 6/1 前確認 VS Code 與 github.com model selector 中已可使用替代模型，並更新工作流／自動化整合。6/1 後不需手動移除 deprecated 模型。

## 社群討論亮點

- Student plan 反應 5.2 是學生方案剩下的少數可用 GPT 模型之一——deprecation 後該層級可用 GPT 模型可能更受限（待官方再確認）
- 引用 [factory.ai code review benchmark](https://factory.ai/news/code-review-benchmark) 指 GPT-5.2 在 code review 任務上表現勝過 5.5 / Opus；對 code review 重度使用者建議在 6/1 前確認 5.2-Codex 在 Copilot Code Review 路徑仍可用
- 從 5.2 直接跳 5.5 而非 5.3 / 5.4，社群質疑是「以 5.5 cost 取代 5.2 cost」（multiplier 可能上升）；遷移後注意 weekly premium 用量
- 年費方案 5.2 提供 500 requests/月——deprecation 後該配額是否在 5.5 上維持，目前公告未明說
