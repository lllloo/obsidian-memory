---
title: "obsidian:defuddle 被意外觸發"
tags:
  - obsidian
  - skill
  - bug
created: 2026-03-17
updated: 2026-03-17
---

遇到 URL 會自動觸發 `obsidian:defuddle`，但本機未安裝 Defuddle CLI，導致失敗。

## 解法

在 CLAUDE.md 明確指定：讀取 URL 時直接用 WebFetch，不觸發 defuddle。

## 相關
- [[Obsidian Skills 總覽]]
