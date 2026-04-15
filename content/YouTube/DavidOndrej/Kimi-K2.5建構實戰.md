---
title: Kimi K2.5 建構實戰指南
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-28
source: https://www.youtube.com/watch?v=aiLZMvMLYMg
---

## Kimi K2.5 是什麼

- 由中國 Moonshot AI 開發，創辦人 Yangzilin 曾任職 Google Brain，博士來自 Carnegie Mellon，共同撰寫多篇 Transformer 核心論文。
- 背後投資方：阿里巴巴、騰訊，累積融資逾 20 億美元，估值超過 40 億美元。
- 被視為繼 DeepSeek 之後又一重大開源突破——在多項 benchmark 上擊敗 Opus 4.5，且便宜 8–10 倍。

## 核心差異點

- K2.0 僅支援文字，**K2.5 原生多模態**（圖像、影片、音頻、文件）。
- 可自動協調最多 **100 個平行子 Agent**——稱為 Agent Swarm（Agent 蜂群）。
- 在前端設計上目前可能是最強的模型，超越 Gemini 3（過去的前端設計冠軍）。
- 定價：$0.6/百萬輸入 token，$3/百萬輸出 token（Opus 4.5：$5 + $25）。

## Claude 爭議

- 有時提問「你是誰」，Kimi K2.5 會回答「我是 Anthropic 的 Claude AI 助手」。
- 可能原因一（較輕微）：Moonshot 使用 Claude 的輸出作為合成訓練資料。
- 可能原因二（嚴重）：有人從 Anthropic 洩漏了模型權重。作者強調這只是推測，並非事實。

## Agent Swarm（蜂群）架構

- 用戶給任務 → 主協調 Agent（Orchestrator）決定是否啟動子 Agent。
- 簡單問題直接回答；複雜任務則生成數個到上百個專業子 Agent。
- **子 Agent 的角色與任務在執行時即時決定**，沒有預設配置——完全根據任務自適應。
- 各子 Agent 同步並行工作，最後由事實查核員驗證，結果匯總至 Orchestrator。
- 複雜任務相比傳統逐步執行，速度提升可達 **4 倍**。

## 架構說明

- **1 兆參數**，混合專家（MoE）架構，每次推論只啟動 **320 億**活躍參數。
- **平行 Agent 強化學習**：模型被訓練為優先並行化，再優化品質——從根本上避免逐步執行的低效。
- 視覺能力從訓練一開始就整合：在 **15 兆 text+image 混合 token** 上訓練，視覺不是附加工具，而是核心能力。

## 如何免費使用（Kilo Code）

1. 在 VS Code 安裝 Kilo Code 擴充套件（搜尋「Kilo Code AI Coding Agent」）。
2. 前往 kilocode.ai 註冊免費帳號。
3. 在模型選擇器中選「**Moonshot Kimi K2.5 Free**」（注意選 2.5，不要選 2.0）。
4. 限時一週免費使用（提醒：訂閱後為 $39/月）。

## Kimi.com 網頁版使用

### Agent Swarm 實測（需升級至付費方案）

- 提示：比較 Moonshot AI、DeepSeek、XAI、Anthropic、OpenAI、Meta AI 過去 18 個月的融資、關鍵招聘、開源發布與 benchmark 進展，生成 2025–2026 地景報告。
- 啟動 6 個平行子 Agent，各自負責一家公司：Rosalind（AI 公司研究）、Leehua、Joker 等。
- 部分以英文搜尋，部分以中文搜尋各自來源。
- 約 8 分鐘生成 400 行詳細報告——人工執行需要數天。

## Kimi Code CLI 使用

1. 在終端機執行安裝指令（curl 一鍵安裝）。
2. 在 IDE 終端機執行 `kimi` 啟動，輸入 `/login` 以訂閱帳號驗證。
3. 確認使用 K2.5 模型並開啟思考模式。

## 前端設計實測

- 參考 Twitter 上一位用戶的 Kimi K2.5 生成的宇宙科技網站（視覺效果極為獨特）。
- 輸入兩張參考圖片（Asur's Relativity、Bond of Union 1956）+ 詳細設計要求。
- 約 8 分鐘生成 1500 行 HTML，單一文件完成。
- 結果：有互動動畫、宇宙感設計、滑順過場效果——不像典型的 AI 生成網站。

## 使用建議

- 不喜歡 Kimi Code 界面？可在 OpenCode/OpenClaw 中透過 OpenRouter 使用 K2.5——並選擇非 Moonshot 的提供商（如 Fireworks、GMI Cloud）以獲得更高速度，且資料不會送往中國伺服器。
- **Fireworks 速度**：140 tokens/sec（比官方 Moonshot API 快很多）。
- 若有隱私顧慮，可透過這些第三方提供商訪問模型。

## 總結

- Kimi K2.5 是開源模型的重大突破：多模態、Agent 蜂群、前端設計一流，且成本只有 Opus 的 8–10 分之一。
- 對於不介意使用中國開源模型的開發者，這是目前最划算的選擇之一。
