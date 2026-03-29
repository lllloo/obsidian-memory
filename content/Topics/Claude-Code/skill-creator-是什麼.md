---
title: skill-creator 是什麼
tags:
  - claude-code
  - skill
created: 2026-03-19
updated: 2026-03-19
---

用來**建立、修改、優化 Claude Code 技能（skills）**的工具。

主要功能：
- **建立新 skill** — 從零開始定義一個新的自動化流程
- **修改現有 skill** — 調整已有 skill 的邏輯或描述
- **執行評估（evals）** — 測試 skill 是否如預期觸發
- **效能基準測試** — 分析 skill 的變異性與穩定度
- **優化觸發描述** — 讓 skill 在正確時機被自動選用

## 使用範例

**建立全新 Skill**
- 「幫我建立一個 skill，讓 Claude 在我說「畫流程圖」時，自動用 Mermaid 語法產生流程圖」

**改善現有 Skill**
- 「我的 ob-note skill 每次都忘記加 frontmatter，幫我修一下讓它更可靠」

**從對話萃取 Skill**
- 「我們剛才做的那個「讀 CSV → 分析 → 產出報告」流程，幫我把它變成一個 skill」

**優化觸發描述**
- 「我的 skill 很少被自動觸發，幫我優化它的 description 讓 Claude 更容易認出來」

**評估 Skill 效果**
- 「幫我測試 commit skill 的品質，跑幾個測試案例看看輸出對不對」

## 相關
- [[Obsidian-Skills-總覽]]