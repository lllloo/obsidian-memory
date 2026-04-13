---
title: Claude Code 加 Codex 等於 AI 之神
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-30
source: https://www.youtube.com/watch?v=L7NPhaUBpZE
---

## 描述

示範如何在 Claude Code 中整合 OpenAI Codex，讓 Opus 4.6 與 Codex 協同工作，並介紹 Codex 帶來的 code review 和 adversarial review 功能。

## 重點摘要

- **整合背景**：OpenAI 開放 Codex 可在 Claude Code 中使用，讓用戶在 Anthropic 生態系內同時使用兩個競爭對手的模型
- **費用優勢**：Codex 的 token 費用比 Opus 4.6 更划算，對使用量大的用戶是好消息
- **主要功能**：
  - **Standard Code Review**：唯讀檢視 Opus 產出的程式碼，給出中性評估
  - **Adversarial Review**：命令 Codex 以嚴苛眼光審查代碼，假設有問題並找出改善點——特別適合解決 AI 模型不善於評估自身輸出的問題（Anthropic 工程 blog 亦提及此問題）
  - **Codex Rescue**：讓 Codex 獨立完成任務，如同在 Claude Code 中使用 Opus 一樣
- **安裝步驟**：執行指定指令加入 marketplace → 安裝 plugin（`codex @openai`）→ 選擇 user scope → reload plugins → 執行 `codex:setup`；使用量與 ChatGPT 帳號綁定
- **協同使用策略**：Opus 負責主要開發，Codex 負責 review 與對抗性審查，兩者互補發揮大於各自之和
