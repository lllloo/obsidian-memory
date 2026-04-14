---
title: Claude Code 與 Harness 實際運作原理
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-13
source: https://www.youtube.com/watch?v=I82j7AzMU80
---

## Harness 是什麼

Harness 是 AI agent 運作的工具集與環境。Claude Code、Cursor、Open Code、Codex CLI 都是 harness；T3 Code 則是包在 harness 上的 UI 層，本身不是 harness。

同一模型在不同 harness 下表現差異顯著。Opus 在 Claude Code 原生 harness 得分 77%，在 Cursor harness 下提升至 93%——差距完全來自 harness 本身。

## LLM 只能輸出文字

LLM 的本質是「給文字，預測下一段文字」，它無法直接操作電腦。所有「寫檔案、執行指令、搜尋程式碼」的能力，都是透過 **tool calling** 實現的。

## Tool Calling 運作流程

1. 系統提示告訴模型它有哪些工具（如 `bash_call`、`read_file`、`edit_file`）
2. 模型在回應中輸出特殊語法，例如：

   ```
   <bash_call>ls -la</bash_call>
   ```

3. 模型停止回應，harness 偵測到 tool call
4. Harness 執行該指令（可能先詢問使用者確認）
5. 執行結果附加到 chat history 末尾
6. 重新呼叫相同模型 API，模型從新的 history 繼續

每次 tool call = 模型暫停 → harness 執行 → 結果回注 → 模型重啟。

## Context 管理

- 模型只知道 chat history 裡的內容，不知道 history 以外的事
- `CLAUDE.md` / `AGENT.md` 是把常用 context 預填到最前面的機制
- 提示中直接告知檔案位置可減少 tool call 次數（模型不需先 search）
- 大 context 會讓模型變笨：Sonnet 超過 50,000–100,000 tokens 後，準確率可能跌至原來的 50%
- 現代模型已足夠聰明，無需把整個 codebase 塞入 context（repomix 式做法已過時）

## 核心工具（最小 harness 只需三個）

| 工具 | 功能 |
|------|------|
| `read_file` | 讀取檔案內容 |
| `list_files` | 列出目錄結構 |
| `edit_file` | 用 old_string → new_string 取代修改檔案 |

生產級工具會再加上 `bash`、`web_search`、`ripgrep` 等。

## 只給 bash 工具也能運作

把所有工具移除只留 `bash`，模型會自動用 bash 指令完成原本需要其他工具的操作。這說明 harness 的工具設計影響的是效率與安全性，不是能力上限。

## Harness 品質差異的根因

Cursor 的 harness 表現好，是因為有工程師的工作就是對每個新模型反覆微調：

- 系統提示的措辭
- 工具的描述文字（model 依靠這些決定用哪個工具）
- 不同模型對相同描述的反應差異很大

實驗：把 `read_file` 描述改成「deprecated，請用 bash」——Gemini 立刻只用 bash，Sonnet 繼續用 read_file；改成「deprecated」後 Sonnet 才切換。同樣的描述對不同模型效果不同，需要針對每個模型個別調整。

## 可以對模型說謊

模型看不到工具的實際程式碼，只看到工具的名稱與描述。因此：

- 可以宣稱提供 bash 但實際做其他事
- 可以讓兩個模型互相對話而不知道對方是模型
- 工具描述是 harness 最重要的調校點之一

## T3 Code 的定位

T3 Code 不提供工具，而是在 Claude Code / Codex CLI harness 上加一層 UI。要使用 T3 Code，必須先在本機安裝並登入對應的 harness。
