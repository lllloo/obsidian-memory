---
title: 本地免費執行 Gemma 4 搭配 Claude Code
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-16
published: 2026-04-08
source: https://www.youtube.com/watch?v=CLXjqdu4Ivc
parent: "[[01.index]]"
---

## 簡介

Google 發布了 Gemma 4（e2b 版本），這是目前準確率最高的開源模型之一，僅需 7.2GB RAM 即可在本地運行。本影片示範如何透過 Ollama 將 Gemma 4 接入 Claude Code，打造完全免費的本地 AI 編碼環境。

## 安裝流程

### 1. 安裝 Ollama 並拉取 Gemma 4

```bash
# 安裝 Ollama（ollama.com 下載）
# 拉取 Gemma 4 e2b 模型
ollama pull gemma4:e2b
```

- 整個安裝流程約 2 分鐘內完成
- Gemma 4 e2b 為輕量版本，7.2GB RAM 即可運行（適合 MacBook 等消費級設備）

### 2. 在 Ollama 中測試 Gemma 4

```bash
ollama run gemma4:e2b
```

確認模型能正常回應後，再接入 Claude Code。

### 3. 將 Gemma 4 接入 Claude Code

Claude Code 支援自訂 API base URL，讓 Ollama 本地服務作為後端：

```bash
# 啟動 Claude Code 時指定 Ollama endpoint
ANTHROPIC_BASE_URL=http://localhost:11434/v1 \
ANTHROPIC_API_KEY=ollama \
claude
```

或在 Claude Code 設定中配置自訂模型，指向 Ollama 的 OpenAI 相容端點。

## Gemma 4 的適用場景與限制

### 適合的場景

- **單一檔案編輯**：修改單個函數、小型重構、調整樣式
- **Micro-refactor**：程式碼優化、命名改善、簡單 bug 修正
- **快速原型**：不需要跨多個檔案協作的小型任務

### 明顯的限制

- **多檔案 context 能力差**：當任務需要理解多個檔案的關聯時，小型本地模型容易失準
- **複雜架構理解不足**：無法像 Claude Sonnet/Opus 那樣理解整體專案結構
- **指令遵循能力有限**：對複雜、多步驟指令的執行穩定性較低

## 更好的免費替代方案

影片推薦另一個更實用的方案：**Claude Code + OpenRouter 免費雲端模型**

- 透過 OpenRouter 接入各家免費額度的雲端模型（如 Gemini Flash 等）
- 比本地小模型的 context 能力強得多
- 不需要管理本地硬體資源
- 詳見作者另一支影片：[Claude Code + OpenRouter](https://youtu.be/o85Y5omRQq0)

## 章節時間戳

| 時間 | 內容 |
|------|------|
| 0:00 | 介紹 |
| 1:39 | 安裝 Ollama 與 Gemma 4 e2b |
| 2:41 | 在 Ollama 中測試 Gemma 4 |
| 4:15 | Gemma 4 接入 Claude Code |
| 4:30 | Gemma 4 的限制 |
| 6:45 | 更好的方案（免費雲端 AI） |

## 重點摘要

- Gemma 4 e2b 是目前最輕量高效的開源模型之一，7.2GB RAM 可本地運行
- 透過 Ollama + Claude Code 組合可實現零成本 AI 編碼環境
- 本地小模型適合簡單單檔任務，多檔案複雜任務仍建議使用雲端模型
- 實務上 OpenRouter 免費雲端模型的 CP 值優於本地小模型方案
