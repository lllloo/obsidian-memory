---
title: 穴居人式 Claude Code 才是新王道（附科學依據）
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-07
source: https://www.youtube.com/watch?v=4FO1Liu-ttk
---

## 描述

分析 Caveman GitHub 專案（72 小時內 5,000 stars），說明強制 Claude Code 簡短回應的實際 token 節省幅度，並解讀背後的學術研究依據。

## 重點摘要

**Caveman 是什麼**
- 強制 Claude Code 像穴居人一樣說話的 skill 集合，刪除所有冗餘回應
- 宣稱可節省 75% 輸出 token、45% 輸入 token
- 安裝只需一行指令，透過 `/caveman` 或自然語言（如「talk like a cave man」）啟用
- 有三個等級：light、full、ultra caveman

**實際 token 節省分析**
- 一個 100,000 token 的 Claude Code session 中，輸出只佔 25%
- 輸出中的「散文回應」（Caveman 影響的部分）僅佔輸出的一小部分
- 實際效果：每個 session 約節省 4–5% 的總 token，而非宣傳的 75%
- 仍值得使用，但要有正確預期

**研究論文支撐**
- 論文：「Brevity Constraints Reverse Performance Hierarchies in Language Models」（2026 年 3 月）
- 研究規模：31 個模型、1,500 個問題
- 發現：近 8% 的問題中，大型模型被小型模型以 28 個百分點差距擊敗（儘管參數量差距達 100 倍）
- 原因：大型模型「過度冗長」，在推理過程中繞圈子並得出錯誤答案
- 解決方案：強制簡潔後，準確率提升 26 個百分點，效能差距縮小多達三分之二
- 根本原因：強化學習訓練時，人類評分者偏好更詳盡的回答，導致模型被訓練為「更囉嗦」

**實用建議**
- 不想用穴居人設定的話，至少在 CLAUDE.md 加入：「Be concise. No filler. Straight to the point. Use less words.」
- 適合簡單問題；複雜推理任務的效果可能不同
- 不影響程式碼生成、錯誤訊息等底層行為，只改變文字回應
