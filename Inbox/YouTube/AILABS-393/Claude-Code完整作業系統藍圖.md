---
title: Claude Code 完整作業系統的藍圖
description: 把 Claude Code 類比成作業系統，CLAUDE.md 為 kernel、MCP 為 driver、skills 為程式、loops/routines 為排程，並以 Opus 4.8 推出的 dynamic workflows 串起整個系統。
created: 2026-06-04
updated: 2026-06-04
source: https://www.youtube.com/watch?v=5LnwJyi1il4
published: 2026-06-03
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - ai-agent
  - automation
---

Claude Code 已從單純的 coding agent 演變成一套協調整台機器的「作業系統」。本片把各個元件對應到傳統 OS 的層次，並聚焦 Opus 4.8 推出的 dynamic workflows 如何把整個系統串起來。

## Claude Code 對應作業系統的各層

作業系統由多個缺一不可的部件組成，Claude Code 各元件對應如下：

- **Kernel（核心）→ `CLAUDE.md` 與 context 檔案**：OS 的 kernel 是控制所有操作的核心層。`CLAUDE.md` 是整個 agent 的驅動程式，若沒設定好，agent 抓不到專案真正的需求，其他部件也會跟著垮。
- **Drivers（驅動）→ MCP**：driver 讓系統與外部裝置互動。Claude 需要外部工具時，透過 MCP 取用並呼叫該工具完成工作。
- **日常程式 → skills 與其他 commands**：存放可重複任務的結構化指令，需要時隨時呼叫。
- **Scheduler / cron → loops 與 routines**：OS 需要排程器在指定時間跑特定任務。Claude Code 近期加入的 loops 與 routines 就是它的 cron job，自動化重複工作，不必盯著它跑。

設定上比真實 OS 輕鬆，不需要灌一堆驅動程式。

## Dynamic Workflows：串起整個系統的關鍵

dynamic workflows 是隨 Opus 4.8 推出的功能，是把整套系統收尾成完整 OS 的那一塊。

- 本質是可重複的指令，會 spawn 多個 agent 來執行被設計的任務。
- 觸發方式：在 prompt 中使用關鍵字 `workflow`。但日常 prompt 也常用到這個字，所以只有當 prompt 真的表達「建立 workflow」的意圖時才會觸發，不會每次都觸發。
- 與其他架構用 markdown 不同，workflow 產生的是 **JavaScript 程式碼**，存放在 `.claude` 資料夾下的 `workflow` 目錄，用整段 script 控制全程。
- 計畫不再活在 context window，而是寫進程式碼，定義 sub-agent 要怎麼一步步執行。
- 它定義嚴格的 schema（等於給 sub-agent 的「表單」），讓輸出符合固定格式；每個 agent 帶著 prompt 與該滿足的表單被呼叫，持續工作直到輸出符合 schema，才回傳結果。

### 呼叫與管理

- 用 slash command 加 workflow 名稱來呼叫，再把要壓力測試的 plan 交給它。
- 它在背景執行，你可以繼續做自己的事。
- 用 `workflow` 指令查看進度：可看到每個 workflow 的各階段、各 agent 呼叫的 model，以及每個任務燒掉多少 token。
- 若 session 在 workflow 執行中結束，進度不會遺失：跑 `resume` 指令即可續跑。每個 workflow 有自己的 ID，resume 時會把快取的 agent 工作從記憶體拉回，從中斷處接續。

## 何時該用 Workflow（成本與判準）

此功能仍在 research preview，dynamic workflows 比一般 Claude Code session 消耗多很多 token，因為底層用多個 sub-agent，每個都跑在獨立的 context window，可能幾小時就燒光 $200 方案。判斷是否該用的關鍵指標：

- **任務能拆成獨立單元**：agent 之間若互相依賴就會互等，失去平行性，spawn workflow 就沒意義。依賴度越低，平行性越好、結果越快。
- **任務大到需要多個 context window**：workflow 的多個 sub-agent 各有自己的 context window，任務要夠大才需要這些分開的視窗，否則只是浪費。每個 sub-agent 跑在全新 context，只回傳結果，其餘推理留在程式碼檔、不進主 context window。
- **任務值得驗證**：當答案出錯的代價高到需要交叉驗證才能往下走時才用，例如 security findings、bug claims、migrations。但驗證會多花 agent、燒 token 與時間，要確定值得。
- **任務是 deterministic**：workflow 用程式碼以固定結構呼叫 agent。若任務需要 agent 在執行時自行評估下一步要做什麼（非 deterministic），就不適合 workflow。

## Workflow vs Goal：寬與深

| | Workflow | Goal |
|---|---|---|
| 決定方式 | deterministic，程式碼決定發生什麼 | 非 deterministic，系統決定下一步 |
| 任務形狀 | 寬（wide）：拆成多個可同時跑的 sub-task | 深（deep）：一次一個任務、逐步深入 |
| 平行 | 呼叫多 agent 平行迭代 | 一次一個任務，不平行 |

選擇時看任務的「形狀」：wide 用 workflow，deep 用 goal。只有任務真的合適時才動用 workflow，以免浪費 token。

對照 skills：skill 是給「需要引導步驟的任務」的可重複指令，但 skill 由單一 agent spawn、同一 agent 讀它的指令，只是把 agent 已會的事做得更好，**不處理長任務**。

## 內建 workflow：deep research

Claude Code 內建一個 dynamic workflow 叫 deep research，等於過去要手動用多個 context 檔與 `CLAUDE.md` 搭出的多步研究 pipeline，現在可從任何專案直接呼叫。它分五個階段、一階接一階：

1. 搜尋資訊
2. 從找到的來源抓取細節
3. adversarial verification 交叉驗證各項主張
4. 把通過驗證的內容綜合成一份最終文件

每個 sub-agent 從 parent 繼承工具；非常吃 token，影片中一次小主題的執行就用掉約 100 萬 token。

除了多步研究，也能自建其他研究 workflow。片中示範一個競品研究 workflow：分四個階段，檢查競品表現、找出其競爭優勢，最後回報。該次執行用掉 67.9 萬 token、34 個 agent，產出完整 markdown 報告；它還會自我改進——遇到問題就套用修正，下次就不再撞同樣的問題。

## 應用一：第二大腦（非程式專案）

把整套 OS 套到 second brain 設定：

- **Kernel → `CLAUDE.md`**：存放如何導覽整個系統的資訊。
- **日常程式 → skills**：承載反覆要做的任務指令。建立方式：在長 session 中發現某件事會常做時，直接請 Claude 把該 session 的學習整理成一個 skill。
- **記憶 → vault 中建立與維護的所有檔案**：記錄你做了什麼、怎麼做，給 Claude 完整 context。
- **外部來源 → MCP**：片中配置 Google Calendar 與 Notion MCP，讓它讀取 Notion 專案檔並同步資料、讀行事曆、建立與更新項目；應遵循的確切格式記在 `CLAUDE.md`。
- **Workflows**：最重要的一塊，讓重複任務平行化交給 sub-agent。片中的 morning brief workflow 會 spin up sub-agent 跨多來源蒐集資訊，回傳一份晨間簡報。
- 用一段時間後應建一個 **audit workflow**：檢查死連結、揪出設定中的每個問題並回報，再據此修復、保持第二大腦的健康。

## 應用二：程式專案

同樣的 OS 模型套到 coding 專案：

- **Kernel → `CLAUDE.md`**：放入所有專案資訊。
- **日常程式 → 為專案配置的 agents**。
- **Hooks**：針對不同情境設定，例如 agent 編輯完檔案後自動格式化。
- **Skills**：為不同任務建立，例如新增 endpoint，讓每個 endpoint 都遵循你要的 schema。
- **Workflows**：例如 ship 前 review 變更、遷移程式碼庫或資料庫、跑 end-to-end 測試確認整個 app 可運作。
- Context 變成 docs 資料夾中的檔案與程式碼本身。

workflow 對專案遷移特別有用：可建一個把整個專案從一個 library 轉成另一個的 workflow，讓各 agent 處理轉換。片中實測同一遷移，沒用 workflow 要超過一小時，用 workflow 只花 21 分鐘。
