---
title: 這樣用 Claude Code 準確度更高：七個實用技巧
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-01
source: https://www.youtube.com/watch?v=D5bRTv6GhXk
---

## 根本原因：Context 衰減

Claude Code 準確度下降的根本原因是 context 過滿。前 20% 表現好，到 40% 開始下滑，60%、80% 準確度大幅降低，導致 bug 增加、幻覺 API、最終要手動撤銷更動。

以下七個技巧都圍繞這個問題展開。

## Tip 1：Context 狀態列

在 terminal 底部顯示即時 context 使用百分比，超過 50% 就執行 `/clear` 重置。

**設定方式：** 下載狀態列設定 MD 檔（作者社群提供），貼入 terminal 並要求 Claude 設定。

**自訂外觀選項：**
- Emoji meter（不同階段顯示不同 emoji）
- Fraction（如 `3/100`）
- Hash bar（`###-------`，視覺顯示進度）

設定後在 VS Code terminal 也同步顯示，同時顯示模型名稱、當前 branch、worktree。

## Tip 2：Sub Agents

`/clear` 重置有效但降低生產力。Sub Agents 讓多個 agent 各自持有獨立的乾淨 context，同時並行工作：

```
Orchestrator
  ├── Sub Agent A：後端 API
  ├── Sub Agent B：測試
  └── Sub Agent C：Code Review
```

優點：各 agent context 獨立 → 不累積 → 減少 bug 和幻覺 → 可並行執行。

## Tip 3：Superpowers 框架

在 Sub Agents 之上加一層「如何計畫」的結構：

1. 澄清需求
2. 生成 spec（執行計畫）
3. 建立 to-do list（每個 sub agent 的任務）
4. TDD：先寫測試 → 定義期望行為 → 寫 app logic → 直到測試通過 → 重構

結果：Claude 寫程式前已有完整測試，減少漫無目的的迭代。

## Tip 4：Agent Teams

傳統 sub agents 互不溝通，orchestrator 要自己轉傳資訊。Agent Teams 在所有 agents 之間建立共享通訊頻道：

```
前端 Agent ↔ 後端 Agent ↔ 資料庫 Agent
```

解決多 agent 協作時的資訊孤島問題。

## Tip 5：Context7 — 即時文件

**問題：** LLM 使用過時訓練資料 → 幻覺 API、舊版語法。

**解法：** Context7 即時拉取最新版本文件。

**設定步驟：**
1. 前往 `contextseven.com/dashboard` 取得 API key
2. 複製安裝指令，貼入 terminal 執行
3. 選擇 **CLI + Skills**（比 MCP 更省 token）
4. 選擇 Claude Code，完成設定

**使用方式：** 在 prompt 中加入：「請用 Context7 fetch 相關文件，依最新文件 fact-check 我們的實作。」

適合用在最終 Review 階段，確保程式碼使用正確的 API 和版本。

## Tip 6：NotebookLM 知識庫

**問題：** 把所有研究文件、PRD、最佳實踐一次塞入 context → context 一開始就很大。

**解法：** 把文件存入 NotebookLM，讓 Claude 按需查詢。

**工作流程：**
1. 把研究素材（YouTube 影片、Google Drive、PRD、網頁）存入 NotebookLM
2. 在 `CLAUDE.md` 的 system prompt 指示：「有問題時查詢 NotebookLM」
3. Claude 執行時只在需要時拉取資料，不在啟動時全部注入

**優點：**
- 初始 context 更小
- 資訊更準確（只用你提供的來源）
- 跨 session、跨 sub agent 持久共享

## Tip 7：CLI 優於 MCP

MCP 在 context 啟動時把所有 data schema 全部注入 → context 一開始就大。

CLI + Skills 的運作方式不同：
- Skills 只在「Claude 正在做相關工作時」才載入
- 其他時候不佔 context

**實測比較（Playwright）：**
Playwright CLI 版本比 MCP 版本 token 消耗更少，且準確度更高。

> 趨勢：Google Trends 顯示 CLI 的搜尋量正在超越 MCP。

## 七個技巧總覽

| # | 技巧 | 解決的問題 |
|---|------|---------|
| 1 | Context 狀態列 | 不知道 context 用了多少 |
| 2 | Sub Agents | 單一 context 累積過多 |
| 3 | Superpowers | 缺乏計畫直接寫程式 |
| 4 | Agent Teams | Sub agents 無法互相溝通 |
| 5 | Context7 | 使用過時 API 文件 |
| 6 | NotebookLM | 研究文件塞爆初始 context |
| 7 | CLI over MCP | MCP 在啟動時注入過多 token |
