---
title: Claude Code + Codex = AI GOD
tags:
  - youtube
  - claude-code
  - codex
  - openai
  - ai
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/L7NPhaUBpZE
---

介紹如何在 Claude Code 中使用 OpenAI Codex plugin，重點在 adversarial review（對抗性程式碼審查）功能，以及 Opus 與 Codex 互補的使用策略。

## Codex Plugin 功能

- **Code Review**：對已完成的程式碼進行唯讀中立審查
- **Adversarial Review**：假設程式有問題，積極找出缺陷（最推薦的功能）
- **Codex Rescue**：在 Claude Code 用量達限時，改由 Codex 執行任務
- **Status**：查看目前任務進度

## 安裝方式

```bash
# 加入 marketplace
# 安裝 plugin
codex:setup
```

使用量綁定 ChatGPT 帳號（免費帳號也可用），成本遠低於 Anthropic。

## Adversarial Review 實測

對一個 Twitter 互動/研究 bot（Supabase + Telegram + AI 回覆系統）進行測試。

七大攻擊面：authentication、data loss、rollbacks、race conditions、degraded dependencies、version skew、observability gaps

**Codex 發現 4 個 HIGH 級問題：**
1. Dedup logic 錯誤
2. Telegram polling 問題
3. Schema drift
4. Dashboard build 問題

**Opus 自我審查結果：**
- 共同發現：Telegram 問題（Opus 評為 critical，Codex 評為 high）
- Opus 額外發現 7 個 high/critical 問題
- Codex 額外發現 3 個 Opus 未找到的問題

## 結論

- Codex ≠ 取代 Opus，而是**第二雙眼睛**
- 同一個 AI 系統規劃 + 執行 + 評估，存在根本性缺陷
- 若已付 ChatGPT $20/月，引入 Codex adversarial review 幾乎零額外成本
- 特別適合用量受限時：用 Opus 規劃，Codex 執行
