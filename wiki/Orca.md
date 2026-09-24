---
title: Orca
description: Orca multi-agent IDE 的架構與運作機制：worktree 隔離、terminal 管理、supervised loop 與協調合約
created: 2026-09-24
updated: 2026-09-24
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - agent-framework
  - dev-environment
---

# Orca

Orca 是一套面向多 agent 協同開發的整合開發環境（multi-agent IDE / ADE）。它將 git worktree 檔案隔離、虛擬終端（terminal）生命週期管理以及監督式多 agent 協調運行時（orchestration runtime）整合為系統一級公民，使人類開發者或協調者 agent（coordinator）能夠有組織地編排、監控並指派多個 coding agent 平行執行任務。

相較於一般的終端多工工具（如 tmux 或 [[Herdr-使用方法]]）或單純的派工看板（如 [[Multica-與-agent-看板的用法與適用邊界]]），Orca 的核心特色在於建立了一套具備狀態機、持久化信箱與合約約束的監督式協作架構（supervised loop）。

## 核心概念與實體架構

Orca 將協調與執行切分為五個核心實體：

```
Run（協調作業容器）
 └── Task DAG（工作單元與相依性）
      └── Dispatch（單次執行嘗試，綁定 Terminal 與 Capability）
           └── Terminal（虛擬終端，運行特定 Agent）
                └── Worktree（獨立 git 分支檢出，檔案系統隔離）
```

- **Worktree**：獨立的 git worktree 檢出目錄。為平行運行的 agent 提供檔案系統層級的實體隔離，防止多 agent 在同一個 working tree 內同時修改產生混亂。Worktree 可綁定 GitHub Issue、Linear Issue 等工作項目上下文。
- **Terminal**：Orca 運行時管理的虛擬終端執行個體（具備唯一句柄，如 `term_<uuid>`）。Terminal 支援串流讀取、PTY 輸入注入（send）、命令派發與終端狀態等待（wait exit / tui-idle）。
- **Run**：一次多 agent 協調作業的頂層容器（如 `run_<id>`）。界定本次編排的根目錄、Task 集合與非同步訊息信箱。
- **Task**：Run 內部 DAG（有向無環圖）中的工作單元。具有嚴謹的狀態機（`ready`、`running`、`succeeded`、`failed`、`blocked` 等）與前置相依性。
- **Dispatch**：Task 的一次具體執行嘗試（attempt / context，如 `ctx_<id>`）。每個 Dispatch 綁定特定的終端與專屬能力憑證（Dispatch Capability，如 `dcap_<id>`）。當某次執行因異常中止或失敗而需要重試時，原 Task 會建立全新的 Dispatch，使前次嘗試可能殘留的晚到訊息或無效心跳無法干擾新的執行。

## Skill 分工判準：orca-cli 與 orchestration

在 Orca 體系中，agent 的操作能力分為兩大層次，分別由兩個 repo-local / 官方 skill 承載：

| 比較維度 | `orca-cli` | `orchestration` |
|---|---|---|
| **核心定位** | 完整交棒（full handoff）與底層環境操作 | 監督式協調（supervised coordination）與流程編排 |
| **協作模式** | 觸發後即交出主導權，原 agent 退場結束回合 | 協調者持續在場監控、等待結果、處理問答與決策 |
| **典型場景** | 「交給另一個 agent」、「換到另一個 worktree 繼續」 | 複雜任務分解、多 agent DAG、需要結果審查與錯誤重試 |
| **管理範圍** | Worktree 增刪查改、Terminal 控制、內建 Browser、排程（Automations）、成果（Artifacts）發布 | Run 建立、Task 定義、Worker 派發（worker-start）、事件監聽（check --wait）、問答仲裁（reply）、終端釋放（release） |
| **完成標準** | 目標 worktree/terminal 與 prompt 送出成功即可結束 | 所有子任務達到確定 outcome、信箱清空、終端資源結清後始得回報人類 |

## CLI 執行檔解析規則與環境陷阱

在 Orca 的命令規格與文件中，統一以 `ORCA` 作為執行檔佔位符。在實際操作與腳本撰寫時，必須注意以下解析規則與命名衝突：

1. **實際執行檔名稱**：
   - 本機安裝的正式發布版 CLI 執行檔為 `orca-ide`。
   - 開發環境（dev build）下則為 `orca-dev`（或 `./config/scripts/orca-dev.mjs`）。
2. **重大陷阱：GNOME 螢幕朗讀器衝突**：
   - 在標準 Linux 與 GNOME 桌面環境中，系統內建的 `/usr/bin/orca` 是 **GNOME 螢幕朗讀器（GNOME Screen Reader）**。
   - 若在 Orca 環境外或一般 bash shell 中直接裸打 `orca`，系統**不會**啟動 Orca IDE，而是會喚醒螢幕朗讀器語音合成程式。
   - **慣例要求**：在腳本、自動化或 agent 提示詞中，應始終呼叫解析後的具體執行檔 `orca-ide`（或檢查環境提供的 stub 指令），切勿在非受控環境裸跑 `orca`。

## Supervised Loop 協調骨幹

`orchestration` 的協調者（coordinator）以狀態驅動的監督迴圈（supervised loop）管理整個流程：

```
run-create ──> task-create ──> worker-start ──> check --wait
                                                   │
     ┌───────────────────┬─────────────────────────┴────────────────────────┐
     ▼                   ▼                                                  ▼
收到 ask:          收到 escalation:                                   收到 worker_done:
發送 reply 繼續    介入排解或轉派                                    結算 outcome，
                                                                      worker-release / retain
```

1. **`run-create`**：初始化協調 Run 容器，錨定工作目錄與通訊管道。
2. **`task-create` & `worker-start`**：定義 Task 相依 DAG；透過 `worker-start` 分派指定 agent（如 Claude Code, Codex, Antigravity）在指定 worktree/terminal 啟動執行，並注入合約開頭引言（preamble）。
3. **`check --wait`**：協調者進入阻塞等待，監聽旗下所有 worker 的訊息與狀態變更。
4. **`reply` 與仲裁**：收到 worker 發出的提問（`ask`）時，由 coordinator 或轉交人類裁決後回覆，解鎖 worker 的阻塞。
5. **`worker-release` / `worker-retain`**：worker 完成並送出 `worker_done` 後，coordinator 審核產出並確認 Task 達成，隨後執行 `worker-release` 歸檔並關閉終端；若使用者希望保留現場除錯，則顯式標記 `worker-retain`。

## Worker 契約與生命週期義務（Worker Contract）

被分派的 worker agent 在執行期間必須嚴格遵守合約規範，確保協調狀態的確定性：

- **Heartbeat（心跳）**：
  - 任務執行中須依約定頻率（通常為每 5 分鐘）發送一次 heartbeat，回報當前階段（如 `investigating`、`implementing`、`reviewing`）。
  - 心跳僅作為存活證明（liveness），不可代替完成宣告。
  - **豁免條件**：當 worker 正處於 `ask` 或 `check --wait` 阻塞等待回覆時，該連線本身即為存活訊號，免發心跳。
- **Check（檢查協調指示）**：
  - 協調者的指示（如中止任務、調整需求）為非中斷式的持久化佇列，worker 不主動查詢就不會得知。
  - worker 必須在每個自然檢查點（例如開始修改新檔案前、跑完測試後、送出完成前）執行 `check --terminal <handle>`。
  - 若收到 `consumer_fenced`，代表該任務已被 coordinator 取消或轉派，worker 必須立即停手退出，不得送出 `worker_done`。
- **Ask（阻塞式提問）**：
  - 遇到需要協調者決策的事項時，**嚴禁**使用本地互動工具（例如 `AskUserQuestion` 或本機 TUI 彈窗，這會導致無人應答而永久卡死）。
  - 必須呼叫 `orchestration ask` 將問題寫入持久化紀錄並阻塞等待回應；若連線超時，應使用既有的 message ID 進行 resume，不重複建立問題。
- **Worker Done（單次完成回報）**：
  - 任務完成或確定無法繼續時，必須且只能發送一次 `worker_done`。
  - 內容規則：`--body` 必須是精確的 3 句話摘要（做了什麼、發現什麼、剩下什麼），並依真實狀況標註 `--outcome succeeded` 或 `--outcome failed`，嚴禁無聲退出或僅在文字中說失敗。
  - 送出 `worker_done` 後立即結束回合進入閒置（idle），不得繼續輪詢或自行關閉終端。

## 與相鄰工具的定位對照

在多 agent 開發與平行執行的工具光譜中，Orca 的定位如下：

- **對比 [[Herdr-使用方法]]**：
  - Herdr 著重於**終端多工器層**（terminal multiplexer），提供 pane/tab 佈局、五態 agent 狀態自動偵測與基礎的 CLI 派工原語（`agent start/prompt/wait`），本質上是輔助人類即時監看的同步操作層。
  - Orca 則是**全功能 multi-agent IDE**：除了具備完整的 worktree 與 terminal 管理，還內建了以 Run/Task/Dispatch 為基礎的 DAG 編排引擎、強制性的 worker 雙向通訊協定，以及內建瀏覽器控制與排程自動化。
- **對比 [[平行跑多個-coding-agent-的工具選型]]**：
  - 在該頁探討的本機平行方案中，Claude Squad 偏向 tmux + worktree 的輕量 TUI；Emdash 與 Nimbalyst 則屬於獨立的 GUI 開發環境。
  - Orca 提供了深度整合 CLI 與 GUI 運行時的架構，使外部 agent 可以作為 coordinator 自主操控 IDE 內部所有資源，實現「agent 編排 agent」的完整閉環。
- **對比 [[平行-agent-產出的合併與-review]]**：
  - 平行 agent 各自在 worktree 產出後，面臨語意衝突與審查難題。Orca 的 Task DAG 相依性與決策閘門機制，使協調者能在合併前安排對抗式 reviewer agent 或自動化驗證步驟，將平行任務的風險收斂在分派生命週期內。

## 來源與強度標註

- 本頁架構、原語與合約規範取自本機 CLI 官方 skill 規格（一手工具規格，未經第三方對抗查證）：
  - `Orca-CLI-Skill.md`（落地於 `raw/fetched/Orca-CLI-Skill.md`）
  - `Orca-Orchestration-Skill.md`（落地於 `raw/fetched/Orca-Orchestration-Skill.md`）
- 本機執行檔解析與 GNOME 衝突為實際系統環境驗證之具體事實。
