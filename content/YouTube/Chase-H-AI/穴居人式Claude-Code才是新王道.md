---
title: "穴居人式 Claude Code 才是新王道（科學原理解析）"
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
published: 2026-04-07
source: https://youtu.be/4FO1Liu-ttk
---

**影片描述**：Chase H 深入分析 Caveman Claude Code（72 小時獲 5,000 stars 的 GitHub repo），拆解它真正能省多少 token、揭示 repo 數字有多誇大，並引用 2026 年 3 月的研究論文說明強制簡潔為何能提升 AI 效能而非只是省 token。

**重點摘要：**
- Caveman repo 宣稱省下 75% output tokens 和 45% input tokens，但這些數字嚴重誤導：只適用於 prose 回應（文字說明）和 CLAUDE.md 等特定部分，並非整體 session。
- 真實計算（以 100K token session 為例）：output 中 prose 約佔 6K tokens，省 4K = 約省 **4%**；input 中 CLAUDE.md 壓縮約省 **1-2%**；合計每個 session 省約 **5%**——不誇張，但長期累積有意義。
- Caveman 完全不影響程式碼生成、tool calls、error messages，只改變 Claude 對你說話的文字風格。
- 更重要的是 2026 年 3 月的研究論文：*Brevity Constraints Reverse Performance Hierarchies in Language Models*——評估 31 個模型、1,500 個問題。
- 研究核心發現：大型模型在約 8% 的問題上被參數量小 100 倍的模型打敗（如 2B 參數模型勝過 400B 參數模型），原因是「spontaneous scale-dependent verbosity」——大模型因 RLHF 訓練偏好詳細答案，導致過度冗長，反而自我矛盾答錯。
- 施加 brevity 限制後：準確率提升最多 **26 個百分點**，效能差距縮小達 **2/3**，原先輸給小模型的場景強制簡潔後反轉勝出。
- 使用方式：`/caveman`（標準）、`/caveman ultra`（極端）、`/caveman light`（輕量），或直接說「talk like a caveman」。
- 即使不用 Caveman，至少在 CLAUDE.md 加一行：「Be concise. No filler. Straight to the point. Use less words.」——科學顯示這對效能有正面影響，不只是省 token。
