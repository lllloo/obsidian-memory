---
title: Google Gemma 4 顛覆開源 AI 格局
tags:
  - youtube
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-08
source: https://www.youtube.com/watch?v=-01ZCTt-CJw
---

## 真正意義上的開源 AI

- Google 發佈 Gemma 4，採用 **Apache 2.0 授權**，是真正自由的開源，不附加商業限制
- 相比之下：Meta Llama 有特殊授權條款、OpenAI GPT OSS 模型雖 Apache 2.0 但更大更笨、Mistral 與中國模型（Qwen、GLM、Kimi、Deepseek）填補市場
- Gemma 4 的特別之處：Made in America、Apache 2.0、智能高、體積小

## 驚人的小尺寸

- 31B 參數版本表現接近 Kimi K2.5 Thinking
- 可用 20GB 下載在單張 RTX 4090 跑，速度約 10 tokens/秒
- 相比 Kimi K2.5 需要 600GB+ 下載、256GB RAM、多張 H100
- Edge 版本小到可在手機或 Raspberry Pi 上執行

## 背後技術：TurboQuant

Google 同步發佈了 **TurboQuant** 量化技術，突破一般「縮小即降效」的瓶頸：

1. 將 XYZ 笛卡爾座標系的資料轉為極座標（半徑 + 角度），利用角度的可預測規律跳過正規化步驟，減少記憶體開銷
2. 使用 **Johnson-Lindenstrauss 轉換**，將高維資料壓縮為單一符號位元（+1 / -1），同時保留資料點間的距離關係

> TurboQuant 並非 Gemma 4 小型化的直接原因，而是另一個平行研究成果。

## Per-Layer Embeddings

Gemma 4 模型名稱帶有「E」（如 E2B、E4B）代表「有效參數」，核心機制是 **per-layer embeddings**：

- 傳統 Transformer：每個 token 在開頭取得一個 embedding，必須攜帶資訊貫穿所有層
- Per-layer embeddings：每一層都有自己專屬的 token mini cheat sheet，資訊在最需要的時機才引入，大幅提升效率
- 結果：模型小、智能高、適合 fine-tuning（可搭配 Unsloth 工具）

## 使用場景

- 適合本地部署、個人實驗、fine-tuning 自有資料
- 作為編程工具仍不及 Claude Code 等高端工具
