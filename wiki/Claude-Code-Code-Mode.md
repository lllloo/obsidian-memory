---
title: Claude Code Code Mode
description: Claude Code 的實驗功能：模型改寫 JavaScript 一次串多個工具呼叫，說明運作、開關、權限與 hook 行為、適用限制
created: 2026-11-17
updated: 2026-11-17
source: https://code.claude.com/docs/en/code-mode
parent: "[[wiki/01.index]]"
tags:
  - claude-code
  - coding-agent
  - ai-agent
---

2026-11-17 回答「什麼是 Claude Code Code Mode」的 Query 回存。**證據強度**：官方 [Code Mode 文件](https://code.claude.com/docs/en/code-mode)與官方 [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) 一手；未實測。官方標明為**實驗功能、預設關閉、任何版本都可能改或移除**，引用前先回查文件。

## 是什麼

一般模式下 Claude 一次發一個工具呼叫（Bash、Read、Edit…），讀完結果再決定下一步。Code Mode 下 Claude 改寫一段 JavaScript，由 Claude Code 在 session 內執行，程式裡把工具當函式呼叫——一段程式就能平行跑多個指令、把前一個結果餵給下一個、只回傳模型需要讀的部分。官方範例：

```javascript
const files = await $`rg -l "function retryPolicy" src`.text();
const target = files.trim().split("\n")[0];
await edit(target, "maxAttempts: 3", "maxAttempts: 5");
({ edited: target, tests: $`npm test -- retryPolicy`.nothrow() });
```

對話裡看到的仍是工具呼叫（如 edit 的 diff），程式本身要按 `Ctrl+O` 開 transcript viewer，展開 **Code** 列才看得到。執行程式的工具名是 `REPL`。

這與 Cloudflare 2025-09 提出的 [Code Mode](https://blog.cloudflare.com/code-mode/) 同一思路：把工具轉成程式 API 讓模型寫碼呼叫，理由是模型看過的真實程式碼遠多於工具呼叫範例（Cloudflare 原文主張，非獨立實證）。同名機制另見 [[四套-coding-agent-能力差異對照]] MCP 列記的 pi codemode（QuickJS 沙箱平行呼叫 MCP 工具），以及 OpenClaw 2.0 的 Code Mode（同樣實驗、預設關，見 `raw/fetched/OpenClaw-2.0-Release-Notes.md`）。

## 適合的工作

官方建議用在需要很多相關工具呼叫的任務：跨多檔重複的修改、要先過濾再讀的搜尋結果、可同時跑的獨立指令。

## 開與關

- **開**：環境變數 `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE=1`，可設在 shell 或使用者層 `~/.claude/settings.json` 的 `env`。**專案層 settings 裡設這個變數會被忽略**——clone 下來的 repo 不能替你打開。首次會要求確認，開啟後 session 頂端顯示 `Code Mode (experimental) is on`。
- **關**：移除該變數或設為 `0`；任一處為 `0` 就優先關閉。
- **組織封鎖**：managed settings 的 `env` 設 `0`；managed settings **只能關、不能替使用者開**。
- **resume 綁定**：Code Mode session 只能在終端、且變數仍為 `1` 時 `--continue`／`--resume`；反之一般 session 開了變數也不會變成 Code Mode。

## 前提條件（行為分水嶺，確切清單回查官方文件）

- CHANGELOG 記載於 v2.1.323 加入；更舊版本不會啟用。與 agent teams 並用另需較新版本（文件標 v2.1.326）。
- 只走 Anthropic 直連的訂閱或 Console 帳號：gateway、Bedrock、Vertex 類雲端、Foundry、自訂 `ANTHROPIC_BASE_URL`、`apiKeyHelper` 都不行；HIPAA 與 ZDR 組織不行。
- 只支援官方文件列出的較新模型；只在終端互動式 `claude` 能用，`-p`、Agent SDK、VS Code 面板、Desktop app、雲端 session 都不行；需 native build。
- 開 OpenTelemetry export 或 `DISABLE_TELEMETRY`（關掉 feature flag 抓取）時無法啟動。啟動失敗時 session 頂端與 `/status` 會寫原因，官方文件有原因對照表。

## 權限與 hook：檢查單位改變了

- 程式內每個工具呼叫**仍以原本工具名**（如 `Bash`）經過 `deny`／`ask` 規則與 `PreToolUse` hook。
- **auto mode 的 classifier 審的是整段程式、不是每個呼叫**，看不到執行期才算出的值（例如從搜尋結果取出的路徑）。必須管住的呼叫要靠規則或 hook，不能只靠 classifier。其他模式則程式直接開跑、照該模式逐個呼叫詢問。
- 要審程式本身，`PreToolUse` hook 匹配 `REPL`、讀 `tool_input.code`。
- shell 指令到 hook 時可能被組合成 `cd 'app' && git push` 這種形式，判斷 shell 的 hook 要逐段檢查（與 [[Claude-Code-Hook-能力邊界]] 談的 hook 輸出契約相關）。
- hook 失敗行為比平常嚴：程式發出的呼叫遇 `PreToolUse` hook 起不來或逾時，即使沒設 `onFailure` 也會被拒；想放行要顯式設 `"onFailure": "continue"`。背景執行時 `UserPromptSubmit` hook 也會跑在程式輸出上（`source` 為 `poll_event`），可能擋掉輸出。

## 其他限制

- 前景執行等程式跑完，**上限十分鐘**（含停在權限詢問的時間）；session 以 auto 或 `bypassPermissions` 啟動時程式可轉背景，最長兩小時，期間可繼續對話。
- 不能用 Remote Control、Claude in Chrome、computer use；不能移到 Desktop app 或轉背景 session。
