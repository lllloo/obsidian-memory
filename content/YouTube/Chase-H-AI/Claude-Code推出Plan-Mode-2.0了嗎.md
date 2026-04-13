---
title: "Claude Code 剛推出 Plan Mode 2.0 了嗎？"
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
published: 2026-04-06
source: https://youtu.be/eEYbwJWVQtQ
---

**影片描述**：Chase H 實測 Claude Code 的 Ultra Plan（從洩漏文件曝光後正式發布）與傳統 Plan Mode 的頭對頭比較，測試對象為 Kanban Board Web App。結論：Ultra Plan 速度大勝，但有無法正確呼叫 Skills 的重大缺陷。

**重點摘要：**
- Ultra Plan 的運作方式：在終端啟動後，規劃被推送至雲端執行，用戶在瀏覽器中看到帶 Mermaid 架構圖的完整規劃，可直接反白標注修改意見，批准後帶回終端執行。
- 使用前提：需要已有至少一個 commit 的 GitHub repo，即使只是 README 也算。觸發方式：輸入 `/ultraplan` 或直接說「ultra plan」。
- 速度差距顯著：Ultra Plan 30 秒內完成規劃；Local Plan Mode 花了 5 分 30 秒（且第一次還卡住需重試）。
- 關鍵缺陷：Ultra Plan 完全忽略了 prompt 中明確指定的 Skills（如前端設計 skill），導致沒有使用 Google Fonts 等效果，視覺品質明顯遜於 Local Plan Mode 的輸出。
- 文件說明極度不足：外界盛傳 Ultra Plan 有「額外 agents 與資源」，但官方文件完全沒有說明，只知道它推到雲端執行。
- 程式碼品質方面：兩者差異不大，Ultra Plan 的版本多了幾百行程式碼，但功能基本等同。
- Skills 問題在 Chase 額外測試中也重現，並非個案——對 Skills 重度用戶來說是重大減分。
- 結論：Ultra Plan 不會取代 Local Plan Mode；速度快但缺 Skills 支援，建議在複雜專案自行評估，簡單專案的測試並不能代表真實場景。
