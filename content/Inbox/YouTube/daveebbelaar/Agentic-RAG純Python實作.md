---
title: Agentic RAG 純 Python 實作
created: 2026-05-11
updated: 2026-05-11
source: https://www.youtube.com/watch?v=RxwjoegpI98
published: 2026-05-10
parent: "[[01.index]]"
tags:
  - youtube
  - agentic-rag
  - rag
  - python
  - pydantic-ai
---

## 核心觀點

從零用純 Python 打造 agentic RAG 系統，目標不是再做一個 coding agent，而是讓 LLM 能存取公司內部、私有或任何外部知識。基本三件套：list、grep、read，正是 Claude Code、Cursor、Codex 等 agent harness 共用的核心工具集。

## Semantic RAG vs Agentic RAG

| 維度       | Semantic RAG                 | Agentic RAG                                |
| ---------- | ---------------------------- | ------------------------------------------ |
| 流程       | 線性，取資料後呼叫 LLM 一次  | 迴圈，LLM 在搜尋／讀取／回呼之間多次調用    |
| 自我修正   | 無                           | 找不到資訊時 agent 會換條件重試            |
| 延遲       | 低                           | 高（多次 tool call）                       |
| 成本       | 低                           | 高                                         |
| 表現上限   | 較低                         | 在有時間/預算時通常勝出                   |

低延遲、追求成本最佳化的場景 → 留在 semantic RAG；願意付出 latency 與 token 成本換正確率 → agentic RAG。

## 三個核心工具

最簡 agentic RAG 只需三個函式作用在 markdown 檔案系統上：

- `list_files()`：列出 notes 目錄下所有檔案
- `grep(pattern)`：依正規表達式搜尋內容，回傳檔名 / 行號 / 該行內容
- `read_file(path)`：讀取單一檔案內容

LLM 在迴圈中自主決定何時呼叫哪個工具、用什麼參數，直到湊齊回答。

## list_files 實作要點

用 `pathlib.Path` 設定 `NOTES_DIR`：

```python
from pathlib import Path
NOTES_DIR = (Path(__file__).parent / "notes").resolve()
```

- `.resolve()` 清掉 symlink 與奇怪字元，得到乾淨絕對路徑
- 列檔用 `NOTES_DIR.glob("*.md")` 抓所有 markdown
- 用 `path.relative_to(NOTES_DIR)` 轉成相對路徑再回傳給 agent，省 token 也避免暴露絕對路徑

## grep 實作要點

```python
import re
pattern = re.compile("connection pool", re.IGNORECASE)
```

逐檔逐行掃：

1. 讀全檔內容 → `splitlines()` 切成 list
2. `enumerate(lines, start=1)` 從 1 開始計行號（人類可讀）
3. 命中時 append `(relative_path, line_number, line_content)` 進結果 list

這就是 coding agent 在 codebase 裡找符合條件位置的同一套機制，差別只在這裡作用於 markdown 知識而非程式碼。

## read_file 實作要點

讀檔前先檢查路徑安全性：

```python
target = Path(file_path).resolve()
if not target.is_relative_to(NOTES_DIR):
    raise ValueError("file outside notes directory")
return target.read_text()
```

`is_relative_to()` 是把 agent 鎖在 `NOTES_DIR` 範圍內的關鍵 sandbox 機制——禁止跳出指定目錄讀任何檔。

## 用 Pydantic AI 串 agent

影片用 Pydantic AI 框架簡化 tool registration 與執行迴圈，但概念可移植到任何 agent framework（LangGraph、自寫 OpenAI / Anthropic API loop 皆可）。

```python
agent = Agent(model="openai:gpt-5.5", tools=[list_files, grep, read_file])
result = agent.run_sync("Why does our nightly deploy job run at this specific time?")
```

問完之後 agent 會自主迴圈，案例中跑了 5 次 tool call 才湊齊答案。

## 用 `agent.iter()` 看內部步驟

預設執行只看得到最終結果，要 debug 改用 Pydantic AI 的 `agent.iter()` 方法攔截每個 tool call：

- 看到 LLM 決定呼叫哪個 tool、丟什麼參數
- 看到 tool 回傳什麼結果
- 啟用 `debug=True` 後連 grep 回傳的 14 筆 match 都會列出

這是優化 agentic RAG 的關鍵——必須能看 model 搜了什麼關鍵字、回傳的文件對不對、再決定如何改 prompt 或 tool docstring 來導向正確結果。

## Tool docstring 即 prompt

LLM 透過 docstring 與參數型別決定何時用 tool、怎麼用：

- docstring 內容會直接塞進 system prompt
- 在 docstring 加 domain knowledge 可導向 agent 搜對方向
- 現代 SOTA model 之所以擅長這套迴圈，是因為各大實驗室都把 coding agent 表現當主要 benchmark 在優化

## Structured Output 與 citation

把回答結構化，方便下游程式取用：

```python
class Citation(BaseModel):
    file: str
    quote: str
    line_number: int

class SearchAnswer(BaseModel):
    answer: str
    citations: list[Citation]

agent = Agent(..., output_type=SearchAnswer)
```

這讓前端可以渲染答案 + 可點擊 citation 跳到原文，是把 agentic RAG 接進產品的基本盤。

## Production 強化重點

正式環境要在 simple 版上加幾層：

### 1. 安全上限參數

- `agent_request_limit`：防止 agent 進入無限迴圈
- `read_max_lines`：限制單檔讀取行數，避免大檔灌爆 context window

### 2. 用 ripgrep 取代 Python 正規表達式

- Rust 寫的 `rg` 速度遠快於純 Python `re`
- 預設忽略隱藏檔與 `.gitignore` 內容
- 透過 `subprocess` 從 Python 呼叫：

```python
subprocess.run(
    ["rg", "--line-number", "--ignore-case", "--no-config", pattern, str(NOTES_DIR)],
    capture_output=True, text=True,
)
```

- 部署環境需把 ripgrep 列為依賴（Mac：`brew install ripgrep`；Windows 有對應安裝指令）

### 3. 錯誤回傳而非 raise

關鍵設計差異：

- **raise** → 整個 agent process 停掉
- **return error string** → LLM 收到人類可讀的錯誤訊息，能 self-correct 再試一次

agent harness 應把所有 file-not-found、permission denied 等 edge case 包成 error message 回傳給 model，讓迴圈繼續跑。

### 4. Logging

加 logger 把 tool call、參數、結果都記下，便於 production debug。

## 部署彈性

同一套概念可換載體：

- **檔案系統**（markdown）：教學示範用，最簡單
- **PostgreSQL**：把 markdown 內容存進 DB，三個 tool 改成 query function 即可
- **VPS / Container App / Serverless**：tool 本身邏輯不變，只改檔案來源／路徑解析

核心不變：list、search、read 三件套 + agent loop。

## 適用情境判斷

- 需要 LLM 對私有資料做多步推理 / 跨檔交叉比對 → agentic RAG
- 即時 chatbot、單次 QA、預算敏感 → 先用 semantic RAG
- 已有 semantic RAG 但部分困難 query 答不好 → 加 agentic RAG 作為 fallback 層
