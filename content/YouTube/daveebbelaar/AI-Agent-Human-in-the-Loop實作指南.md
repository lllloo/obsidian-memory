---
title: 如何為 AI Agent 建構 Human-in-the-Loop（實作指南）
tags:
  - youtube
  - ai-agent
  - human-in-the-loop
  - python
created: 2026-04-13
updated: 2026-04-13
published: 2026-01-19
source: https://www.youtube.com/watch?v=7GOxUgVTz3s
---

## Human-in-the-Loop 的核心概念

Human-in-the-Loop（HITL）是在 agentic 應用中，在關鍵節點暫停流程、等待人類確認或反饋再繼續的機制。

適用場景：
- 銀行轉帳超過一定金額
- LLM 能自動處理 50% 的案例，其餘 50% 仍需人工介入
- 任何需要在上線前降低風險的 LLM 應用

兩種技術方法：
- **LLM 作為 Router**：使用結構化輸出決定行動，再以 if/else 邏輯過濾需要確認的步驟
- **Tool Calling**：LLM 以 while 迴圈決定呼叫哪個工具，在執行工具前攔截並檢查是否需要確認

## Python 實作基礎

### Router 方式（結構化輸出）

```python
from pydantic import BaseModel, model_validator
from typing import Literal

class Action(BaseModel):
    action_type: Literal["check_balance", "transfer", "deposit"]
    amount: float | None = None
    requires_confirmation: bool = False

    @model_validator(mode="after")
    def enforce_confirmation(self):
        # 強制規則：超過 100 的轉帳必須確認
        if self.action_type == "transfer" and self.amount and self.amount > 100:
            self.requires_confirmation = True
        return self
```

重點：將「需要確認」的判斷邏輯移到 Pydantic validator，而非依賴 LLM 自行判斷，可提升可靠性。

執行流程：
1. LLM 回傳 action plan（多個 Action 組成的清單）
2. 遍歷 action plan，遇到 `requires_confirmation=True` 時暫停
3. 使用 `input()` 等待使用者輸入 Y/N
4. 依結果執行或取消

### Tool Calling 方式

```python
while True:
    response = client.responses.create(...)
    if not response.tool_calls:
        return response.text  # 無工具呼叫，直接回傳
    
    for tool_call in response.tool_calls:
        if tool_call.name == "transfer" and tool_call.args["amount"] > 100:
            # 攔截，等待確認
            approval = input("Confirm? (Y/N): ")
            if approval != "Y":
                continue
        # 執行工具
        execute_tool(tool_call)
```

## 生產環境模式

### 模式一：SSE Streaming（即時互動應用）

適用：聊天機器人、AI 助手等使用者主動等待的場景。

完整流程：
1. 使用者透過前端送出請求 → POST `/chat`
2. API 層轉發至 Agent 處理
3. Agent 發現需要確認 → 將**狀態存入資料庫**（包含訊息歷史、待執行動作、所有參數）
4. Agent 透過 API 回傳「需要確認」訊號 → 前端顯示 Approve/Deny 按鈕
5. **SSE 連線關閉**（已儲存狀態，不需保持連線）
6. 使用者點擊 Approve → POST `/execute?approved=true&state_id=xxx`
7. API 從資料庫載入狀態 → Resume → 執行動作 → Stream 結果回前端

關鍵：連線在等待確認時關閉，避免因網路逾時或使用者長時間不回應而丟失狀態。

### 模式二：Async Process（後端批次工作流）

適用：由 API、Webhook、Queue 觸發的後端流程，無使用者主動等待。

完整流程：
1. 後端事件觸發流程（如：發票進來）
2. Worker 執行 Agent
3. Agent 發現需要確認 → 儲存狀態 → 流程停止
4. **發送通知**（Email 或 Slack）給負責人，附帶 Approve/Deny 按鈕
5. 負責人點擊 Approve → 呼叫 API endpoint
6. 載入儲存的狀態 → Resume → 執行 → 發送完成通知

與模式一的差異：沒有前端 SSE 串流，改以通知服務（Slack/Email）銜接人工決策。

## 關鍵設計原則

1. **Deferred Execution（延遲執行）**：需要確認時，儲存狀態而非執行。永遠不要在等待確認期間保持執行中的連線或進程。

2. **State Serialization（狀態序列化）**：持久化儲存 Agent 的完整上下文，包含：
   - 訊息歷史（message history）
   - 待執行動作（pending actions）
   - 工具參數（tool call parameters）

3. **Stateless Resume（無狀態恢復）**：每次恢復都從儲存中重新載入狀態，不依賴記憶體中的任何資料。即使使用者一週後才按下確認，系統依然能正確恢復。
