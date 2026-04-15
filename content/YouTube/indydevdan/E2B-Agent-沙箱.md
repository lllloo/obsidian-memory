---
title: E2B Agent Sandboxes：部署 Claude Agent 的專屬空間
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-11-17
source: https://www.youtube.com/watch?v=1ECn5zrVUB4
---

## 核心概念：Agent Sandbox 是什麼

Agent Sandbox 是給 AI agent 使用的**隔離執行環境**。當你使用 Manus、ChatGPT、Claude 的程式碼執行功能時，背後就是這種技術。E2B 是目前最佳的實作工具，同類工具還有 Modal。

三大優勢：
- **Isolation（隔離）**：每個 agent 有完全獨立的環境，安全、可刪除、ephemeral
- **Scale（規模）**：同時啟動多個 sandbox，並行執行大量 agent
- **Agency（自主性）**：agent 在自己的環境中有完整控制權，操作自己的 file system、工具、config

## Best of N 模式

一個問題用多個 agent 並行解決，取最佳結果：

- 建立一個 orchestrator agent，教它如何啟動 sandbox
- 同一個 prompt 執行多份（例如 3 forks × 3 prompts = 9 個 sandbox）
- 每個 agent 獨立執行，因 LLM 非確定性，每次結果都不同
- 事後比較各版本，挑選最佳解

範例指令結構：
```bash
uv run ox <github_url> --branch <branch_name> --model <model> --forks <n> --prompt "<prompt>"
```

## 架構設計

**三層架構**（類似 CLI → MCP → Skill）：
1. **Sandbox CLI**（`ox`）：管理 sandbox 的底層工具，wrap E2B SDK
2. **MCP Server**：包裝 CLI，讓任何 Claude Code agent 都能透過 MCP 呼叫
3. **Orchestrator Agent**：透過 MCP 啟動並管理多個 sandbox agent

**關鍵 agent 設定**：
- 使用 Claude Code SDK 建立 custom agent
- `allowedTools` / `disallowedTools` 嚴格定義 agent 可用工具
- 自訂 system prompt 完全覆蓋 Claude Code 預設 system prompt
- 每個 sandbox 有 lifetime（例：1800 秒 = 30 分鐘），到期自動關閉

**E2B SDK 核心操作**：
```
init sandbox → create → connect → execute → kill sandbox
```

## 工作流程示範

1. Orchestrator agent 讀取需求（例：Reddit 的 landing page 批評貼文）
2. 用 agentic prompt 將需求轉為具體 prompt variants
3. 對每個 prompt variant 啟動 3 個 sandbox（`--forks 3`）
4. 每個 sandbox 內的 agent：clone repo → 執行修改 → 啟動 server → 回傳 public URL
5. Orchestrator 收集所有 PR 與 preview URL，開啟瀏覽器供人工審核
6. 選出最佳版本，merge PR，部署

## 取捨與限制

- **成本**：每個 sandbox 需要獨立 API key 呼叫，無法使用 Claude Code Max/Pro 訂閱
- **工程成本**：需要自行建置 sandbox 工具鏈
- **Review 瓶頸**：大量並行輸出需要人工審核，planning 與 reviewing 成為主要工作
- **適合場景**：RL 訓練、isolated 快速環境、資料分析；UI 小改動有點 overkill

## 適用位置

Agentic Scaling Framework 的最頂層：
```
單一 agent → 更好的 agent → 更多 agent → custom agent → orchestrator + sandbox
```
