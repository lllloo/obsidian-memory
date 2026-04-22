---
title: Claude Code 本地免費私密運行
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-18
source: https://www.youtube.com/watch?v=GHGGkIMYDxo
parent: "[[01.index]]"
---

## 概念

Claude Code 的 agentic harness 可以脫離 Anthropic 模型，改接本地開源模型。做到 100% 免費、100% 私密、100% 本地。

## 本地模型的取捨

**效能比較（SWE verified benchmark）**

| 模型 | 分數 | 備註 |
|------|------|------|
| Opus 4.6 / Sonnet 4.6 | ~80% | 雲端付費 |
| GLM 4.7（48GB RAM） | 73.8% | 多數人無法運行 |
| GLM 4.7 Flash / Qwen 2.5 | ~59.2% | 相當於 Claude 3.7 Sonnet |

大多數人的硬體可用模型約等於一年前的前沿模型（Claude 3.7 Sonnet，2025 年 2 月發布）。

主要犧牲：
- 效能降低約 20%
- 速度明顯較慢（在個人電腦硬體上運行）
- 5090 顯卡測試仍有顯著速度差距

## 安裝步驟

**1. 安裝 Ollama**

前往 `ollama.com` 複製安裝指令貼入終端機。

**2. 選擇模型**

三種方式選擇適合自己硬體的模型：
- 問 Claude Code：「我想下載開源模型，哪個適合我的硬體？」
- 使用 LLM fit 工具（GitHub 開源）
- 詢問任何 AI chatbot

**3. 下載模型**

```bash
ollama pull glm4.7-flash
```

（不要用 `ollama run`，那是直接執行，這裡需要先 pull）

**4. 設定 alias**

依作業系統（Mac/Linux/Windows Git/PowerShell）複製對應指令，設定 `claude-lo` alias，原理：
- `ANTHROPIC_AUTH_TOKEN` 設為 `ollama`
- `ANTHROPIC_BASE_URL` 指向 `localhost:11434`

```bash
# 之後用 claude-lo 啟動本地版本，claude 啟動正常版本
claude-lo
```

## 適用場景

1. **用量限制時的備用**：等待 Max plan 用量重置期間使用
2. **簡單任務**：寫作、基礎內容、研究性任務（不需大量 tool calls 的）
3. **資料隱私需求**：處理客戶敏感資料，不想傳送到外部伺服器

不適合：複雜 coding 任務、需要 30-50 次 tool calls 的工作。

## Ollama Cloud（進階）

Ollama 提供雲端版本，可運行原本需要 48GB RAM 的大模型，但需付費，且資料不再完全本地。是完全本地與完全雲端之間的中間選項。
