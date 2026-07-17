---
title: pi-workflow 編排 harness 與本 vault 的分野
description: pi-workflow 這類命名工作流編排器定性為「編排層」prior art，說明它與本 vault「知識組織層」的分野，及為何其命名 workflow 目錄機制不宜引入
created: 2026-07-15
updated: 2026-07-17
source: "https://github.com/AgwaB/pi-workflow"
published: ""
parent: "[[wiki/01.index]]"
tags:
  - agent-framework
  - ai-agent
  - coding-agent
---

# pi-workflow 編排 harness 與本 vault 的分野

[pi-workflow](https://github.com/AgwaB/pi-workflow)（AgwaB）是給 Pi agent 用的**命名工作流編排 CLI**：把 subagent worker 依 stage graph 串起來跑，結果在 stage 間傳遞，run 記錄可 inspect／stop／resume，並附一個唯讀 board TUI。用法是自然語言喚起某個命名流程（"用 deep-research workflow 研究這個 repo 並總結架構取捨"）。

評估緣起：被問「本 vault 能不能參考 pi-workflow 的流程」。結論是**當編排層 prior art 可以，當要引入的模板不行**——它解的問題在本環境已被更貼合的工具解掉。（強度：源自 pi-workflow README/docs 自述，未實跑；定性判斷，非實證比較。）

## 它是什麼（編排層）

- **6 種 stage pattern**（截至查核時 README 列舉，數量與命名以官方為準）：`single`（單步）／`foreach`（扇出）／`reduce`（綜合）／`loop`（有界重複）／`dag`（巢狀圖）／`dynamic`（自適應編排）。
- **4 個內建命名流程**（同上，數量隨版本可增減）：deep-research（查證＋附引用建議）、deep-review（多視角 code/design 審查）、spec-review（需求可追溯）、impact-review（變更風險分析）。
- run artifact 存 `.pi/workflows/`，可檢視可續跑；`workflow-guide` skill 供自建專案流程的 scaffold＋validate。安裝需 Node 22+（確切 minor/patch 版以官方 changelog 為準）。

用 [[Building-Effective-Agents-Anthropic]] 的二分法定位：pi-workflow 屬 **workflow**（LLM 與工具走**預先定義的程式碼路徑**、路徑固定可預測），不是動態自主的 agent。其 stage pattern 直接對應該文五種編排模式：`foreach`＋`reduce` 是**路徑固定**的 parallelization（扇出項目預先定義、再綜合），而 [[多智能體研究系統-Anthropic]] 的 orchestrator-worker 關鍵在**子任務非預先定義、由主控動態委派**，較貼近 pi-workflow 的 `dynamic`（自適應編排）pattern，不是 `foreach`＋`reduce`。

## 兩層分野

關鍵定性：**pi-workflow 是「編排層」（怎麼協調多 agent 分工），不是「知識組織層」（知識怎麼編譯、互聯、維護）。**

| | pi-workflow 觸及 | 本 vault 核心資產 |
|---|---|---|
| 知識組織層 | ✗ 不碰（`.pi/workflows/` 只是流程 run 記錄，非複利知識） | ✓ Karpathy LLM Wiki 三層架構＋Ingest/Query/Lint（見 [[LLM-Wiki-知識管理模式]]） |
| 編排層 | ✓ stage graph 編排器 | 已有等價物（見下） |

**知識層無可借**：本 vault 的價值在知識編譯一次後持續互聯維護（複利資產），pi-workflow 完全不處理這件事。

**編排層已被覆蓋**：stage graph（扇出→驗證→綜合、loop-until、resume）在本環境已有——(1) Claude Code 內建 **Workflow 工具**本身就是 stage graph 編排器：能做 stage graph 串接、fan-out/pipeline 平行、loop-until 迴圈、對抗式 verify，run 可 resume 續跑（介面識別名隨版本可變），功能上是 pi-workflow 的對應甚至超集；(2) 具體流程也已 codify 成 skill：`deep-research`（扇出＋多票對抗查證＋綜合）≈ pi-workflow 的 deep-research，`mini-research`（一項目一 subagent、成本可控）是它沒有的省成本變體。

## 為何不引入其命名 workflow 目錄機制

不建議把 pi-workflow「建一批命名 workflow 目錄」的機制搬進 vault，兩個理由：

1. **職能重疊**——編排本來就有 Workflow 工具＋既有 skills 撐著，再鋪一層是重複。
2. **更硬：違反本 vault 反過度工程紀律**——`schema/MEMORY.md` 明訂 skill 升級要**同一流程滿 3 次**才提議、deep-research 回存刻意**不開** skill。先鋪一堆流程正是要避免的。這條紀律的實證支撐見 [[AI-自主工作流的實證檢驗]]（越複雜的編排未必換到更好結果）。

**唯一值得留意的啟發**：它把 review 拆成 deep-review／spec-review／impact-review 這種「命名、可重複、多視角」的清單化思路。若本 vault 某個流程日後真的重複滿 3 次、且長出既有 skill 沒有的專屬結構，再考慮 codify——不是現在。

## 交叉引用

- [[Building-Effective-Agents-Anthropic]]——pi-workflow 在 workflows/agents 二分法中的定位與五種編排模式對應。
- [[多智能體研究系統-Anthropic]]——orchestrator-worker 架構（子任務動態委派），對應 pi-workflow 的 `dynamic` pattern；其 `foreach`／`reduce` 則較接近路徑固定的 parallelization。
- [[LLM-Wiki-生態實作比較]]——本 vault 採用拍板的相鄰比較頁（那頁比的是知識層實作，本頁補的是編排層工具的分野）。
- [[LLM-Wiki-知識管理模式]]——本 vault 知識層的設計原型，pi-workflow 不觸及的那一層。
- [[Agent-Harness-Engineering-框架綜述]]——harness 工程的 workflows/agents 二分綜述，本頁「編排職能已被 harness 覆蓋」的定位即座落於此主軸。
- [[Context-優先與多-agent-的適用邊界]]——多 agent 何時才划算的判準頁（含 Cognition／MAST 反面實證），支撐本頁「先鋪一層命名 workflow 違反反過度工程紀律」的論點。
