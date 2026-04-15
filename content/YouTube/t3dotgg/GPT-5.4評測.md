---
title: GPT-5.4 評測
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-06
source: https://www.youtube.com/watch?v=HD5TWE8xD7o
---

## 版本說明

- GPT-5.3 Codeex → GPT-5.3 Instant → **GPT-5.4 Thinking**（跳過 5.3 Thinking）
- 同日發布 GPT-5.4 Pro（$30/M input, $180/M output）
- Codeex 模型系列可能到此為止，「Codeex」改為指產品線（CLI、app）而非模型

## 主要改進

**推理效率**
- 使用更少 reasoning tokens 達到相同結果；Medium 約 500 tokens，High 約 1,100 tokens
- X High 反而可能過度推理導致退步，建議一般用 High

**情境控制**
- 支援 100 萬 tokens 上下文（超過 272k 以 2x input + 1.5x output 計費）
- 明顯改善「插入新指令不忘舊任務」的問題
- 對話中途加入修正（mid-conversation steering）更可靠

**工具使用**
- Tool Search：模型能依需求找工具，不再預設所有工具都在 context 中
- 瀏覽器操作改用 JavaScript 執行（而非像素座標點擊），速度與準確度大幅提升
- 工具呼叫數減半但 Towne bench 表現更好
- Web search 準確度：89.3%（vs 5.2 的 65.8%）

**回歸項目**
- Function call 中的 prompt injection 命中率從 0% 退步到約 2%，需注意使用者生成內容

## Skate Bench V2 成績

- Gemini 3.1 Pro Preview：97%
- GPT-5.4 High：82%
- GPT-5.4 X High：81%（過度推理反而差）
- GPT-5.4 Pro Thinking：79%

## 費用

- 5.4 High：$2.50/M in, $15/M out（略高於 5.2）
- 5.4 Pro：$30/M in, $180/M out
- Artificial Analysis 全套測試費用：$2,951（vs 5.2 的 $234）；仍比 Opus 4.6 和 Sonnet 4.6 便宜

## 仍然不擅長的領域

- **前端 UI 設計**：GPT-5.4 在視覺設計依然落後 Opus 和 Gemini 一個世代
- UI 任務建議：先用 Gemini 做頁面佈局，精細調整交給 Opus；GPT 的「到處放卡片」風格仍然嚴重

## Goldbug 挑戰（Pro 能力展示）

- GPT-5.4 Pro 在 17 分鐘內解出 Defcon Goldbug 的 C-Shanty 密碼題（Theo 團隊花了 3 天）
- 此前無任何模型接近解出

## 提示技巧

- 模型非常服從指令，system prompt 影響力遠超以往
- 官方提示指南建議：明確指定工具路由、是否可並行、何時應詢問使用者確認
- 在 context 還薄的對話初期，工具路由可能不準確，建議先給前置條件說明
- 可透過輸出合約（output contract）嚴格控制回應格式
