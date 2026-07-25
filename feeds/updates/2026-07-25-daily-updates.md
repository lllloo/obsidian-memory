---
title: "2026-07-25 Daily Updates"
created: 2026-07-25
updated: 2026-07-25
tags:
  - updates
  - copilot
  - opencode
---

## GitHub Copilot

### 2026-07-24（[Claude Opus 5 is now available in GitHub Copilot](https://github.blog/changelog/2026-07-24-claude-opus-5-is-now-available-in-github-copilot)）

**繁中摘要**：GitHub Copilot 新增 Claude Opus 5 模型選項，設計用於需要嚴謹推理、有效工具使用的複雜長時任務，適合較吃重的 coding agent 場景。

- **模型上線**：Claude Opus 5（Anthropic 最新 Opus 模型）現可在 GitHub Copilot 中選用。

---

## OpenCode

### v1.18.5 · 2026-07-24（[Changelog](https://opencode.ai/changelog)）

**繁中摘要**：OpenCode v1.18.5 聚焦 core 模型相容性修復與 desktop app 對新版 server 的整合，包含 Claude adaptive thinking 處理、OpenAI Responses phase 修復等。

- **Model handling 修復**：改善 Claude adaptive thinking 在更多 response 型態下的處理，並避免 OpenAI Responses phase handling 可能中斷對話的問題。
- **其他 core 修復**：Mistral reasoning history 一致性、prompt caching 穩定化、MiniMax M3 variant 選擇修正、search 中 symlink path 保留。
- **Desktop 更新**：大量調整以支援新版 server（terminal transport、session timeline、event streaming），含 optimistic updates、agent toggle 同步、session status 復原等。

---
