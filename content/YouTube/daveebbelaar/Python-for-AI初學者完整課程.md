---
title: Python for AI 初學者完整課程
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-10-21
source: https://www.youtube.com/watch?v=ygXn5nV5qFc
---

## 課程定位

專為想做 AI 應用的人設計，聚焦實用，去掉一般 Python 課程中對 AI 開發沒用的部分。從安裝到建構 AI 聊天助理，一次到位。課程使用 Cursor/VS Code，搭配 UV 管理依賴。

## 環境設定

### 安裝與工具

- Python 安裝：python.org/downloads，Windows 需勾選「Add to PATH」
- 編輯器：VS Code + Python extension、Pylance、Jupyter
- 依賴管理：UV（比 pip 快，推薦取代 pip）
- 虛擬環境：`python -m venv .venv`，或用 UV 管理

### 專案結構

- 每個專案一個資料夾 + 一個虛擬環境
- 依賴記錄在 `requirements.txt` 或 `pyproject.toml`
- 環境變數放 `.env`，用 `python-dotenv` 載入

## Python 基礎

### 資料型別與運算

- 數字：int、float；字串：str，f-string 格式化（`f"Hello {name}"`）
- 布林：True/False；運算子：算術（`+`, `-`, `*`, `/`, `//`, `%`, `**`）、比較、邏輯（`and`, `or`, `not`）
- 快捷賦值：`x += 1`、`x *= 2`

### 資料結構

- List：有序可變，`[]`，支援 slicing、`append`、`remove`、`sort`
- Dictionary：鍵值對，`{}`，`keys()`/`values()`/`items()`
- Tuple：不可變序列，`()`，適合固定資料
- Set：無序不重複，`{}`，適合去重與集合運算

### 控制流程

- `if` / `elif` / `else`
- `for` 迴圈搭配 `range()`、list comprehension
- `while` 迴圈

### 函式與模組

- `def` 定義，位置參數、關鍵字參數、預設值、`*args`、`**kwargs`
- `return` 回傳值；全域 vs 區域變數作用域
- `import` 模組：`import os`、`from pathlib import Path`、`import json`

## 物件導向

- `class` 定義類別，`__init__` 初始化
- 繼承（`class Child(Parent)`）、方法覆寫
- 常用內建：`dataclass`（簡化資料類別）

## 檔案操作與錯誤處理

- 讀寫檔案：`with open(path, 'r') as f:`
- JSON：`json.loads()`、`json.dumps()`
- 錯誤處理：`try` / `except` / `finally`；常見例外類型

## AI 相關應用

### OpenAI API 整合

```python
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

### 結構化輸出（Pydantic）

```python
from pydantic import BaseModel
class Response(BaseModel):
    answer: str
    confidence: float
```

### 最終專案：AI 聊天助理

- 讀取 CSV/文字資料
- 建立對話迴圈，保存 message history
- 讓 AI 根據自訂資料回答問題
- 儲存對話記錄至檔案

## 課程資源

- 課程手冊：python.datalumina.com
- 84 個章節，涵蓋環境設定 → Python 基礎 → 進階功能 → AI 整合
