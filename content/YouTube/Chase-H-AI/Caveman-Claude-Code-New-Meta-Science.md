---
title: "Caveman Claude Code Is the New Meta (Here's the Science)"
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/4FO1Liu-ttk
---

Chase H 深入分析 Caveman Claude Code 的原理：強迫 Claude Code 說話像穴居人，不只省 token，還可能提升輸出品質。

## Caveman 是什麼

GitHub repo「caveman」（72 小時內獲 5,000 stars）強迫 Claude Code 用最簡短的語言回應，去除所有冗詞。目標：省 token + 提升效能。

## Token 節省的真實數字

repo 宣稱省下 75% output tokens，但實際上需要拆解：

- **Output tokens 組成**：tool calls + code blocks + **prose 回應**（Claude 的文字說明）
- Caveman 只影響 prose 回應部分，約佔總 session 的 6%
- 實際節省：**總 session 約 4%**，非 75%
- Input tokens（CLAUDE.md 壓縮）：約省 1-2% of 總 session
- **合計：每個 session 省約 5%**

雖然不是誇大的數字，但長期累積仍有意義，尤其對用量受限的用戶。

## 科學支持：研究論文

論文：*Brevity Constraints Reverse Performance Hierarchies in Language Models*（2026 年 3 月）

- 評估 31 個模型、1,500 個問題
- 核心發現：大型模型在約 8% 的問題上，被比自己小 100 倍的模型打敗
  - 例：2B 參數模型勝過 400B 參數模型
- 原因：**RLHF 訓練偏差**——人類評分者偏好詳細回答，導致大模型傾向過度冗長，反而自我矛盾答錯
- 術語：spontaneous scale-dependent verbosity（規模依賴的冗長性）

### 施加 brevity 限制後的效果
- 準確率提升最多 **26 個百分點**
- 效能差距縮小達 **2/3**
- 原先輸給小模型的場景，強制簡潔後反轉勝出

## 如何使用

```bash
/caveman          # 標準模式
/caveman ultra    # 極端模式（剛爬出海洋）
/caveman light    # 輕量模式
```

或直接說：「talk like a caveman」、「less tokens please」

- 不影響程式碼生成、tool calls、error messages（完整保留）
- 只改變 Claude 的文字說明輸出

## 結論

即使不用 Caveman，至少在 CLAUDE.md 加一行：

> Be concise. No filler. Straight to the point. Use less words.

科學顯示這對效能有正面影響，不只是省 token。
