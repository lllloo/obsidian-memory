---
title: Claude Code Agent Teams 協作
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-09
source: https://www.youtube.com/watch?v=MSyWjPDrHJw
parent: "[[01.index]]"
---

## Agent Teams vs Sub Agents

| 面向 | Sub Agents | Agent Teams |
|------|-----------|-------------|
| 平行執行 | 是 | 是 |
| Agent 間溝通 | 否（需透過 orchestrator 或寫檔案） | 是（直接溝通）|
| 每個 agent 是否獨立 session | 否 | 是（完整獨立 terminal session）|
| 管理方式 | Orchestrator 協調 | Team lead 開啟/關閉成員 |

Agent teams 的核心改善：解決 sub agents 無法直接溝通的問題，team members 可透過共享 mailbox 傳訊息。

## 啟用方式

```bash
# 目前實驗性功能，預設關閉
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

狀態儲存在 `.claude` 資料夾，以任務名稱識別。

## 架構

- **Team lead**：建立團隊、分配任務、協調工作、合成結果、優雅關閉成員
- **Team members**：從 shared task list 取得任務並執行
- **Shared mailbox**：members 之間直接溝通
- **Shared task list**：所有 members 可見的待辦清單

## 使用案例

**Code review + fix 平行化：**
- Member 1：找出 codebase 問題，逐 bug 傳訊給 Member 2
- Member 2：Member 1 找到問題後立即開始修復，同時 Member 1 繼續找下一個
- 效果：review 與 fixing 同時進行，大幅縮短時間

**多視角除錯（4 個 agents）：**
- 各 agent 從不同角度調查同一個 bug
- Team lead 等待所有 agents 完成後分析匯總
- 2-3 分鐘完成 vs 線性調查需 5-10 分鐘
- Token 消耗大（每個 agent 有獨立 context window）

**長期任務平行建構（6 個 agents）：**
- 2 個 agents：研究 + 建立基礎環境（安裝依賴、設定環境）
- 4 個 agents：各負責一個頁面（等待環境就緒後才解鎖）
- Agents 彼此溝通確保 fonts、styling 一致性
- 整個流程消耗約 170k tokens，從單一 prompt 完成整個 app

## Best Practices

- **明確 scope**：在 prompt 或 task 文件中定義每個 agent 的工作範圍
- **獨立任務**：agents 不應同時編輯相同檔案（會造成衝突）
- **提醒 team lead 等待**：主 agent 有時會不耐煩，自行接手 member 的任務
- **任務大小要適中**：太小 → 協調開銷高；太大 → 失敗浪費大
- **監控執行**：發現 agent 偏離時立即介入給予新指令
