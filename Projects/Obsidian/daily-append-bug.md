---
title: Obsidian CLI — daily:append 失效
tags:
  - obsidian
  - cli
  - bug
created: 2026-03-17
---

# Obsidian CLI — `daily:append` 失效

## 問題

透過 Obsidian CLI 操作 vault 時，`daily:append` 會回傳 exit code 127 導致失敗。

## 解法

拆成兩步驟：

1. `obsidian daily:path` 取得今日路徑
2. `obsidian append path="<date>.md" content="內容"`

## 啟示

將 workaround 寫入 CLAUDE.md，讓 AI 下次自動避開。
