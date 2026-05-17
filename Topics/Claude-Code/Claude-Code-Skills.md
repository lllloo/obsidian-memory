---
title: Claude Code Skills
created: 2026-03-29
updated: 2026-05-08
tags:
  - claude-code
  - ai-tools
  - moc
---

Skills 是把可重用流程、知識、best practices 打包成可延遲載入工作模組的格式——最小單位是含 `SKILL.md` 的資料夾，Claude 依 description 自動觸發或用 `/skill-name` 手動呼叫。官方已把 custom commands 併入 skills 概念，要 supporting files / auto invocation 一律走 skill。

> **兩個語境別混**：
>
> - **Agent Skills 通用規格**（[agentskills.io](https://agentskills.io/)）：定義 `SKILL.md` + progressive disclosure + supporting files 的開放標準
> - **Claude Code Skills**：對同一概念的實作，多了 `disable-model-invocation`、`context: fork`、`agent` 等 Claude Code 專屬欄位

字元上限 / 保留字 / `SKILL.md` 全大寫等命名硬規則見 [[Claude-Code-Skill-Command-命名]]，本文聚焦立場與實務判斷。

## 立場

- **Skill vs MCP 解不同問題**：Skill 解「流程怎麼做、何時做、有哪些慣例」，MCP 解「可以呼叫哪些外部能力」——常見搭配是 skill 寫流程、MCP 提供原子能力
- **別把 token 節省當選 Skill 的主因**：Skill 確實 token 友善（progressive disclosure 只 metadata 常駐），但選 Skill 的理由是「流程封裝可重用」——token 是 bonus，不是 driver
- **不是所有重複都該包 skill**：寫完只用一次的 skill 就是 prompt template，不該做成 skill；重複出現後再抽成 skill

## 常見陷阱

- **Skill bloat**：description 重疊 / 粒度太細 / 邊界不清 → Claude 選錯 skill 或該觸發時不觸發。重疊功能寧可合併
- **跨 surface 同步幻覺**：custom skills 不會在 Claude.ai / API / Claude Code 之間自動同步——分發是另一個問題，社群有不同 Meta-Skill 模式可參考但都不是官方內建
- **`description` 寫太泛 / 太保守**：只寫「做什麼」沒寫「何時該用」→ undertrigger。把使用情境寫進 `description` / `when_to_use`，常見 phrasing 前置

## 來源

- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [anthropics/skills](https://github.com/anthropics/skills) — 含 `skill-creator` 半自動建立工具
