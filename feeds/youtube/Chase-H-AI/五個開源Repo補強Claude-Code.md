---
title: 修復 Claude Code 95% 問題的五個開源 Repo
description: 盤點補強 Claude Code 五大弱項的免費開源工具：Claude Video 影片理解、NotebookLM-PI 研究、Graphify 知識圖譜記憶、Impeccable 前端設計、Ponytail token 節省。
created: 2026-07-10
updated: 2026-07-10
source: https://www.youtube.com/watch?v=IRPEfl2BD_c
published: 2026-07-07
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - workflow
---

## 前提：Claude Code 的五個天生弱項

Claude Code 開箱即用已經很強，但在**影片、前端設計、記憶、研究、token 消耗**五個面向天生偏弱。以下五個開源工具各補一塊，全部免費。

## Claude Video——讓 Claude 看得懂影片

- 作者 Brad Automates，5,000+ stars，近期竄升中。目標是讓 Claude 能「攝入」使用者給的影片（非 AI 生成影片）；這是 Claude 原生沒有的能力，主流模型中大致只有 Gemini 具備。
- 不只取 transcript，還會在適當時機智慧抽取影片畫格（frames），補足「畫面上實際發生什麼」的脈絡；若影片沒有 transcript（如 Loom），會自動改走 Groq 的 Whisper 模型免費產生。
- 不是每秒 24 格全丟，而是依模式決定抽格策略，共四種模式：
  - **transcript**：只取字幕、不抽格
  - **efficient**：只取影片自帶的 key frames，依片長最多 50 張
  - **balanced**：依場景變化（並比對 transcript 用詞）最多 100 張，多數人適用
  - **token burner**：同 balanced 但無張數上限，耗時且燒錢
- 安裝：從 marketplace 安裝，或直接把 skill 的 URL 丟給 Claude Code。價值在於不必繞道 Gemini API 額外付費，全部留在 Claude Code 內完成。

## NotebookLM-PI——把 NotebookLM 搬進終端機

- 讓 Claude Code 透過 CLI 呼叫 NotebookLM，等於一個非官方 API；web 版能做的（slide deck、資訊圖表、podcast 等）都能做，還多出一些 web UI 沒有的功能（readme 有完整清單）。
- 定位是研究的中間地帶：原生 web search 太淺，深度研究動輒大量 subagent 燒上千萬 token 又太重。
- 附帶好處是變相取得免費的 LLM 呼叫——把部分研究與綜合工作卸載到 Google 伺服器（模型是 Gemini，弱於 Opus 與 Fable，但免費）。
- 安裝只需把 URL 丟給 Claude Code；相依的 Playwright（瀏覽器自動化）運行時對使用者完全透明。
- 作者最愛的用法：餵大量同主題 YouTube URL 一次綜合。NotebookLM 只看 transcript，但因在 Google 體系內，處理 YouTube URL 非常順。

## Graphify——程式庫的知識圖譜記憶

- 解決的問題：讓 Claude Code 快速回答關於超大 codebase 或文件庫的問題——給它一張可循路徑的「地圖」。
- 把 codebase 拆解成節點、依主題聚類成知識圖譜；提問時從問題到答案有清楚路徑。
- **不是 RAG**：沒有 vector index、沒有 embedding，不是 LightRAG；定位介於 Obsidian 與真正的 RAG 系統之間，像「輕量版 graph RAG」——複雜度低得多，卻拿到許多相同的記憶效益。
- 檔案類型彈性高：不限 markdown，PDF、圖片、影音都能處理。

### 加碼：Obsidian skills repo

由 Obsidian CEO 建立的官方 skills 集合。內容很簡單，就是幾個 skill，但等於由 Obsidian 創造者親自教 Claude Code 最佳實踐；用 Obsidian 搭配 Claude Code 的人不該錯過。

## Impeccable——前端設計 skill

- 作者目前最愛的前端設計 skill，已被納入 GitHub 官方 AI package。
- 一個 skill 內含 23 個指令：craft、shape、critique、layout、colorize 等。例如 `colorize` 會替單色介面加上策略性用色；官網每個指令都有 before/after 對照（標準 Claude Code 前端 skill vs Impeccable）。
- **live mode** 是亮點：執行後把頁面開在 localhost 瀏覽器上，可點選元件、即時比對套用前後效果，把終端機改碼變成視覺化設計工具——遠勝「嘿，弄好看一點……再試一次……更高級一點」的循環。
- 作者評價高於 Anthropic 官方前端設計 skill 與 UIUX Pro Max。

## Ponytail——降低 token 消耗

- 宣稱讓 Claude Code 便宜 20%、快 27%，且產出品質不變。
- 原理：在動工前設一連串關卡——這功能真的需要自己寫嗎？是否已存在？有沒有現成 library？——確定要寫時再用最少量的程式碼完成。
- 官方 benchmark 用 Haiku 測（repo 內附完整 benchmark 可自行重跑）：程式碼行數、token、成本、時間全面低於 baseline。
- 作者疑慮「用 Opus／Fable 還成立嗎」並實測：用 Opus 跑同一組 benchmark 效益反而更大，Fable 亦同。
- benchmark 與真實情境是否一致因用例而異，但試錯成本低：跑幾次不喜歡就移除。同類型工具還有 Caveman 值得一看。
