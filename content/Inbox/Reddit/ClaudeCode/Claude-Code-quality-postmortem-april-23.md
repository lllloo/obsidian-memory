---
title: An update on recent Claude Code quality reports
created: 2026-04-28
updated: 2026-04-28
source: https://www.reddit.com/r/ClaudeCode/comments/1stq3gk/an_update_on_recent_claude_code_quality_reports/
published: 2026-04-23
tags:
  - reddit
  - claude-code
  - bug
  - ai-tools
---

> **繁中摘要**：Anthropic 官方 postmortem 公開三個導致 Claude Code 體感變差的 bug（reasoning effort 默認從 high 降到 medium、thinking cache 每回合誤清、verbosity 限制 prompt），均已修復；4/23 全用戶 usage limit 重置，API 層全程未受影響。

---

## 原文重點

連結貼文，原文在 Anthropic 官方 engineering blog：<https://www.anthropic.com/engineering/april-23-postmortem>

確認三個獨立 bug，全部命中 Claude Code 客戶端（API 層未受影響）：

### Bug 1：reasoning effort 默認被改低

- 期間：2026-03-04 ～ 04-07
- 影響：Sonnet 4.6、Opus 4.6
- 為了解決 UI 卡頓抱怨，把預設 reasoning effort 從 `high` 降到 `medium`
- 結果：延遲下降但使用者普遍感覺「變笨」
- 修復：04-07 revert，現預設為 Opus 4.7 用 `xhigh`、其餘 `high`

### Bug 2：thinking cache 誤清

- 期間：2026-03-26 ～ 04-10（v2.1.101 修復）
- 影響：Sonnet 4.6、Opus 4.6
- `clear_thinking_20251015` API header 帶 `keep:1` 的實作有 bug：每個 turn 都清 reasoning，而不是只在 idle session 清一次
- 症狀：Claude 顯得健忘、重複；usage limit 因為持續 cache miss 被燒得很快
- 為什麼難抓：屬於 stale session corner case；同期不相關的 server 實驗遮蔽了訊號
- 發現方式：用 Opus 4.7 做 code review 抓到 Opus 4.6 自己沒看出的問題

### Bug 3：verbosity 限制 prompt

- 期間：2026-04-16 ～ 04-20
- 影響：Sonnet 4.6、Opus 4.7
- 加了一條 system 指示：

  ```
  Keep text between tool calls to ≤25 words.
  Keep final responses ≤100 words unless task requires more.
  ```

- 效果：在更廣的 eval 上掉 3% 分數
- 修復：04-20 在 v2.1.116 revert

### 補償

- 04-23 起所有訂閱者 usage limit 全部重置
- API 層全程未受影響——只直接打 API 的使用者不受這三個 bug 影響

## 社群討論亮點

- 有用戶反映近期 tool use 仍偶有錯誤或「偷懶不用 tool」的情況，且在 Claude Chat / Cowork 比 CC 更明顯——postmortem 涵蓋的三個 bug 修完之後，仍可能有其他殘留 issue 待觀察。
- 有人問「這代表 4.7 現在可用了嗎」——postmortem 預設答案是 yes，因為 Bug 1 的新預設就是 Opus 4.7 配 `xhigh`，且 Bug 2 的 review 是用 4.7 抓出來的。
