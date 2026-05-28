---
title: Codex plugin for Claude Code
created: 2026-05-08
updated: 2026-05-28
source: https://github.com/openai/codex-plugin-cc
tags:
  - claude-code
  - codex
  - code-review
---

Codex plugin for Claude Code 是 OpenAI 出的 plugin，讓 Claude Code 內可以呼叫 Codex 做 code review 或委派任務。觸發情境：取得跨模型獨立 review（`/codex:review`，read-only）、用 steerable 挑戰式 review 質疑設計選擇（`/codex:adversarial-review`）、把問題委派給 Codex 用便宜模型快速試方向（`/codex:rescue`）。需要 ChatGPT 訂閱或 OpenAI API key，共用 Codex 用量額度；安裝細節以 README 為準。

## 連結

- Repo：<https://github.com/openai/codex-plugin-cc>
- Codex 官方：<https://developers.openai.com/codex/>

## 相關

- [[Claude-Code-Review-工作流]] — 跨模型 review 補充工具
