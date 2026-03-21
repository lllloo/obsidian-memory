---
title: Obsidian CLI 整合指南
tags:
  - obsidian
  - claude-code
  - cli
created: 2026-03-17
updated: 2026-03-17
---

透過 **Obsidian CLI** 讓 Claude Code 操作 Obsidian vault。

Claude Code 使用 `obsidian:obsidian-cli` skill 呼叫 CLI 指令，直接讀寫 vault 內的筆記。

## 常用指令

| 指令                                         | 說明        |
| ------------------------------------------ | --------- |
| `obsidian daily:path`                      | 取得今日日記路徑  |
| `obsidian append path="..." content="..."` | 寫入內容到指定筆記 |
| `obsidian search query="..."`              | 搜尋 vault  |

## 相關
- [[Obsidian Skills 總覽]]
- [[daily-append-bug]]
