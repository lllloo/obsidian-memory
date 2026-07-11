---
title: "Hermes Agent (Nous Research)"
description: Nous Research 開源的自我進化 AI agent，內建學習迴路：從任務經驗自動生成並改良 skill、跨 session 累積記憶與使用者模型，跨多平台運行
created: 2026-07-08
updated: 2026-07-08
source: "https://github.com/nousresearch/hermes-agent"
published:
tags:
  - clippings
---

# Hermes Agent

> 本檔為 GitHub repo README + 官方 docs（hermes-agent.nousresearch.com）擷取彙整，作為 raw 事實來源。標語：*The agent that grows with you*。

## 定位

Nous Research 開源、MIT 授權的「自我進化」AI agent。與一般 agent 最大差異是內建 **learning loop**：從完成的任務中自動萃取 skill、使用中自我改良、週期性提醒自己持久化知識、全文檢索過往對話、跨 session 建立對使用者的理解模型。定位為 coding / personal agent，強調記憶與技能是複利成長的資產。語言組成以 Python（~82%）為主，其次 TypeScript。

## 學習迴路（差異化核心）

- **Agent-curated memory**：agent 自管記憶，靠週期性 nudge 提醒把知識持久化。
- **Autonomous skill creation**：完成複雜任務後自動把流程萃取成可重用 skill。
- **Skill self-improvement**：skill 在使用過程中自我修正。
- **Autonomous Curator**：自主策展人——評分、合併重疊、封存過時、寫每輪報告、保護 pinned skill。
- **FTS5 cross-session recall**：SQLite FTS5 全文檢索過往對話 + LLM 摘要，做跨 session 回憶。
- **Honcho 使用者建模**：AI-native 跨 session 使用者模型；dialectic 三段推理（Initial Assessment → Self-Audit → Reconciliation），depth 1–3 可調，本質是鏈式自我批判以提升建模品質。

## 架構組件

| 組件 | 作用 |
|---|---|
| Agent Core（`/agent`） | 主推理迴路 |
| Gateway（`/gateway`） | 單一 process 橋接多通訊平台 |
| Skills System（`/skills`） | 可攜、可分享的程序性記憶，相容 agentskills.io 開放標準 |
| Tools（`/tools`，60+） | 內建工具集，可組配 toolset |
| MCP Integration | 接外部 MCP server，可過濾工具存取 |
| Subagents | 隔離、可平行的子代理 |
| TUI（`/ui-tui`） | 完整終端介面：多行編輯、slash 指令自動完成、對話歷史、串流工具輸出 |
| SOUL.md | 全域人格／語氣設定 |
| Context Files | 專案級脈絡，塑形所有對話 |
| Voice Mode | 跨 CLI/Telegram/Discord/VC 的即時語音互動 |

## 記憶供應者（可插拔）

內建記憶之外，另有 8 個外部 memory provider 外掛：Honcho、OpenViking、Mem0、Hindsight、Holographic、RetainDB、ByteRover、Supermemory；提供知識圖譜、語意檢索、自動事實抽取、跨 session 使用者建模等能力。

## 訊息 Gateway（多平台）

單一 gateway process 支援 18–20+ 平台：CLI、Telegram、Discord、Slack、WhatsApp、Signal、Matrix、Mattermost、Email、SMS、Feishu/Lark、WeCom、Weixin、QQ Bot、Yuanbao、DingTalk、Microsoft Teams（外掛）、Google Chat、Home Assistant 等。

## 部署後端（Terminal Backends）

Local、Docker、SSH、Singularity、Modal（serverless、閒置近零成本）、Daytona（serverless、閒置休眠）；部分資料另提到 Vercel Sandbox。serverless 後端讓 agent 可長駐又省成本。

## Model 供應者

Model-agnostic：Nous Portal（自帶 web search / 生圖 / TTS / browser）、OpenRouter、OpenAI、任意 custom endpoint；透過 `/model` 切換，宣稱可達 300+ models。

## 安裝與常用指令

```bash
# Linux/macOS/WSL2
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
# Windows PowerShell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

安裝器內含 Python 3.11、Node.js、ripgrep、ffmpeg 與可攜 Git Bash。常用：`hermes`（互動 CLI）、`hermes model`、`hermes gateway`、`hermes setup`、`hermes skills`、`hermes claw migrate`（自 OpenClaw 匯入 persona/記憶/skill/API key）。

## 周邊生態

- **hermes-agent-self-evolution**：用 DSPy + GEPA（Genetic-Pareto Prompt Evolution）演化 skill / tool 描述 / system prompt / code；純 API、無需 GPU 訓練，每次優化約 $2–10。
- 社群 awesome list、第三方 docs repo（mudrii/hermes-agent-docs，v0.2.0）。

## 授權

MIT，open source，Nous Research 出品。
