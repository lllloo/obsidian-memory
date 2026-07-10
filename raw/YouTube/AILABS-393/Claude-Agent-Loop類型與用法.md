---
title: Claude Loops 威力驚人——實際該這樣用
description: 拆解五種 agent loop（stateless、learning、multi-agent review、verification、workflow improvement）的設計、設定方式與適用場景，避免用錯 loop 白燒 token。
created: 2026-07-10
updated: 2026-07-10
source: https://www.youtube.com/watch?v=8wsM0euQOvc
published: 2026-07-09
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - ai-agent
  - loop-engineering
  - sub-agent
---

## Loop Engineering 核心概念

- Loop engineering 的核心：你不再是寫 prompt 驅動 agent 的人，而是把它變成一個「自己寫 loop」的系統——agent 自主處理一切，邊做邊學、從遇到的問題成長、自己決定下一步。
- 依結果可分兩大類：**deterministic loop**（結果已知，agent 有可靠方式對照檢查自己的工作，做到達標為止）與 **non-deterministic loop**（結果未知，沒有可靠的自我檢查方式，需要其他機制把關）。
- Loop 燒 token 的印象多半來自「用錯類型的 loop 做錯的工作」；選對類型才划算。

## Stateless Loop（無狀態迴圈）

- 所有其他 loop 的基礎積木。特徵：**不保存任何狀態、不自我改進**——沒有從過程中學習變聰明的環節，因此是最簡單的 loop。
- 經典例子是 Ralph loop：同一任務重複執行、不留記憶，偵測到任務完成即停。
- Claude Code 的 goal command 是最佳示範：在 goal 指令後描述要建的東西，Claude 設為目標開始工作；每當主 agent 認為任務完成，會用較小的模型（Claude Code 中是 Haiku）比對 prompt 需求複查，沒做完就 reprompt 主 agent 補完。
- 弱點：完全仰賴模型自行判斷「做完了沒」，沒有客觀標準。因此最適合**需求可以用硬性方式驗證**的功能。
- 搭配測試的作法：先寫好測試再叫 Claude 實作，goal 設為「讓該功能通過所有測試」，agent 寫 code → 跑測試自查 → 直到全綠才標記完成。測試齊全後才能放心給 agent 真正的自主權。
- 建議在 `CLAUDE.md` 加一行：**每個可運作的版本都存檔**。app 之後被改壞時，agent 可直接回滾到最後可用版本繼續，而不是憑記憶撤銷變更。

## Learning Loop（學習迴圈）

- 與 stateless 相反：不是做完一件事就停，而是**持續改進一個會重複使用的東西**（skill 或 workflow）。
- 運作方式：執行 skill → 觀察表現 → 依所學改進，並完整記錄每一課；之後實際使用該 skill 時，agent 知道過去什麼會出問題而避開。
- 實作：建立一個 skill loop command 觸發迴圈，指令內容是呼叫一個 skill improver agent，並持續呼叫直到沒有可改進之處。使用時執行 command 並傳入要改進的 skill 即可。
- 迴圈分多輪進行。每輪改動後跑一組測試與檢查，並啟動獨立的 Claude session 在背景執行（只吃傳入的 prompt、不停下來要權限、回報輸出）。
- Session 內會**用 skill 與不用 skill 各跑一次實作**，量測 skill 的實際影響，據此精準找出要改的地方並直接修改。
- 關鍵產物是 skill 內的 `learning.md`：一份結構化的改進日誌，記錄每輪嘗試了什麼、有無 skill 的結果各如何、以及累積的教訓——agent 靠它知道什麼有效、什麼沒效，一輪輪把 skill 磨到最佳版本。

## Multi-Agent Review Loop（多代理審查迴圈）

- 單一 reviewer agent 獨扛所有審查面向會有盲點；review 本質上就該來自多重視角。多個 agent 分別從不同維度審查，能互補彼此的盲區，讓審查完整得多。概念接近 Andrej Karpathy 發布的 LLM Council——多個 agent 互相討論、辯論議題，用多模型的推理收斂到正確答案。
- 範例配置四個 agent：
  - **事實正確性檢查**：配 web search 等工具，能對照真實來源。
  - **Domain checker**：檢查被審查的內容是否真的切合目標。
  - **Safety critic**：看敏感內容、安全風險、政策違規等日後可能出事的點。
  - **Style critic**：確保內容清楚、寫得好、符合目標風格。
- 四者由一個 orchestrate command 串起：內含管理與協調全部 agent、處理各自回報 feedback 的詳細指示。執行 command 指定要審查的對象即可啟動。
- 同樣多輪運作：每輪把所有 agent 都轉起來，主 agent 套用第一輪回報的修正後，再全部啟動跑下一輪；最後一輪結束時 app 狀態明顯更好。
- 若想讓 agent 彼此直接溝通，可改用 agent teams 工作流（更接近 LLM Council 體驗）；影片作者仍選 orchestrator，因為需要一個 agent 持有前幾輪的 context 才能正確協調流程。此類 agent 不限 coding，任何任務皆可用。

## Verification Loop（驗證迴圈）

- 雙 agent 結構：一個負責實作、一個替實作打分數，實作者的唯一目標是把指定指標的分數拉到最高。整個審查工作流由一個自建 command 協調。
- 以 Cursor 的 thermonuclear review 為評分核心：強力的 code review skill，檢查程式碼的乾淨與健康程度，用不可妥協的標準做深度審查，確保後續好維護。它跑 dynamic workflow——把審查面向 fan out 給多個 subagent 同時處理。
- 兩個角色：**implementer** 讀 PRD 實作功能；**thermonuclear code reviewer** 只回傳審查分數，不配編輯工具（只審不改）。
- 流程：執行 review loop command → 先理解 app 目標 → 跑第一輪 thermonuclear review → 把發現（含阻擋 app 啟動的 critical 問題）記進 JSON 檔 → 啟動 implement agent 修復 → 持續循環。
- 成本警告：審查維度多、dynamic workflow 又同時展開大量 subagent，**非常耗時且燒 token**。建議只在整個 app 已具規模、需要徹底審查時使用；也可改用普通 reviewer agent 建同款 loop（不用 dynamic workflow），省時省 token。

## Workflow Improvement Loop（工作流改進迴圈）

- 前面所有 loop 都缺「改進 loop 本身」的步驟，而那才是 loop 該做的核心。此 loop 不只重複任務，還回頭檢視流程本身並提出改進——與 learning loop 的差別：learning loop 改進的是流程中的一個元件（skill），這個改進的是**整個流程**。
- 入口是 iterate command，作為每輪執行的 orchestrator。三個 agent：
  - **Builder**：負責實作，每輪交付 app 的一項需求。
  - **Scorer**：依預先定義的 rubric（app 的品質護欄）評分（滿分 100），分數記進追蹤每輪的 JSON 檔。
  - **Process optimizer**：真正負責自我改進的角色——在一般 loop 的 plan → implement → verify → repeat 循環外，多一步回顧該輪迭代、提出讓工作流更好的建議，確保 app 高品質、步驟正確。
- 使用方式：執行 `iterate all`（把整個 app 拆成多個部分放進單一 workflow 實作）。
- 最終產出不只是蓋好的 app，還有一套**經過測試與精煉、每個步驟都被驗證過確實必要**的工作流。
