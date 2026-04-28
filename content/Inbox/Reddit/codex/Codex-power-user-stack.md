---
title: With this setup CODEX is far better than Claude Code
created: 2026-04-28
updated: 2026-04-28
source: https://www.reddit.com/r/codex/comments/1sxgx3l/with_this_setup_codex_is_far_better_than_claude/
published: 2026-04-27
tags:
  - reddit
  - codex
  - ai-tools
  - workflow
---

> **繁中摘要**：作者整理切到 Codex 全職後使用的 7 個搭配 repo（skills、orchestration、token tracking、context 壓縮、knowledge graph、model 切換器），用來補強 Codex CLI 在實務工作流上的缺口。

---

## 原文重點

切換到 Codex 全職後，作者認為真正讓 Codex 拉開與 Claude Code 差距的不是模型本身，而是周邊 setup。以下是他列出的 7 個 repo 與用途：

- **`ComposioHQ/awesome-codex-skills`**（2.7k stars）— Codex 專屬 skills 清單，含 `gh-fix-ci`、`sentry-triage`、`changelog-generator`、`connect`（透過 Composio 串 Slack / Notion / GitHub 等 1000+ apps）。作者表示 "fixed CI in 30 seconds" 多半靠這個 repo。
- **`openai/codex`**（78.3k stars）— 官方 CLI 本體。需注意網路上很多 "Codex" 工具其實是非官方 wrapper，從這個 repo 開始才是正解。
- **`ComposioHQ/agent-orchestrator`**（6.5k stars）— 在 git worktree 上跑多個 Codex session 並行，一個 worktree 一個 agent，CI failure 自動處理。配合 GPT-5.5 在 1% quota 仍持續執行的特性可疊加效益。
- **`ryoppippi/ccusage`**（13.4k stars）— CLI，列出每個 Codex session 的實際 token 花費，用來抓出靜默燒掉週限額的 runaway tool loop。
- **`JuliusBrussee/caveman`**（48k stars）— 把 Codex 回應壓成 caveman english，宣稱可省 ~65% token，週末 quota 見底時的工具。
- **`safishamsi/graphify`**（36.4k stars）— 為 codebase 建 knowledge graph，讓 Codex 進新 repo 時的 onboarding 時間大幅縮短。
- **`farion1231/cc-switch`**（52.8k stars）— 桌面工具，在 Codex / Claude Code / OpenCode / Gemini 之間切換 model，作者周圍跑 Codex 的人多半用這個切。

## 社群討論亮點

- 留言質疑 `awesome-codex-skills` 可能是 astroturfing：repo 內 skill 引用不存在的 script（舉例 `competitive-ads-extractor/SKILL.md`），質疑為何能累積到 2.7k stars。**評估這份清單時 awesome-codex-skills 需保留懷疑態度**，其餘 repo 未被質疑。
- 有人回報用 Codex 搭配 OpenCode 也運作良好，並非一定要走原文這套 stack。
