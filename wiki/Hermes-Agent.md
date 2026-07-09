---
title: Hermes Agent
description: Nous Research 開源的自我進化 AI agent：學習迴路自動生成並改良 skill，跨 session 累積記憶與使用者模型
created: 2026-07-08
updated: 2026-07-09
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

> 這套哲學與本 vault 背後的 [[LLM-Wiki-知識管理模式]] 同源——**知識/技能編譯一次後持續維護，維護成本趨近零**。差別在維護對象：Hermes 讓 agent 自主策展 **skill 庫**，LLM Wiki 讓 agent 維護互聯的 **markdown wiki**。兩者都把「簿記雜活」交給不會膩的 LLM。

## 核心差異：學習迴路（Learning Loop）

一般 agent 每個 session 從零開始；Hermes 讓經驗沉澱下來：

| 機制 | 作用 |
|---|---|
| Agent-curated memory | agent 自管記憶，靠週期性 nudge 提醒把知識持久化 |
| Autonomous skill creation | 完成複雜任務後自動把流程萃取成可重用 skill |
| Skill self-improvement | skill 在使用過程中自我修正 |
| Autonomous Curator | 自主策展人：評分、合併重疊、封存過時、寫每輪報告、保護 pinned skill |
| FTS5 cross-session recall | 全文檢索過往對話 + LLM 摘要，做跨 session 回憶 |
| Honcho 使用者建模 | dialectic 三段推理（Initial Assessment → Self-Audit → Reconciliation）建立「你是誰」的模型 |

其中 **skill 相容 agentskills.io 開放標準**——與本 repo `CLAUDE.md` 遵循的同一標準，理論上 skill 可跨 Hermes / Claude Code / Cursor 等工具移植。

## 架構組件

- **Agent Core** — 主推理迴路
- **Gateway** — 單一 process 橋接多通訊平台（Telegram、Discord、Slack、WhatsApp、Signal、Matrix、Feishu、Teams… 官方稱 18–20+ 平台）
- **Skills System** — 可攜、可分享的程序性記憶
- **Tools（60+）** + **MCP Integration** — 內建工具集，並可接外部 MCP server 且過濾工具
- **Subagents** — 隔離、可平行的子代理
- **SOUL.md**（全域人格）／**Context Files**（專案級脈絡）— 塑形對話行為

記憶層可插拔：內建之外另有 8 個 memory provider 外掛（Honcho、Mem0、Supermemory、ByteRover 等），提供知識圖譜、語意檢索、自動事實抽取等。

## 部署與 Model

- **Terminal backends**：Local、Docker、SSH、Singularity、**Modal**（serverless、閒置近零成本）、**Daytona**（serverless、閒置休眠）——serverless 後端讓 agent 長駐又省錢。
- **Model-agnostic**：Nous Portal（自帶 web search／生圖／TTS／browser）、OpenRouter、OpenAI、任意 custom endpoint，`/model` 切換宣稱 300+ models。

## 成本控制

Hermes 24/7 長駐（有別於跑完即停的 Claude Code），背景任務、self-evolving memory 與 90+ 預裝 skill 的 header 都持續吃 token，成本靠設定治理（拆解見 [[Hermes-Agent-Token成本優化設定]]）：

- **模型路由是帳單最大槓桿**：auxiliary tasks 與 subagents 預設 fallback 到主模型，改指便宜模型；effort level 依任務調，簡單任務關 thinking。
- **Context 瘦身**：調低壓縮門檻與 target ratio、精簡 memory/agent files、一次性指令用 ephemeral system prompt 不寫進 context files。
- **削減常駐 context**：每則訊息都附帶全部已啟用的 tools/skills/MCP，不用的直接關；MCP 用 tool search 按需載入單一工具。
- **Hard limits 防空轉**：max tokens、max turns（預設 150 可下修）、hard stop、cron job 回合上限，避免卡住時燒光額度。
- 用量追蹤：token 使用記錄存 root database，`insights` 指令看近 30 天成本分解。

## 周邊

- **hermes-agent-self-evolution**：DSPy + GEPA 演化 skill/prompt/code，純 API、無需 GPU 訓練，每次優化約 $2–10——把「skill 自我改良」再往離線最佳化推一層。

## 關聯

- 原始資料：[[Hermes-Agent-NousResearch]]、[[Hermes-Agent-Token成本優化設定]]（token 成本拆解與設定）
- 同源哲學：[[LLM-Wiki-知識管理模式]]（知識複利 vs. Hermes 的技能複利）
- 記憶架構對照：[[Claude-Code-記憶系統六層比較]]——Hermes 屬「agent 自策展記憶 + skill」路線，且與其中 Level 3 的 openclaw 血緣相關（`hermes claw migrate` 自 OpenClaw 匯入）。
