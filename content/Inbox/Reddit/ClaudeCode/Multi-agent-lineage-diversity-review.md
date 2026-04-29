---
title: "Claude + Codex + Opencode = God Mode"
created: 2026-04-29
updated: 2026-04-29
source: https://www.reddit.com/r/ClaudeCode/comments/1sxs8c0/claude_codex_opencode_god_mode/
published: 2026-04-28
tags:
  - reddit
  - claude-code
  - workflow
  - multi-agent
  - subagent
---

> **繁中摘要**：作者用 tmux 同時跑 Claude / Codex / Gemini / Kimi / DeepSeek 多個 agent，重點在 reviewer 必須跨 model lineage（Codex + Gemini + OpenCode 各一）才能避免同家族 blind spot；用 `/work` command 建 context pack、3 reviewer 平行 review、共識才放行。

---

## 原文重點

- **基本訂閱組合**（成本只是既有訂閱費）：
  - Claude 20x plan（Opus 4.6 / 4.7）
  - 3x Codex CLI，分別跑在不同 ChatGPT Plus 帳號（reset window 不衝突）
  - Gemini 3.1 Pro Preview
  - Kimi K2.6 + DeepSeek V4 Pro，透過 OpenCode Go（比 API key 便宜，Kimi 還有 3x limit）
- 在 Claude 內建 `/work` command，處理四種任務形狀：plan / implement / major bug / minor bug
  - 對每個任務組 context pack，平行送 3 個 reviewer，等共識
- **關鍵設計：lineage diversity**
  - Reviewer 組合固定為 1 Codex + 1 Gemini + 1 OpenCode
  - 同家族模型共享 blind spot，3 個 Codex session 互審等同 echo chamber
  - 三個 lineage 都同意才開 gate，否則 Claude 修改後再跑一次
- **Merge 前 4 題 checklist**（由 Claude 填，作者再決定 merge / fix first / override with reason）：
  1. coding principles
  2. architecture drift
  3. tests pass
  4. reviewer consensus
- 觀察：Opus 自己跑時 failure 是 silent 的——code 看起來合理、tests pass，但 subtle bug 或 design drift 之後才浮現。讓不同 model family 重讀同一份 code 抓出意外多的問題

## 社群討論亮點

- 有人提到 [`nyldn/claude-octopus`](https://github.com/nyldn/claude-octopus) 是現成做類似事情的 repo
- 多人問 `/work` prompt 與 orchestrator 內容（作者表示願意分享，留言中尚未貼出）
- 同類做法分享：design (Gemini) → plan (GPT-5.5) → build (Sonnet/Kimi) → validate/audit (GLM-5.1/GPT-5.5) 的 loop，外加 GH Copilot 管 commits/pushes
- 痛點留言：自架 Claude+Codex 雙 agent 容易「talk past each other」，需要設計 reconcile 機制讓兩邊整合而非各說各話
