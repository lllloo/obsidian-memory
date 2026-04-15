---
title: Cursor 錯誤減少 90%：TDD 與記憶體庫
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-04-22
source: https://www.youtube.com/watch?v=dF4uCZAY1tk
---

## 兩個核心技術

針對大型複雜專案，兩個工作流大幅降低 Cursor 的錯誤率：
1. **Test-Driven Development（TDD）**：先寫測試，讓 Cursor 自己迭代到通過
2. **Memory Bank**：讓 Cursor 在跨 session 時保有專案上下文

## TDD 工作流

**適用場景**：複雜函式第一次不會寫對，但你需要精確定義輸入輸出的情況。

**流程：**
```
Create a function that [描述功能].
First write some tests, then implement the code, 
then run tests and iterate code until all tests pass.
```

搭配 **Yolo mode（auto-run）**，Cursor 會自動：
1. 撰寫測試案例（從基礎到邊緣案例）
2. 實作函式
3. 執行測試
4. 修正失敗的 case，加入 debug log
5. 反覆迭代，直到全部通過

**關鍵好處**：Cursor 在迭代特定函式時，不會動到其他地方，避免連帶破壞。

## Memory Bank 工作流

Memory Bank 由 Cline 引入的概念——讓 AI coding agent 維護一組描述專案狀態的 Markdown 檔案，每次開啟新 session 時先讀取這些檔案恢復上下文。

**核心檔案結構（`memory-bank/` 資料夾）：**

| 檔案 | 內容 |
|------|------|
| `projectBrief.md` | 核心需求與目標 |
| `productContext.md` | UX 與運作方式 |
| `activeContext.md` | 目前工作重點、最近變更、待決策事項 |
| `systemPatterns.md` | 系統架構、關鍵技術決策 |
| `techContext.md` | 技術棧、依賴、檔案結構 |
| `progress.md` | 已完成、待完成的任務清單 |

**在 Cline 使用：**
- `initialize memory bank`：掃描專案並建立所有檔案
- `continue`：讀取 memory bank 並從上次中斷處繼續
- `update memory bank`：完成任務後更新記錄

**在 Cursor 使用：**
1. 從 cursor-memory-bank 專案複製 cursor rules 到專案根目錄
2. 建立四個 Custom Mode：**VAN**（初始化）、**PLAN**（拆解任務）、**CREATIVE**（探索與除錯）、**BUILD**（實作）
3. 每個 mode 有對應的 system prompt，讓 Cursor 動態載入相關 rules

**四個模式的用途：**
- **VAN**：掃描現有專案，建立 memory bank（包含複雜度分析）
- **PLAN**：根據 memory bank 拆解任務，按依賴順序排列
- **CREATIVE**：討論技術選型、分析 bug 的多種可能根因
- **BUILD**：實作功能，完成後更新 memory bank

**對既有專案同樣有效**：刪除舊的 memory bank，切到 VAN mode，讓 Cursor 讀取整個專案重新建立，提供更好的起始上下文。
