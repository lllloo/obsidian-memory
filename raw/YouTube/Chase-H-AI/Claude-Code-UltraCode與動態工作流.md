---
title: Claude Code UltraCode 與動態工作流
description: 拆解 Claude Code 的 UltraCode 與 dynamic workflows——用客製化 harness 與多 sub-agent 對付大型複雜任務，對抗 context rot、agentic laziness 與 goal drifting。
created: 2026-06-08
updated: 2026-06-08
source: https://www.youtube.com/watch?v=6cmi7qyFwEE
published: 2026-06-07
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - sub-agent
  - workflow
---

## UltraCode 是什麼

UltraCode 與 effort level 綁定。在 Claude Code 輸入 `/effort` 會看到從 low 到 UltraCode 的等級光譜；Opus 4.8 預設為 high。輸入 `/ultracode` 會同時觸發兩件事：

- effort level 從 high 拉到 extra high（注意不是 max，而是介於 high 與 max 之間的 extra high）。
- 自動開啟 dynamic workflow orchestration——Claude Code 會自行判斷某個 prompt 需不需要動態工作流。

換句話說，UltraCode 是一層自動判斷：複雜任務就走動態工作流，簡單任務維持靜態 harness，使用者不必自己決定。

## 靜態 harness vs 動態工作流

- **靜態 harness（預設）**：單一 session、單一 context window，不主動拆 sub-agent、不做對抗式自我審查。耗 token 少，給通用答案。多數問題夠用。
- **動態工作流**：針對問題建出客製化 harness（novel 的解題路徑）。引入多個各司其職的 sub-agent，各自帶獨立 context window 與聚焦目標，最終給出針對性結論。

以「該不該把 checkout 服務換供應商」為例：靜態 harness 只做幾次 web search 再摘要；動態工作流則會去讀帳務程式碼、比對新供應商文件、估算交易量定價、派一個 devil's advocate agent 反駁，最後給出具體建議而非通用答案。

## 觸發方式

- `/ultracode`：交給 Claude Code 自動判斷是否需要動態工作流。
- `/workflows`（或自然語言「use workflows」）：強制為當前 prompt 建立動態工作流，類似手動 invoke 一個 skill。

## 為什麼需要動態工作流

單一 context window 處理複雜任務時間一拉長，表現就變差。Anthropic 部落格〈A Harness for Every Task: Dynamic Workflows in Claude Code〉點名的三個問題都可歸入 context rot：

- **Agentic laziness**：交付大範圍任務時只做一部分。
- **Self-preferential bias**：Claude 傾向偏好自己的產出，尤其被要求對照 rubric 自評時。同一 context window 內自評自己的程式碼特別不可靠。
- **Goal drifting**：複雜任務跑久了會偏離原始目標。

解法是用動態工作流把任務拆給多個獨立 sub-agent，各自帶 fresh context window 與隔離的聚焦目標——與 GSD、superpowers 這幾個月的方向收斂到同一點：用有限 context window 處理大任務，最終都回到 sub-agent 與 fresh context。

## 工作流模式（workflow patterns）

部落格列舉的幾種模式（非窮舉），動態工作流會自動判斷該套哪一種：

- **Classify and act**：任務含多個子任務，先用 classifier 分流再派給合適 sub-agent。
- **Fan out and synthesize**：deep research 型，從大量（可能上百）來源抓資料，不只摘要，還要交叉驗證，最後產出整合報告。
- **Adversarial verification**：對抗式驗證。
- **Loop until done**：迴圈直到完成。
- **Tournament-style**：多組想法與評審競賽，最後選出贏家。
- **Generate and filter**：生成後過濾。

## 底層運作與 deep research demo

動態工作流在 runtime 實際執行一段 script（與 agent teams 機制不同），且工作流可儲存重複使用，性質類似 skill。

Claude Code 內建一個預載的 deep research 動態工作流，與 web app 上既有的 deep research 類似。更新版的 Claude Code 直接輸入 `/deep research` 加上 prompt 即可。啟動後會在背景跑，分五個階段：

```
scope → search → fetch → verify → synthesize
```
