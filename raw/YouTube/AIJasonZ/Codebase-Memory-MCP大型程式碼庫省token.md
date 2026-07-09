---
title: 如何用 Codebase Memory MCP 在大型程式碼庫將 coding agent 的 token 砍半
description: 把程式碼庫轉成關係圖譜，讓 coding agent 靠 get-architecture、trace-path 等工具理解跨檔跨 repo 的相依與變更 blast radius，token 用量近乎減半。
created: 2026-07-06
updated: 2026-07-06
source: https://www.youtube.com/watch?v=iWRmtPdFbGw
published: 2026-06-30
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - mcp
  - context-engineering
  - token-optimization
---

## 問題：coding agent 把程式碼當純文字讀

在大型程式碼庫叫 coding agent 改東西時的典型失敗：agent 先 grep，得到一大片 match，再一個個開 20 個檔案，最後仍漏掉一半可能被牽連的地方。

根本原因：程式碼庫本身已經是一張圖——每個 import、每個 function call 都是一條邊，但 agent 把這個結構丟掉，只當成扁平文字在讀。

傳統流程的成本問題：

- grep 回傳一堆檔案，agent 逐檔追蹤、逐檔讀取。
- 每次讀檔把整個大檔倒進 context window，很容易爆掉。
- Claude Code 雖有 sub agent 幫忙管理搜尋任務的 context，但相當慢。
- 程式碼庫越大問題越嚴重；production 通常不只一個 repo，要 agent 跨 repo 理解相依關係更困難。

## 解法：Codebase Memory MCP

把程式碼庫轉成 coding agent 能實際跟隨的地圖，等於給 agent 一個 GPS。當 agent 要改某個檔案時，工具會明確告知所有相關檔案，讓每次 PR review 都清楚看到變更的 blast radius。

與過去一堆做 codebase index / retrieval 的專案差異：

- 過去專案多半靠 LLM pipeline 生成 knowledge map，容易很快過期；或不契合 coding agent 的工作流。
- 本專案主要以 C / C++ 寫成，是目前最快、最有效率的 code intelligence engine。連 Linux kernel 這種規模都能在 3 分鐘內索引完整個程式碼庫，一般較小的程式碼庫幾秒內就建好 index。

## 核心機制：純程式化的關係圖譜

從程式碼抽出 function、message、class 等根節點，建立關係圖，不需載入上千行程式碼就能快速理解一個檔案是什麼。

- 關係可跨檔建立：三個檔案各自抽出 function / class / message，組成 cross-file graph。
- 同樣流程套用到所有檔案，形成整個程式碼庫（甚至跨 repo）的巨大圖譜。
- 整個過程極快，因為完全沒有 LLM 介入，純程式化。

## Agent 可用的工具集

- `get architecture`：回傳程式碼庫架構的快速總覽，讓 agent 輕鬆理解整體結構。
- `search graph`：定位某個 function 的節點。
- `trace path`：畫出 call chain，理解這個 function 被誰用、會牽動什麼。
- 對圖譜下 query：取得平常很難拿到的資訊。例如「所有呼叫 `handle order` 這個 function 的檔案裡，哪些還沒有測試覆蓋」。
- 取得特定 function 的 code snippet。
- PR review 時做 change detection，快速看出每次 PR 對架構的衝擊。

## 關鍵設計：用 pre-tool-use hook 兜底

作者認為這是本專案比其他方案更實用的地方。

- 過去很多專案失敗的原因：就算給了 agent memory search / codebase search 工具，agent 常搞不清楚何時該用這個特殊工具、何時該用一般 grep；而各家 coding agent（Claude Code、Codex）又都在優化自己的 grep 工具。
- 本專案承認這點，改用 pre-tool-use hook：就算 agent 忘了呼叫 graph search、只用一般 grep 搜某個 function，一般 grep 照跑並回傳結果，同時 hook 會攔截並把圖譜的額外豐富資訊夾帶進 grep 結果。
- 結果：不再依賴 agent 每次都主動呼叫特殊 MCP 工具。作者建議：若你在做 MCP，強烈推薦採用這種利用 Claude Code / Codex hook 的模式。

## 安裝與使用

- 安裝有兩種命令：基本版，或帶圖形視覺化的版本（加 `--ui`）。執行後會把 MCP 裝進你的 coding agent。
- 對 agent 說「Help me use codebase memory MCP」，它會開始設定 index。
- 若程式碼庫已有良好文件，會自動套用 filter（例如作者的程式碼庫自動判斷某些資料夾並決定忽略）。
- 索引一個 semi-complex 的大型 monorepo（含多個子資料夾）只花幾秒。
- 索引完成後即可用 `search graph`、`trace path` 等工具。
- UI 版可在 terminal 執行 `codebase memory MCP --ui=true` 並指定 port，開啟 web UI 檢視圖譜。

## 實例：追蹤隱藏的 canvas lock

以 Superdesign（vibe design 平台）為例，後端有個 `create design draft node` 工具，agent 收到 prompt 時會呼叫它，在無限畫布上新增 design node。

- 隱藏機制 `canvas lock`：因為同一時間可能有多個 agent 在同一畫布上創作，會造成 conflict 與 race，於是用 canvas lock 讓一切走 queue。
- 這個 lock 很隱蔽：`create design` 工具沒有直接呼叫它，而是往下委派好幾層，所以它甚至不在這個檔案裡。
- 對任何 agent 或人類來說，只讀這一個檔案、或 grep 「lock」，這層保護是真實存在卻不可見的。
- 用 MCP 叫它「從 memory notes 追蹤 `create design draft node` 到 canvas lock 的流程」，幾秒內就回傳完整流程。

## Token 對比數據

比較「使用 vs 不使用」codebase memory MCP：

第一個問題（取得完整流程）：

- 使用 MCP：message 部分約 11,000 token。
- 不使用 MCP：約 38,000 token。

第二個問題（「改動這個 lock 會壞掉什麼」，trace break impact）：

- 使用 MCP：跑約 1 分鐘，成功找出全部 13 處 call site，只用約 33,000 token。
- 不使用 MCP：約 64,000 token，接近兩倍。

## 其他

- 作者已把這個 MCP 更新進他的 setup codebase harness skill；執行該 skill 會連同 end-to-end 測試、啟動本地 server 的 script toolkit、可在遠端 sandbox 跑平行 agent 測試等一起設定好。
- 專案開源，可複製並套用到自己的程式碼庫；可搜尋 GitHub「AI Builder Club skill」找到 repo。
