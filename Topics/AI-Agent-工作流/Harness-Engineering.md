---
title: Harness Engineering
created: 2026-04-21
updated: 2026-06-11
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
- **通用工具比客製 JSON schema 工具穩**：LLM 對 `grep` / `git` / `npm` 這類通用 CLI 有更豐富訓練先驗，自訂工具 schema 越多越脆；但前提是資料本身已經結構化、命名一致、可被檔案系統與 CLI 讀懂（Vercel 在 text-to-SQL agent 拿掉 80% 工具後速度 / token / 成功率都改善）。延伸手法是**用型別系統當 guardrail**：與其讓 LLM 直接猜 raw JSON，不如讓它產出能編譯的程式碼再轉換——n8n 官方 MCP 讓模型寫 TypeScript、經 type-check / 編譯驗證後才轉成 workflow JSON，型別系統先過濾掉大量結構錯誤
- **大型 codebase 用 file system 導航勝過 RAG**：把整個 codebase embedding 後 semantic search，容易拿到過期或相似但錯誤的檔案、central index 與實際檔案系統不同步、agent 據此幻覺出不存在的 module / symbol；改用 file system + shell + 精準讀檔逐步縮小範圍（與 agentic RAG 的 `list/grep/read` 骨架同理）更穩、更省 context——這是「通用工具勝過客製抽象」在 code navigation 上的體現
- **狀態外部化才能續跑**：progress 文件、feature checklist、task graph、git commits——把「只存在對話裡」的資訊拉回 repo；compaction 可以降低重開 session 的頻率，但長任務仍需要 handoff artifacts、必要時 reset，以及可被下一輪 agent 接手的外部狀態
- **依賴變更也是 runtime guardrail**：讓 agent「必須先證明 dependency 值得加入」而非自由安裝，把套件變更變成可審核事件

## 命名史與爭議

詞很新、業界尚無嚴格定義，公認起點是 2026-02-05 Mitchell Hashimoto《My AI Adoption Journey》——他自陳「不知道業界有沒有公認叫法，姑且叫它 Harness Engineering」，核心理念是 agent 一犯錯就改造系統讓它絕不再犯。隨後 OpenAI 那篇標題帶 Harness Engineering 的文章正文其實只提了一次 Harness，被推測是受 Hashimoto 啟發後才把詞放進標題；LangChain《The Anatomy of an Agent Harness》則把公式定調為 `Harness = Agent − Model`。

**是不是噱頭**：它用到的技術沒一個是新的——linter、任務拆解規劃、品質評估機制早就存在，Harness Engineering 只是把它們重組到一個新詞下，提供的是系統思維框架而非顛覆性新技術。懷疑論的兩個攻擊點：(1) 新瓶裝舊酒還造詞宣傳；(2) 隨模型能力增強，今天的 Harness 設計遲早被模型自身吸收而不再需要。

合理立場：**不是噱頭，但也不是終局**，而是過渡期的關鍵技術。模型仍會犯錯、幻覺、在複雜任務偏離軌道，在此現實下誰把 Harness 搭得更穩，誰就更早把模型能力轉成生產力。

## 框架實作

- [[GAN-Style-Harness]] — Planner / Generator / Evaluator 三角的具體實作
- [[bookmark-Superpowers-Agent開發框架|Superpowers]] — 偏 TDD / implementation gates 的流派
- [[bookmark-GStack-Agent開發框架|GStack]] — 偏規劃 / design / QA 的 workflow pack
- [[bookmark-BMAD-Agent開發框架|BMAD]] — 偏 agile lifecycle / 12+ 軟體角色 persona 接力
- [[bookmark-Spec-Kit-Spec驅動開發框架|Spec-Kit]] — 偏 Spec-Driven Development，以 spec 為 first-class artifact 驅動 code 生成

多 agent 協作機制（Subagent / Agent Teams / Forked subagent / worktrees）見 [[Claude-Code-多-Agent-協作]]；再往上一層的協作拓撲（人管 ticket、agent 在 ticket 層工作回報，「狀態外部化」推進成 ticket 系統即 state machine）見 [[Ticket-驅動的-Agent-協作]]。

## 來源

- [Harness engineering: leveraging Codex in an agent-first world (OpenAI)](https://openai.com/index/harness-engineering/)
- [Harness design for long-running application development (Anthropic)](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [We removed 80% of our agent's tools (Vercel)](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools)
- [My AI Adoption Journey (Mitchell Hashimoto)](https://mitchellh.com/writing/my-ai-adoption-journey) — 詞源
- [The Anatomy of an Agent Harness (LangChain)](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness) — 定調 `Harness = Agent − Model`
