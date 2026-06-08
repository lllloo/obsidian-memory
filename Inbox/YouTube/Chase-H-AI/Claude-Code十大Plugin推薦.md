---
title: Claude Code 十大 Plugin 推薦（2026 年 6 月）
description: 盤點 10 個較新且實用的 Claude Code plugin、skill 與 CLI——涵蓋知識圖譜、計畫對齊、對抗式審查、Obsidian 自動整理、前端設計與內容生成。
created: 2026-06-08
updated: 2026-06-08
source: https://www.youtube.com/watch?v=IShdbDP4Jgg
published: 2026-06-06
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - plugin
---

挑選原則：刻意避開大家已熟知的大名（如 Superpowers、Frontend Design），都是相對新、較少人提的工具。

## Graphify（知識圖譜）

把 Claude Code 指向某個 repo，將整個 code base 轉成知識圖譜，當作給 Claude Code 的「地圖」。好處是回答 code base 問題比預設的 grep 更省 token、更準確。

- 安裝後附帶 Graphify skill，教 Claude Code 哪個工作該用哪個指令。
- `/graphify` 跑過 code base 建圖；加 Obsidian flag 可為該 repo 生成一個全新 Obsidian vault。
- `hook` 指令可在每次 commit 後自動重建，保持更新；重建僅做 AST，不涉及 LLM，是 deterministic、零 API 成本。

## Grill Me + Grill with Docs（計畫對齊）

來自 Matt Pocock 的兩個 skill，是「plan mode 強化版」。比標準 plan mode 問更多、更深的問題，讓使用者與 Claude Code 對齊，且 skill 輕量、token 成本低。

存在理由：軟體開發最常見的失敗是 misalignment——你以為 Claude Code 懂你要什麼，看到成果才發現它根本沒懂。只靠 plan mode 問三個問題就期待完全對齊，多半會失望。

## Grill Me Codex（對抗式審查層）

作者本人製作，在 Matt Pocock 的 Grill Me / Grill with Docs 上加第二層。理由：光跟 Claude Code 對齊計畫不夠，還想要第二雙眼睛審視。非資深工程師無法判斷計畫是不是最佳路徑，而 Claude Code 也不能完全信任它自評自己的程式碼（Anthropic 本身也提過這點）。

做法：把 Codex 帶進唯讀沙箱審查計畫，與 Claude Code 來回最多五輪，雙方對齊後才給通過。兼得 Matt Pocock 的 Grill Me 與 Codex 對抗式審查的好處。

## Codex 官方 plugin

OpenAI 官方推出的 Claude Code Codex plugin。若覺得 Grill Me Codex 那種多輪來回太重，只想讓 Codex 做單次審查或攻一個 feature，這個剛好。在 Claude Code terminal 內可用：

- `review`：基本審查。
- 明確的 adversarial review：深入一些你可能沒想到的特定領域。
- Codex rescue：讓 Codex 在旁獨立處理某個特定 feature。

即使沒付 OpenAI 也能用——Codex 現在有免費 tier（usage 會受限）。是不想全押 Codex、又想要第二雙眼睛時的好起點。

## Claude Obsidian（自動整理 vault）

把 Karpathy 談的 wiki 式 Obsidian vault 組織方式自動化。丟進來源後，Claude 讀取、抽取 entity 與概念、更新交叉引用、歸檔成結構化 vault；每次注入內容 vault 都更豐富，讓 Claude Code 能更有效處理大量結構化或非結構化文件。每個 session 結束時 Claude 更新一份 hot cache，下個 session 直接帶完整近期 context，不需重述。

## Karpathy 的 claude.md

170k 星、較舊但仍值得提。只是一份 claude.md，列出 Claude 應永遠遵守的慣例，表面看顯而易見卻很受用：

1. Think before coding
2. Simplicity first
3. Surgical changes
4. Goal-driven execution

價值在把這些 codify 進 claude.md，讓每件事都遵循；這些 guideline 傾向謹慎而非一味求快。

## Impeccable（前端設計）

作者最愛的前端設計工具，單一 skill 但涵蓋 23 個指令（colorize、animate、onboard、distill、quieter 等），主打對抗 AI slop。官網用視覺化逐一展示每個指令（如 bolder、animate）在 Claude Code 預設 vs Impeccable 下的差異。另有 live mode：啟動 dev server、開出網站，可直接點選頁面元素即時編輯。

## Higgsfield CLI + MCP（AI 圖像／影片）

一站式整合各家 AI 圖像／影片生成器。作者每週用多次，常拿來做 carousel——用 Higgsfield CLI 串接特定 AI 圖像生成器做成完整自動化流程。Higgsfield MCP 則適合前端設計時把圖像或影片帶進 UI。

## NotebookLM-py（CLI）

作者每天用、最愛的工具。讓 Claude Code 接上 NotebookLM，並提供介面內做不到的功能：batch download、slide 修訂、把 slide deck 匯出成 PowerPoint 等。可把原本耗 token 的 AI 任務 offload 到免費的 NotebookLM 與 Google 伺服器。因為是 CLI，可整合進各種 skill；NotebookLM 處理 YouTube 影片特別強（同屬 Google）。

## n8n 官方 MCP server

n8n 在 AI 工具箱仍有一席之地，尤其面對需要親自上手簡單自動化的客戶。官方 MCP 是市面上最好的選項，比過去那些 hacky 方案好得多，self-hosted 版也能用（等同免費）。除了最後檢查，幾乎不必進 n8n canvas。
