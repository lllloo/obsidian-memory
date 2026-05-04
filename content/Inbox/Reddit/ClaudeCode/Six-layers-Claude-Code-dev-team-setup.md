---
title: Six layers that turned my Claude Code into a 24/7 dev team
created: 2026-05-04
updated: 2026-05-04
source: https://www.reddit.com/r/ClaudeCode/comments/1szwytx/six_layers_that_turned_my_claude_code_into_a_247/
published: 2026-04-30
tags:
  - reddit
  - claude-code
  - workflow
  - subagent
  - skill
---

> **繁中摘要**：作者把 Claude Code 工作流分六層（CLAUDE.md / 跨 session memory / Skills / Subagents / Hooks / Background tasks）並貼出可重用的範例設定，整套跑在 $20 Pro plan 上。社群對「真有用」存疑但結構與工具清單具參考價值。

---

## 原文重點

### 第 1 層：CLAUDE.md（專案根目錄）

每個 session 開頭讀。範例骨架：

```markdown
## project
- stack: next.js 14, typescript, tailwind, postgres via prisma
- monorepo: /apps/web, /apps/api, /packages/shared

## conventions
- all components in PascalCase
- API routes return { data, error } format
- no default exports except pages
- tests live next to source files, named *.test.ts

## architecture decisions
- chose prisma over drizzle (dec 2024): type safety priority
- chose zustand over redux (jan 2025): less boilerplate

## current focus
- migrating payment system from stripe checkout to stripe elements

## rules
- never mass edit more than 3 files without showing me the plan first
- always run existing tests before writing new ones
- if a task takes more than 5 steps, create a plan document first
```

要點：conventions 殺 nitpick；decisions 阻止 Claude 重新爭論已定案選擇；rules 編碼那些「在 chat 反覆糾正」的事。

### 第 2 層：跨 session memory（Obsidian + 兩個工具）

Vault 結構（靈感來自 Karpathy 的 [llm-wiki](https://github.com/karpathy/llm-wiki)）：

```
/vault
  /decisions    每個架構決策含 context
  /errors       踩過的 bug 與修法
  /patterns     在本 codebase 有效的 code pattern
  /sessions     每日 session 摘要
  /stack        每個工具的文件
  Memory.md     使用者輪廓、preference
  index.md      master index
```

搭配：

- **claude-mem**：每個 session 壓縮入 persistent store，下個 session 帶入
- **[claude-subconscious](https://github.com/0xfurai/claude-subconscious)**：背景 agent 觀察 session、被動寫 memory，無需 prompt

### 第 3 層：Skills（特化的 markdown）

- `/plugin install superpowers@claude-plugins-official`：強制 brainstorm → spec → plan → TDD → implement → review，code 動之前要先寫 spec 給人類批准
- Trail of Bits security skills：每個 PR 自動 audit
- Anthropic 官方 skills：PDF / DOCX / XLSX / data analysis 參考實作
- **tdd-guard**：阻擋跳過測試的 commit，block 訊息會解釋缺什麼

### 第 4 層：Subagents

每個角色獨立 context window 與 CLAUDE.md：architect（設計與 spec）等。避免單 session 第四個任務之後 context 被污染。

### 後續層級

原文 selftext 已截斷，第 5、6 層（推測為 Hooks、Background tasks）未完整呈現於本筆記。

## 社群討論亮點

- **$20/month 質疑**：第一名留言（64 分）認為這套不可能在 $20 Pro plan 撐超過 15 分鐘，暗示作者沒揭露真實 token 消耗
- **行銷嫌疑**：另一個高分留言（19 分）質疑這是隱性銷售第三方 CLI 工具，沒提供真實證據
- **Agent 寫自己的 logic**：有開發者反映 agent 傾向自己寫邏輯而非用既有 function，這是上述 conventions/patterns 層想解決的痛點
