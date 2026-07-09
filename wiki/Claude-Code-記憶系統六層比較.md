---
title: Claude Code 記憶系統六層比較
description: 從原生 CLAUDE.md 到跨工具統一大腦，六個層級的 AI 記憶方案沿「儲存位置」與「召回機制」兩軸拆解，含各層適用情境與升級門檻
created: 2026-07-08
updated: 2026-07-09
parent: "[[wiki/01.index]]"
tags:
  - claude-code
  - memory
  - context-engineering
  - rag
  - knowledge-graph
---

# Claude Code 記憶系統六層比較

各家 AI 記憶方案（Mem0、Karpathy LLM Wiki、openclaw、Hermes、MemPalace、LightRAG、ClaudeMem…）其實**不是互相競爭，而是不同使用情境下處理記憶的不同方式**。它們回答同一個問題：給 agent 一個任務時，如何在正確時機取得正確 context？來源見 [[Every-Claude-Code-Memory-System-Compared-(So-You-Don't-Have-To)]]。

## 兩條分辨軸

所有方案的差異只在兩件事：

1. **儲存位置（storage）**——資料放哪、什麼結構：markdown vs. vector、本地 vs. 雲端。
2. **召回機制（recall）**——Claude 怎麼取得：自動複製進 context vs. 存 database 需要時才搜。

核心敵人是 **context rot**：載入的 context 越多，模型對已載入資訊的召回越不完整。因此所有層級的共同紀律是**索引化 + 按需載入**（CLAUDE.md 控制在 ~200 行內，其餘拆獨立檔用引用）。

## 六個層級

| Level | 方案 | 儲存 | 召回 | 何時升級到這層 |
|---|---|---|---|---|
| **1** 原生 | CLAUDE.md + automemory（`memory.md`） | 本地 markdown，索引結構 | session 啟動自動載入索引 | 預設就有，免費；先正確使用 |
| **2** 可靠召回 | John Connelly / Paweł Huryn 的 hook 系統 | 本地 markdown，`~/.claude/memory` 雙層 | session start hook 注入記憶索引 | 常重複告訴 Claude 它早該知道的事 |
| **3** 語意搜尋 | **memsearch**（Zilliz，移植自 openclaw）／ ClaudeMem | markdown + 語意向量 | UserPromptSubmit hook 自動注入 top-N 語意匹配 | 用超過一個月、檔案變多、關鍵字搜尋失效 |
| **4** 逐字召回 | **MemPalace** | 本地 SQL（實體關係）+ Chroma vector（逐字分塊） | session end / pre-compaction hook 背景索引；記憶宮殿式定址 | 想找當初決策的「確切文字」 |
| **5** 自組織知識庫 | **Karpathy LLM Wiki** ／ Recall（代管）／ LightRAG（企業級） | 純 markdown，raw + wiki 兩層 | 讀 index 找頁再鑽（無需 vector DB） | 定期消化文章/影片/podcast，要跨來源互聯的「第二大腦」 |
| **6** 跨工具單一大腦 | **OpenBrain**（Nate Jones）／ Mem0 | 自有 Postgres（Supabase），`thoughts` 表 + embedding | MCP server 當前門，各 AI 工具共用同一 DB | 跨多個 AI 工具（手機 ChatGPT、桌面 Claude Code…）要共用記憶 |

Level 1–3 資料夾結構相近、**可疊加同跑**；Level 5、6 屬不同領域（不只記憶對話，而是互聯知識 / 跨工具共腦）。

## 幾個關鍵取捨

- **markdown 優先 vs. vector/MCP**：memsearch 把一切存成可讀 markdown 並自動注入；ClaudeMem 走 MCP，需 Claude 主動決定呼叫搜尋工具，功能多（dashboard、團隊、費用追蹤）但較重。
- **本地擁有 vs. 代管租用**：MemPalace、OpenBrain 讓你完全擁有資料；Recall、Mem0 資料活在對方伺服器（可匯出 markdown，但等於租）。
- **摘要 vs. 逐字**：Level 3 存摘要（省空間、可能漏細節）；Level 4 逐字不摘要，理論上什麼都不丟，但取回內容非 markdown、不可直讀。

## 在本 vault 的定位

- 本 vault 就是 **Level 5 / Karpathy LLM Wiki** 的實作——見 [[LLM-Wiki-知識管理模式]]。適合對特定主題深度研究、跨來源互聯；作者原意即「不是操作性記憶，而是內容消化型第二大腦」。
- [[Hermes-Agent]] 出現在來源的開場清單，屬「agent 自策展記憶 + skill」路線；且其 `hermes claw migrate` 對應本文 Level 3 反覆提到的 **openclaw** 記憶架構（memsearch 即移植自 openclaw）——Hermes 與 openclaw 同一血緣，值得日後專門對照。

## 關聯

- 原始逐字稿：[[Every-Claude-Code-Memory-System-Compared-(So-You-Don't-Have-To)]]
- Level 5 深入：[[LLM-Wiki-知識管理模式]]、[[LLM-Wiki-Karpathy]]
- openclaw 血緣的 agent：[[Hermes-Agent]]
