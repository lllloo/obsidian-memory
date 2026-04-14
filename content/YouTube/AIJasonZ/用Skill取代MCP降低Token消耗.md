---
title: 用 Skill 取代 MCP 降低 Token 消耗
tags:
  - youtube
  - claude-code
  - mcp
  - ai-agent
created: 2026-04-14
updated: 2026-04-14
published: 2026-01-24
source: https://www.youtube.com/watch?v=fG95XsBO5U4
---

## 問題：MCP 的 Token 開銷

每個 MCP server 都會把所有工具 schema 載入 context window，不管當前任務用不用得到，持續消耗 token。

## Skill + CLI 方案

### 概念

Skill 只在被召喚時載入，且每個 skill 只消耗 10-50 token（只有 title + description）。實際執行時，agent 用 bash 指令呼叫 CLI 工具，結果直接回傳。

換算：原來 MCP 工具佔的 token 量可放約 4,000 個 skill，遠超實際需求。

### Manus 的做法（參考）

- 基礎工具（read/write/edit）永遠載入
- 其他工具包成 CLI，只有一條 prompt 說明可用指令
- Agent 需要時直接 `run <command>`

## MCPorter：把 MCP 轉成 CLI

開源工具，讓 agent 透過 command line 執行任何 MCP server：

```bash
# 安裝
npx @mcporter/cli context7 resolve-library-id --libraryName="react"
```

使用流程：
1. 不在 Claude Code 設定 MCP server
2. 改建立對應的 `skill.md`，描述何時使用、有哪些指令
3. Agent 自動載入 skill prompt 並執行 CLI

## Agent Browser 範例（Browser MCP vs CLI 比較）

| | Chrome MCP | Agent Browser CLI |
|--|--|--|
| 工具數量 | 多（click/drag/type 等獨立工具） | 整合為 CLI 指令 |
| Context 佔用 | ~2% context window | 更小 |
| Token 剩餘 | 87,000 | 117,000 |
| Token 節省 | — | 約 70% |

## 自動化新增 MCP Skill

建立一個 `add-new-mcp` skill：
1. Agent 接到新 MCP 描述後自動執行
2. 安裝並測試 MCP server
3. 建立對應 skill.md（列出所有可用函式）

之後新增任何 MCP 都只需告訴 agent 一句話。

## Super Design CLI 範例

```bash
npm install -g @superdesign/cli
superdesign login
# 加入 skill
npx skills @superdesign.dev/superdesign-skill
```

用 `/superdesign` 呼叫 skill，agent contextual 載入並透過 CLI 執行設計操作。
