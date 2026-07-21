---
title: Pi Agent 可自我擴展的 coding harness
description: 拆解 Pi Agent 的 extension 系統與五個核心 package，說明為何 OpenClaw 選它當底層，以及如何用其 SDK 打造自有 agent 產品
created: 2026-07-21
updated: 2026-07-21
source: https://www.youtube.com/watch?v=MsPhMhfvgD4
published: 2026-07-14
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - claude-code
  - context-engineering
---

## Pi Agent 特別在哪

Pi Agent 本質上是一個 coding agent。作者的看法是：Claude Code 與 Codex 這類 coding agent 之間，近幾週實質差異已經很小。那為什麼 OpenClaw 會選 Pi Agent 當基底？

關鍵不在模型或工具數量，而在**能不能改 harness 本身**。Claude Code、Codex、OpenCode 都有各自的 SDK 與 CLI 可供包裝，但你無法修改 harness 內部的運作方式。例如 Claude Code 有 dynamic workflow，Codex 使用者沒辦法叫 Codex「把 dynamic workflow 實作成你 harness 的一部分」，反之亦然。

Hook 系統確實開放了部分客製化空間——例如每次工具呼叫前檢查自訂的權限規則、回傳 true / false 決定是否放行。但仍有限；GitHub issues 上有大量使用者想改卻改不到的場景。

Pi Agent 的設計哲學正相反：**harness 應該去適應使用者，而不是反過來**。

## 極簡預設 + extension 系統

Pi 預設只是一個最小版本的 coding agent，只有四個關鍵工具：執行 bash 指令、寫檔、讀檔、編輯檔案。沒有 sub-agent、沒有 agent teams，連 MCP 都不內建。

但它可以靠 **extension** 任意擴充。extension 開放的修改面涵蓋工具、context、hooks、session 管理、指令、UI，幾乎無所不包：可新增工具、指令捷徑、provider、模型 provider，以及幾乎所有你會需要的 hook。

UI 本身也開放。作者示範把 Pi Agent 的 UI 改成任意樣式，甚至直接對 agent 說「我想在 prompt 輸入框看到天氣資訊，幫我客製 UI」——Pi 會自動去讀 extension 文件、寫出天氣 widget 的 extension，接著 `/reload` 就立即載入剛剛自己生出來的新版 harness。

**extension 可以由人寫，也可以由 agent 自己寫**：Pi Agent 內建相關知識，並清楚知道目前載入了哪些 extension、該怎麼寫，因此能即時自我修改。

## package catalog：把別人的功能裝回來

Pi 有一個 package catalog，可安裝他人寫好的 extension。幾乎所有 Claude Code / Codex 的熱門功能都已經有人實作：TODO 功能、MCP adapter、Chrome 瀏覽器存取、ask user question 工具、sub-agents、plan mode、dynamic workflow，甚至 computer use。

以 dynamic workflow 為例：複製該 package、執行安裝指令、reload，之後 prompt 中包含 workflow 之類的關鍵字就會觸發，也能用 `/workflow` 叫出幾乎與 Claude Code 一模一樣的 workflow UI。

甚至有 package 直接把 Pi Agent 變成 Claude Code 或 Codex，打包了那些 harness 的專屬工具。也有讓你在 agent 執行時玩小遊戲的 extension。部分套件品質未必好，但技術上可以直接叫 agent 幫你改進或重建。

## Pi hyper：Claude Code 做不到的那種擴充

一個突顯 Pi 優勢的例子是名為 Pi hyper 的 package。它攔截每一次工具呼叫的 hook，對 bash 指令結果做**前處理**，只回傳相關且最小量的資訊給 agent。

例如 agent 跑 `git log` 看近期 commit，原始輸出包含 hash、作者、日期、內文與 diff 區塊等大量資訊；這個 package 會清理成只留有用的部分，該類指令可減少約 96% 的內容，其他測試指令也砍掉約 80–90% 的 token。

**這件事在 Claude Code 或 Codex 難以實作**，因為它們的 pre-tool-use hook 只能對工具呼叫「附加」資訊，無法直接修改工具呼叫的結果。

這套 extension 系統正是 OpenClaw 的起點：OpenClaw 主要自建的是連接 app、Slack 與 web 介面的 gateway，agent runtime 直接用 Pi Agent——沿用其 agent loop、模型層與 session 管理，再擴充 MCP、memory、sub-agent、ACP 等。若改用 Claude Code SDK 或 Codex CLI，這種程度的客製會困難得多。

## 寫 extension 的實例

在任一專案資料夾或家目錄建立 `.pi` 資料夾，其中放 `extensions` 資料夾即可。extension 用 TypeScript 撰寫。

**1. 修改 context——讓 agent 永遠知道當前 git 狀態**

寫一個函式跑 git 指令取得分支、可用 worktree、未 staged 變更、近期 commit，整理成 git 摘要，再用 `pi.on_before_agent_start` 修改 system prompt，把 git context 附加在預設 system prompt 之後。放進去後下次載入 Pi Agent 就自動帶著這些 context，可以直接問「這裡的 git 資訊是什麼？不要用任何工具回答我」驗證。

**2. 自訂工具——讀取剪貼簿**

用 `pi.register_tool` 給定名稱、label、description 與參數，再定義實際函式即可。之後問「我剪貼簿裡有什麼？」就會呼叫該工具。

**3. Permission gate——用小模型做權限守門**

情境是 agent 要給團隊使用，但每個人可存取的資訊層級不同。與其讓訊息直接進 agent、或讓 agent 自己判斷權限，不如先用一個便宜快速的小模型做權限檢查：通過就照常進 agent，屬於危險資訊就直接中止 session。

這個 extension 用到兩個 package：`pi coding agent`（提供 extension API）與 `pi ai`（可輕鬆對任意模型發起呼叫）。實作大致是：

- 定義一個以 Haiku 為 gate model 的判斷流程，輸出 allow / deny 與理由
- 包成一個小的 decide 工具，帶上 system prompt 與 user message，載入使用者放在根目錄的 `permission.md` 政策與使用者請求
- session 開始時載入政策資訊
- 使用者每次送出訊息後，UI 顯示「權限檢查中」，等待模型結果；被拒就在 UI 顯示封鎖訊息並完全跳過 agent，否則照常執行

測試時在 `permission.md` 寫下「只有 Jason 能取得營收資料」，再去問「六月營收多少」，就會觸發權限檢查並回報無權存取。

大多數時候你其實不必自己學寫 extension，直接跟 Pi Agent 講，它會自我演化。

## 五個 package：拿 Pi 當 SDK 建產品

作者認為 Pi 真正的威力不在當 coding agent 用，而在**拿它當底層建 AI 產品**。Pi Agent repo 內含五個 package：

| Package | 定位 |
|---|---|
| `ai` | 類似 Vercel AI SDK 的模型呼叫層，內含 OAuth 功能，可讓使用者接上自己的 Claude Code / Codex 訂閱 |
| `agent` | agent loop 本身，約等於 Vercel AI SDK 的 `streamText` 加上一個小型 agent loop |
| `coding agent` | 在前兩者之上加入 read / write / edit / bash 等必要工具、session 管理、context window 壓縮、extension 系統與 SDK。可視為 Claude Code Agent SDK 的等價物，但完全可客製、可接任何模型 |
| `tui` | 把 coding agent 包成終端 UI |
| orchestrator | 排程工作與委派任務給不同 Pi agent process，較為實驗性 |

依產品型態選用對應的 package，即可用 Pi 生態系搭出自己的 agent 產品骨架。

## 兩種產品型態的差異

**本地 agent**（跑在使用者自己電腦上）：`coding agent` package 幾乎給足所需，再靠 extension、自訂 UI 與 task trigger 擴充即可。作者舉的例子是一個建在 Pi 之上的 coding agent，加了大量新工具讓效能接近 Claude Code / Codex，終端內有編輯器式介面，甚至能把某段對話 session 發佈給他人，產生可掃的 QR code 或可分享的 URL。

**Web 託管 agent**：Pi coding agent SDK 預設與本機檔案系統綁得較緊，而 web 部署時 agent 跑在共用後端、每個使用者各有自己的 sandbox，因此需要調整：

- 不用預設的 session manager（它直接綁本機檔案），改把 session 資訊存進自己的 DB，並自行管理 context 壓縮
- 對預設的 bash / read / write 工具包一層，讓操作落在該使用者的 sandbox 內

作者強調用 Claude Code Agent SDK 也一樣要處理這些問題，不是 Pi 獨有的負擔。

## 用 resource loader 客製每個 session

建 web chat agent 時仍用 `pi coding agent` package，但改用 default resource loader 傳入額外的 extension 與 skill。做法大致是：

- 定義 inline extension，例如一個攔截特定 bash 指令的 guardrail
- 定義自訂工具，例如取得 MRR 的工具
- 建立 resource loader，指定 agent 的工作目錄、載入 extension 的目錄，以及是否要從 `.pi` 資料夾載入 extension 與 skill
- 傳入自訂 extension（如上述 guardrail）與額外 skill，藉此控制每個 agent session 能存取哪些能力
- 用 `create agent session` 傳入自訂工具與 resource loader，之後依事件型態在 UI 呈現對應資訊

作者用同一套 SDK 做了一個可自主啟動並經營公司的託管 agent 系統的複刻版：以 Pi 的 coding agent SDK 當 agent runtime，拆成 11 個 agent，由一個圍繞 task entity 建構的 orchestrator 協調，並持久化狀態、context 與工具 proxy。
