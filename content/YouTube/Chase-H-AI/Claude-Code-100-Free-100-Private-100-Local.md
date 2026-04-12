---
title: "Claude Code: 100% Free. 100% Private. 100% Local."
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/GHGGkIMYDxo
---

示範如何將 Claude Code 的 agentic harness 套在本地開源模型上，實現完全免費、完全私密的本地執行環境。

## 本地模型的取捨

| 面向 | 正常 Claude Code | 本地 Claude Code |
|------|-----------------|-----------------|
| 模型能力 | Sonnet/Opus 4.6（~80% SWE） | GLM 4.7 Flash（~59%，相當於 Claude 3.7 Sonnet） |
| 速度 | 快 | 慢（受本機硬體限制） |
| 費用 | 按計畫收費 | 完全免費 |
| 隱私 | 資料送至 Anthropic | 完全本機，不離開電腦 |

- 頂尖本地模型（GLM 4.7、Qwen 3 Coder）達 Opus 91% 效能，但需 48GB RAM，多數人硬體不足
- 一般人可用的：GLM 4.7 Flash、Qwen 2.5 等小參數模型

## 安裝步驟

1. 安裝 **Ollama**（`ollama.com`）
2. 下載模型：`ollama pull glm4.7-flash`
3. 設定 alias（依 OS 不同，指令在 Chase AI 社群）：
   - 設定 `ANTHROPIC_AUTH_TOKEN=ollama`
   - 設定 `ANTHROPIC_BASE_URL=http://localhost:11434`
4. 使用 `claude-lo` 啟動本地版，`claude` 繼續使用正常版

## 適用場景

1. **達到使用量上限時**：作為等待 reset 的備用方案
2. **簡單任務**：寫作、基礎研究、不需大量 tool calls 的工作
3. **敏感資料處理**：客戶資料、不能外傳的內容

## 注意事項

- Ollama 雲端 API 選項提供更強模型但不再完全私密
- 速度差異顯著（示範中即使用 5090 顯卡仍慢很多）
