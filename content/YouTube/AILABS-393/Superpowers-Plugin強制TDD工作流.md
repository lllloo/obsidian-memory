---
title: Superpowers Plugin 強制 TDD 工作流
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-25
source: https://www.youtube.com/watch?v=romGzY0Xu0s
---

## Superpowers 是什麼

Superpowers 是強制執行傳統軟體開發方法論的 Claude Code plugin（24 小時獲得 58,000 stars）。核心差異：不只是 spec 撰寫框架，而是帶有**嚴格 gates** 的執行強制，未通過當前步驟不得進入下一步。內建 TDD、DRY、YAGNI 等開發原則，所有 best practices 都原生整合，不需手動設定。

安裝方式：

```bash
# 先 register marketplace command，再從 marketplace 安裝
# 重啟 Claude Code 後生效
```

## 開發流程

**Brainstorming phase：**
- 自動啟動，不猜測需求，主動提問釐清 app、目標用戶、tech stack
- 給出三個架構方案供選擇
- 提供 UX 設計、專案結構確認
- 所有決策記錄到 `docs/` 資料夾
- 內建 Git commit 每個變更（其他框架需手動執行）

**Planning phase：**
- 將大型應用拆解為可實作的子任務
- 與 Claude 內建 plan mode 的差異：Superpowers 是「執行強制」，Claude plan mode 只是「給 agent 的指引」

**Implementation phase（Sub agent 驅動）：**
- 自動為每個 sub agent 建立獨立 git work tree
- Agents 彼此隔離，避免相互覆蓋
- 每個任務完成後啟動獨立 review sub task 驗證實作
- Code reviewer 通過才進入下一個任務
- 完成後詢問是否 merge 到 main 或建立 PR，並清除所有 work trees

注意：Context 消耗快，一次迭代約用掉 50% context window，適時執行 `/compact`。

## TDD 強制執行

Agents 先寫測試，再寫實作，禁止修改測試檔案：

```
# Prompt cue 範例
如果有 1% 機率需要使用 skill，就使用它
```

測試失敗時，plugin 阻止 Claude 修改測試，強制修正實作。

## Systematic Debugging

四階段系統化除錯：

1. 識別根本原因（提問定位）
2. 隔離 bug
3. 縮小實際原因
4. 套用修復 + 測試驗證

## 彈性使用策略

不需要完整流程的任務（如純 UI 調整）可只執行 brainstorming + planning，再另行請 Claude 直接實作，省去流程開銷。Plugin 會維持一致的 Git commit 格式。

**建議原則**：Claude 擅長的事讓它自由處理；容易失敗的複雜實作才啟動完整流程。
