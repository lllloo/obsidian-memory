---
title: "35 個 Claude Code 概念全解析（非工程師也能懂）"
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
published: 2026-04-08
source: https://youtu.be/UAMAAoSPu8o
---

**影片描述**：Chase H 專為非技術背景用戶整理 35 個 Claude Code 核心概念，分四個學習階段從入門到 Power User。目標是讓完全新手也能建立清晰的路線圖，不被每天湧出的新功能壓垮。

**重點摘要：**
- claude.ai vs Claude Code 的最大差異：兩者用同樣的 AI 大腦（Opus 4.6），但 Claude Code 有「手」——能實際操作電腦（寫程式、存取檔案、與系統互動），claude.ai 只能對話。
- 安裝只需一行指令：Mac/Linux/WSL 和 Windows PowerShell 各有對應版本，輸入 `claude` 即可啟動；推薦用 VS Code 作為入門環境，既有終端機又能看到檔案結構。
- 三種權限設定：預設（每次確認）、Accept Edits On（自動編輯文件但 bash 指令仍需確認）、`--dangerously-skip-permissions`（完全略過，效率最高但需謹慎）；多數用戶最終都停在第三種。
- Plan Mode 的核心價值：強迫 Claude Code 先規劃再執行，透過來回問答填補 prompt 的漏洞；是提升輸出品質最簡單的方式。
- 使用心態最重要：不要只是盲目按 Accept——當 Claude Code 推薦技術棧時，要追問「為什麼用這個」，Claude Code 是無限耐心的導師，主動追問才能與只會複製貼上的「vibe coder」區別開來。
- CLAUDE.md 是專案記憶文件：Claude Code 每次執行任何操作都會參考它，放的內容要真正重要且幾乎適用於所有 prompt；Claude Code 建立專案時會自動生成。
- Context Window 管理是隱藏的高階技能：建議不超過 20 萬 tokens；越接近上限，Claude Code 效能越差且每次 prompt 成本越高；用 `/clear` 重置 session，Claude Code 會從 codebase 而非對話記憶恢復狀態。
- 進階概念包含：Skills（Markdown 指令集）、Plugins（官方市集）、Multi-agent（平行處理）、MCP（連接外部工具）、Git 整合、Ultra Plan、LightRAG、Obsidian 知識庫、GWS CLI 等，新手不需馬上學，知道存在即可。
