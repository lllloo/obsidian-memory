---
title: Claude Code 整合
tags:
  - obsidian
  - claude-code
  - cli
created: 2026-03-17
---

# Claude Code 整合

## 連結方式

透過 **Obsidian CLI** 讓 Claude Code 操作 Obsidian vault。

Claude Code 使用 `obsidian:obsidian-cli` skill 呼叫 CLI 指令，直接讀寫 vault 內的筆記。

## 常用指令

| 指令                                         | 說明        |
| ------------------------------------------ | --------- |
| `obsidian daily:path`                      | 取得今日日記路徑  |
| `obsidian append path="..." content="..."` | 寫入內容到指定筆記 |
| `obsidian search query="..."`              | 搜尋 vault  |

## 相關

- [[Skills]] — 完整 skill 說明
- [[daily-append-bug]] — CLI 已知問題
