---
title: Claude.md 正在拖累 Claude Code（唯一例外）
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-23
source: https://www.youtube.com/watch?v=V3xDTx2XwGg
---

## ETH Zurich 研究結論

《Evaluating agents.md》研究測試多個 coding agent 與 LLM 模型的結果：

- 8 項測試中，5 項「沒有 claude.md」的結果更好
- 有 context 檔的情況，推理成本增加超過 20%
- **結論**：不必要的 context 讓任務更難，若使用應只包含最少量的必要資訊

## 為何 Claude.md 有反效果

### 無效的導覽

本意是幫 Claude Code 快速找到正確檔案，但測試顯示找到檔案所需的步驟數不減反增，同時每步都要先讀 context 檔，成本更高。

### 冗餘文件

Claude Code 本就會主動掃描程式碼庫，額外提供的說明多半是它自己能找到的資訊，形成重複。

### 過多工具呼叫

Context 檔導致 agent 讀更多、搜尋更多、寫更多（不是因為任務需要，而是因為指令要求它這樣做）。對任務無關的 90% 指令仍然每次被讀取，形成 context 污染。

### 模型強度無關

更強的模型生成的 context 檔並不比較好，問題出在架構本身，不是內容品質。

## 對實際使用者的建議

- 來自技術背景、清楚知道 claude.md 應放什麼：可手寫精簡版，只放「Claude Code 無法從程式碼本身發現的資訊」
- 不具技術背景：建議直接刪除 claude.md，什麼都沒有好過充滿 `/init` 生出的冗贅內容

## 唯一例外：個人助理型 Agent

研究中一個特殊測試：完全移除 repo 內所有文件（README、範例程式碼等）後，加入 claude.md 反而提升效能約 2.7%。

這說明 claude.md 在「幾乎沒有其他文件的 repo」才有價值。符合這個情境的典型例子：

- **Obsidian Vault**：龐大的 Markdown 檔案集合、沒有程式架構可供 Claude Code 遍歷、沒有 README
- **個人助理專案**：慣例與溝通風格比程式架構更重要

這類情況適合手寫 claude.md，記錄的是個人習慣、溝通偏好，而非程式碼規範。且不應用 `/init` 自動生成，而是人工撰寫。

## `/init` 的更新

Anthropic 已更新 `/init`（需在設定中開啟實驗性功能）：
- 改為互動式多階段流程
- 傾向更精簡的輸出
- 引導使用者思考「這條規則是不是應該做成技能或 hook」而非放在 claude.md

但更新的 `/init` 仍不是根本解決方案，問題出在 claude.md 的架構本身。
