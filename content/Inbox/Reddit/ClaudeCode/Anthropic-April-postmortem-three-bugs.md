---
title: Anthropic just published a postmortem explaining exactly why Claude felt dumber for the past month
created: 2026-04-27
updated: 2026-04-27
source: https://www.reddit.com/r/ClaudeCode/comments/1str8gi/anthropic_just_published_a_postmortem_explaining/
published: 2026-04-23
tags:
  - reddit
  - claude-code
  - ai-tools
---

> **繁中摘要**：Anthropic 於 4/23 公開 postmortem，3 月初到 4 月中 Claude Code「變笨」其實是三個獨立 bug 疊加：reasoning effort 默默降級、reasoning history 被 cache bug 清空、system prompt 限制 25 字。三者皆已於 v2.1.116（4/20）修復。

---

## 原文重點

三個獨立 bug，影響不同流量切片、時程不同步，所以症狀看起來是隨機品質下滑，內部難以定位。

**Bug 1：reasoning effort 默默從 high 降到 medium（3/4 起）**

- 為了降延遲，把 Claude Code 預設的 reasoning effort 從 `high` 改 `medium`
- 使用者立刻有感
- 4/7 還原

**Bug 2：cache bug 導致 Claude 忘記自己的 reasoning（3/26 起）**

- 試圖優化 idle session 的記憶體
- bug 造成每個 turn 都清空 reasoning history（不是只清一次）
- Claude 一邊執行任務，一邊忘記自己為什麼那樣決策
- 副作用：每個 request 都變成 cache miss → usage limit 消耗異常快

**Bug 3：system prompt 把回覆限制在 25 字（4/16 起）**

- 加入字面：`keep text between tool calls to 25 words. Keep final responses to 100 words.`
- 對 Opus 4.6 與 4.7 的程式碼品質都造成可量測的下降
- 4/20 還原

**狀態**：三個 bug 都已於 4/20 v2.1.116 修復；訂閱戶 usage limit 在 postmortem 公布當天重置。

## 社群討論亮點

- 官方 postmortem 全文：<https://www.anthropic.com/engineering/april-23-postmortem>
- 留言指出社群數週的「Claude 變笨」回報並非錯覺，三個 bug 對應的時間點與症狀都吻合
- 有人質疑 usage limit 在週五前重置（週末多數人不上機），實際補償有限
