---
title: Change to usage based billing
created: 2026-04-28
updated: 2026-04-28
source: https://www.reddit.com/r/GithubCopilot/comments/1sx896q/change_to_useage_based_billing/
published: 2026-04-27
tags:
  - reddit
  - github-copilot
  - ai-tools
---

> **繁中摘要**：GitHub 官方 email 通知 6/1 起 Copilot Pro / Pro+ 將從 PRU（Premium Request Units）改為 GitHub AI Credits 的 token-based usage billing；上週已先做暫時性 usage 限縮，待新計費上線後會放寬。

---

## 原文重點

來源：原 po 收到的官方 email（Copilot Pro / Pro+ 訂閱者）。

**6/1 生效的關鍵變更：**

- **PRU → GitHub AI Credits**：原本的 Premium Request Units 換成「每月 AI Credits 額度」
- 計費依據從 request 計數改為 **token consumption**（input + output + cached tokens），按各 model 的 listed API rate 換算
- Copilot code review 的 agentic 架構也納入 credits 消耗
- **annual 訂閱者**：在現行 plan 到期前維持原價，但 model multipliers 在 6/1 會調整（見 [New multipliers](Copilot-new-multipliers-June-1.md)）

**過渡期：**

- 上週起對個人 Copilot plan 做了 [暫時性 usage 限縮](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/)，目的是改善 6/1 切換前的 reliability / performance
- 新計費上線後 usage limit 會放寬

## 社群討論亮點

- **「Copilot Pro $10/月 = $10 AI Credits」**：等於每月買一張會過期的禮物卡，沒有比直接買 API token 更划算
- **改走 API rate 後的選項邏輯**：既然按 API 費率計價，留言質疑「為何不直接用 Codex 或 Claude Code」——GHCP 失去「premium request 額度比 raw API 便宜」的價值錨
- **prosumer-only 趨勢**：多名留言者觀察到 AI 工具正在離開「個人 / 業餘使用者」價位帶，未來 6–24 個月會更明顯，建議在 plan 到期前評估遷移路徑（self-host + Roo Code / Continue、或直接 API + Cline / Cursor）
- **官方 multiplier 表參考**：[Models and pricing 文件](https://docs.github.com/copilot/reference/copilot-billing/models-and-pricing#model-multipliers-for-annual-copilot-pro-and-copilot-pro-subscribers)
