---
title: Claude.md is RUINING Claude Code (w/ One Exception)
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/V3xDTx2XwGg
---

根據 ETH Zurich 研究報告，Claude.md 等 context 檔案實際上讓 AI agent 表現更差、成本更高，並探討唯一例外情境。

## 研究結論（ETH Zurich）

> 「Context files tend to reduce task success rates compared to providing no repository context, while also increasing inference cost by over 20%.」

- 8 項測試中，5 項是「無 Claude.md」表現更好
- 有 context file 時，inference cost 增加超過 20%
- 更強的模型並不能產出更好的 context 檔案

## Claude.md 讓 AI 變差的原因

1. **無法提供有效概覽**：Claude Code 找到正確檔案的步驟並未減少，反而增加
2. **冗餘文件**：Claude Code 本就會自行遍歷 codebase，額外文件只是重複
3. **過度工具呼叫**：agents 傾向盲目遵守 Claude.md，導致搜尋更多檔案、讀取更多檔案、產生更多 token
4. **Context 污染**：與當前任務無關的 90% 規則仍會被載入

## 實際建議

- 一般 coding 專案：**直接不用 Claude.md**，特別是非技術背景用戶
- 若要用，**人工撰寫並精簡**，只放 Claude Code 無法從 codebase 自行判斷的資訊
- 能做成 skill 或 hook 的規則，就不要放進 Claude.md

## 唯一例外：個人助理型專案

研究發現，當 repository **完全沒有任何文件**時，LLM 生成的 context file 可提升約 2.7% 表現。

適合使用 Claude.md 的場景：
- **Obsidian vault 類的個人助理**：大量 markdown 文件、沒有 code 架構、沒有 README、持續成長的文件庫
- 這類場景中 Claude.md 主要記錄的是溝通偏好與個人習慣，而非程式碼規範

## /init 的最新更新

- Anthropic 更新了 `/init`（需在 settings 中啟用實驗功能）
- 新版是互動式多階段流程，更精簡，推動使用 skills 和 hooks
- 但仍非根本解決方案——根本問題在於架構本身，而非 Claude.md 的品質
