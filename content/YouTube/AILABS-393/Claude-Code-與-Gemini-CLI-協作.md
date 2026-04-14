---
title: Claude Code 與 Gemini CLI 協作開發工作流程
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: ""
source: https://www.youtube.com/watch?v=XdtBAm2pM-0
---

## 為什麼要把 Claude Code 和 Gemini CLI 混用

- Gemini 模型在 UI 設計和創意輸出上表現優異，尤其是給予較少指令時
- Claude Opus 整體穩定性與 tooling 生態（Claude Code）更成熟
- 兩者各有強項，卻沒有原生的協作機制

## Agent Chatter — 解決跨 Agent 溝通的工具

**Agent Chatter** 是一個聊天介面，讓不同 AI agent 即時互相協調：

- 支援 Claude Code、Gemini CLI、Codex，以及開源模型（Kimmy、Quen 等）
- 透過共享聊天頻道讓各 agent 互相傳訊、協作實作
- 可節省成本：昂貴模型做規劃，輕量模型做實作
- 開源專案，AILABS 有 fork 一份並改善了 UI

## 安裝與啟動

1. Clone repo 至本機
2. Mac/Linux 需先安裝 **tmux**（terminal multiplexer，用於管理多個 terminal session）
3. Windows 可直接執行腳本
4. 每個 agent 需要一個獨立 terminal；若跑 4 個 agent，需要 4 個 terminal 並排執行
5. 啟動後在 `localhost` 打開聊天介面，即可看到所有 agent

## 使用前準備

### 1. 先初始化框架

在啟用工具之前，先把 Next.js（或其他框架）初始化完畢，避免多 agent 同時操作造成衝突。

### 2. 設定 Permissions

每個 agent（Claude Code、Gemini CLI）需要各自的 `settings.json`，手動設好適當 permissions：

- 必要的指令（file edit、build command）不需要人工審核
- 高風險指令保留人工確認
- MCP 工具也要在設定檔中配置，否則每次都需要手動批准

### 3. agents.mmd 共同指令檔

Claude 使用 `CLAUDE.md`，Gemini 使用 `gemini.md`，兩者互不讀取對方的指令檔。

解法：建立 `agents.mmd`，並在兩者的指令中加入規則，讓雙方都以 `agents.mmd` 為主要指引。

### 4. Planning 模板

準備 PRD、backend spec、UI spec 等模板，讓 agent 填入後保持結構一致，避免產出多餘內容。

### 5. 命名與角色分配

可以幫每個 agent 命名並分配角色（如 Gemini 命名為 UI Designer），agent 會根據設定的 persona 運作。

## Loop Guard 設定

預設 loop guard = 4，代表 agent 間最多互傳 4 次訊息就會暫停並等待人工輸入：

- 可以調高，讓 agent 更長時間自主協調
- 觸發後發送 `continue` 繼續

## 實際工作流程

```
1. 建立 agents.mmd + planning 模板
2. 在聊天介面建立不同頻道（前端、後端）
3. 提供 app 想法 → Planner agent 產出計畫並通知你審核
4. 批准後，Planner 自動通知 Gemini UI Designer 實作 UI spec
5. Planner 與 UI Designer 來回協調實作細節
6. Builder agent 獲得前端工程師解鎖，開始前端實作
7. 後端頻道同步讓 Planner 和 Builder 驗證 backend spec
8. 使用 Planner mode（三段式）：Presenter → Challenger → Synthesizer，交叉驗證計畫
9. 最終由 Planner 作為 orchestrator，並行派遣 UI Designer 和 Builder 實作
```

## 注意事項

- Agent 之間可能覆蓋彼此的檔案，尤其是前後端同時修改相同檔案時
- 建議在複雜場景下讓各 agent 使用獨立的 work tree，再由一個 agent 統一 merge 和 review
- 此工具透過 MCP 讓 Claude 發送回覆並讀取聊天記錄，實現雙向溝通
