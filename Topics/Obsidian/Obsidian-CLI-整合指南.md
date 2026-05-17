---
title: Obsidian CLI 整合指南
created: 2026-03-17
updated: 2026-05-08
source: https://github.com/kepano/obsidian-skills
tags:
  - obsidian
  - claude-code
  - skill
  - cli
---

讓 AI agent 讀寫 Obsidian vault 的 CLI 整合，由 Obsidian 共同創辦人 kepano 維護於 `obsidian-skills` 集（遵循 AgentSkills.io 標準，多 AI harness 通用）。Claude Code 透過 `obsidian-cli` skill 呼叫，直接讀寫筆記、搜尋、操作 properties 與 daily notes。觸發情境：建立／搬移筆記、跨筆記搜尋、daily notes 操作（`/ob` 流程預設使用）；指令清單與語法以 `obsidian --help` 或官方 repo 為準。

## 連結

- Skills repo：<https://github.com/kepano/obsidian-skills>
- 官方 CLI 說明：<https://obsidian.md/help/cli>

## 相關

- [[defuddle]] — 同 kepano 維護
- [[daily-append-bug]] — `daily:append` 在特定環境失效
