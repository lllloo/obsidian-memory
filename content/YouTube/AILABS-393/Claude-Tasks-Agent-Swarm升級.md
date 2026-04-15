---
title: Claude Tasks 的 Agent Swarm 升級令人難以置信
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-27
source: https://www.youtube.com/watch?v=li8bIt-mjbA
---

## Agent Swarm 的核心概念

Claude Code 推出了重大更新，新的 agent swarm 系統改變了 Claude Code 處理複雜任務的方式。核心想法是讓多個 AI agent 協調處理複雜任務、產生 sub-agents，並平行管理依賴關係。

- 現在可以像跟專案經理說話一樣跟 Claude 溝通，給它一個大型任務，Claude 自動分解並委派
- 任務可以在執行 clear 指令甚至重啟 session 後繼續存活
- 每個 agent 擁有獨立的 context window，不再共用單一 context

過去使用 Claude 時需要頻繁 compact，因為即使任務分解了，最終仍是一個大腦試圖在有限 context window 中保持複雜流程。現在這些手動管理工作已內建到產品本身。

## 任務系統的運作機制

主要的 Claude 扮演**任務協調者**角色，建立任務圖（task graph）：

1. 識別並將工作分解成較小任務
2. 判斷每個任務的類型：
   - **循序**（sequential）：前一個任務完成後才能開始
   - **平行**（parallel）：無依賴關係，可同時執行
3. 每個任務遵循完整工作流程：調查 → 規劃 → 實作，各階段互相鎖定
4. 任務圖建立後，根據複雜度分配不同模型——探索資料夾等簡單任務不需要 Opus，用 Haiku 或 Sonnet 即可

每個 agent 獲得全新的 200K context window，與其他流程完全隔離。

## 任務持久化：外部化到檔案系統

過去任務寫在 context window 中，context 填滿後必須 compact，待辦事項容易在過程中混亂。現在任務改以 JSON 檔案儲存：

- 位置：`.claude/` 資料夾下，每個 session 有一個以 session ID 命名的資料夾
- 每個 JSON 檔案包含：名稱、描述、狀態
- 關鍵欄位：
  - `blocks`：被當前任務阻擋的任務清單
  - `blocked_by`：阻擋當前任務執行的任務清單

這個依賴圖確保正確的執行順序，Claude 無法跳過尚未完成的必要任務。邏輯外部化到檔案結構後，即使 session 結束、終端機關閉，系統狀態也不會遺失。

設定環境變數可用自訂名稱識別 session，確保任務不會因為 ID 變更而遺失。

## 平行化帶來的效率提升

Claude 識別哪些任務可平行、哪些不行，以此節省時間：

- 例如：任務 1 和任務 2 無依賴 → 同時產生兩個 agent 執行
- 任務 3 和 4 被任務 1 阻擋 → 等任務 1 完成後才開始

原本需要五波循序執行的五個步驟，透過平行化只需三個循環就能完成。不僅省時，也降低成本——模型對應任務的複雜度調配資源，不在小任務上浪費多餘 token。

## Co-work 的使用情境

Co-work 本質上是面向非開發者的 Claude Code，有更多護欄防止 agent 意外刪除或破壞不該動的東西，對非技術用戶更友善。

同樣支援 agent swarm 機制，適合用於：

- **整理專案資料夾**：產生多個 agents 批次讀取檔案，為每個專案建立摘要文件
- **可行性與市場研究**：透過問答生成全面的研究報告，儲存到連接的資料夾
- **與 Notion 整合**：管理頻道的內容發想流程

完成研究和 PRD 文件後，交由 Claude Code 負責實際實作。Claude Code 讀取文件、分析 PRD 各節，識別可平行處理的部分，同時產生多個 agents 分頭執行。

## 使用技巧

- Claude 通常自動分解複雜任務，但如果它判斷任務不夠複雜就不會分解
- 可明確提示：「將這個任務分解成有依賴關係的子任務」
- 用 `Ctrl+T` 查看待辦清單
- 長期專案設定 CLI flag 為專案名稱，確保任務即使關閉終端機也能延續
