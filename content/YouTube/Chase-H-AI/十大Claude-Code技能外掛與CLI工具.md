---
title: 十大 Claude Code 技能、外掛與 CLI 工具（2026 年 4 月）
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-09
source: https://www.youtube.com/watch?v=KjEFy5wjFQg
parent: "[[01.index]]"
---

## 1. Codex Plugin

將 OpenAI Codex 接入 Claude Code，專門用於程式碼 review。LLM 天生對自己的程式碼評價偏高，由外部 agent 做 adversarial review 可得到更直率的批評。

**安裝：** 搜尋「Codex plugin Claude Code」找到 GitHub，複製指令貼入 Claude Code，執行 `reload plugins` 與 `/codex:setup`。需要 OpenAI 帳號（ChatGPT $7/月 Go 方案即可）。

**常用指令：**
```
/codex:adversarial-review   # 對抗式審查，深入檢查實作品質
/codex:review               # 一般審查
/codex:rescue               # 讓 Codex 接管特定功能的開發
```

## 2. Obsidian + Obsidian Skills

Obsidian 作為 markdown 組織工具，與 Claude Code 結合成輕量 RAG 系統（參見 [[Karpathy的Obsidian-RAG加Claude-Code作弊碼]]）。

Obsidian CEO 本人提供的官方 skills（GitHub repo），教 Claude Code 如何最佳化使用 Obsidian。適合任何大型且持續成長的 markdown 文件庫，或個人助理類型的專案。

## 3. Auto Research

機器學習實驗自動化工具：安裝後告訴 Claude Code 要優化的目標（程式或 skill），它會自動跑一系列實驗、丟棄沒改善的變更、提交有改善的變更，全程無需人工介入。適合需要反覆優化某個東西的情境。

## 4. Awesome Design（awesome.design.md）

解決 Claude Code 前端設計能力不足的問題。靈感來自 Google Stitch，將熱門網站（Claude、Notion、Figma、Pinterest 等）轉為詳細的設計 markdown 模板，涵蓋按鈕、色彩、字型等完整規格。

**使用方式：** 選一個風格接近的網站模板，貼入 Claude Code 作為設計基礎。釋出首週達 38,000 stars。

## 5. Firecrawl CLI + Skill

網頁抓取工具，可繞過反爬蟲防護，回傳 LLM 友好的結構化格式。有兩個版本：
- **付費 API 版**：完整防爬功能，可應對高防護網站
- **免費開源版**：基本爬取功能，不含專有防爬引擎

安裝：一行指令搞定。

## 6. Playwright CLI

**比 Playwright MCP 更有效且更便宜**，是 2026 年的推薦選項。

差異點：Claude in Chrome extension 基於截圖（慢且貴）；Playwright CLI 讀取 accessibility tree（快且準）。

使用情境：讓 Claude Code 自動開啟 Chrome 實例、測試網頁、送出表單、登入網站等。安裝後直接用自然語言描述要做什麼，Claude Code 會自行選用正確的 Playwright 指令。

## 7. NotebookLM Pine CLI + Skill

NotebookLM 本身沒有 API，透過這個 CLI 工具讓 Claude Code 與 NotebookLM 溝通。

**比原生 NotebookLM 多的功能：** 批次下載、修改投影片、完整文字存取、程式化分享。

**主要優勢：** 分析工作外包給 Google 伺服器，大幅節省 Claude Code token 消耗。適合 token 使用量高的用戶。

## 8. Skill Creator Skill（官方 Plugin）

建立、測試、優化自訂 skills，並提供**量化基準測試**：可以跑 A/B 測試比較「有 skill vs 沒有 skill」或「改版前 vs 改版後」的效能差異，用數據決定 skill 是否真的有改善。

**安裝：** 在 Claude Code 內執行 `/plugin`，搜尋 skill creator skill 安裝。

## 9. LightRAG

開源 Graph RAG 系統，Obsidian 方案的進階替代品。適合：
- 文件量超過 Obsidian 可處理的規模
- 客戶專案或需要更嚴謹 retrieval 的情境

比 Microsoft GraphRAG 輕量且免費。

## 10. GWS（Google Workspace CLI）

由 Google 員工開發（非官方產品但品質接近官方），連接 Claude Code 與 Gmail、Google Docs、Calendar。

**優點：** 附帶大量預建工作流 skills（重新排程會議、整理雲端硬碟、排程重複事件等），不需要自己組合指令。

**缺點：** 初始設定需在 Google Cloud Console 手動開啟多個權限，步驟較繁瑣。

**建議：** 安裝後，讓 Claude Code 讀取整個 GWS skills repo，挑出與你日常工作流程相關的 skills，不要全部載入。
