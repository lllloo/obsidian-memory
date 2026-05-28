---
title: Claude Code 內容自動化 Pipeline
created: 2026-05-27
updated: 2026-05-28
source: https://www.youtube.com/watch?v=7q_rbT1a9dE
published: 2026-03-30
tags:
  - claude-code
  - content-automation
  - workflow
---

把 Claude Code 變成一人內容機器的共通骨架，不在於用了哪些工具，而在於**哪些階段該 skill 化、哪些該保人工、生成能力該如何抽象**。

## Pipeline 骨架

```
創意源（step 0）→ 研究 → 構思 → 腳本 → 分發
```

- **創意源（step 0）**：持續抓 trending 訊號當靈感入口——定時掃 Twitter / GitHub trending，依 velocity / authority / timing 等評分，去重後存進 vault。讓 pipeline 有源源不絕的素材，而非每次從零想題目。
- **四階段各自 skill 化**：研究（抓參考、外包分析給不吃自己 token 的服務如 NotebookLM）、構思（競爭格局 + 多個方向排名）、腳本（hook / outline / title）、分發。**高階 skill 呼叫子 skill**，輸出都落 vault 便於關聯。

## 兩條核心判斷原則

1. **Claude Code 是協作者，不是自動執行者**：每個階段都要人工介入確認，否則輸出會很通用且糟糕。值得 skill 化的是**重複的 evergreen 流程**；構思 / 篩選這類決定品質的步驟要保人工。
2. **生成工具抽象成單一通道，而非綁單一工具**：影像 / 影片生成模型「最佳工具每週都在換」，個別串接麻煩到沒人做。用一個 MCP 通道（如 Higgsfield，一次接十多個 image / video 模型）解綁，整套流程才能腳本化、串進 cron。注意 MCP 多為 **fire-and-forget**，要請 agent 定時輪詢取回成品。

## 混合策略：不必全 AI 生成

- **視覺風格最重要的部分（如 cover）**用 AI 出圖；
- **資訊型的部分（如 body slide）**改用 HTML / code 渲染，省 token、降成本。
- 重點是「現在我們有選擇」，依每個元素的價值決定生成方式。

## 收斂與放大

- **收進單一 high-level skill**：把整支流程包成一個 skill（如「每日 GitHub trending carousel」），產出評得起時間的 evergreen 內容類型，每天自動更新、輸出數個變體供人篩選。
- **一源多分發**：一部長片可 cascade 成 blog（SEO + 本人寫作風格）、Twitter thread、LinkedIn、短影片多平台，單一內容覆蓋多通路。

## 相關

- [[Claude-Code-Skills]] — pipeline 各階段的 skill 化載體
- [[Claude-Code-記憶系統選型]] — 創意源與產出落地的 vault（L5 知識庫）
