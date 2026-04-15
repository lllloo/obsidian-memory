---
title: Agentic 終局：用 Claude Code SDK 建構自訂 Agent
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-09-22
source: https://www.youtube.com/watch?v=6wR6xblSays
---

## 為什麼需要 Custom Agents

開箱即用的工具（Claude Code、Codex CLI、Gemini CLI）是為所有人的 codebase 設計的，不是為你的。這個不匹配隨著 codebase 成長，會消耗數百小時和數百萬 token。

**Custom Agent 的價值**：讓你的算力服務你的領域、你的問題、你的邊緣案例。真正的 alpha 在這裡：在大多數工程師和 agent 無法開箱即用解決的困難特定問題上。

## Claude Code SDK 核心架構

基本結構（以 Pong Agent 為例）：

```python
# 設定 options（系統提示、模型、工具等）
options = ClaudeCodeOptions(
    system_prompt=load_system_prompt(),
    model="claude-sonnet-4-5",
    allowed_tools=[...]
)

# 建立 agent，執行 query
agent = ClaudeCodeAgent(options)
response = agent.query(user_prompt)

# 處理回應（解析 blocks）
for block in response.blocks:
    if isinstance(block, TextBlock): ...
    if isinstance(block, ToolUseBlock): ...
    if isinstance(block, ResultMessage): ...
```

## 最重要的概念：System Prompt

**System Prompt 完全覆蓋 Claude Code 的預設 system prompt**。

這意味著：
- 你建立的是一個全新的 agent，不是「改良版 Claude Code」
- System prompt 影響每一個 user prompt，所有工作都被 system prompt 乘以
- System prompt 是 custom agent 最重要的元素，沒有例外

兩個選項：
1. **完全覆寫**：`system_prompt=my_system_prompt`（建立 true custom agent）
2. **附加**（extend）：在 Claude Code 預設上面加內容（擴展 Claude Code 而非取代）

## 八個 Custom Agent 示範（從簡到繁）

### Pong Agent（最基礎）
- 僅修改 system prompt
- 無論輸入什麼，永遠回應「pong」
- 示範：system prompt 的完全控制力

### Echo Agent（加入 Custom Tool）
工具的定義方式：
```python
@tool(name="echo", description="Echo text with optional transforms")
def echo_tool(params: dict) -> str:
    # 在這裡回到確定性程式碼
    ...
    return result
```

**重要**：建立 in-memory MCP server 給 agent 使用：
```python
mcp_server = create_sdk_mcp_server([echo_tool])
options = ClaudeCodeOptions(mcp_servers=[mcp_server], ...)
```

**注意**：Claude Code SDK 預設仍包含 15+ 個工具，即使你不需要，它們仍消耗 context window。需要明確用 `allowed_tools` 控制。

**`query` vs `ClaudeSDKClient`**：
- `agent.query(prompt)`：單次問答
- `ClaudeSDKClient`：持續對話，保持對話歷史（follow-up prompts）

### Micro SDLC Agent（Multi-Agent + UI）
- Plan → Build → Review → Ship 四個 agent 接力
- 任務透過 WebSocket 串流到前端 UI
- 每個 agent 有獨立的 tool permissions（permission system）
- 拖曳任務到「Plan」欄位觸發整個 workflow
- 工作在 out-of-loop 自動完成，UI 即時顯示進度

## Core Four 在 Custom Agent 中的管理

每個 Custom Agent 都需要掌握的四個槓桿點：

| 槓桿 | 控制方式 |
|------|---------|
| **Context** | `allowed_tools`、system prompt 長度、是否 append 或 overwrite |
| **Model** | `model="claude-haiku-4-5"`（簡單任務降級省錢） |
| **Prompt** | System prompt + user prompt 的設計 |
| **Tools** | 自訂 MCP server、限制 allowed_tools |

**原則**：簡單 agent 用 Haiku（便宜快速），複雜任務用 Sonnet（強大）。

## Custom Agent 的部署情境

適合建立 custom agent 的場景：
- **Script 內嵌**：在資料處理腳本中加入 agent 判斷
- **Data stream**：對即時資料流進行 agentic 處理
- **Interactive terminal**：建立專屬工作流程的 terminal 工具
- **User interfaces**：讓 agent 在你的產品 UI 中直接操作

## 進化路徑

```
使用現有工具（Claude Code）
  → Better agents（學習 prompt + context engineering）
  → More agents（sub-agents、parallel）
  → Custom agents（Claude Code SDK）
  → 建立「建造系統的系統」
```

一旦工作變得夠專業化，out-of-the-box agent 的效率就會下降。這時候投入建造 custom agent 的 ROI 最高。
