---
title: 近期 10 大 Claude Code 開源工具精選
created: 2026-05-04
updated: 2026-05-04
source: https://www.youtube.com/watch?v=6cYBFfA7Nyk
published: 2026-05-02
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
---

## Caveman Skill

- 第一個月就拿下 50,000+ stars，作者每天都用
- 把 agent 回應改成「穴居人風格」——「why say many word when few do trick」，避免 verbose 輸出
- 等級分 light、full、ultra；作者個人停在 light
- 官方宣稱省 75% output tokens 但實測整體只省約 5%（因為僅改變輸出字數，不影響 thinking 與輸入 ingest）
- 真正價值來自 March 2026 論文 *Brevity Constraints Reverse Performance Hierarchies in Language Models*：強迫強模型給簡潔答案，反而**減少答錯率**（因為不會「talk way into wrong answer」）
- 安裝：repo 內指令一行貼進 terminal，或把 repo URL 丟進 Claude Code 說「跑 Caveman」即可

## Graphify

- 讀檔建 knowledge graph，給 Claude Code 結構化記憶
- 官方數據：每查詢比 raw file 讀取省 71.5× tokens
- 與 Obsidian 比較：Obsidian 只是 markdown 介面，**不是真正 knowledge graph**；與 light rag、rag-everything 這類 graph rag 比較，Graphify 介於 Obsidian 與真 RAG 之間
- 多模態：能讀 PDF、screenshot、diagram；影片透過 Whisper 抽取
- **不使用 embedding**——適合想加強 Obsidian 記憶層、又不想跨入完整 RAG / embedding 系統的人

## Claude Video

- 上週剛推出，~400 stars
- 讓 Claude 能「看影片」：FFmpeg 抽 frame + Whisper 抽 audio，組合餵給 Claude Code
- 預設 frame budget 隨片長：30 秒影片 30 frames；10+ 分鐘只 100 frames（避免 token 爆炸）
- 取代既有兩條路（送去 Notebook LM、API 呼叫 Gemini），適合不想被 Gemini 綁住的場景

## Open Design

- Claude Design 的開源克隆，可用任何 coding agent（Claude Code / Codex / Gemini 等）
- 完全本地免費，不會撞 Claude Design 的 usage 上限
- 多了 image / video API 接入功能
- 底層整合四個工具：Huashu Design、Guzheng PowerPoint Skill、Open Code Design、Multika
- 加上 31 個 skills，等於本地版 Claude Design

## Codeburn

- 跨 16 個 AI coding tool 追蹤 token 用量、成本、效能
- 比 Claude Code 內建 `/usage` 詳盡許多
- 拆分維度：activity、project、model、core tool、shell command、MCP server
- 不只報告問題，會給優化建議協助降 token 消耗
- 與 Caveman 一樣是「margin upside、零下行風險」的輕量工具

## Impeccable 3.0

- 前端設計專用，3.0 版上週推出
- 重大更新：可在**瀏覽器內直接編輯**前端設計（live mode）
- 單一 skill 但內含 23 個 commands
- 官網提供每條 command 的 before/after 對照
- 在瀏覽器點選元件 → 可在右側 sidebar 進行不同變體比較

## Design Extract

- 是 awesome-design.md（70K stars）的進階版
- awesome-design.md 限制：只能挑現有條目（11 Labs 等）
- Design Extract 可指向**任何網站**做拆解，抓 layout system、responsiveness、interaction states、motion language、component anatomy、brand voice 等
- 用 headless browser 抓資料，不只是截圖

## Career Ops

- 把任何 AI coding CLI 變成完整 job search command center
- 評估職缺、生成客製 PDF、掃描求職入口、batch 處理、追蹤求職流程
- **不是大量亂投**——更像 scalpel，幫你篩出真正合適的職缺、為每個 listing 客製履歷
- 底層用 Playwright 導航頁面
- 流程：貼 job URL → 分類 → 比對 fit → 產報告與 PDF → 更新 tracker

## Browser Harness

- 想成「會自我改進的 Playwright」
- 每次執行任務後會更新自己的 agent skill file，記錄「在 Amazon 怎麼做有效、什麼無效」
- 類似 mini Ralph loop（self-healing browser agent）
- 還新，<10K stars，但這種 agentic browser 是值得追蹤的方向

## n8n MCP Server

- 嚴格說 n8n 與此 MCP 都不算純開源（fair use、可本地部署）
- 與其他第三方 n8n MCP 的關鍵差異：用 **TypeScript 而非自動產 JSON**——可在輸入 instance 前先做 type-check 與編譯驗證
- Claude Code → n8n MCP → 編譯 TypeScript → 驗證 → 轉 JSON → 自動寫入 instance
- 適合 niche 自動化（簡單流程、需要可視化交給非技術 client）

## 作者結語

- AI 工具 landscape 變動極快，每月新東西層出不窮
- 重點不是全用，是知道有哪些選項；尤其 Caveman、Codeburn 屬「純上行、零成本」級別
