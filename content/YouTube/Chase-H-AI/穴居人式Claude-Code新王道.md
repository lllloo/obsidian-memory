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

## Caveman 是什麼

GitHub repo「why say many word when few word do trick」：強制 Claude Code 像穴居人一樣說話，刪除所有冗餘文字回應，72 小時內累積 5,000 stars。

**宣稱效果：** 節省 75% 輸出 token、45% 輸入 token。

**安裝：** 一行指令。啟用方式：`/caveman`、或說「talk like a cave man」、「cave man mode」、「less tokens please」。

三個等級：`light`、`full`、`ultra caveman`。

注意：error message 原文照錄不動；程式碼生成、底層推理完全不受影響，只改變文字回應。

## 實際 token 節省量（不是宣傳數字）

以 100,000 token session 為基準拆解：

```
總 token：100,000
├── 輸入（75%）：75,000 tokens
│   └── 系統提示（Claude.md 等）← Caveman 壓縮影響此處
│       實際節省：~1,000–2,000 tokens（非宣稱的 45%）
└── 輸出（25%）：25,000 tokens
    ├── tool calls（工具呼叫）
    ├── code blocks（程式碼）
    └── prose responses（文字回應）← Caveman 影響此處
        實際節省：~4,000 tokens（非宣稱的 75%）
```

**實際總節省：約 4–5%（~5,000 tokens/session）**，非 75%。

5% 仍然值得，尤其在高頻使用的環境下累積效果明顯，但不要期望能從 5x 方案升級到 20x 方案。

## 學術研究支撐

論文：**「Brevity Constraints Reverse Performance Hierarchies in Language Models」**（2026 年 3 月）

- 規模：31 個模型、1,500 個問題（皆為開放權重模型）
- 發現：在近 8% 的問題中，大型模型被小型模型以 **28 個百分點**差距擊敗，即使參數量差距達 100 倍（如 2B 模型擊敗 400B 模型）
- 原因：大型模型「過度冗長（spontaneous scale-dependent verbosity）」，在推理時繞圈子導致得出錯誤答案，研究稱之為 **overthinking**
- 解決方案：強制簡潔後，準確率提升 **26 個百分點**，效能差距縮小最多達 2/3

**根本原因：** 訓練時的 RLHF（強化學習+人類評分），人類評分者偏好更詳盡的回答，導致模型被訓練為「更囉嗦」而非「更正確」。

研究結論：brevity constraints 完全逆轉了效能階層，大型模型從輸給小型模型，變成重新勝出。

## 實用建議

即使不使用 Caveman，至少在 `CLAUDE.md` 加入：

```
Be concise. No filler. Straight to the point. Use less words.
```

這對簡單直接的問題效果最明顯。複雜推理任務的效益可能不同（研究中的案例偏向直接問答類問題）。
