---
title: RAW Agentic Coding：從零建立 Agent Skill
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-16
published: 2025-12-08
source: https://www.youtube.com/watch?v=X2ciJedw2vU
parent: "[[01.index]]"
---

## 核心方法論

建立任何 skill 之前，先想、先計畫，再讓 agent 實作。用紙筆定義：
- **Purpose**：這個 skill 解決什麼問題？
- **Problem**：現有工作流的痛點？
- **Solution**：預期的輸出物是什麼？

> 「Begin with the end in mind」—— 定義清楚 end state，agent 才能正確建造。

## 本影片範例：Fork Terminal Skill

**目的**：從現有 agent session 中 fork 出新 terminal，帶著 context summary 啟動新 agent（Claude Code、Gemini CLI、Codex CLI）。

**使用情境**：
- 轉移 context 到新 agent，避免原 session context 耗盡
- 並行跑多個 agentic coding tools
- 從現有工作中 offload 子任務

## Skill 目錄結構

```
.claude/skills/fork-terminal/
  skill.md              # 核心：漸進式披露 skill 如何運作
  tools/
    fork-terminal.py    # Python 工具腳本（用 uv 執行）
  prompts/
    fork-summary-user-prompt.md  # 對話摘要模板
  cookbook/
    cli-command.md      # 一般 CLI 指令 fork 說明
    gemini-cli.md       # Gemini CLI 特定指引
    codex-cli.md        # Codex CLI 特定指引
    claude-code.md      # Claude Code 特定指引
```

## skill.md 設計原則

- 是「pivot file」，所有其他 agent 文件圍繞它旋轉
- 包含：purpose、工具清單、條件判斷邏輯（何時用 fork summary）
- 用 `## Variables` 定義 static 變數（避免重複寫）
- 用 `### Fork Summary User Prompts` 說明何時及如何傳遞對話摘要

## Fork Summary User Prompt 模板

```yaml
# 格式：base agent 填入後傳給 fork agent
history:
  - user_prompt: "..."
    agent_response: "..."
  - user_prompt: "..."
    agent_response: "..."
summarized_user_prompt:
  context: "This is the history of the conversation..."
  next_request: "<填入下一個使用者請求>"
  response_summary: "..."
```

關鍵指示（在 skill.md 中）：
- 不要直接更新此檔案，讀取後用來建構新 prompt
- `IMPORTANT`: 只傳遞給 agentic coding tools（需啟用工具）

## Skill 建立流程（實戰）

```bash
mkdir fork-terminal-skill && cd fork-terminal-skill
git init --branch main
claude code  # 啟動 in-loop 模式

# 在 Claude Code 中：
# 1. 貼上目錄結構規劃
# 2. "build, use empty files"
# 3. 逐步填入各檔案內容（skill.md → tools → prompts → cookbook）
```

## 三種 Fork 使用情境

### 情境 1：跑原始 CLI 指令
```
fork terminal ffmpeg --input ...
```

### 情境 2：啟動新 agentic coding tool
```
fork session codex-cli summarize work done, then write 20-line readme
```

### 情境 3：帶摘要 fork（重要）
```
fork terminal use claude-code to XYZ, summarize work so far, include summary
```

## 測試與調整

- 用 `esc` + `↑` 在 Claude Code 中 rewind 歷史記錄，重試失敗指令
- 看 skill 是否正確讀取 `fork-summary-user-prompt.md` 並傳入新 agent
- 確認新 agent 收到 YAML 格式的 prompt history

## 核心結論

Skills 重要是因為：**可重用的 prompts + 可重用的 code = 解決特定問題的一致、可部署工具**。

一切最終仍回歸：**Core Four = Context + Model + Prompt + Tools**。
