---
title: OpenAI Realtime API 改用 WebSocket
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-04
source: https://www.youtube.com/watch?v=sFEDAkJy9Dc
---

## 改變的核心

OpenAI 的 API 從 REST（SSE streaming）改為 WebSocket，帶來：
- 頻寬減少 **90%+**
- 多工具呼叫的 agentic 執行速度提升 **20-40%**

## 為什麼以前要傳送整段歷史

AI 模型是**無狀態**的：每次工具呼叫結束後，模型「死掉」，再次生成時需要重新載入全部 context。

**一次 agent 執行的完整流程：**
1. 使用者發送 prompt → 模型回應並呼叫工具
2. 工具執行完畢 → 把 system prompt + 所有歷史 + 新工具結果一起傳回 API
3. API 尋找可用 GPU → 載入整段 context → 繼續生成
4. 每次工具呼叫都重複步驟 2-3

**問題**：100 個工具呼叫 = 100 次傳送整段 context（可能是 2MB 文字）換 8 個回應 token。

## 快取不解決這個問題

- 快取（Prompt Cache）是**計算成本**的優化，不是**傳輸量**的優化
- 快取的 key 是 context 的 hash，因此仍需把整段 context 傳過去讓 API 去比對
- Compaction 是把 context 壓縮，會破壞快取，是不同的權衡

## WebSocket 的本質是什麼

WebSocket 不只是協議升級，而是一個**保證**：整個 session 期間的請求都打到同一個 API 節點。

- 同一節點可以保持 in-memory 狀態（auth、cache 位置、context）
- 工具呼叫完成後只需傳送**新的**工具結果，不用重傳整段歷史
- 無需重新驗證、無需重新查找快取、無需重新路由

## 不適用的場景

- **Chat app 對話型使用**：每次使用者輸入之間有長時間間隔，維持 WebSocket 連線不划算
- 每個使用者訊息傳一次完整 context 是合理的；每個工具呼叫傳一次才是問題

## 影響

- OpenAI 已將設計開源為 **Open Responses** 標準，其他 provider（Anthropic、Gemini）也可實作
- 標準目前尚未包含 WebSocket 部分，但預計很快會加入
