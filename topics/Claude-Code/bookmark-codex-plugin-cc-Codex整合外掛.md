---
title: Codex plugin for Claude Code
created: 2026-05-08
updated: 2026-06-23
source: https://github.com/openai/codex-plugin-cc
tags:
  - claude-code
  - codex
  - code-review
---

Codex plugin for Claude Code 是 OpenAI 出的 plugin，讓 Claude Code 內可以呼叫 Codex 做 code review 或委派任務。觸發情境：取得跨模型獨立 review（`/codex:review`，read-only）、用 steerable 挑戰式 review 質疑設計選擇（`/codex:adversarial-review`）、把問題獨立委派給 Codex 調查／嘗試修復（`/codex:rescue`，非 read-only、會改碼；預設模型由 Codex 自選，可選較小模型或背景執行，視任務可能耗時）。需要 ChatGPT 訂閱或 OpenAI API key，共用 Codex 用量額度；安裝細節以 README 為準。

## 連結

- Repo：<https://github.com/openai/codex-plugin-cc>
- Codex 官方：<https://developers.openai.com/codex/>

## 相關

- [[Claude-Code-Review-工作流]] — 跨模型 review 補充工具
