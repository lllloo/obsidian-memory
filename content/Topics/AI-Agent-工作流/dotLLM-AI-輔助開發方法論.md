---
title: dotLLM — AI 輔助開發方法論的大型驗證
created: 2026-04-24
updated: 2026-04-25
source: https://kokosa.dev/blog/2026/dotllm/
published: 2026-04-14
tags:
  - claude-code
  - ai-agent
  - ai-coding
  - workflow
---

dotLLM 是一個很好的大型案例：它不是玩具 demo，而是用 Claude Code + 多模型 review，在兩個月內從零做出 .NET / CUDA / OpenAI-compatible 的 LLM inference engine。它證明的不是「AI 會自己寫完所有東西」，而是：**當文件、review、skills 與人類決策一起工作時，AI 可以把高紀律工程放大。**

## 這個案例最值得抄的四件事

### 1. 文件不是 overhead，是執行介面

作者最重視的兩份文件：

- `ROADMAP.md`：把整個專案拆成可執行步驟與依賴
- `CLAUDE.md`：專案「憲法」，寫架構原則與硬規則

外加每個子系統的設計文件（例如 quantization、attention、CUDA 等），讓 AI 在動手前**先讀 spec，再改 code**。

### 2. 寫 code 的模型，不要同時 review 自己

作者讓 Claude Code 主要負責實作，再用 Codex / Gemini 做 PR review。這種**跨模型 review** 能補盲點，抓到 race condition、索引錯誤、cache key collision 這類真正會出事的 bug。

### 3. Skills 要包住 PR 生命週期

像 `/plan-step`、`/create-pr`、`/apply-pr-comments`、`/finish-pr-comments`、`/merge-pr` 這類技能，把 planning、修 review comments、push、merge 變成可追蹤的工作流，而不是每次重新口述。

### 4. 不要 YOLO loop

作者明確拒絕 fire-and-forget：每個 plan 先讓人核准，再進實作。這很值得記，因為它的核心觀念是：**我要 drive 這個系統，不是把方向盤整支交出去。**

## 反面教訓也同樣有用

- **架構級決策仍然要人做**：例如 attention 方案、GPU interop、runtime 限制
- **AI 會違反你自己寫下的規則**：最後還是要靠 pre-tool hook / 檢查腳本兜底
- **卡 loop 時，人要介入 brainstorm，不是無限加 prompt**

## 對工作流的啟示

- `CLAUDE.md` + 設計文件 + task roadmap，這三件事是最穩的外部記憶
- 跨模型 review 值得變成常規，而不是豪華加購
- prompt 很重要，但 **hook / checker / review gate** 更可靠

## 金句

> AI amplifies discipline; it doesn't replace it.

## 來源

- [dotLLM article by Konrad Kokosa](https://kokosa.dev/blog/2026/dotllm/)