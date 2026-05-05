---
title: How to "Shrink" Your Claude 5-Hour Limit to 1–4 Hours (and Why That's Actually Useful)
created: 2026-05-05
updated: 2026-05-05
source: https://www.reddit.com/r/ClaudeCode/comments/1t3dnmp/how_to_shrink_your_claude_5hour_limit_to_14_hours/
published: 2026-05-04
tags:
  - reddit
  - claude-code
  - workflow
  - best-practices
---

> **繁中摘要**：Claude 的 5 小時用量視窗是 rolling，從「該週期第一則訊息」開始計時。利用 Claude Code Routines 用 cron 提早 ping 一個輕量訊息，把窗口起點對齊到實際工作時間，等於把可用視窗從 5 小時「縮成」剩餘 1–4 小時對齊到自己想要的時段。

---

## 原文重點

### 問題

- Claude 用量是 5 小時的 rolling window，從該週期**第一則訊息**開始計時
- 早上 8 點隨手測試一下 → 視窗已經開始；10 點才真正開工 → 只剩 3 小時可用

### 解法：用 Claude Code Routines 預先 ping

讓 routine 在「想要的工作起點之前」自動發一則輕量訊息，把 5 小時視窗的起點推到那個時間。

步驟：

1. 進 Claude Code 網頁
2. 開 **Routines** → **New Routine**
3. 命名（例：`warmup`）
4. 指令設成極簡的東西，例如 `wake up claude`
5. 選 **Custom Schedule**
6. 填 cron 表達式
7. Create

提示：用 **Claude Haiku 4.5** 跑這個 routine，最便宜、ping 一下夠用。

### 公式

```
Routine trigger time = Work start time − (5h − desired remaining hours)
```

### 範例

| Work starts | Want remaining | Trigger routine at | Cron expression       |
| ----------- | -------------- | ------------------ | --------------------- |
| 10:00       | ~3 hours       | 08:00              | `0 3,8,13,18,23 * * *` |
| 09:00       | ~2 hours       | 06:00              | `0 1,6,11,16,21 * * *` |

Routine 從 anchor 時間每 5 小時觸發一次，因此每個新週期都會以相同 offset 對齊到你的工作日。

### 重點注意

- 不會增加配額，只是平移視窗起點
- 工作時間穩定的人比較有用；每天時段差很多就無感
- 開工時剩 2–3 小時通常已經夠做一段實作

## 社群討論亮點

- 手機 Haiku 開新對話只送 `.` 然後立刻 stop，效果相同（推開視窗起點，且幾乎不耗 token）——比 routine 更輕量的手動版
- 不想配 cron 的替代版：手機鬧鐘設在工作前 2 小時，響的時候手動發一句訊息；同樣是平移視窗，零設定
- 補充討論串：[Reddit 上關於 5 小時視窗實際行為的更多資訊](https://www.reddit.com/r/ClaudeCode/s/fg2YOf15qo)
