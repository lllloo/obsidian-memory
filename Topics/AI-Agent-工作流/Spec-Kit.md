---
title: Spec Kit
created: 2026-05-08
updated: 2026-05-29
source: https://github.com/github/spec-kit
tags:
  - claude-code
  - agent-framework
---

Spec Kit 是 GitHub 出的 Spec-Driven Development toolkit，把 specification 從「事前文件」提升為可執行、可生成的 first-class artifact——以 spec 為中心驅動 agent 生成 code，改 spec 等於改 code。可跨 30+ agent host，包含 Claude Code、Codex CLI、GitHub Copilot、Cursor、Gemini CLI 等。

## 社群評價與何時不該用

社群普遍認同「先講清楚再寫」的方向正確，但多數團隊仍在小規模試用觀望，等工具與底層模型更成熟。實務上的保留意見：

- **規格完美 ≠ 產出穩定**：即使花大量心力寫完美規格，AI 最終產出的 code 品質仍不一定穩。
- **小專案太重**：對需要快速迭代的小型專案，整套立法式流程（constitution → specify → plan → tasks → implement）顯得過重。

長期風險：

- **依賴外部模型穩定性**：底層模型行為一變，整個 workflow 可能失效。
- **prompt template 脆弱**：核心邏輯深植在提示範本裡，維護它與 30+ agent 的相容性是巨大長期負擔。
- **失去掌控感**：`/speckit.implement` 這類高度抽象指令可能讓開發者對最終 code 失去掌控、不利技能成長。

本質上 spec-kit 是在賭：結構化開發流程的價值，會不會比單純追求更強的模型更高。

## 連結

- Repo：<https://github.com/github/spec-kit>
- Docs：<https://github.github.io/spec-kit/>

## 相關

- [[Harness-Engineering]] — spec-driven 取徑
