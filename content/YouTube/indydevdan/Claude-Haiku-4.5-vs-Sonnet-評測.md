---
title: Claude Haiku 4.5 閃電速度 Agentic 編碼：能打敗 Sonnet 嗎？
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-10-20
source: https://www.youtube.com/watch?v=aA9KP7QIQvM
---

## 核心問題：何時用 Haiku 取代 Sonnet？

Haiku 4.5 是 Anthropic 的「便宜快速計算模型」，核心優勢：
- **速度**：平均每次 tool call 比 Sonnet 快近 1 秒；達到 100-200+ tokens/秒
- **價格**：Sonnet 的 1/3（含 cache 後更便宜）
- **思考能力**：Haiku 4.5 是 thinking model（3.5 是純 base model）

## 實測比較（三個任務）

### 任務一：文件摘要（Find & Summarize Files）

- Haiku：74 events，36 tool calls，更快完成
- Sonnet：找到 32 個檔案；Haiku：只找到 31 個（漏掉 1 個，3% 失誤率）
- Sonnet 的 summary 按照「第二句說明檔案在哪裡被使用」的指令，Haiku 幾乎完全忽略這個要求

**結論**：Haiku 快但不精確，對 prompt 的複雜指令追蹤較弱

### 任務二：規劃新功能（Planning）

- 任務：規劃三個新功能（UI themes、10 分鐘 activity timer、regex 搜尋）
- Haiku 違反了 prompt 中「不要用 sub-agent」的指令，自己跑了 sub-agent
- Sonnet 的計畫比 Haiku 長 3-4 倍，細節豐富得多

**結論**：Haiku 不是好的規劃器，無法深度思考，輸出表面層次的計畫

### 任務三：實際 Coding（Build Feature）

- Haiku 在 ~3 分鐘內完成，25 tool calls
- 成功實作：regex 搜尋欄、10 分鐘 timer
- 失敗：三個 UI theme 的 wiring 沒完成（顏色存在但沒接上去）

**結論**：可以做中等複雜度的 coding，但會漏掉重要細節

### 任務四：抓取文件並回答問題（Fetch Docs）

- 結果：Haiku 和 Sonnet 幾乎相同
- 有趣：在某個問題上，Haiku 反而抓到 Sonnet 漏掉的細節
- 兩個模型都給出很好的結構化摘要

**結論**：文件抓取與問答，Haiku 表現接近 Sonnet

## 模型定位

**Haiku 適合（便宜版）：**
- 文件摘要、結構化資料摘要
- 簡單程式碼生成
- Pattern matching
- 作為 Scout agent（快速蒐集資訊）
- 事件摘要（大量 agent events 的 real-time 摘要）
- 檔案重構（由 Sonnet 規劃，Haiku sub-agent 執行，Sonnet 驗收）

**Sonnet 適合（貴但強）：**
- 規劃與架構設計
- 複雜 debug
- 長時間 agentic coding jobs
- 生產環境的安全敏感工作
- 需要精確遵循複雜指令的任務

## Agent Model Stack 概念

```
Haiku (weak) → Sonnet (base) → Opus (strong)
便宜快速      → 均衡          → 強大但貴
```

每家 AI 公司都有類似的模型堆疊，關鍵在於：
- 有「optionality」可以在對的時機用對的模型
- 不要為了 Sonnet 能做的工作付 Opus 的價錢
- 不要為了 Haiku 能做的工作付 Sonnet 的價錢

**實際應用規則**：新開任務時先問「Haiku 能完成這個嗎？」能的話就用 Haiku。

## 效能衡量指標

`Tool calls ≈ 計算量 ≈ 產出影響`

越多 tool calls 在越短時間內 = 越高效率（前提：在做有價值的工作）。
