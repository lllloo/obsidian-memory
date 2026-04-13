---
title: Claude Code 推出 Plan Mode 2.0 了嗎
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-06
source: https://www.youtube.com/watch?v=eEYbwJWVQtQ
---

## 描述

測試 Claude Code 新功能 Ultra Plan，與傳統 Plan Mode 進行頭對頭比較，評估兩者在速度、品質與 skill 呼叫方面的差異。

## 重點摘要

- **Ultra Plan 是什麼**：Claude Code 洩漏資料中出現的新功能，已正式發布。在本地 terminal 啟動 plan mode 後，將計畫推送至雲端 Claude 網頁介面進行處理
- **啟用方式**：在最新版 Claude Code 輸入 `ultraplan` 或 `/ultraplan` 即可觸發，需事先建立含至少一個 commit 的 GitHub repo
- **速度差異顯著**：Ultra Plan 約 30 秒完成規劃，本地 Plan Mode 同一任務花費超過 5 分鐘
- **使用者介面優勢**：Ultra Plan 提供網頁介面，可直接 highlight 計畫內容留言修改，比在 terminal 輸入更直覺
- **主要缺點**：測試中 Ultra Plan 未遵循 prompt 中指定的 frontend design skill，忽略了 Google Fonts 等設計細節；本地 Plan Mode 則有正確呼叫 skill
- **程式碼品質**：由另一個 Claude Code session 比較兩個方案，差異不大，Ultra Plan 多出幾百行程式碼
- **適用場景**：Ultra Plan 可能在極度複雜的大型專案才能展現優勢，小型 Kanban board 測試不足以拉開差距
- **結論**：尚不建議完全取代本地 Plan Mode，skill 無法正確呼叫是重大問題，建議自行測試複雜專案
