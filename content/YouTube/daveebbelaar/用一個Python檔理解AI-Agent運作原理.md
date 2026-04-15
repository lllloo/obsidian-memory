---
title: 用一個 Python 檔理解 AI Agent 運作原理
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-09-30
source: https://www.youtube.com/watch?v=Q3Gb7Rjre3U
---

## 目標

用 200 行 Python 從零建構一個 AI Coding Agent，能夠讀取、列出、編輯本地檔案。透過逐步拆解了解所有 agentic AI 應用的底層機制。

## 專案結構

- 執行環境：UV（自動管理依賴，無需手動建 venv）
- 模型：Claude claude-sonnet-4-5（Anthropic）
- 7 個遞進腳本（01 → 07），從基礎到完整 agent

## 核心概念

### 工具（Tools）

Agent 的本質：LLM + 一組工具定義。工具是帶有 name、description、input_schema 的 JSON 規格，讓 LLM 決定何時呼叫。

```python
from pydantic import BaseModel

class ToolDefinition(BaseModel):
    name: str
    description: str
    input_schema: dict
```

三個基礎工具：
- `read_file`：輸入 path → 回傳檔案內容
- `list_files`：輸入 path → 回傳目錄清單
- `edit_file`：輸入 path、old_text、new_text → 替換內容

### Agent 類別初始化

```python
class AIAgent:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.messages = []        # 對話歷史
        self.tools = []           # 工具清單
        self._setup_tools()
```

### 工具實作（Python 端）

```python
def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()

def list_files(path: str) -> list:
    return sorted([
        f"{item} (dir)" if os.path.isdir(os.path.join(path, item)) else item
        for item in os.listdir(path)
    ])

def edit_file(path: str, old_text: str, new_text: str):
    with open(path, 'r') as f:
        content = f.read()
    content = content.replace(old_text, new_text)
    with open(path, 'w') as f:
        f.write(content)
```

## Agent 對話迴圈

```python
def chat(self, user_input: str):
    self.messages.append({"role": "user", "content": user_input})
    
    while True:
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            messages=self.messages,
            tools=self.tool_schemas
        )
        
        assistant_message = {"role": "assistant", "content": []}
        
        for block in response.content:
            if block.type == "text":
                # LLM 直接回覆文字
                assistant_message["content"].append(block)
            elif block.type == "tool_use":
                # LLM 決定使用工具
                assistant_message["content"].append(block)
                result = self.execute_tool(block.name, block.input)
                # 把工具結果加回 messages，觸發下一輪 LLM 呼叫
                self.messages.append({
                    "role": "user",
                    "content": [{"type": "tool_result", "tool_use_id": block.id, "content": result}]
                })
        
        self.messages.append(assistant_message)
        
        if response.stop_reason == "end_turn":
            break
```

**重點**：每次 tool_use 都需要兩次 LLM 呼叫：第一次決定要用哪個工具，執行後把結果送回，第二次才生成最終回覆。

## System Prompt 與個性化

```python
SYSTEM_PROMPT = """
You are a terminal-based coding assistant.
Output only plain text without markdown formatting.
Do not use asterisks in responses.
"""
```

- Cursor、Claude Code 等工具的核心差異就在 system prompt 的設計
- GitHub 上有 [system-prompts-and-models-of-ai-tools](https://github.com/) 可參考各大工具的完整 prompt

## 互動式 CLI

```python
while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye")
        break
    response = agent.chat(user_input)
    print(f"Assistant: {response}")
```

## 執行方式

```bash
# UV 會自動安裝依賴
uv run 07_main.py
```
