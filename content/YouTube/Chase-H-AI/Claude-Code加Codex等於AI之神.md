---
title: Claude Code + Codex = AI 之神
tags:
  - youtube
  - claude-code
  - codex
  - openai
  - ai
created: 2026-04-12
updated: 2026-04-12
published: 2026-03-30
source: https://youtu.be/L7NPhaUBpZE
---

**影片描述**：介紹如何在 Claude Code 中安裝並使用 OpenAI Codex plugin，重點展示 adversarial review（對抗性程式碼審查）功能，以及 Opus 與 Codex 如何互補合作，讓輸出結果大於兩者各自之和。

**重點摘要：**
- Codex plugin 提供四個功能：中立 code review（唯讀）、adversarial review（主動找缺陷）、Codex Rescue（Claude 用量達限時改由 Codex 執行）、Status 查詢。
- Adversarial review 的核心原理：讓 Codex 假設程式碼已出問題，針對七大攻擊面（authentication、data loss、rollbacks、race conditions、degraded dependencies、version skew、observability gaps）主動挖掘漏洞。
- 使用量綁定 ChatGPT 帳號，免費帳號也可用，成本遠低於 Anthropic，如果已付 $20/月 ChatGPT，幾乎是零額外成本。
- 實測用 Twitter 研究 bot（Supabase + Telegram + AI 回覆系統）測試：Codex 找到 4 個 HIGH 級問題（dedup logic、Telegram polling、schema drift、dashboard build）。
- Opus 自我審查對比：Opus 多找到 7 個 Opus/Codex 共享問題外的問題；Codex 則多找到 3 個 Opus 漏掉的問題——兩者互補，各有盲點。
- 關鍵洞察：讓同一個 AI 系統負責規劃、執行、評估三件事，存在根本性缺陷；引入 Codex 作為第二雙眼睛可有效規避。
- 安裝極簡單：兩行指令加入 marketplace 並安裝，再執行 `codex:setup` 完成 ChatGPT 帳號綁定即可使用。
- 適合情境：Anthropic 用量受限時，用 Opus 規劃、Codex 執行（Codex Rescue）；任何專案想要外部獨立審查時用 adversarial review。
