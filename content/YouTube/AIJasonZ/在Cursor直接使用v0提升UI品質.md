---
title: 在 Cursor 直接使用 v0 提升 UI 品質
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-05-25
source: https://www.youtube.com/watch?v=0KYWJWY62d4
parent: "[[01.index]]"
---

## v0 模型整合 Cursor

v0 釋出了自己的 AI model，可直接在 Cursor 內使用，帶來比預設模型更好的 UI 生成品質。

## 設定步驟

1. 開啟 Cursor 設定 → Models
2. OpenAI Base URL 填入：`api.v0.dev/v1`
3. 前往 v0.dev → Settings → 產生 API key
4. 貼回 Cursor 並點 Verify

注意事項：
- Cursor 目前不原生支援 v0 model，需透過 OpenAI 相容 API 接入
- 使用 v0 model 時需開啟 OpenAI API key；切回 Claude 時記得關掉，否則會出現錯誤提示
- 呼叫 GPT-based model 時，背後實際呼叫的是 v0 model

## 使用工作流

**適合用 v0 model 的場景：**
- 建立主畫面的視覺基礎（spacing、font、color 風格定調）
- 一次建一個頁面，不要要求建整個應用（v0 在複雜 scaffolding 上容易卡住）

**切換策略：**
1. 先用 v0 model 建出主要畫面，確立設計風格
2. 切換到 Claude 3.7 或 Claude 4 繼續開發功能
3. 需要新畫面時再切回 v0

**關鍵優點：**
v0 已建立的 style、spacing、color 範例，會讓後續其他 model 在生成新畫面時自動沿用同樣風格，維持整體 UI 一致性。
