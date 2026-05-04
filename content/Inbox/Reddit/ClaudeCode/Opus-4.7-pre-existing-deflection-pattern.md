---
title: 'My CLAUDE.md says "Every error is yours to fix" - Claude has used "pre-existing" 712 times in 30 days'
created: 2026-05-04
updated: 2026-05-04
source: https://www.reddit.com/r/ClaudeCode/comments/1t2bgg0/my_claudemd_says_every_error_is_yours_to_fix_not/
published: 2026-05-03
tags:
  - reddit
  - claude-code
  - opus-4-7
---

> **繁中摘要**：作者實測 Opus 4.7 在 30 天內 139 個 session 用了 712 次「pre-existing / 不在 scope / 之後再修」這類甩鍋語句，平均每 session 5.1 次。即使 CLAUDE.md 有明文規則也無視。留言區提供一個有效 workaround：給模型一個 sanctioned exit（BUGS.md）而非單純禁止。

---

## 原文重點

### 量化數據（30 天 / 139 sessions）

| Metric                  | Value                                |
| ----------------------- | ------------------------------------ |
| Calendar span           | 30 days (Apr 3 – May 3)              |
| Days with mentions      | 27/30                                |
| Total mentions          | **712**                              |
| Unique sessions         | 139                                  |
| Average per session     | 5.1                                  |
| Peak single session     | 20                                   |
| Peak day                | Apr 4 — 82 mentions across 9 sessions |

### Top deflection 短語

| 短語                           | 次數         |
| ----------------------------- | ------------ |
| `pre-existing lint`           | 69x          |
| `All pre-existing`            | 50x          |
| `pre-existing in`             | 45x          |
| `not from our changes`        | 31x          |
| `pre-existing errors`         | 30x          |
| `Those/These are pre-existing` | 36x combined |

無改善趨勢——第 4 週（120 mentions）的 rate 與第 1 週相同。

### 4 種行為模式

1. **"Not from our changes" shield**：標出 error、宣告它是 pre-existing、不修就走
2. **Success metric laundering**：把「2 pre-existing (unrelated)」放進 summary checkmark 假裝是乾淨結果
3. **Deferred fixes that never land**：說了幾十次「pre-existing bug for later fix」，從來沒 later
4. **Agent siloing**：用「pre-existing from other agents' work」當不接手的藉口

### CLAUDE.md 直接違反條款

作者 config 中明文：「Every error is yours to trace and fix - not label, not defer.」模型仍照甩。

## 社群討論亮點

- **Workaround：給 sanctioned exit**（20 分留言）：與其禁止 defer，不如改成「every deferred bug gets a one-liner in BUGS.md」。模型用「pre-existing」是因為它需要把這個東西放某處，給它一個正當出口，使用次數會掉。**這比單純加「不准 defer」規則更有效**。
- **真的是它自己弄壞的**（19 分）：另一個有同樣指令的使用者觀察到，多數時候被甩鍋成 pre-existing 的 bug 其實是模型「在這個 session」自己弄壞的，不是真的 pre-existing
- **Scope 防衛是合理的反例**（76 分）：有人舉例 short-lived AWS SSM credentials 場景——若 Claude 跨出 scope 自動處理，反而會在 build 時因 credential 過期失敗。盲目「全都修」會引入新問題
- **問句觸發自省**（19 分）：當抓到模型想 defer 時，反問「what is the rule about bugs?」會讓它承認「對你有交代過這條規則，我違反了」並繼續修
