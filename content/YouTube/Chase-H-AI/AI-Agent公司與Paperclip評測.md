---
title: AI Agent 公司與 Paperclip 評測
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-15
source: https://www.youtube.com/watch?v=Rgb-Kx-kkaA
---

## 什麼是 Agent 編排平台

一類新工具，讓使用者建立並管理由 AI agents 組成的「公司」。代表工具：Paperclip（2 週內累積 24,000 GitHub stars）。

特徵：
- 開源為主
- 可視化 dashboard 管理多個 agent
- 仿企業組織架構（CEO → C-suite → 工程師）
- 心跳機制（每 5、30、60 分鐘 agent 自動喚醒查看新指令）
- 使用者扮演「董事會」角色，保有完整監督權

類似工具：Claw Empire、Clawith、OpenClaw Mission Control、CrewAI。

## 這只是生產力劇場嗎

作者的結論：**要看情境**。

核心問題在於人類反饋迴圈：
- 用 Claude Code 開發時，最有價值的是緊密的迭代循環——看到輸出立刻給方向，很多時候方向是主觀的、事先無法預測的
- 多層 agent 傳話（board → CEO → COO → 工程師）會累積偏差，最終產出「回歸平均」的結果，品質下降

## 適合 vs. 不適合的場景

**不適合**：從零開始建立新產品。需要頻繁的主觀判斷和即時調整，多層 agent 傳話會讓結果偏離預期。

**適合**：已建立好的系統，執行重複性的授權任務。比如：
- 固定流程的自動化
- 已定義好的工作流反覆執行
- 你不在時讓 agent 代為處理

關鍵區分：**委派（delegation）vs. 創造（creation）**。創造需要人在場，委派才適合自動化。

## Paperclip 評價

架構設計本身紮實，dashboard 直覺好用：
- 可見每個 agent 狀態（live/idle）
- 可調整心跳頻率
- Agent 想增加成員時需要詢問批准，不會自行決定

但問題在使用情境：大多數看到這個工具的人會以為可以用它「從頭建公司」，這是錯誤的期待。

## 重要提醒

「感覺很有生產力」和「實際有生產力」是兩件不同的事。這類工具現在最大的風險是被濫用於不適合的場景，產生大量看起來很忙但品質低落的輸出。
