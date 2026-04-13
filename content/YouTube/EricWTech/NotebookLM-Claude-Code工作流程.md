---
title: "這個 NotebookLM + Claude Code 工作流程強得誇張"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-26
source: https://youtu.be/fV17ZkPBlAc
---

**影片描述**：示範如何結合 NotebookLM 與 Claude Code，透過開源工具 `notebooklm-py` 讓 AI Agent 能程式化存取 NotebookLM 的所有功能，以 BookZero.ai 的 35 個競品深度分析為實際案例，展示從建立 Notebook、插入來源到下載研究報告的完整自動化流程。

**重點摘要：**
- **為何結合這兩個工具**：Claude Code 擅長「執行」（寫程式、呼叫工具），NotebookLM 擅長「理解」（將雜亂文件與研究資料整理成 grounded 結構化知識）；組合後先用 NotebookLM 建立知識庫，再將理解結果傳給 Claude Code 執行後續動作。
- **notebooklm-py 開源工具**：提供完整的 NotebookLM CLI 與 Python API，支援建立/列出/重新命名/刪除 Notebook、插入來源、擷取問答歷史、設定 persona、切換深度/快速研究模式、下載音訊/影片/投影片等所有 Web UI 功能。安裝：`pip install notebooklm-py[browser-login]`，首次透過瀏覽器 Google 登入後憑證儲存在根目錄。
- **整合到 Claude Code**：兩種安裝 Skill 的方式效果相同——`notebooklm install-skill`（CLI）或 `npx` 的 open skill ecosystem 指令；安裝後 Claude Code 可用 Slash 指令或自然語言呼叫 NotebookLM 功能。
- **實際案例：BookZero.ai 35 個競品分析**：Tier 1（8 個核心競品）進行深度研究、Tier 2（40 個競品）快速查詢，合計約 250 個來源放入 Notebook 1；Tier 3（17 個競品）約 136 個來源放入 Notebook 2；Claude Code 自動完成建立 Notebook、插入來源、執行研究、下載結果（PPT、MD、JSON 三種格式）。
- **實際問答示例**：問「基於競品分析，BookZero 的賣點是什麼？」，NotebookLM 回答核心賣點為「超快速 AI 收據提取與比對」及「三步驟極簡流程（上傳→匯入→比對）」，並建議產品方向延伸至即時帳務對帳與自動化財務洞察。
- **延伸應用場景**：技術決策（分析 Jira 票券 + 知識庫決定功能方向）、內容行銷（結合 SEO skill 與競品知識庫生成比較型部落格文章）。
- **工具組合價值**：讓 AI Agent 不只「執行」，還能先「理解」大量非結構化資料後再行動，特別適合需要從大量來源中萃取洞察的競品分析、市場研究等任務。
