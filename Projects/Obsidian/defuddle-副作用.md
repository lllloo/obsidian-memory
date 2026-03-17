---
title: obsidian:defuddle 被意外觸發
tags:
  - obsidian
  - skill
  - bug
created: 2026-03-17
---

# `obsidian:defuddle` 被意外觸發

## 問題

使用 Obsidian skill 時，遇到 URL 會自動觸發 `obsidian:defuddle`，但本機未安裝 Defuddle CLI，導致失敗。

## 解法

在 CLAUDE.md 明確指定：讀取 URL 時直接用 WebFetch，不觸發 defuddle。

## 啟示

Skill 的副作用不透明，需要靠 CLAUDE.md 主動覆蓋預設行為。
