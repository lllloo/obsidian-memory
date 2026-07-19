---
title: "2026-07-19 Daily Updates"
created: 2026-07-19
updated: 2026-07-19
tags:
  - updates
  - codex
---

## OpenAI Codex

### v0.144.6 · 2026-07-18（[Bug Fixes](https://github.com/openai/codex/releases/tag/rust-v0.144.6)）

**繁中摘要**：修正 GPT-5.6 Sol／Terra／Luna 模型 bundled instructions 裡的 context window 數字，正確標示為 272,000 tokens，避免用量規劃時看到錯誤上限。

- **Context window 更正**：三個 GPT-5.6 系列模型的 context window 標示修正為 272K tokens（PR #33972、#34009）。

---

### ChatGPT for iOS 1.2026.188 · 2026-07-13

**繁中摘要**：iOS App 為 Codex tasks 加入行內視覺化，並改善工作建立與管理體驗，同時修掉幾個 UI 狀態還原的問題。

- **Codex tasks 行內視覺化**：新增可靠連結、工具活動樣式、檔案開啟回饋與 composer 控制項。
- **Bug fix**：修正 Fast mode 選擇還原、approval preset 與部分 UI 回應性問題。

---
