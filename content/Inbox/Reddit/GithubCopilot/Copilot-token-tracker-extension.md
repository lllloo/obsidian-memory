---
title: "Instead of guessing about Copilot limits, let's collect some actual data"
created: 2026-04-27
updated: 2026-04-27
source: https://www.reddit.com/r/GithubCopilot/comments/1stbocm/instead_of_guessing_about_copilot_limits_lets/
published: 2026-04-23
tags:
  - reddit
  - github-copilot
  - ai-tools
---

> **繁中摘要**：VS Code marketplace 上的 `RobBos.copilot-token-tracker` 可從本機 VS Code Copilot logs 解析過去 30 天的 token 使用量，附 model breakdown、sessions、thinking tokens、預估成本，是討論 rate limit 時可拿來對齊資料的客觀依據。

---

## 原文重點

- Extension：[copilot-token-tracker](https://marketplace.visualstudio.com/items?itemName=RobBos.copilot-token-tracker)（作者 RobBos）
- 資料源：本機 VS Code Copilot logs（不需額外 API key）
- 提供視圖：
  - 過去 30 天 token usage
  - Model breakdown（可看出單一模型的吃量比例）
  - Sessions
  - Thinking tokens
  - 預估成本
- 用法建議：被 rate limit 的人裝起來貼截圖，與沒被限流的人對比，有機會反推真正觸發 weekly cap 的 usage pattern

## 社群討論亮點

- 實測案例：作者重度使用 Opus 4.6 一週多後被 cut off；改用 GPT 5.4 同樣強度時 token 消耗只是「一小部分」，明顯佐證 Opus 系列吃量級距大於 GPT 5.4
- 另一案例：Copilot Pro 用戶當天同時觸發 session rate limit 與 weekly rate limit，並在單一 CLI session 看到 1.4M tokens，明顯異常於日常使用，工具讓「異常 session」更容易抓出
- 開放問題：tracker 中的 `Sessions` 是否等同於 Copilot 計費的 `Requests` 尚無定論
- 工作流調整：有用戶看完數據後改採 Copilot + Codex 各分一半負載，Opus 留給需要深度 discovery 的任務
