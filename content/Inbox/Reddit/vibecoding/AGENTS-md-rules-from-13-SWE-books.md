---
title: I rewrote 13 software engineering books into AGENTS.md rules.
created: 2026-04-27
updated: 2026-04-27
source: https://www.reddit.com/r/vibecoding/comments/1suo2vy/i_rewrote_13_software_engineering_books_into/
published: 2026-04-24
tags:
  - reddit
  - vibecoding
  - ai-tools
  - best-practices
---

> **繁中摘要**：作者把 13 本經典軟體工程書（Clean Code、DDD、Refactoring、Pragmatic Programmer 等）改寫成 AGENTS.md 規則集，支援 Claude Code、Codex、Cursor；repo 在 ciembor/agent-rules-books。

---

## 連結

<https://github.com/ciembor/agent-rules-books>

支援工具：Claude Code、Codex、Cursor

收錄書單：

1. A Philosophy of Software Design — John Ousterhout
2. Clean Architecture — Robert C. Martin
3. Clean Code — Robert C. Martin
4. Code Complete — Steve McConnell
5. Designing Data-Intensive Applications — Martin Kleppmann
6. Domain-Driven Design — Eric Evans
7. Domain-Driven Design Distilled — Vaughn Vernon
8. Implementing Domain-Driven Design — Vaughn Vernon
9. Patterns of Enterprise Application Architecture — Martin Fowler
10. Refactoring — Martin Fowler
11. Release It! — Michael T. Nygard
12. The Pragmatic Programmer — Andrew Hunt and David Thomas
13. Working Effectively with Legacy Code — Michael Feathers

## 社群討論亮點

- **LLM 指令上限是真實限制**（top comment, 48 票）：HumanLayer 等研究指出 LLM 可靠遵循的具體指令數約 50–100 條；單一本書改寫的 rule set 就會吃光額度，不留空間給 planning/implementation 自訂指令——意思是「全部塞進 AGENTS.md」不可行，要挑著用
- **LLM 已被這些書訓練過**：可直接寫「follow best practices and guidelines from \[書名\]」就有效，不一定需要外掛規則檔（爭議點，作者觀點需自行驗證）
- 實務建議：選 1–2 本當前專案最相關的（如 legacy 改造拿 Working Effectively with Legacy Code、領域複雜拿 DDD Distilled）做為 governance 基底，而非全部疊上
