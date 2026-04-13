---
title: Pi Coding Agent：唯一真正的 Claude Code 競爭者
tags:
  - youtube
  - claude-code
  - pi-agent
  - agentic-engineering
created: 2026-04-13
updated: 2026-04-13
published: 2026-02-23
source: https://www.youtube.com/watch?v=f8cfH5XX-XU
---

## 為何 Pi 是唯一的競爭者

Claude Code 已成為主流工具，但主流工具有主流的限制。Pi Agent 的反擊策略：**開源 + 完全可客製化**。

作者策略：80% Claude Code + 20% Pi（用於深度實驗性 agentic coding）。

## 設計哲學對比

| 面向 | Claude Code | Pi Agent |
|------|-------------|----------|
| 開源 | 否 | 是（Mario Zechner 開發） |
| 預設體驗 | 豐富 out-of-box defaults | 最小化（200 token system prompt） |
| 安全模式 | 5 種確認模式 | 無（預設 YOLO mode） |
| 模型選擇 | 優先 Anthropic 模型 | 任何模型 |
| 可觀測性 | 漸趨抽象 | 完全透明 |
| 版本固定 | 不可 | 可 fork/pin |
| Sub-agent 支援 | 原生支援 | 需自行建構 |
| 企業功能 | 完整 | 幾乎沒有 |

Pi 是 openclaw（前身 maltbot/clawbot）的底層引擎。

## 三層客製化能力

### Tier 1：基礎 Harness 客製化

透過 `pi -e <extension>` 堆疊 extensions：

- **Pure Focus**：移除所有 UI，只剩輸入框，保持心流
- **Minimal**：自訂 footer（顯示 model、context window）
- **Cross Agent**：指定載入 skills、commands、agents 的路徑（作者載入 41 個 global skills）
- **Purpose Gate**：啟動時詢問 agent 目的，附加至 system prompt，全局導引行為
- **Tool Counter**：footer 即時顯示工具呼叫統計
- **Theme Cycler**：Ctrl+X 切換 13 個客製化主題（含 Synth Wave 84）

```bash
# 堆疊多個 extensions
pi -e pure-focus -e tool-counter -e theme-cycler
```

### Tier 2：Multi-Agent Orchestration

Pi 沒有原生 sub-agent 支援，但可完全自建：

- **Sub-agent Widget**：用 `/sub <prompt>` 觸發，結果持久顯示在 UI
- **Agent Team**：定義 scout、planner、builder、reviewer、documenter 等角色
  - 用 YAML 設定不同 team 組合，`/agent-team` 切換
- **Agent Chain（Pipeline）**：三個 scout agent 依序執行，前一個的輸出是下一個的輸入

**Till Done 擴充功能**：
- 所有工具呼叫必須先在 task list 建立待辦項目才能執行
- 任務未完成時持續提示 agent 繼續工作
- 用 hooks 攔截 `ls` 等指令，強制先建 task 再執行
- 即使用較弱的模型（Haiku），透過控制 harness 也能提升結果品質

```typescript
// extension 結構（TypeScript）
// 範例：till-done extension（~700 行）
registerCommand('till-done', ...)
registerTool(agent => ...)
onInputHook(...)
onToolCallHook(...)
onAgentEndHook(...)
```

### Tier 3：Meta-Agent（建構 agent 的 agent）

將 Pi 的各項能力拆分為 8 個**子領域專家 agent**，由主 orchestrator agent 根據需求組合呼叫：

- 主 agent 問 8 個專家，並行執行
- 主 agent 根據結果自動建構新的 Pi extension

## 功能比較總表

| 功能 | Claude Code | Pi Agent |
|------|-------------|----------|
| System Prompt 自訂 | 有限 | 完全覆寫 |
| Hooks 數量 | 主要 hooks | 25+ hooks |
| Footer/Status Line | 可改 | 完全客製 |
| 工具註冊（in-loop） | 需 skill/MCP | 直接在 extension 註冊 |
| 多模型支援 | Anthropic 優先 | 任何模型 |
| Sub-agent | 原生 Task tool | 需自建 |
| Agent Teams | 原生 | 需自建 |
| Agent Chains/Pipelines | 無 | 需自建 |
| MCP 支援 | 有 | 無（改用 CLI script） |
| 企業採用 | 完整 | 僅實驗用 |
| Key Bindings | 有限 | 完全自訂 |
| 權限模式 | 多種 | 只有 YOLO |

## 選擇策略

**用 Pi 的情況：**
- 需要完全控制 agent harness
- 想用任何模型
- 要對抗 Claude Code lock-in 風險
- 已掌握所有 out-of-box 功能，想突破極限
- 建構 Outloop agentic 系統

**用 Claude Code 的情況：**
- 企業環境
- 需要穩定、開箱即用的體驗
- 團隊規模大

## 核心理念

> 「每個工程師都受其工具所限。要超越別人，就不能用別人都在用的工具。」

Specialization 不止於 model 和 prompt，要延伸到 **agent harness 本身**。
