---
title: Graphify 與 Obsidian 整合
description: Graphify 可把 repo 或文件轉成知識圖譜，再輸出為 Obsidian vault，讓 Claude Code 用圖譜與來源文件定位脈絡。
created: 2026-06-11
updated: 2026-06-11
source: https://www.youtube.com/watch?v=mWLDn49_8HA
published: 2026-06-08
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - obsidian
  - knowledge-graph
---

## 核心想法

Graphify 能把 codebase、文件、PDF、圖片或影片等資料夾轉成 knowledge graph。Obsidian 則提供可讀、可管理、可連結的 markdown vault。

兩者合併的用途是：先用 Graphify 從大型 repo 或文件集中抽出概念與連結，再把這些節點與來源文件搬進 Obsidian，讓 Claude Code 不只看到孤立的知識圖譜，也能把它放進更大的 vault 脈絡裡查詢。

## Graphify 輸出的不是原文件清單

影片示範用 Claude Code 官方文件做 corpus：

- 抓取約 145 份文件。
- Graphify 從中抽出 591 個 concept nodes。
- 建立 685 條 connections。
- 分成 67 個 communities。

每個 node 不是一份原始文件，而是 Graphify 從文件中抽出的概念。例：`context window` 可能連到 `path scoped rules`、`sub-agent separate context window`、`post tool use hook`、`extended 1 million token context` 等相關概念。

這種 graph map 讓 Claude Code 查問題時不只是 `grep` 字串，而是能沿概念關係找到相關來源。

## 匯出為 Obsidian vault

Graphify 內建 Obsidian 輸出旗標，可生成一個 Obsidian vault。操作上可直接要求 Claude Code：

```text
download the official Claude Code documentation
point Graphify at it
then use the graphify obsidian command to turn it into a vault
```

Graphify 會把每個 node 轉成 markdown file，並建立對應 backlinks。影片中的例子會產生數百個 concept stub，並以 Obsidian link 表示原本 graph 裡的邊。

## 必須接回來源文件

只把 graph nodes 轉成 markdown 還不夠。單一 node 檔案如果只有標題與連到其他 node 的 edges，Claude Code 仍缺少實際內容。

影片示範的補強指令是：把來源文件拉進 vault，並讓每個 node 連回原始文件。這樣 Claude Code 查 `auto mode` 或 `bundled skills` 時，會先看到概念節點，再沿連結讀到完整來源文件。

換句話說，Obsidian 版 Graphify 不只是漂亮 graph，而是「概念路標 + 原文來源」的查詢地圖。

## 四種導入策略

大量匯入幾百份 markdown 會污染主 vault，因此影片列出四種策略：

| 策略 | 適用情境 |
|---|---|
| 獨立 vault | 只想在 Obsidian UI 裡看 Graphify 結果，不需要混入主 vault |
| quarantine subfolder | 想放進主 vault，但保留一鍵刪除的退路 |
| harvest | 讓 Claude Code 只挑有價值的節點或來源搬入 |
| redistribution | 讓 Claude Code 重新分配到主 vault 的既有結構，整合度最高但最難復原 |

影片建議先用獨立 vault 或 quarantine subfolder。直接把 600 個檔案散進主 vault，後續很難清理。

## 對本 vault 的啟示

Graphify + Obsidian 適合「把大型外部 corpus 做成可查地圖」，但不等於應該直接寫進主 vault。對已經有 Inbox / Cards / Topics 流程的 vault，更合理的做法是：

- 先獨立輸出或放進隔離資料夾。
- 檢查哪些概念真的會被長期使用。
- 只把已內化、能形成判斷的部分升成 Card。
- 原始 graph dump 保留可刪除邊界。

這和本 vault 的原則一致：AI 產生的結構本身不是價值，能被讀、被用、被整合進決策的內容才值得留下。
