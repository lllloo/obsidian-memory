---
title: Library Meta-Skill：跨裝置分發私有 Skills、Agents 與 Prompts
tags:
  - youtube
  - claude-code
  - agent-harness
  - skills
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-16
source: https://www.youtube.com/watch?v=_vpNQ6IwP9w
parent: "[[01.index]]"
---

## 問題定義

工程師在 10+ 個 codebase 工作時，會遭遇：
- Skills / Agents / Prompts 四散各處
- 跨 repo 產生大量重複與失同步
- 與隊友和 agent 裝置分享時沒有統一機制
- 私有 agentic 工具沒有版本控制

## 解決方案：Library Meta-Skill

一個 meta-skill（skills.md），搭配一個 YAML 參考清單（library.yaml），做為所有私有 agentic 工具的單一真相來源。

**核心概念**：Library 不存儲實際程式碼，只存 Git repo 或本地路徑的**參考（reference）**。

## Library 檔案結構

```yaml
# library.yaml
defaults:
  skills: ~/.claude/skills
  agents: ~/.claude/agents
  commands: ~/.claude/commands

catalog:
  skills:
    - name: meta-skill
      source: git@github.com:indydevdan/meta-agentics.git
      path: skills/meta-skill.md

    - name: deploy
      source: git@github.com:your-org/private-agentics.git
      path: skills/deploy.md

  agents:
    - name: meta-agent
      source: git@github.com:indydevdan/meta-agentics.git
      path: agents/meta-agent.md

  prompts:
    - name: meta-prompt
      source: git@github.com:indydevdan/meta-agentics.git
      path: prompts/meta-prompt.md
```

## Library Skill API（命令列表）

| 指令 | 功能 |
|------|------|
| `/library list` | 列出所有參考，並 git pull 取得最新版 |
| `/library add <items> from <source>` | 新增項目到 library.yaml |
| `/library use <pattern> install [locally\|globally]` | 從 library clone 安裝到指定目錄 |
| `/library push <name>` | 將本地修改 push 回原 repo |
| `/library sync` | 同步所有項目到最新版本 |
| `/library search <query>` | 搜尋 catalog |

## 典型工作流程

### 1. 新增 Skills 到 Library

```bash
# 在含有新 skills 的 repo 中執行
/library add meta-agent meta-prime meta-prompt meta-skill from GitHub URL
```

系統會：
1. git pull 取得最新 library.yaml
2. 搜尋本地對應的 skill 檔案
3. 新增參考到 library.yaml（不移動檔案）

### 2. 在新裝置安裝 Skills

```bash
# 先 clone library repo
git clone git@github.com:you/your-library.git ~/.claude/library

# 啟動 agent 後執行
/library use meta-* install globally
```

### 3. 更新 Skill 後同步

```bash
# 修改 skill 後
/library push meta-prompt
```

## 安裝到 Mac Mini Agent 裝置的示範

1. 在 agent 裝置終端機：`git clone <library-repo> ~/.claude/library`
2. 啟動 Pi coding agent，執行：`/library use meta-* install globally`
3. Pi 自動顯示載入的 skills 從 1 個增加到 5 個
4. 在任何目錄都可使用 `/meta-prompt`、`/meta-agent` 等

## Meta-Agentics 四件組

| 項目 | 用途 |
|------|------|
| `meta-prompt` | 按照固定格式快速產生新 prompt（約 800 行模板）|
| `meta-skill` | 建立新 skill 的 skill |
| `meta-agent` | 建立新 agent 的 skill |
| `meta-prime` | 主指令 slash command |

格式模板（meta-prompt 產出結構）：
```markdown
## Purpose
## Variables
## Instructions
## Workflow
## Examples
```

## 設計原則

- **純 Agent 應用**：整個 Library 只是 `skills.md` + `library.yaml`，零程式碼
- **Private-first**：私有 Git repo 存放真正有價值的專屬工具，不公開
- **Reference-based**：Library 只存指標，不複製代碼，確保同步
- **Agent-operable**：整個工作流程可由 agent 自動執行

## 適用規模判斷

| 情況 | 建議 |
|------|------|
| 1-2 個 codebase | 不需要，直接用 Claude Code plugins 即可 |
| 10+ 個 codebase | 強烈建議建立 Library |
| 多台裝置或 agent 裝置 | 必要 |
| 有工程師團隊共用 agentics | 必要 |

## Agentic 路徑

Base Agent → Better Agent → More Agents → Custom Agents → Orchestrator Agent

Library Meta-Skill 在「More Agents」和「Custom Agents」階段開始變得必要。
