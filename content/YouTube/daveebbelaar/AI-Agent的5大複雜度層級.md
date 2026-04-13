---
title: AI Agent 的 5 大複雜度層級
tags:
  - youtube
  - ai-agent
  - software-architecture
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-13
source: https://www.youtube.com/watch?v=BaXTos7B1vY
---

## 核心問題

在開始建構 AI 系統時，最關鍵的決策是：**你需要多高的複雜度？**

簡單的 LLM call 或工作流程，有時就足以解決問題，不需要完整的 agent 系統。以下 5 個層級幫助你做出正確選擇。

## 層級 1：Augmented LLM

最基本的形式：單一 LLM API call，配合結構化輸出（Structured Output）。

```python
# 單一 API call + 結構化輸出
response = client.messages.create(...)
```

使用時機：任務明確、輸入輸出已知、不需要動態決策。

## 層級 2：Prompt Chaining 與路由（DAGs）

過去 2 年 Dave 最常推薦的模式：**有向無環圖（Directed Acyclic Graph, DAG）**。

核心概念：
1. 對輸入資料分類（LLM 負責）
2. 依分類走不同的確定性邏輯（if-else）

範例：客服工單進來 → LLM 分類（帳單問題、技術問題、一般問題）→ 各分類走不同的處理流程

**優點**：可靠、可測試、易維護  
**挑戰**：隨著系統成長，DAG 可能變成複雜的「弗蘭肯斯坦圖」（特別是多人開發、多分支時），除錯困難。

這仍然是 B2B 生產環境中最主流、最可靠的自動化方式。

## 層級 3：LLM with Tools（工具呼叫）

在 DAG 的邊界節點（Edge Nodes）引入工具呼叫，讓 LLM 動態決策：

- 查詢資料庫
- 查找政策文件
- LLM 決定呼叫哪些工具，可在 loop 中多次呼叫

這才算是真正的「Agentic」行為：代理在 loop 中對工具進行推理。

**生產案例**（Langfuse 截圖）：客服自動化系統，已運行 1.5 年。在分析工單的邊界節點，代理配備了以下工具：
- `request_missing_info`：向客戶索取缺少的資訊
- `get_product_rules`：查詢退換貨政策知識庫

最佳實踐：**不是非此即彼**，最好的系統結合兩者——儘量先用 DAG 分類路由，只在最後的邊界節點才用工具呼叫。

## 層級 4：Agent Harness

賦予代理完整的運行時環境（Runtime）：

- Bash 執行
- 檔案系統存取
- 網路搜尋
- MCP 伺服器整合
- 外部 API

技術選項：
- **Claude Agent SDK**（`pip install claude-agent-sdk`）：用 Python 啟動類似 Claude Code 的環境
- PydanticAI、LangGraph
- TypeScript：pimono（OpenClaw 的底層）

```python
# Claude Agent SDK 範例（簡化）
agent = ClaudeAgent(
    system_prompt="...",
    allowed_tools=["read", "glob", "grep"],
    mcp_servers=[...],
    max_budget=10.0,  # 重要：設定預算上限
    # 可加 sub_agents、env_vars 等
)
result = agent.run("處理這個客服請求")
```

執行過程範例：
```
Agent: 讓我看看有哪些檔案... (glob)
Agent: 讀取退款確認文件... (read)
Agent: 決定需要的行動... (生成結果)
```

**重要警告**：這個層級非常強大但也危險。在生產環境中要：
- 限制允許的工具（不要開放寫入、不要開放網路爬行）
- 放入容器隔離
- 設定 `max_budget` 和 `max_turns`

## 層級 5：Multi-Agent Orchestration

多個代理協同工作，每個子代理擁有**獨立的 context window**：

```python
# Claude Agent SDK 的多代理設定
orchestrator = ClaudeAgent(
    agents=[
        SubAgent(model="claude-sonnet", tools=["search"], ...),
        SubAgent(model="claude-opus", tools=["write"], ...),
    ],
    ...
)
```

**為何需要獨立 context？**  
長任務中，代理搜尋知識庫後可能用掉 70–80% 的 context，之後繼續工作會受限。子代理各自有獨立 context，完成後回報給 orchestrator，orchestrator 的 context 保持乾淨。

目前狀態：高度實驗性，不可靠，成本昂貴。Datalumina 目前不在生產環境使用。

## 五個層級總覽

| 層級 | 名稱 | 可靠性 | 成本/延遲 | 適用場景 |
|------|------|--------|-----------|---------|
| 1 | Augmented LLM | 最高 | 最低 | 簡單、確定性任務 |
| 2 | DAG（路由） | 高 | 低 | 可分類的業務流程自動化 |
| 3 | LLM + Tools | 中高 | 中 | 需要動態查詢的邊界節點 |
| 4 | Agent Harness | 中 | 高 | 編程代理、複雜單次任務 |
| 5 | Multi-Agent | 實驗性 | 最高 | 長時間、大規模研究任務 |

## 工程師的實踐原則

- **永遠用最簡單的層級解決問題**
- 各層級可以組合使用，不是非此即彼
- DAG + 邊界節點工具呼叫 = 目前生產環境的最佳實踐
- 理解這 5 個層級，有助於看穿任何新 AI 工具的本質（例如 OpenClaw = agent harness + WhatsApp + 技能檔案）

## 理解 AI 工具的底層

當新工具引發炒作時（例如 OpenClaw），能夠拆解它：

> "這不過是另一個 agent harness：LLM + 工具 + 技能 markdown 檔案 + prompts"

這樣的心智模型讓你不會被每週的 AI 熱點帶跑，始終保持冷靜的工程師視角。
