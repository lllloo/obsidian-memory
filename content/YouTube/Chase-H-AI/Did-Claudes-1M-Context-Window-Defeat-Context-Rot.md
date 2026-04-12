---
title: Did Claude's 1M Context Window Defeat Context Rot?
tags:
  - youtube
  - claude-code
  - context-window
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/dk0QMbsdV8s
---

Anthropic 正式釋出 Claude Opus 4.6 與 Sonnet 4.6 的 100 萬 token context window，並探討這是否真正解決了長期困擾大型語言模型的 context rot 問題。

## 重點摘要

- **100 萬 token 正式上線**：Opus 4.6 與 Sonnet 4.6 全面支援，需 Claude Max、Teams 或 Enterprise 方案
- **Eight Needle Test 數據**：
  - Opus 4.6：78.3（從 256K 到 1M token 僅下降約 14%）
  - GPT 4.5：36
  - Gemini 3.1 Pro：26
  - Sonnet 4.5：18.5
  - Opus 4.5 thinking（128K）：27.1
- **Opus 4.5 → 4.6 的躍進**：context window 從 200K 擴展至 1M（5 倍），有效性提升約 3 倍，是巨大的突破
- **對比過去的 context rot**：Chroma 去年的研究顯示，過去模型在 100K-200K token 後就急劇退化；Opus 4.6 的曲線平緩得多
- **價格不變**：9K token 與 900K token 價格相同，不再有倍率加成
- **媒體限制提升**：圖片/PDF 頁面上限從 100 提升至 600

## 實務建議

- **不再需要在 100K-120K 時強制 clear**：可以繼續工作更長時間
- **每 100K token 約損失 2% 效能**：作為粗略估算基準
- **仍有 33K token 的 autocompact buffer**
- **如果不需要維持 session**：還是在 200K 附近 clear 最佳，不必承受任何退化
- **如果需要大 codebase**：現在可以放心使用更大的 context

## Eight Needle Test 說明

在 100 萬 token 的對話中，嵌入 8 首關於狗的詩，然後在不同 token 位置要求模型回憶特定那首詩。越後面的測試越難，用來衡量模型的長程記憶能力。
