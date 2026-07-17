---
title: Agent Harness Engineering 框架綜述
description: 以 Anthropic 系列工程論述與 arXiv 原始碼級 taxonomy 為主幹的 harness 工程綜述：定義範疇、方法論主軸、實作橫向比較與 meta-harness 演進方向
created: 2026-07-10
updated: 2026-07-17
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - agent-framework
  - context-engineering
  - coding-agent
---

# Agent Harness Engineering 框架綜述

Harness engineering 指圍繞 LLM 建構 scaffolding 系統的工程學科：agentic loop、tool use、context 管理、記憶與驗證迴路。本頁彙整 deep-research（2026-07-10，24 來源、25 條主張三票對抗式查證，**25 confirmed／0 refuted**）的確認結果。核心論述目前以 Anthropic 系列工程文章最完整——這既是本頁的主幹，也是本頁最大的證據偏倚（見文末「證據限制」）。

## 定義與範疇

Harness 是包裹在 LLM 外圍、負責「模型推理以外一切」的軟體基礎設施：呼叫模型、路由 tool calls、決定何時停止、錯誤恢復、狀態持久化。常見公式化表述為「Agent = Model + Harness」，harness 涵蓋 tools、memory、workspace、guardrails。（強度：定義類主張跨 Hugging Face、Databricks、Firecrawl 等多方獨立來源一致，屬術語共識。）

## 概念框架：Anthropic 系列論述時間線

以下皆為 Anthropic 第一方工程文章，架構描述已逐字查證原文；**效能宣稱均為 vendor 內部數據、無獨立複現**，引用時應保留此標註。

### 1. Building Effective Agents（2024-12）——基礎分類

- **workflows vs agents 二分**：workflows 是 LLM 與工具經預先定義程式碼路徑編排；agents 是 LLM 動態指揮自身流程與工具使用並保有控制權。此二分被 Spring AI 官方文件、Simon Willison 等廣泛採納，2026 年仍是標準分類。
- **五種具名 workflow 編排模式**：prompt chaining、routing、parallelization（sectioning／voting）、orchestrator-workers、**evaluator-optimizer**（即 generator-evaluator 迴路的原型論述）。
- **方法論立場**：據與數十個團隊合作經驗，最成功的實作不是用複雜框架，而是簡單、可組合的模式；由簡入繁。（強度：vendor 觀察性經驗宣稱，非受控實證。）

來源：[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)——augmented LLM 基石、各模式適用時機、ACI／工具 prompt engineering 與兩個應用域等完整內容見 [[Building-Effective-Agents-Anthropic]]。

### 2. Multi-agent research system（2025-06）——orchestration 與經濟性

- **orchestrator-worker 模式**：lead agent 協調、委派給可平行運作的專門 subagents。
- 內部評測中 Opus 4（lead）＋Sonnet 4（subagents）比單一 Opus 4 agent **高 90.2%**，優勢集中於可平行探索的廣度型查詢。（強度：第一方內部評測、未經獨立複現，勿當通用結論引用。）
- **token 經濟性**：agent 約耗 chat 的 4 倍 token，多 agent 系統約 15 倍。（強度：Anthropic 內部生產遙測、非產業平均；屬自陳成本承認，被多方轉引無爭議。）

來源：[Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)——完整搜尋方法論、CitationAgent 與 prompt 工程細節見 [[多智能體研究系統-Anthropic]]。

### 3. Context engineering（2025-09）——context 是有限資源

- 定義：「在 LLM 推論過程中策展與維護最佳 token 集合的策略集」，範疇超越 prompt engineering。
- 理論基礎：**context rot**——token 數增加時回憶準確度下降，成因與 transformer n² attention 及訓練分佈有關。（強度：context rot 現象另有 Chroma 2025-07 獨立研究佐證，「context rot」一詞即源自 Chroma 而非 Anthropic。）
- long-horizon 三類技術：**compaction**（近上限時摘要重啟）、**structured note-taking／agentic memory**（筆記持久化到 context window 外再拉回——本 vault 的 [[LLM-Wiki-知識管理模式]] 即屬此類）、**sub-agent 隔離**（乾淨 context 深入工作、只回傳約 1,000–2,000 token 摘要）。
- Claude Code 實作 hybrid 策略：CLAUDE.md 前期直接載入＋glob/grep 做 just-in-time 檢索。

來源：[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

### 4. Claude Agent SDK（2025-09）——核心迴圈

- 核心回饋迴圈：**gather context → take action → verify work → repeat**，與 Claude Code 共用 tools、agent loop、context 管理。
- 由 Claude Code SDK 更名而來，反映用途從 coding 擴展到一般 agent。
- context 管理主張檔案系統即可檢索 context（**agentic search**：grep／tail 選擇性載入）；建議先 agentic search、需要更快才加 semantic search。（強度：機制描述經官方文件與第三方教學佐證；社群有「grep-only 耗 token」的效率批評，但不否定機制本身。）

來源：[Building agents with the Claude Agent SDK](https://claude.com/blog/building-agents-with-the-claude-agent-sdk)

### 5. 長時運行 harness（2025-11）——狀態管理與驗證迴路

- **雙 agent 架構**：initializer agent 首輪建置環境；coding agent 每 session 增量推進並留下 artifacts，跨多個 context window 工作。
- **feature 狀態檔**：initializer 把初始 prompt 展開成 200+ features 的需求檔；coding agent 被 prompt 限制一次一個 feature、只能改 `passes` 欄位。（強度：此限制是 prompt 級而非機械強制；效能改善為第一方單案例自述。）
- **驗證迴路實證**：明確提示用瀏覽器自動化（Puppeteer MCP）做端對端測試可大幅提升表現；未明確提示時模型傾向未測試就標記 feature 完成。（強度：單一任務內部實驗、無量化 benchmark；文章自承部分 bug 類別瀏覽器工具仍看不見。）
- 核心宣稱：即使 frontier 模型（Opus 4.5）無 harness scaffolding 仍建不出 production 品質 web app。

來源：[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

### 6. Managed Agents（2026-04）——meta-harness 與「腦手解耦」

- **harness 假設會過期**：harness 把「模型當下做不到的事」寫死進架構，模型升級後變 dead weight。實例：Sonnet 4.5 有 context anxiety（近 token 上限提前收尾），harness 加了 context reset；Opus 4.5 該行為消失，機制成了包袱。
- 因應：把 agent 系統虛擬化為三個獨立演進層——**session**（append-only 事件日誌，「存活於 context window 之外的 context object」，經 getEvents() 切片／回捲／轉換）、**harness**（呼叫模型並路由 tool call 的 loop）、**sandbox**（執行環境）。
- 設計哲學：「對 Claude 周邊介面有主見、對具體 harness 無主見」；Claude Code 定位為其中一種通用 harness，任務專用 harness 在窄域仍勝出。（強度：發佈距查證僅約 3 個月，是否被業界採納尚無證據。）

來源：[Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

## 實作橫向比較：arXiv 原始碼級 taxonomy（2026-04）

首個 source-code 層級的 coding agent scaffold 比較——13 個開源 agent（OpenCode、Gemini CLI、Codex CLI、OpenHands、Cline、Aider、SWE-agent、mini-swe-agent、AutoCodeRover、Agentless、Prometheus、Moatless Tools、DARS-Agent）按 12 維度、三層（control architecture／tool-environment interface／resource management）分析：

- **控制迴圈是組合不是類型**：五種 loop primitives（ReAct、generate-test-repair、plan-execute、multi-attempt retry、tree search）的組合；13 個中 11 個組合多個 primitives，7 個以 sequential ReAct loop 為主。
- **工具表面差異巨大但能力收斂**：從 0 個 LLM 可呼叫工具（Aider，使用者驅動）到 37 個 action classes（Moatless Tools，full MCTS）；但 read／search／edit／execute 四類出現在所有給 LLM 自主權的 agent。
- **context compaction 有七種策略**：硬截斷、sliding window、LLM 摘要、選擇性丟棄 tool result、SWE-agent polling、Gemini CLI verification probe、Cline 主動 compaction。

（強度：**medium**——單一作者 arXiv preprint（[2604.03515](https://arxiv.org/abs/2604.03515)）、未同儕審查、樣本限 coding agents；但主張多為可機械驗證的原始碼事實，附檔案路徑與行號。）

## 方法論主軸（跨來源綜合）

1. **由簡入繁、可組合模式優於重框架**（Anthropic 經驗值；12-Factor Agents 等實務者觀點同向）。
2. **context 是有邊際報酬遞減的有限資源**，compaction／note-taking／subagent 隔離是三大應對。
3. **驗證迴路是品質關鍵**——generator-evaluator、瀏覽器端對端測試；沒有 verify 環節模型會「自認完成」（但必要不充分——測試可被 agent 從內部滿足，證據見 [[AI-自主工作流的實證檢驗]]）。
4. **harness 假設有生命週期**——為當下模型缺陷加的機制，模型升級後要重估、移除，否則變 dead weight。

## 證據限制（2026-07-10 查證拍板）

1. **來源高度集中 Anthropic 第一方**：25 條存活主張中 21 條出自 Anthropic 自家文章。架構描述以第一方為適格來源，但所有效能宣稱（90.2%、「dramatically improved」）皆 vendor 內部數據。
2. **通用框架比較缺口**：OpenAI Agents SDK、LangGraph、AutoGen、CrewAI、smolagents 的逐框架設計哲學比較**沒有存活主張直接覆蓋**——本頁不含這部分內容，勿從本頁推論框架優劣；需另行以各框架官方文件補查。
3. **Karpathy 觀點無存活主張支撐**——研究問題明列但查證後無可引用內容，本頁不引述。
4. **時效風險**：領域演進極快；本頁記錄的具體機制（context reset、passes 欄位限制等）依 Anthropic 自己的「harness 假設會過期」論點，本身就有同樣的過期風險。

被否決主張：本輪 0 條。

## 開放問題

- 通用框架（LangGraph 等）的抽象層級與設計哲學逐一比較（本輪證據缺口，見上）。
- 90.2% 多 agent 優勢有無第三方複現？15 倍 token 成本何時划算的量化邊界？
- Managed Agents 的 session/harness/sandbox 三層是否會成為跨 vendor 標準介面？
- harness 假設「dead weight 化」的生命週期管理有無系統性方法？目前只有 Anthropic 單案例敘事。

## 相關頁

- [[AI-自主工作流的實證檢驗]] — **本頁記錄業界主張該怎麼做，該頁檢驗這些主張有多少獨立證據**。特別是本頁「驗證迴路是品質關鍵」一節：該頁證實測試本身可被 agent 篡改（ImpossibleBench、Cursor 稽核），驗證迴路必要但不充分。
- [[Claude-Code-記憶系統六層比較]] — 本頁 context engineering 一節的三類技術（note-taking／agentic memory）正是該頁六層記憶方案的理論依據。
- [[Hermes-Agent]] — 自我進化 agent 實作，其 skill 生成與有界記憶設計可對照本頁的 harness 構件範疇。
- [[LLM-Wiki-知識管理模式]] — 本 vault 的設計原型，屬 structured note-taking／agentic memory 路線的知識庫形態。
- [[Context-優先與多-agent-的適用邊界]] — **直接補救本頁「來源集中 Anthropic」的證據限制**：引入 Cognition（別建多 agent）與 UC Berkeley MAST 失敗實證兩個非 Anthropic 來源，界定多 agent 的適用邊界。
- [[pi-workflow-編排-harness-與本-vault-分野]] — 該頁把 pi-workflow 定位為編排層 prior art，其「編排職能已被 harness 覆蓋」的論點即座落於本頁的 workflows/agents 二分主軸。
- [[OpenSpec]] — spec-driven 工具的具體實作，該頁以本頁作「業界怎麼說該建 agent」的框架層綜述互補，本頁回指其工具細節。
