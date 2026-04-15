---
title: Claude Code 2.0 Agentic 編碼：其他工具根本沒在競爭
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-10-06
source: https://www.youtube.com/watch?v=nGhsgdQplHw
---

## 主要示範：Claude Agent SDK 遷移

**任務**：將舊版 Claude Code SDK 程式碼遷移至 Claude Agent SDK 新語法，同時讓 agent device 建構 OpenAI Realtime API 原型。

**兩個平行工作流程**：
1. **In-loop（本機）**：用 `/scout-plan-build` workflow 遷移 SDK 語法
2. **Out-loop（Agent Device）**：`/afk-agents` 交辦任務，每 60 秒回報進度

## Scout-Plan-Build 三步驟 Workflow

這是一個**組合式 agentic prompt**，用 Claude Code 2.0 的「slash command 呼叫 slash command」功能鏈接三個步驟：

### Step 1：Scout（偵察）
- 用 4 個並行 sub-agent 搜尋需要修改的檔案
- 使用**多個模型**取得多角度觀點：Gemini Flash、CodeX、Gemini Flash Preview、CodeX
- 輸出：`relevant_files.md`，包含每個檔案的 offset 和需讀取的字元數

### Step 2：Plan（規劃）
- Planner 讀入 Scout 的輸出（relevant files）和文件 URL
- 抓取外部文件到本地（供後續 pipeline 共用）
- 輸出：詳細的修改計畫

### Step 3：Build（建構）
- 高階 prompt，把 plan 傳入 build prompt
- 執行所有修改，測試，驗證

**優點**：把「搜尋檔案」從 planner 的工作分離出去，讓 planner 的 context window 保持乾淨。

## Claude Code 2.0 新功能與注意事項

**Slash Command 可以呼叫 Slash Command**：
```
/scout-plan-build prompt="migrate to Claude Agent SDK" docs="https://..."
```
內部可以直接寫 `/scout`、`/plan`、`/build`，Claude Code 會依序執行。

**Auto-compact 功能（注意！）**：
- 預設 `auto-compact: true`，會在 context 滿之前自動消耗 22% context
- 建議關閉：執行 `/config` → 設定 `auto-compact: false`
- 關閉後恢復 91% 可用 context

**Output Style 截斷問題**：
- Claude Code 2.0 預設截斷大量輸出，設計方向偏向一般使用者
- 解決：設定自訂 output style（Observable Tools Diff TTS）顯示完整 tool calls、diffs、和語音摘要

## R&D Framework（Reduce & Delegate）

管理 context window 的唯一兩種方式：
- **Reduce**：減少不必要的 context
- **Delegate**：把工作分派給 sub-agent，移出 primary agent 的 context window

Scout workflow 就是 Delegate 的實踐：搜尋工作不需要 planner 的全能力，用便宜快速的模型完成。

## Agent Device 概念

**什麼是 Agent Device**：
- 一台專門執行 agent 任務的機器（如 M4 Mac Mini）
- 接受任務 → 自主執行 → 定期回報（每 60 秒）
- 完整 log 記錄，可追溯整個執行過程

**操作方式**：
```bash
/afk-agents prompt="build three OpenAI agent SDK prototypes" docs="<url>"
```

Agent device 收到後：Plan → Build → Ship（包含 git push）全部自動完成。

## 核心觀念

**為什麼 Claude Code 比 Codex CLI / Gemini CLI 更強**：
- 不只是複製功能，而是建立在自家 agent harness 上
- 強大 prompt 在 Claude Code 的執行環境中有高度遵從性（adherence）
- 可以組合 slash commands、sub-agents、hooks、output styles 成複雜 workflow

**「建造建造系統的系統」**：
- 投資 reusable prompts
- 讓 agent 建構程式碼，工程師設計 agentic workflow
- 兩個 prompt 就能啟動整個開發流程

**Context Window 仍是根本限制**：
- 即使有 delegation，primary agent 本次仍消耗 51% context
- 解決方案：AI Developer Workflows（ADW），結合舊世界的程式碼和新世界的 agent
