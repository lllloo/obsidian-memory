---
title: 全新 Jev + Claude OS 改變所有 AI 工作流
description: Agentic OS 分視覺、記憶、skill 三層，本地語音加 Jev 三級模型路由，Obsidian 當結構化記憶，skill 骨幹最關鍵。
created: 2026-10-08
updated: 2026-10-08
source: https://www.youtube.com/watch?v=EOdXR6lU5ZA
published: 2026-09-24
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - obsidian
  - multi-model
  - workflow
---

> [!note] 本片 transcript 為阿拉伯語自動翻譯版，內容依翻譯稿整理為繁中。

需要 Agentic OS 的理由不是華麗的 dashboard，而是打造一套圍繞你與你工作的客製系統，善用手邊最好的 AI 工具（GPT-6 Astra、Claude Opus 5.5、Jev），做到在 terminal 裡做不到的事。

## 三層架構

- **視覺層**：作者的介面串接社群帳號數據、行事曆，能檢視並觸發所有 skills 與 automations，可選擇在 Claude Code 或 Codex 上執行。原為 web app，也移植成 Obsidian plugin，仍可在其中開 terminal；有分頁看受眾狀況、AI 圈動態，以及研究分頁（GitHub trending、YouTube 精選影片、Hacker News）。重點是 100% 可客製。
- **記憶層**：用 Obsidian。價值不在知識圖譜（好看但不是 RAG），而是建立對人與 AI 都合理的檔案／資料夾結構，在上千個檔案中也能快速精準找到答案。採 Karpathy 的 Obsidian 架構。
- **Skill 層**：一切的骨幹。把每日、每週例行事務轉成 skills，適合的再轉成 automations；其產出（報告、圖表）回饋到 AIOS 中。

## 架構與 Jev 路由

一個語音請求的流程：

1. 從 Obsidian plugin（或 Jarvis 介面，兩者行為相同）發出語音請求。
2. 進入 bridge：把請求記錄到 Obsidian，並啟動本地語音系統。
3. 本地 Whisper（開源）轉文字；回應的 Jarvis 風格語音由本地開源模型 Kokoro 合成，可換成任何聲音。語音全程在本機完成。
4. 文字送到 Jev 分類成三級：
   - **Tier 1**：極簡單、要即時回應的請求，如「顯示晨間簡報」或 Obsidian 內的「開 terminal」。不經 AI 模型，幾百分之一秒完成。
   - **Tier 2**：需要一點思考但不複雜，如「今天最大的 AI 新聞是什麼」。交給最小的模型（Haiku 或 Luna，視用 Claude Code 版或 Astra 版而定）；想全本地化也可換成本地模型。
   - **Tier 3**：真正複雜的任務，如「做一份說明 Jev 與 Fable、Astra 等標準 LLM 差異的講解」。在 terminal 中啟動 Claude Code 或 Codex。
5. 所有輸出與對話都記錄回 Obsidian。

### 為何用 Jev 當路由器

- Jev 是 AI 系統但不是 LLM；有人說它能在某些情況取代 Claude Code 或 Codex，這只在特定情境部分成立，整體而言不對。
- 它讓你問模糊問題、拿回精確的機率。例：客戶說「上月取消訂閱又被扣款」，LLM 回「這是帳務問題，轉 billing」；Jev 不回句子，而是回「billing 機率 92%」。
- 答案一樣，但 Jev 快約 200 倍且便宜，最適合「預先定義好選項、問該怎麼做」的情境，模型路由正是如此。這裡也能放 Haiku 或 Luna，但有 Jev 就沒必要。

## Skill 骨幹：最重要的一層

作者認為只做這一段就能贏過 99% 的 Claude Code／Codex 使用者。做法只有兩件事：

- **讓 AI 讀你的使用紀錄**：Claude Code 與 Codex 會保存過去 30 天以上的對話紀錄。直接問：「根據我過去 30 天怎麼用你，有哪些可以做成 skill？」這就是完整 prompt，不需特殊流程。
- **對著麥克風講 10–20 分鐘**：不必有條理，把每天／每週的例行工作全部講出來，再問「根據我剛說的，有哪些可以做成 skill 或 automation 來減輕我的負擔？」

兩種做法都不需要事先知道答案，能完成約 90% 的工作。要轉成 automation 也只需請 Claude 處理：可用 Codex 的排程任務手動設定，也能讓系統建立由本機觸發的 automation。

Skills 與 automations 的產出常是報告與工作成果，與其散落各處，不如集中到 dashboard：指標、行程、任務拆解、晨間新聞、受眾指標、深度研究等，內容完全依個人需求客製。

## 記憶層：Obsidian 的真正價值

- Obsidian 是免費的 markdown 桌面工具，常與 Claude Code、Codex 搭配做「第二大腦」：在 vault 資料夾裡跑 Claude Code，讓它取用關於你的所有資訊。
- 近來第二大腦名聲變差，是因為大家高估了 Obsidian：它不會讓 Claude Code 或 Codex 記憶變好，只是讓 vault 裡的檔案好瀏覽。
- 系統的力量 100% 取決於檔案與資料夾怎麼組織；一個資料夾塞一千萬個雜亂檔案，用 Obsidian 也沒用。
- Karpathy 的結構：vault 底下三個子資料夾——
  - `raw`：原始資料，例如請 AIOS 研究 AI agents 後下載的大量資料。
  - `wiki`：把 raw 整理成類似維基百科的文章，例如 AI agents 子資料夾，含自主編程、工具使用模式等。
  - `outputs`：衍生產出，例如依 wiki 文章做的 PowerPoint 簡報。
- 結構清楚，Claude 查 vault 時有明確地圖與路徑，找得快又有效率；人也同樣好找。
- 不一定要照這三個資料夾，只要對人與 Claude／Codex 都合理即可；可以直接請 AIOS「這是我的 vault，幫我想一個組織結構」，它會規劃並搬移檔案。
- 強烈建議在 vault 的 `CLAUDE.md` 或 `AGENTS.md` 寫明 vault 結構與新增內容的方式，避免它偏離軌道。

## 視覺層：團隊與客戶才是主要價值

- 所有 skill 都有可交付產出，要負責的指標也都集中在一個客製 dashboard。
- 價值在引入團隊成員與客戶時最明顯：在 terminal 裡做的東西很難交給他們，但客製 dashboard 很容易為任何人建置。
- 可把 workflow、skills、automations 做成按鈕，背後呼叫 headless 的 Claude 或 Codex 執行；任何人坐到 dashboard 前（Obsidian plugin 或 web app 皆可），不必會操作就能用到 Claude Code／Codex 約 90–95% 的能力。
- 對行銷與新成員 onboarding 幫助很大，即使你自己有技術能力也不應低估。它不是一體適用的方案，可客製正是其力量所在。
