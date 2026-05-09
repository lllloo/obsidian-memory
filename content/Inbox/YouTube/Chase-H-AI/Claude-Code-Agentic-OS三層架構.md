---
title: Claude Code Agentic OS 三層架構
created: 2026-05-09
updated: 2026-05-09
source: https://www.youtube.com/watch?v=Bgxsx8slDEA
published: 2026-05-04
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - agentic-os
  - obsidian
  - skill
  - automation
---

## 核心主張

多數人把 Claude Code 當吃角子老虎機——隨機提示、隨機任務、隨機結果。改用 Agentic OS 架構後，可以把日常工作流程系統化、可追蹤、可優化，最終可移交給團隊成員或客戶。

三個組成要素：

1. **架構層（Skill 設定）**：最重要，可單獨使用就有價值
2. **記憶層（Obsidian）**：讓 AI 能存取與回查過去的資訊
3. **可視化層（Dashboard）**：將 skill 與 automation 包裝成按鈕，降低使用門檻

## 第一層：架構（Skill 設定）

### 從工作流到 Skill 的路徑

```
個人 & 商業活動
  → 分解為 Domain（領域）
  → 每個 Domain 拆為離散 Task
  → Task 轉成 Skill（可重複執行，每次結果一致）
  → Skill 判斷是否需要自動化 → Automation
```

**Domain 範例**：記憶、生產力、研究、內容創作、社群、業務……因人而異。

**Skill vs Automation 的選擇**

- 每天固定發生的任務（如早晨趨勢掃描）→ 適合做成 Automation
- 深度研究類任務 → 不適合自動化，保持 Skill 即可
- Claude Code 可協助判斷應做成 local automation 還是 remote automation

### 這樣做的意義

把工作流 codify 成 Skill 後：
- 每次執行方式一致，結果可預期
- 可移交給不熟悉終端機的團隊成員或客戶（最終搭配 dashboard 按鈕執行）
- 可賣給客戶，作為 AI agency 的交付物

## 第二層：記憶（Obsidian Vault）

### 為何用 Obsidian

Obsidian 本質是一個操作 Markdown 檔案的介面。Claude Code 可以直接處理 Markdown，對 99.9% 的使用者而言不需要 vector database 或輕量 RAG。

Obsidian 是全功能 RAG 系統與純 Markdown 之間恰當的中間地帶。

### Karpathy 結構（三資料夾）

- **Raw**：暫存區，放所有未整理的研究內容或對話紀錄
- **Wiki**：從 raw 提煉成的知識型文章（類似百科條目，有結構、有深度）
- **Output**：最終輸出物（簡報、報告等）

作者自己的變體：`archive`、`content`、`ops`、`personal`、`projects`、`raw`、`wiki`

重點在於結構對 Claude Code 要清晰可讀，而非完全照抄某一模板。

### CLAUDE.md 的作用

在 vault 根目錄放 `CLAUDE.md`（或 `claude.md`）——這個檔案幾乎會附加到每一個給 Claude Code 的 prompt：

1. 說明這個 OS 是什麼、如何運作
2. 明確描述記憶結構（哪種資料放哪個資料夾），讓 Claude Code 以更少 token 找到目標

不設這個檔案，Claude Code 就不知道記憶結構，系統效率大幅下降。

## 第三層：可視化（Dashboard / 可觀察性）

### Dashboard 的核心邏輯

把 Skill 與 Automation 對應到 UI 按鈕。點擊按鈕 → 自動填入對應 prompt → 以 `--headless`（`-p` flag）模式啟動一個無介面的 Claude Code 實例執行任務。

使用者完全不需要開終端機。

**Dashboard 顯示內容範例**

- 5 小時用量視窗、每週用量
- 當日已用 routine 數量
- Vault 近期變更
- 趨勢預測

可依個人需求完全客製化，一個 prompt 就能讓 Claude Code 加入新的監控項目。

### 為何這對 Agency 工作很重要

- 可以讓完全不懂終端機的人執行複雜的 Claude Code 工作流
- 將 skill 包裝成按鈕後可作為產品交付給客戶
- 可追蹤執行紀錄，進一步優化 skill 設計

## 建置流程建議

1. 開啟終端機，用語音輸入進行 stream-of-consciousness 描述自己的日常任務
2. Claude Code 會逐一問：這個任務能轉成 Skill 嗎？需要 Automation 嗎？
3. 過程使用 skill-creator skill 自動生成對應 skill
4. 完成架構後再設定 Obsidian vault 結構
5. 最後建置 dashboard（有專屬 prompt 可啟動）

## 整體價值

即使只做第一步（Skill 架構），不做記憶層與 dashboard，也已經遠超過大多數 Claude Code 使用者的系統化程度。三層合在一起，就是一個可以持續優化並可移交的 AI OS。
