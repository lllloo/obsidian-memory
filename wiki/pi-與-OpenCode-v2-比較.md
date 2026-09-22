---
title: pi 與 OpenCode v2 比較
description: 兩套 MIT 開源終端 coding agent 的取捨：pi 極簡單進程、靠 TypeScript extension 自組；OpenCode v2 常駐 server 電池全含，plugin 生態重來
created: 2026-09-22
updated: 2026-09-22
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - agent-framework
---

2026-09-22 回答「幫我比較 pi 跟 opencode v2」的 Query 回存。來源為兩方官網／README、第三方比較文與一份實測基準；OpenCode v2 官方 release notes 頁面與 GitHub API 當日皆取不到，v2 變更細節來自二手轉述，強度標「中」。

**一句話**：pi 是「可程式化的極簡 harness」，OpenCode 是「電池全含的 Claude Code 替代品」。差別不在誰強，而在你想自己組還是拿現成的。

## 對照表

| 面向 | pi（badlogic／earendil-works） | OpenCode v2（anomalyco，前 sst） |
|---|---|---|
| 定位 | 單進程極簡 agent，官方口號「Adapt Pi to your workflows, not the other way around」 | client-server：一個常駐 server 同時餵 TUI、Desktop、Web 與自訂 client |
| 內建工具 | 只有 read／write／edit／bash（grep／find／ls 可啟用） | 12+ 內建工具、LSP 診斷、Plan mode、subagents、MCP、permissions（allow/ask/deny） |
| 明確不做 | 無內建 MCP、無 subagent、無權限彈窗、無 plan mode、無 todo、無背景 bash；官方回答一律是「寫 extension 或跑容器」 | 幾乎都內建 |
| 擴充方式 | TypeScript extension **在 agent 進程內跑**，25+ 個 hook（含 `input`、`before_agent_start`、context 修剪、session 分支事件），TUI 任何區塊可改 | JSON config＋plugin＋skill＋MCP，約 20 個事件；TUI 封閉，不能塞自訂 UI |
| Session | JSONL 存成樹，`/tree`／`/fork`／`/clone` 就地分支；compaction 有損但全史保留在 JSONL | 多分頁平行 session、跨裝置同步（v2 新增） |
| 執行模式 | interactive／print-JSON／RPC／SDK 四種 | TUI／Desktop（Electron）／HTTP API＋生成的 TypeScript client |
| Provider | 約 15–20 家；本機模型（MLX／GGUF）支援受好評 | 75+ 家，含 Ollama／LM Studio／llama.cpp |
| 資源 | 單進程；system prompt＋tool 定義不到 1k tokens | 常駐服務，RAM 1GB+；prompt 約 6.9k tokens |
| 授權／熱度 | MIT；約 108k★（2026-09-22），近月成長率明顯高於 OpenCode | MIT；約 209k★（2026-09-22） |

星數與 provider 數變動快，引用前回 GitHub 看當下值。

## OpenCode v2 是什麼（信心中，二手轉述）

v2.0.0 於 2026-09-11 打 tag，之前先開公測。核心改動：runtime 從 Bun 換 Node（解記憶體問題）、Desktop 從 Tauri 換 Electron、API 整套重設計並文件化、預設跑常駐背景服務、多分頁平行 session、skill 熱重載不炸 prompt cache。**v1 plugin 在 v2 不能用**，這是維護者 Dax 公測時明講的破壞性變更。v1.18.x 在 2026-09 仍持續出版本，兩線並行維護一陣子。

**勿引用**：某交易所新聞稿宣稱 OpenCode「160 萬星、月活 750 萬開發者」，星數與 GitHub 實際（約 20.9 萬）差一個數量級，該來源數字不可信，本頁只取其對變更項目的描述且已與 Dax 推文交叉核對。

## 實測數據（單一來源）

Composio 2026-08-21 基準：30 題硬任務、同用 DeepSeek V4 Pro。pi 21/30 通過、總花費 $1.64；OpenCode 19/30、$2.25。pi 較慢（中位 363 秒對 281 秒）。作者最後打 6:6 平手。**一次性、單一模型、單一作者**的基準，不能當普遍結論；token 開銷差距（1k 對 6.9k）倒是結構性的，可複現。

## 怎麼選

- **選 pi**：想自己控制 agent loop、要極省 token、常換本機模型、需要 session 樹分支來除錯。代價是 MCP／permission／subagent 都要自己接。
- **選 OpenCode v2**：要 Claude Code 等級的開箱功能、團隊要權限控管、要 LSP 診斷、想從 Desktop／Web 多端接同一個 server。代價是更重，且 v2 剛出、plugin 生態要重來。

## 關聯

- [[LLM-方案定價與-coding-agent-比較]]——訂閱額度能否給第三方 harness 用：OpenAI「Codex for Open Source」明列支援 OpenCode 與 pi，兩者都吃得到 ChatGPT 訂閱；Claude 訂閱兩者都不能用。本頁是能力取捨，該頁是錢從哪來。
- [[OpenClaw-與-Hermes-的實地使用心得]]——該頁引用的 `sshine` 試過含 pi 與 opencode 在內五套 harness，批的是 Hermes 過度工程；與本頁「pi 極簡、OpenCode 電池全含」的光譜合看，Hermes 落在比 OpenCode 更重的一端。
- [[pi-workflow-編排-harness-與本-vault-分野]]——pi-workflow 是給 pi 用的編排 CLI，正是 pi「無內建 subagent、自己用 extension 組」哲學的第三方產物。
- [[Coding-agent-指示檔與規則載入機制對照]]——本頁的「擴充方式」列只點到 extension 與 plugin；該頁把「指示檔與規則能否依路徑條件載入」單獨挖開，pi 靠 `tool_call`／`tool_result` 自製、OpenCode `instructions` 只能全載，兩者都沒有 Claude Code rules 的等價物。
- [[Agent-Harness-Engineering-框架綜述]]——該頁的 13 套 scaffold 原始碼比較含 OpenCode；本頁補 pi 這個「極簡到不進比較清單」的對照端點。
