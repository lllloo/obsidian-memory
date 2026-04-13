---
title: "Karpathy 的 Obsidian RAG + Claude Code = 作弊碼"
tags:
  - youtube
  - claude-code
  - obsidian
  - rag
created: 2026-04-12
updated: 2026-04-12
published: 2026-04-04
source: https://youtu.be/OSZdFnQmgRw
---

**影片描述**：Chase H 拆解 Andrej Karpathy 在 Twitter 分享的 Obsidian 知識庫系統——無需向量資料庫、無需 embeddings，卻能達到類似 RAG 的效果。核心洞見是 LLM 能自然維護 index 文件，讓 Claude Code 以極低成本在大量 Markdown 文件中找到答案。

**重點摘要：**
- Karpathy 系統的核心結構：Obsidian vault 下分 `raw/`（暫存所有原始資料）與 `wiki/`（主知識庫），wiki 下有 `master-index.md` 作為目錄，再依主題建立子資料夾各含 `index.md`，Claude Code 查詢時先讀 master-index 再定位。
- 資料注入有兩條管道：Obsidian Web Clipper（Chrome 擴充，一鍵將網頁轉 Markdown 送入 raw/）和 Claude Code 自動研究（告訴 Claude 主題，讓它自行搜尋並直接建立 wiki）。
- 重要插件：安裝「Local Images Plus」解決 Web Clipper 不下載圖片的問題，自動將圖片本地化；Web Clipper 的 Note Location 需改設為 `raw`。
- CLAUDE.md 的角色：定義知識庫的遍歷規則與 wiki 格式規範，讓 Claude Code 不用浪費大量 tool call 就能找到資料。
- 與傳統 RAG 的差異：Obsidian 系統完全透明（可直接在 Obsidian UI 看到所有文件），而 LightRAG/RAG Anything 是黑盒；Obsidian 適合個人或小團隊（數百至數千份文件），真正的 RAG 才適合企業規模。
- 何時需要轉移到真正的 RAG：當文件量明顯超出 Obsidian 系統的處理能力（數萬份以上），查詢速度或準確性下降時再遷移，不必過早優化。
- Chase 的實測：讓 Claude Code 建立一個 Claude Code Skills 的 wiki，Claude 自動上網研究、整合 raw/ 資料，生成帶有 wikilinks 的結構化 wiki，效果良好。
- 結論：多數個人和小團隊根本不需要真正的 RAG；先用 Obsidian，感覺不夠用再說——爭論哪個更好不如直接試。
