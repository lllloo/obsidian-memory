---
title: Claude Code 記憶系統六層比較
description: 從原生 CLAUDE.md 到跨工具統一大腦，六個層級的 AI 記憶方案沿「儲存位置」與「召回機制」兩軸拆解，含各層適用情境與升級門檻
created: 2026-07-08
updated: 2026-07-24
parent: "[[wiki/01.index]]"
tags:
  - claude-code
  - memory
  - context-engineering
  - rag
  - knowledge-graph
---

# Claude Code 記憶系統六層比較

各家 AI 記憶方案（Mem0、Karpathy LLM Wiki、OpenClaw、Hermes、MemPalace、LightRAG、ClaudeMem…）其實**不是互相競爭，而是不同使用情境下處理記憶的不同方式**。它們回答同一個問題：給 agent 一個任務時，如何在正確時機取得正確 context？來源見 [[Every-Claude-Code-Memory-System-Compared-(So-You-Don't-Have-To)]]。

> **證據強度**：本頁對各方案機制的描述（儲存/召回實作、血緣關係如「memsearch 移植自 OpenClaw」「MemPalace 用 SQL+Chroma」「OpenBrain 用 Supabase Postgres」）均出自上述**單一影片來源**的主講人陳述，未經獨立查證、非對抗式驗證結果；引用個別機制細節前宜回查各方案官方文件（2026-07-10 標註）。

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
| **3** 語意搜尋 | **memsearch**（Zilliz，移植自 OpenClaw）／ ClaudeMem | markdown + 語意向量 | UserPromptSubmit hook 自動注入 top-N 語意匹配 | 用超過一個月、檔案變多、關鍵字搜尋失效 |
| **4** 逐字召回 | **MemPalace** | 本地 SQL（實體關係）+ Chroma vector（逐字分塊） | session end / pre-compaction hook 背景索引；記憶宮殿式定址 | 想找當初決策的「確切文字」 |
| **5** 自組織知識庫 | **Karpathy LLM Wiki** ／ Recall（代管）／ LightRAG（企業級） | 純 markdown，raw + wiki 兩層 | 讀 index 找頁再鑽（無需 vector DB） | 定期消化文章/影片/podcast，要跨來源互聯的「第二大腦」 |
| **6** 跨工具單一大腦 | **OpenBrain**（Nate Jones）／ Mem0 | OpenBrain：自有 Postgres（Supabase），`thoughts` 表 + embedding；Mem0：純雲端 SaaS，官方整合路徑無法指向自架後端（見下「取捨」節與 [[Mem0]]） | MCP server 當前門，各 AI 工具共用同一 DB | 跨多個 AI 工具（手機 ChatGPT、桌面 Claude Code…）要共用記憶 |

Level 1–3 資料夾結構相近、**可疊加同跑**；Level 5、6 屬不同領域（不只記憶對話，而是互聯知識 / 跨工具共腦）。

## 幾個關鍵取捨

- **markdown 優先 vs. vector/MCP**：memsearch 把一切存成可讀 markdown 並自動注入；ClaudeMem 走 MCP，需 Claude 主動決定呼叫搜尋工具，功能多（dashboard、團隊、費用追蹤）但較重。
- **本地擁有 vs. 代管租用**：MemPalace 全本地；OpenBrain 是自有 DB 實例（跑在 Supabase 代管平台上，但 schema 與資料歸你、可遷移自管）；Recall、Mem0 則是 vendor 的記憶即服務，資料活在對方伺服器（可匯出 markdown，但等於租）。**Mem0 需分層看**（2026-07-20 查證修正）：軟體本身是原版 Apache 2.0、可完全自架（raw LICENSE 實查，無 Commons Clause／BUSL 附加），但**官方整合路徑（plugin／MCP／CLI）全部只連雲端**，要自架得走社群 MCP 或自接 SDK。故「等於租」對採用體驗成立、對軟體授權不成立——細節與失效模式見 [[Mem0]]。
- **摘要 vs. 逐字**：Level 3 存摘要（省空間、可能漏細節）；Level 4 逐字不摘要，理論上什麼都不丟，但取回內容非 markdown、不可直讀。

## 在本 vault 的定位

- 本 vault 就是 **Level 5 / Karpathy LLM Wiki** 的實作——見 [[LLM-Wiki-知識管理模式]]。適合對特定主題深度研究、跨來源互聯；作者原意即「不是操作性記憶，而是內容消化型第二大腦」。
- [[Hermes-Agent]] 出現在來源的開場清單，屬「agent 自策展記憶 + skill」路線；且其 `hermes claw migrate` 對應本文 Level 3 反覆提到的 **OpenClaw** 記憶架構（memsearch 即移植自 OpenClaw）——Hermes 與 OpenClaw 同一血緣，值得日後專門對照。

## 關聯

- 原始逐字稿：[[Every-Claude-Code-Memory-System-Compared-(So-You-Don't-Have-To)]]
- Level 5 深入：[[LLM-Wiki-知識管理模式]]、[[LLM-Wiki-Karpathy]]；Level 5 的生態實作全景（nvk、Hermes skill、Astro-Han、Letta MemFS）見 [[LLM-Wiki-生態實作比較]]
- OpenClaw 血緣的 agent：[[Hermes-Agent]]
- 人類 PKM 方法論對照：[[第二大腦方法論比較]]（BASB／PARA／Zettelkasten，與本頁討論的 agent 記憶方案分屬不同層次，但共享「擷取—組織—檢索」結構性問題）
- coding agent 訂閱生態對照：[[LLM-方案定價與-coding-agent-比較]]（Claude Code 等三方案定價與模型天花板比較，與本頁的記憶系統選型同屬「怎麼選 coding agent」的決策脈絡）
- harness 工程脈絡：[[Agent-Harness-Engineering-框架綜述]]——本頁六層記憶方案在 Anthropic context engineering 論述中對應 structured note-taking／agentic memory 技術，理論依據見該頁。
- Level 5 路線的失效面：[[Agent-維護知識庫的已知失效模式]]——本頁列各層方案怎麼運作，該頁記 Level 5（自組織知識庫）長期由 agent 維護會怎麼壞，並標明 model collapse 類比不成立；向量／自動抽取路線（Level 3、Mem0）的失效模式則見 [[Mem0]]。
- 記憶方案的共同風險實證：[[AI-自主工作流的實證檢驗]]——記憶檔過長會被 agent 忽略、compaction 靜默丟棄約束，是本頁各層方案共通的失效模式。
- 按「目的」切的互補視角：[[Agent-記憶兩大路線-知識庫與-memory-bank]]——本頁按「儲存／召回」技術光譜切六層，該頁按「知識資產複利 vs 專案工作記憶」切兩路線，並補收本頁未正面收的 coding-agent memory bank（Cline 等）。
- 記憶分層的觀念前身：[[Building-Effective-Agents-Anthropic]]——該文 augmented LLM 的 memory 增強是本頁六層方案的最小前身；本頁把「最小、可組合的 context 元件」原則展開成完整的儲存／召回光譜。
- 跨 repo 消費本頁結論的路徑：[[跨專案第二大腦整合模式]]——該頁的 context manifest 與 ADR 回鏈範例都以本頁為被引用的共用研究頁，是本頁選型結論外送到其他專案的具體交接格式。
- 多 agent 場景的記憶對應：[[多智能體研究系統-Anthropic]]——該系統的 external memory 與 subagent handoff（把成果寫回共享記憶再交棒）正對應本頁的記憶分層，是六層方案在多智能體協作下的落地形態。
