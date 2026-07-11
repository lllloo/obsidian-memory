---
title: Hermes Agent
description: Nous Research 開源的自我進化 AI agent：學習迴路自動生成並改良 skill，跨 session 累積記憶與使用者模型
created: 2026-07-08
updated: 2026-07-11
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - agent-framework
  - skill
  - mcp
  - automation
---

# Hermes Agent

Nous Research 開源、MIT 授權的**自我進化 AI agent**，標語 *The agent that grows with you*。定位為 coding／personal agent，與 Claude Code、OpenClaw 同類，但差異化主打**內建學習迴路**：記憶與 skill 是會複利成長的資產，而非每次從零開始。原始資料見 [[Hermes-Agent-NousResearch]]。

> 這套哲學與本 vault 背後的 [[LLM-Wiki-知識管理模式]] 不只是「同源」，而是**同一套官方 skill**：Hermes 內建的 `llm-wiki` skill 直接聲明採用 Karpathy 的 LLM Wiki pattern，與本 vault 的三層架構一一對應——證明這套方法論已被獨立產品化，不是本 vault 的孤例。差別在 Hermes 另外疊了一條獨立複利軸：`llm-wiki`（陳述性知識，是什麼）之外，還有自主 **skill 庫**複利程序性知識（怎麼做），兩軸互補、各自演進。

## 核心差異：學習迴路（Learning Loop）

一般 agent 每個 session 從零開始；Hermes 讓經驗沉澱下來：

| 機制 | 作用 |
|---|---|
| 有界核心記憶（Bounded core memory） | `MEMORY.md`／`USER.md`，各 2,200／1,375 字元上限（官方文件快照值，隨版本可變；出處 [[Hermes-Agent-NousResearch]]），session 開始一次性注入、中途絕不改變（保留 prefix cache）；寫爆時**不自動摘要精簡，直接報錯**，逼 agent 自己合併/刪除過時條目 |
| Autonomous skill creation | 完成複雜任務（5+ 次工具呼叫）成功、解決錯誤、使用者糾正、或發現非顯而易見流程時觸發，自動把流程萃取成可重用 skill；預設免人工核准即可寫入 |
| Skill self-improvement | skill 在使用過程中自我修正 |
| Autonomous Curator | 自主策展人：評分、合併重疊、封存過時、寫每輪報告、保護 pinned skill |
| `llm-wiki` skill（官方內建） | **逐字複刻 Karpathy 的 LLM Wiki 模式**（raw/wiki/schema 三層），文件明言「Based on Andrej Karpathy's LLM Wiki pattern」——見 [[LLM-Wiki-知識管理模式]] |
| 外接長期知識庫 | 8 個 memory provider 外掛（Honcho、Mem0、Supermemory、ByteRover 等）可選接，提供知識圖譜、語意檢索、自動事實抽取等，對應核心記憶（大腦）之外的圖書館 |

> ⚠️ **更正**（2026-07-09 deep-research 對抗式驗證）：先前版本描述的「agent 靠週期性 nudge 記憶」與「FTS5 全文檢索過往對話＋LLM 摘要做跨 session 回憶」查無官方文件依據，已被驗證駁回（0–3 票），改以上表「有界核心記憶」的官方逐字描述取代。

其中 **skill 相容 agentskills.io 開放標準**——與本 repo `CLAUDE.md` 遵循的同一標準，理論上 skill 可跨 Hermes / Claude Code / Cursor 等工具移植；但「skill 目錄結構與本 vault `.agents/skills` 慣例高度同構」一說同樣查無依據，已被驗證駁回，勿引用。

> ⚠️ **待查風險**：背景 skill-review agent 曾有產生非預期副作用的案例，Autonomous skill creation／Autonomous Curator 的品質把關機制尚待確認失敗模式再借鑑（未解問題見 [[第二大腦方法論比較]]）。

## 架構組件

- **Agent Core** — 主推理迴路
- **Gateway** — 單一 process 橋接多通訊平台（Telegram、Discord、Slack、WhatsApp、Signal、Matrix、Feishu、Teams… 官方稱 18–20+ 平台）
- **Skills System** — 可攜、可分享的程序性記憶
- **Tools（60+）** + **MCP Integration** — 內建工具集，並可接外部 MCP server 且過濾工具
- **Subagents** — 隔離、可平行的子代理
- **SOUL.md**（全域人格）／**Context Files**（專案級脈絡）— 塑形對話行為

記憶層可插拔：內建之外另有多個 memory provider 外掛可選接（見上表「外接長期知識庫」）。

## 任務／待辦管理：Kanban board

待辦事項、roadmap、task 不是放在有界核心記憶（`MEMORY.md`／`USER.md`）裡，而是另立一套獨立子系統：**SQLite 存儲的多 profile 持久任務佇列**（`~/.hermes/kanban.db`，WAL 模式；多板時 `~/.hermes/kanban/boards/<slug>/kanban.db`）。核心設計是「每次交接是一列任何 profile（或人）都能讀寫」，用以區分更輕量的 `delegate_task`（RPC 式、父層阻擋等子層返回、失敗即失敗、無審計軌跡）。原始細節見 [[Hermes-Agent-Kanban]]。

- **Task 狀態機**：`triage → todo → ready → running → blocked → done → archived`，欄位含 `assignee`、`priority`、`workspace`（scratch/dir:\<path\>/worktree）、`max_retries`、`goal_mode` 等；`task_links`／`task_comments`／`task_runs`／`task_events` 等附屬表提供依賴、協作留言、重試歷史、審計日誌。
- **Agent 工具**：`kanban_show`／`kanban_list`／`kanban_complete`／`kanban_block`／`kanban_heartbeat`／`kanban_comment`／`kanban_create`／`kanban_link`／`kanban_unblock`，worker 與 orchestrator 走不同典型流程。
- **Dispatcher** 每 60 秒巡一輪：回收逾時聲明與崩潰 worker、依 `task_links` 自動把父層 `done` 的子任務從 `todo` 升到 `ready`、控管全板／per-profile 並行上限。
- 定位：Kanban 給「跨 agent 邊界、需存活重啟、可能要人工介入、需事後可探知」的工作；純同步子推理仍用 `delegate_task`。

這與本 vault [[MEMORY]] 的角色形成對照：本 vault 目前把「操作狀態」與「待追蹤開放問題」混記在同一份有界快照檔；Hermes 則是**有界核心記憶（穩定事實/偏好）與任務佇列（進行中工作、需要跨 session 存活的 to-do）分屬兩個獨立子系統**，前者小而穩定，後者專門承載狀態機與協作審計。

## 部署與 Model

- **Terminal backends**：Local、Docker、SSH、Singularity、**Modal**（serverless、閒置近零成本）、**Daytona**（serverless、閒置休眠）——serverless 後端讓 agent 長駐又省錢。
- **Model-agnostic**：Nous Portal（自帶 web search／生圖／TTS／browser）、OpenRouter、OpenAI、任意 custom endpoint，`/model` 切換宣稱 300+ models。

## 成本控制

Hermes 24/7 長駐（有別於跑完即停的 Claude Code），背景任務、self-evolving memory 與 90+ 預裝 skill 的 header 都持續吃 token，成本靠設定治理（拆解見 [[Hermes-Agent-Token成本優化設定]]）：

- **模型路由是帳單最大槓桿**：auxiliary tasks 與 subagents 預設 fallback 到主模型，改指便宜模型；effort level 依任務調，簡單任務關 thinking。
- **Context 瘦身**：調低壓縮門檻與 target ratio、精簡 memory/agent files、一次性指令用 ephemeral system prompt 不寫進 context files。
- **削減常駐 context**：每則訊息都附帶全部已啟用的 tools/skills/MCP，不用的直接關；MCP 用 tool search 按需載入單一工具。
- **Hard limits 防空轉**：max tokens、max turns（來源快照時預設 150，屬版本可變預設值，可下修）、hard stop、cron job 回合上限，避免卡住時燒光額度。
- 用量追蹤：token 使用記錄存 root database，`insights` 指令看近 30 天成本分解。

## 周邊

- **hermes-agent-self-evolution**：DSPy + GEPA 演化 skill/prompt/code，純 API、無需 GPU 訓練，每次優化約 $2–10——把「skill 自我改良」再往離線最佳化推一層。

## 關聯

- 原始資料：[[Hermes-Agent-NousResearch]]、[[Hermes-Agent-Token成本優化設定]]（token 成本拆解與設定）、[[Hermes-Agent-Kanban]]（任務佇列技術細節）
- 同源哲學：[[LLM-Wiki-知識管理模式]]（知識複利 vs. Hermes 的技能複利）
- `llm-wiki` skill 治理細節與其他實作對照：[[LLM-Wiki-生態實作比較]]——sha256 漂移偵測、封閉 tag taxonomy、矛盾交使用者複核等機制在生態中的定位。
- 記憶架構對照：[[Claude-Code-記憶系統六層比較]]——Hermes 屬「agent 自策展記憶 + skill」路線，且與其中 Level 3 的 OpenClaw 血緣相關（`hermes claw migrate` 自 OpenClaw 匯入）。
- 人類 PKM 對照：[[第二大腦方法論比較]]——Hermes 的「有界核心記憶 vs. 外接 llm-wiki／provider」雙軸結構，與 BASB（資源/專案管理）vs. Zettelkasten（深度連結）的互補分工邏輯同構（中等信心，2026-07-09 對抗式驗證）。
- harness 工程脈絡：[[Agent-Harness-Engineering-框架綜述]]——Hermes 的 loop、skill 生成與有界記憶等構件可對照該頁的 harness 定義範疇（tools／memory／guardrails）。
