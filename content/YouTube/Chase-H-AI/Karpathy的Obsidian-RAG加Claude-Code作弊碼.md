---
title: Karpathy 的 Obsidian RAG 加 Claude Code 作弊碼
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-04
source: https://www.youtube.com/watch?v=OSZdFnQmgRw
parent: "[[01.index]]"
---

## 核心概念

Andrej Karpathy 在 Twitter 發文說明一個輕量知識庫系統：不需要向量資料庫、embedding 或複雜的 retrieval pipeline，只用 **Obsidian 的資料夾結構**就能達到與 LightRAG、RAG-Anything 相同的效果。

與傳統 RAG 的關鍵差異：傳統 RAG 用 embedding 做向量搜尋；此系統依賴 LLM 的長上下文能力，搭配結構化的 wiki 目錄直接讀取檔案。Obsidian 作為前端，讓使用者可視化地看到所有文件，而非黑箱。

## 系統架構

```
Obsidian vault/
├── raw/           ← 資料匯入的 staging 區
│   └── （文章、論文、PDF、repo）
└── wiki/
    ├── master-index.md    ← 所有 wiki 的總索引
    ├── ai-agents/
    │   ├── index.md
    │   └── ...
    ├── rag-systems/
    └── content-creation/
```

**資料流：**
1. 原始資料（文章、論文、repo）進入 `raw/` 資料夾
2. Claude Code 讀取 `raw/` → 整理成 wiki 格式 → 存入 `wiki/` 對應子資料夾
3. `master-index.md` 自動維護所有 wiki 的索引
4. 查詢時：Claude Code → `wiki/` → `master-index.md` → 找到對應 wiki → 回答問題

## 設定步驟

**1. 安裝 Obsidian**

前往 obsidian.md 下載，完全免費。建立一個資料夾作為 vault（建議直接命名為 `vault`）。

**2. 建立資料夾結構**

用 Claude Code 在 vault 目錄下建立上述結構，直接貼上作者提供的 prompt 即可。

**3. 建立 CLAUDE.md**

在 vault 根目錄建立 `CLAUDE.md`，說明知識庫的規則與遍歷方式，讓 Claude Code 知道如何高效瀏覽文件、不浪費 token。

**4. 安裝資料匯入工具**

- **Obsidian Web Clipper**（Chrome extension）：將任何網頁轉為 markdown 直接存入 `raw/`
  - 設定：在 extension 選項的 note location 改為 `raw`（預設是 `clippings`）
- **Local Images Plus**（Obsidian 社群插件）：讓 Web Clipper 抓取的文章保留圖片

## 兩種資料匯入方式

**手動匯入（Obsidian Web Clipper）**
- 瀏覽任何網頁 → 點擊 extension → 自動存入 `raw/`
- 適合你主動想研究的特定資料

**Claude Code 自動研究**
- 直接告訴 Claude Code 要研究的主題，讓它自己上網搜尋並整理成 wiki
- 例：「建立一個關於 Claude Code skills 的 wiki，已有部分資料在 raw/ 裡，請自行補充研究」
- Claude Code 可以完全自主完成，`raw/` 資料夾主要是給人類使用的暫存區

## 何時應該改用真正的 RAG

- 個人或小型團隊、文件量不到數千份 → Obsidian 足夠
- 需要擴展到數萬甚至數百萬份文件 → 考慮 LightRAG 等系統
- 建議：先用 Obsidian，真的超出邊界再遷移，不用一開始就過度設計
