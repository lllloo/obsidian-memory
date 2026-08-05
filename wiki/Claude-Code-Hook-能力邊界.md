---
title: Claude Code Hook 能力邊界
description: 五種 hook type 各能做什麼、輸出契約如何決定能力上限，以及由此推出的「要 LLM 加工資料流就放在資料落地端」設計原則
created: 2026-08-05
updated: 2026-08-05
source: https://code.claude.com/docs/en/hooks
parent: "[[wiki/01.index]]"
tags:
  - claude-code
  - ai-agent
  - automation
  - context-engineering
---

Hook 是 Claude Code 在特定事件點回呼外部邏輯的機制。討論「能不能讓 hook 幫我做 X」時，真正的限制幾乎不在事件夠不夠多，而在**該 type 的輸出契約允許回傳什麼**——這一點是本頁的核心。

## 五種 type

| type | 執行方式 | 輸出能力 |
|---|---|---|
| `command` | 本地 shell 命令，stdin 收 JSON、stdout 回 JSON | **最完整**：allow/block、改寫 tool 輸入輸出、注入 context、可 `async` |
| `http` | POST 到外部端點，請求／回應體同 command | 同 command（少了 `async`） |
| `mcp_tool` | 呼叫已連線 MCP server 上的工具 | 工具輸出若為合法 JSON 即視為決策 |
| `prompt` | 把你的 prompt 加 hook input 送給一個快模型（預設 Haiku），單輪 | **只有** `{ok: true}` / `{ok: false, reason}` |
| `agent` | 同上但有多輪工具存取（Read／Grep／Glob，最多 50 turns） | 同 `prompt`，只有 allow/block |

`prompt` 與 `agent` 是 Claude Code 代管的 LLM 呼叫——不需要 API key、不需要外部依賴，看起來很誘人。但它們的**出口只有一個 allow/block 閥門，內容過不去**。這不是缺欄位，是定位：它們的職責是「判斷要不要放行」，不是「產出內容存起來」。`/goal` 就是內建的 session-scoped prompt-based Stop hook 捷徑，正是這個定位的典型用法。

`agent` type 官方標為 experimental，並建議正式用途改用 `command`。

## 幾條容易踩到的硬限制

- **不是所有事件都支援所有 type**。`SessionStart` 與 `Setup` 只支援 `command` 與 `mcp_tool`——想在 session 開場用 LLM 判斷點什麼，這條路直接不通。
- **只有 `command` 能 `async`**。其餘 type 一律阻塞當下流程；`Stop` 上掛一個同步的 LLM hook，等於每輪回覆結束都要等它跑完。
- **`Stop` 上的 `ok: false` 不是「擋下來」而是「繼續」**——reason 會被當成 Claude 的下一個指令、回合繼續。想用它把資料回傳給自己，結果是拿那段文字去戳模型繼續講話（連續 8 次 block 後 Claude Code 會 override 強制結束回合）。
- **`claude -p` 會遞迴**。在 command hook 裡 shell out 呼叫 Claude，那個 session 一樣會載入你的全域 hook，於是它結束時又觸發同一個 hook。要靠環境變數旗標自己擋。

## 推論出的設計原則

**要對資料流做 LLM 加工，把它放在資料落地端，不要放在 agent harness 端。**

harness 端（hook）受制於上述輸出契約：能回什麼、能不能非同步、會不會遞迴，全都不是你能決定的。而資料落地之後——Firestore trigger、資料庫 CDC、佇列消費者——沒有任何一條限制成立：非同步是預設、不會遞迴、想寫回哪個欄位都行，而且**同一份資料無論由哪個工具寫入都會經過同一條加工路徑**，跨 harness 的重複實作自然消失。

這個判準也適用於反方向：純粹的**放行判斷**（測試過了沒、這個指令危不危險）本來就該留在 hook，因為它需要的正是 hook 獨有的能力——在動作發生前介入。兩者的分工線是「你要的是決策還是內容」。

[[Claude-Code-記憶系統六層比較]] 裡的多數方案把 hook 當作記憶的注入與捕捉點，正落在 hook 擅長的那一側；而 [[Mem0]] 的 plugin hook 之所以會有可觀的原始碼實測消耗，也是因為它把加工塞進了 harness 的同步路徑。

## 時間抗性註記

本頁依 2026-08-05 的官方 hooks 文件整理。事件清單與 type 支援矩陣會隨版本增修，`agent` type 尤其標明 experimental、行為可能變動；要精確判斷某個事件支不支援某個 type，一律回查官方文件的支援矩陣，別憑本頁的快照下結論。核心的輸出契約差異（`prompt`／`agent` 只回 allow/block）則是定位使然，比清單本身穩定。
