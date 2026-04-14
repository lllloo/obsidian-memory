---
title: Anthropic 意外洩漏 Claude Code 原始碼事件
tags:
  - youtube
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-01
source: https://www.youtube.com/watch?v=mBHRPeg8zPU
---

## 事件經過

2026 年 4 月 1 日凌晨 4 點，Anthropic 在發佈 Claude Code npm 套件 `2.1.88` 版時，意外將 **57MB 的 source map 檔案**一同打包進去，導致超過 50 萬行 TypeScript 原始碼完全公開。

安全研究員 Qiao Fan Sha 在幾分鐘內發現，程式碼隨即在網路上大量鏡像與複製。Anthropic 法務團隊發出 DMCA 下架要求，但為時已晚。

**根本原因（推測）：** Claude Code 以 **Bun.js** 建置，而 Bun.js 在約 3 週前被回報有在 production 環境輸出 source map 的 bug。Bun.js 此前已被 Anthropic 收購。

## 洩漏後的連鎖反應

- 有人用 OpenAI Codex 將洩漏的 TypeScript 程式碼重寫為 Python，建立 **Claw Code** 專案，成為史上最快突破 50,000 GitHub stars 的 repo
- 另有人 fork 洩漏程式碼並讓它相容所有模型，稱為 **OpenClaw**
- 有人送 pull request 想把洩漏程式碼合回 Anthropic 官方 repo，很快被刪除

## 從洩漏學到的技術細節

**架構本質：**
- Claude Code 並非神秘的未來科技，而是「動態 prompt 三明治 + TypeScript 膠水」
- 整個 input → output 流程共 11 個步驟，已有人做成網站解析

**硬編碼指令：**
- 大量 hard-coded 字串反覆告訴 Claude「請不要做奇怪的事」
- 這些 comment 比一般人工 codebase 多很多，因為它們是寫給 AI 看的，而非人類

**Anti-distillation Poison Pills：**
- Claude Code 對可能竊取輸出的競爭對手設置陷阱：假裝某些工具存在，實際上不存在
- 若有人用 Claude 輸出訓練新模型，該模型會學到虛假的工具知識，導致能力下降
- 反諷：原始碼洩漏後，競爭者現在知道真正存在的約 25 個工具，Bash tool 尤其重要（超過 1000 行）

**Undercover Mode：**
- 一組指令讓 Claude 在 commit 訊息與輸出中完全不提及自己
- 官方目的：防止模型代號洩漏
- 社群猜測：讓 AI 程式碼混入開源專案不被發現

**Regex 憤怒偵測器：**
- 用簡單 regex 偵測 prompt 中的粗口（如「balls」等），判斷用戶是否有不好的體驗
- 偵測到後只是記錄事件，不採取其他行動

## Roadmap 洩漏

程式碼中隱藏的功能旗標與未發佈功能：

- **Buddy**：類似 Tamagotchi 的開發者隨身寵物（可能是愚人節玩笑）
- **Opus 4.7** 與新模型 **Capiara**（可能是 Mythos 的代號）
- **Ultra Plan**、**Coordinator Mode**、**Demon Mode**
- **Chyus**（希臘文「神的時間」）：背景 agent，使用 dream mode 整合記憶、依排程在背景為你工作

## 啟示

這次洩漏對計劃 IPO 的 Anthropic 是重大打擊，也提醒所有開發者：**你的機密應用，距離開源只差一個 `npm publish`。**
