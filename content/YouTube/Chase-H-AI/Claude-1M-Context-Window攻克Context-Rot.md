---
title: Claude 1M Context Window 攻克 Context Rot
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-14
source: https://www.youtube.com/watch?v=dk0QMbsdV8s
parent: "[[01.index]]"
---

## 重大突破

Anthropic 對 Opus 4.6 和 Sonnet 4.6 全面開放 1M token context window。真正值得關注的不是 token 數量的增加，而是**效能在大 context 下沒有大幅下降**——這才是過去幾年「超大 context window」一直是假命題的根本問題所在。

## 數據解析（Eight Needle Test）

Eight Needle Test：在長達百萬 token 的對話中，隨機放置 8 個「針」（特定請求），在不同 token 深度問模型把這些針找回來。

| 模型 | 分數 |
|------|------|
| **Opus 4.6** | **78.3%**（256K → 1M，僅下降 14%） |
| GPT-4 5.4 | 36% |
| Gemini 3.1 Pro | 26% |
| Sonnet 4.5 | 18.5% |
| Opus 4.5（前代） | 與 Gemini 相近 |

從 Opus 4.5 到 4.6：
- Context window 從 200K 擴展到 1M（5 倍）
- 效能提升 3 倍
- 750,000 token 的旅程中只下降 14%

對比 Chroma 去年的 Context Rot 研究：當時所有模型在超過 100K tokens 後都出現斷崖式效能下滑，這已成為 Claude Code 使用者的操作準則。

## 對 Claude Code 使用習慣的影響

**舊準則（Chroma 研究後）**：到 100K-120K tokens 必須 clear，否則輸出品質會顯著下降。

**新準則**：
- 每增加 100K tokens 約損失 2% 效能（粗略估算）
- 不再需要焦慮地在 100K 就清空 context
- **如果可以清，仍建議清**（從 0 開始總比從 700K 開始好）
- **如果需要繼續**，可以放心維持更長的對話，不必做各種 hacky 的 context 管理

## 其他細節

**可用範圍**：需要 Claude Code Max plan、Teams 或 Enterprise。

**定價調整**：之前超過 200K tokens 有額外費率，現在無論 9K 還 900K tokens，費用相同。

**媒體容量**：圖片/PDF 頁面上限從 100 提升到 600，效能仍穩定。

**1M tokens 下 Opus 4.6 的意義**：即便在 1M tokens 時，效能仍與 GPT-4 5.4 相當，遠超 Gemini 3.1 Pro。這才是真正的技術突破。

Claude Code 的 autocompact buffer 仍為 33K tokens，這部分不變。
