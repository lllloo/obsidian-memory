---
title: Claude Code 與 RAG 的七個層次
tags:
  - youtube
  - claude-code
  - rag
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-13
source: https://www.youtube.com/watch?v=kQu5pWKS8GA
parent: "[[01.index]]"
---

本影片以「七個層次」的架構解構 Claude Code 的記憶問題，從最基礎的原生記憶系統一路進化到多模態 Agentic RAG，為每個層次提供學習路線圖。

## 核心問題：Claude Code 與記憶

AI 系統可靠回答過去對話或大量文件的問題，是多年來持續在解決的挑戰。傳統答案是 RAG（Retrieval-Augmented Generation）。本影片的目的是給出清晰的路線圖，讓你了解自己目前在哪個層次，以及如何進階。

**Context Rot（情境衰退）**：在同一個對話中持續使用 Claude Code，隨著 context window 填滿，回應品質會下降。例如 context 到 256k token 時效能為 92%，到尾聲可能只剩 78%。這是促使升級記憶架構的根本動機。

## Level 1：AutoMemory（原生自動記憶）

- Claude Code 自動在 `~/.claude/projects/<project>/memory/` 建立 markdown 記憶檔
- 根據對話自行判斷哪些內容值得記下，類似 Post-it 筆記
- **陷阱**：多數人停留在這個層次，因為害怕結束 session 導致失憶，所以無限延長對話——反而造成 context rot
- **升級條件**：學會主動管理記憶，而不是依賴自動機制

## Level 2：CLAUDE.md（主動指令記憶）

- 每個專案的 `CLAUDE.md` 是 Claude Code 執行任何任務前都會讀取的指令檔
- 可用 `/init` 指令讓 Claude Code 自動產生，也可手動編輯
- **用途**：記錄專案規則、偏好設定、常用指令、重要背景資訊
- **陷阱**：把所有東西塞進單一檔案，導致難以維護

## Level 3：多檔案記憶架構

- 不依賴單一 CLAUDE.md，改用多個專責檔案管理不同類型的記憶
- 範例：GSD（Get Shit Done）工具的做法——分開維護 `project.md`、`requirements.md`、進度追蹤檔等
- **優點**：更清晰的記憶分區，易於查找與更新

## Level 4：Obsidian 外部知識庫（Andrej Karpathy 方案）

- 將知識存放在 Obsidian vault，讓 Claude Code 透過 RAG 查詢
- Karpathy 的 LLM 知識庫影片獲近 2000 萬次觀看，驗證了此方案的實用性
- **適合對象**：大多數使用者——這個層次對多數情境已經足夠
- **核心概念**：把知識從對話 context 中解耦，存放在外部可查詢的結構化系統

## Level 5：Naive RAG（基礎向量 RAG）

- **流程**：文件 → 切 chunk → embedding model 轉換為向量 → 存入 vector database → 查詢時取出最相近的 chunk 餵給 LLM
- Vector database 是標準資料庫的特殊變體，儲存高維度向量而非純文字
- **限制**：各 chunk 之間是孤立的，缺乏關聯性；適合單純的語意相似度查詢

## Level 6：Graph RAG（LightRAG）

- 核心理念：**萬物互聯**，資料點之間有明確的關係（relationship）
- 每個節點有描述、名稱、類型、來源檔案，以及與其他節點的關係連結
- **LightRAG** 是最輕量的 Graph RAG 實作，比其他方案更易部署
- **優點**：關係型查詢效果顯著優於 Naive RAG，尤其適合知識密集型問題

## Level 7：Agentic RAG（多模態，最高層次）

- **重點**：多模態攝取（Multimodal Ingestion）
- **RAG Anything**：可將圖片、非文字文件（如掃描版 PDF）匯入 LightRAG 知識圖譜
- **Gemini Embedding 2**（2026 年 3 月發布）：支援將影片本身嵌入向量資料庫
- 這是整個領域的發展方向——不再只處理文字，而是處理任何格式的資訊

## 升級路線建議

| 層次 | 技術 | 適合情境 |
|------|------|----------|
| 1 | AutoMemory | 入門，自動但被動 |
| 2 | CLAUDE.md | 所有專案必備 |
| 3 | 多檔案架構 | 複雜專案 |
| 4 | Obsidian RAG | 多數人的終點，已夠用 |
| 5 | Naive RAG | 大量文件查詢 |
| 6 | LightRAG | 需要關聯性查詢 |
| 7 | Agentic RAG | 多模態、生產級系統 |
