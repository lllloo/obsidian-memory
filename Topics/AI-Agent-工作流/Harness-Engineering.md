---
title: Harness Engineering
created: 2026-04-21
updated: 2026-05-27
tags:
  - claude-code
  - ai-agent
  - harness
---

**Harness Engineering** 是設計、建置、迭代 agent harness 的工程實踐，跟 Prompt Engineering / Context Engineering 並列。

Agent = Model + Harness。Harness 是 prompt 之外、把 instructions、tools、runtime guardrails、互動方式組裝成「agent 失敗時有外部機制把它拉回正軌」的系統——重點不是 prompt 多神，而是失敗 recovery 機制。

> 命名：OpenAI 用 **Harness Engineering**，Anthropic 用 **harness design**。兩者在同一個問題域，但重心不同：前者偏 agent-first engineering discipline，後者偏長任務 app development 的具體 harness 設計。

## 代表性架構：Planner / Generator / Evaluator

Anthropic 的 long-running app development harness 把複雜任務拆成三個主要角色，適合拿來理解「生成」與「評估」為什麼要分離：

| 角色 | 職責 | 重點 |
|---|---|---|
| Planner | 規劃 | 定義目標、範圍、驗收標準（產品層，非技術細節） |
| Generator | 實作 | 根據 plan 交付，跟 git / tests / runtime 整合 |
| Evaluator | 驗證 | 站在對立面找 bug、找缺口；不跟 generator 共用自我評價 |

## 立場

- **Generator 不要自評**：LLM 對自己輸出過度自信，主觀任務（UI / 產品完成度）尤其明顯——把評估獨立出來品質才會穩
- **通用工具比客製 JSON schema 工具穩**：LLM 對 `grep` / `git` / `npm` 這類通用 CLI 有更豐富訓練先驗，自訂工具 schema 越多越脆；但前提是資料本身已經結構化、命名一致、可被檔案系統與 CLI 讀懂（Vercel 在 text-to-SQL agent 拿掉 80% 工具後速度 / token / 成功率都改善）
- **狀態外部化才能續跑**：progress 文件、feature checklist、task graph、git commits——把「只存在對話裡」的資訊拉回 repo；compaction 可以降低重開 session 的頻率，但長任務仍需要 handoff artifacts、必要時 reset，以及可被下一輪 agent 接手的外部狀態

## 框架實作

- [[GAN-Style-Harness]] — Planner / Generator / Evaluator 三角的具體實作
- [[Superpowers框架]] — 偏 TDD / implementation gates 的流派
- [[GStack框架]] — 偏規劃 / design / QA 的 workflow pack
- [[BMAD框架]] — 偏 agile lifecycle / 12+ 軟體角色 persona 接力
- [[Spec-Kit]] — 偏 Spec-Driven Development，以 spec 為 first-class artifact 驅動 code 生成

多 agent 協作機制（Subagent / Agent Teams / Forked subagent / worktrees）見 [[Claude-Code-多-Agent-協作]]。

## 來源

- [Harness engineering: leveraging Codex in an agent-first world (OpenAI)](https://openai.com/index/harness-engineering/)
- [Harness design for long-running application development (Anthropic)](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [We removed 80% of our agent's tools (Vercel)](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools)
