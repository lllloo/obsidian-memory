---
title: Master Index
created: 2026-04-15
updated: 2026-04-15
tags:
  - index
---

## 資料夾索引

```
content/
├── Cards/         — 快速筆記（CSS、Docker、設計工具等）
├── Clippings/     — 網頁剪貼
├── Inbox/         — 日記（格式：YYYY-MM-DD.md）
├── Templates/     — 模板（card.md、daily.md）
├── Topics/        — 主題 MOC，3 個子目錄
│   ├── Claude-Code/   — Skills、Agent Packages、Hooks、GAN Harness
│   ├── Obsidian/      — CLI 整合、Skills、Quartz 部署
│   └── 切版/          — Pencil 讀取規則、Flexbox、Border 規則
└── YouTube/       — 390 篇影片摘要，13 個頻道
    ├── AIJasonZ/              — Cursor、Gemini、Claude 設計工作流
    ├── AILABS-393/            — Claude Code 進階技巧、OpenClaw、RAG
    ├── Chase-H-AI/            — Claude Code 實戰、RAG、Obsidian 整合
    ├── DavidOndrej/           — AI Agent、AutoResearch
    ├── EricWTech/             — Claude Code 自動化、Skill 系統
    ├── Fireship/              — 科技新聞、開源工具
    ├── ModernSoftwareEngineeringYT/ — TDD、Clean Code、軟體工程文化
    ├── SkillLeapAI/           — Claude、Google AI 工具介紹
    ├── aiadvantage/           — AI 工具週報、ChatGPT/Claude 新功能
    ├── daveebbelaar/          — Python、AI Agent 工程、LLM Evals
    ├── indydevdan/            — Agentic 工程、Claude Code SDK
    ├── mreflow/               — AI 週報、科技趨勢分析
    └── t3dotgg/               — 開源、OpenAI、Anthropic 時事評論
```

## Tag 查詢指南

共 78 個 tag，主要分布：

| 主題 | Tags | 建議搜尋位置 |
|------|------|------------|
| Claude Code 實作 | `claude-code` (59篇) | YouTube/ |
| AI Agent 架構 | `ai-agent` `multi-agent` `agentic-engineering` `agent-harness` | 全 vault |
| RAG / 知識庫 | `rag` `memory` | YouTube/ |
| 測試 / 軟工 | `software-engineering` `playwright` `pydantic` | YouTube/ |
| Obsidian 操作 | `obsidian` `cli` | Topics/ + Cards/ |
| 前端 / CSS | `frontend` `css` `flexbox` `ui-design` | Cards/ + YouTube/ |
| Python / 工程 | `python` `api` `docker` | YouTube/ + Cards/ |

## 查詢策略

- **主題明確** → 先查 `Topics/` 對應子目錄
- **找影片摘要** → 依頻道特性選 `YouTube/<頻道>/`
- **跨主題** → Grep 搜尋 tag（`tags:.*<tag名稱>`）
