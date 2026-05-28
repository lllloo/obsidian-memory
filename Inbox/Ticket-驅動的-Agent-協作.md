---
title: Ticket 驅動的 Agent 協作
created: 2026-05-27
updated: 2026-05-28
source: https://www.youtube.com/watch?v=M_AmPWmkpwA
published: 2026-05-02
tags:
  - ai-agent
  - harness
  - workflow
---

**coding agent 的瓶頸已從模型能力轉移到人類的注意力。**「人類在哪一層介入」因此成為協作設計的核心問題——這是 OpenAI Symphony 帶來的 paradigm 判斷，比「主 agent 如何拆派子 agent」（機制層，見 [[Claude-Code-多-Agent-協作]]）高一個層級。

## 從管 session 到管 ticket

coding agent 的用法演進：auto-complete → 單一互動式 session → 同時開多個 isolated worktree 平行處理。但人在 3 個以上 session 下會頻繁 context switch、甚至把指令送錯 thread——管多 session 的工具（Superset、Conductor）治標不治本。

關鍵觀察：**軟體工作流本來就以 deliverable（issue / ticket / milestone）為單位**。工程主管管上千人不是逐 PR 審查，而是看最終產出。解法是把人往上抬一層——**人管 ticket，agent 在 ticket 層工作並透過 ticket 回報**，ticket tracker 變成 durable **state machine**，人不必盯個別 session。

## 架構三元件

- **Scheduler**：背景程序定期掃 board，發現 to-do ticket 就建 isolated workspace、起 agent session、管 lifecycle。
- **workflow.md**：repo 內版控的單一設定檔——YAML frontmatter = scheduler 設定（撿哪種 status、平行上限、workspace 建好跑哪些 programmatic hook 把環境備好）；Markdown body = 每回合渲染給 agent 的 system prompt（此 repo 的 ticket SOP、如何驗證、何謂完成、何時找人）。
- **外部 state machine**：Linear / Jira / Trello 等，承載 ticket 狀態流轉。

設計刻意保持彈性：不綁 Linear、不綁特定 agent，官方用 `spec.md` 描述設計，可丟給任何 coding agent 改寫到別的 tracker 或語言。

**為何優於自建 admin panel / UI**：config 與 code 同放、版控、走一般 PR 修改；新增 agent 能力 = 改一份 markdown，其餘流程自動跟上。

## Harness 前提：agent 能 atomically 完成 ticket

Symphony 能跑的前提是環境調好，讓 agent 拿到所有需要的東西。harness 三件事：

1. **可開機**：一個 script 備齊環境，agent 不必摸索。
2. **文件 index**：`CLAUDE.md` / `agents.md` 編好主題索引。
3. **自我驗證**：實作完能跑端到端測試並附證據——**多數團隊缺這項**。

補自我驗證的高 ROI 解是 **Playwright CLI（不是 MCP）**：MCP 在 context 常駐、不用也吃 token；CLI 是按需呼叫的 skill，且內建 `video start/stop` 把 session 錄成影片直接 upload 到 ticket 供人驗證。這呼應 vault 反覆出現的立場——**通用 CLI / skill 按需呼叫優於常駐 MCP**（見 [[Harness-Engineering]]）。

## 相關

- [[AI開發者商業定位]] — agent 接管工作流的商業 / 職涯視角
- [[Harness-Engineering]] — 「狀態外部化」被推進成「ticket 系統即 state machine」
- [[Claude-Code-多-Agent-協作]] — 機制層的子 agent 拆派，與本篇協作拓撲層互補
- [[Codex-Goals-長任務迴圈]] — 單一長任務的迴圈封裝，ticket 內的 agent 可用它跑
