---
title: 讓 Hermes Agent 幾乎免費：Token 成本優化設定
description: 拆解 Hermes agent 的 token 消耗來源，從模型選擇、context 壓縮、精簡工具與 skill 到 hard limits，逐項調設定降低成本又不犧牲輸出品質。
created: 2026-07-06
updated: 2026-07-06
source: https://www.youtube.com/watch?v=5d02TYoOzfE
published: 2026-07-01
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - token-optimization
  - automation
---

## 什麼在吃 token

- token 是模型讀寫文字的建構塊；input 不只你的 prompt，還含 system prompt、整段對話歷史，以及每則訊息都會附帶的東西：每個 skill 的 header（名稱+描述，永遠載入）、你設定的 MCP tools、memory 與 user files。
- Hermes 預裝 90 個 skill，且會隨使用增長（把值得重用的 workflow 都變成新 skill）；此外它會掃描對話尋找建新 skill 的機會，這也燒 token。
- **self-evolving memory**：持續從對話擷取關於你的細節寫入 memory 並自行更新，以保留 context 客製回答——同樣燒 token。
- Hermes **24/7 運行**（跟「跑一次就停」的 Claude Code 不同），可跑在 local server 或 VPS；背景任務多會推高用量。單次跑很便宜，但重複或大量類似 job 累積起來就貴。MCP tools 與 hooks 也載入 context；跑 goals 也花錢。
- **追蹤方式**：所有 token 使用資料存在 root 資料夾的 database，可請任何 agent 讀出詳細分解（自安裝以來的 sessions、tokens、成本）。`insights` 指令則給近 30 天的成本分解、各部分用量、最常用的工具與 skill、活動模式與最長 session。

## 模型設定（帳單最大來源）

- 若已有訂閱（如 codex 訂閱）可直接接 Hermes，透過既有訂閱付費、無額外費用。
- Anthropic 與 Gemini 訂閱雖被列為可用，實際**不能**這樣用（不能直接用 Claude Code），需另外的 API——因為用訂閱這樣接算違反其政策。故目前 codex 訂閱是最佳選項。
- **Open Router**：單一 API key 可接更多模型、適合全公司使用，但每個 token 都計費（好處是能第一次清楚看到成本）。搭配 **Parto router** 依任務實際需求路由到對的模型（13 個模型分不同 tier，從便宜基本到昂貴強大）。
- `config.yaml` 內可省 token 的設定：
  - **auxiliary tasks**（背景小任務，如讀圖、搜 skill、載 MCP tools、寫 profile 描述）預設 model=`auto`，會 fallback 到主模型。把這些指向較便宜的模型，主模型就不用在小事上燒貴 token。
  - **sub-agents**：各自有獨立 context window、token 很重（每個等於自己的 session、只回報結果）。可為 sub-agents 設較便宜的模型。
  - **effort level**（模型回答前思考多少）：調到 max 輸出更好但更燒 token。依任務調整，簡單任務可完全關掉 thinking。

## 精簡 context window

- 常按 **compress**：以「至今為止的摘要」開新 session，省大量 token 又保留 context。
  - 預設壓縮門檻 50%（context 半滿即壓）；多數情況調低較好，減少每 turn 需送的訊息量與每則訊息成本。
  - **target ratio**：壓縮後仍會保留一部分未壓縮 token 附上以維持 context；可設更低，讓較少舊對話帶入 context。
  - 也可控制每個 tool result 實際進入 context 的量（在 Open Router 上因要顧成本而把先前調高的值降回來）。
- 一次性、只需單一 session 的指令用 **ephemeral system prompt**，別寫進 Hermes context files。
- 組織好 local 系統（如 second brain）讓 agent 按需一點一點載入，而非一次拉入用不到的 token。
- 精簡 memory files 與 agent files（它們全程都在 context 裡，越小每則訊息塞給模型的越少）。
- 可關 **automemory**（停止收集 memory、也不讓 memory files 進 context）省錢，但等於放棄 Hermes 一大優勢；作者自身 workflow 選擇保留（要它跨團隊透過 Slack 共享公司 context）。
- Hermes 出錯時別只是再 prompt 一次，用 **undo** 退回最近一則訊息（只退一則、非多則），再給明確說明哪裡錯、要避免什麼的新 prompt。

## 削減工具、skill 與 MCP server

- 每個 agent 可用的工具都隨每則訊息當作 context 送出，所以砍掉不用的工具。
- Hermes 內建 17+ 個工具，`hermes list` 可看全部；用桌面 app 或 `tools disable <name>` 關閉（例：不碰 codebase 的團隊 profile 就關掉 code execution，另留專用 profile 做那件事）。
- Hermes 也附大量多半用不到的 skill，關掉所有不需要的，skill 清單只留實際會用的、避免占 context。
- MCP server 同理：斷開沒在用的；保留的把 **tool search 設 auto**（如 Claude 的 tool search，需要時才載入單一工具，而非全程留在 context）。

## Hard limits

- **max tokens** 設成固定數字，控制模型能產出的 output 量，省 output 成本並推向精簡回答。
- **max turns** 預設 150（工作時思考、call tool、讀輸出、權衡的回合數）；agent 卡住時會燒光所有 turn 反覆重送 context。作者調到 **60**，避免它卡在解不了的問題上空轉。
- **hard stop** 從 false 改 true：卡住且沒有進展時直接停下，防無謂 loop。
- **cron jobs**（按排程自行運行的任務）預設 max turns 無上限；設成固定數字，避免背景 job 無限燒 token。
