---
title: Obsidian
description: 用 Obsidian 搭 Claude Code 維護半自動卡片盒：CLI 整合、skills、defuddle 網頁清洗與踩坑筆記
created: 2026-03-22
updated: 2026-06-05
tags:
  - obsidian
---

用 Obsidian 搭配 Claude Code 打造個人知識庫的筆記集合。

## 工作流

- [[跨專案內容整理到-Inbox]] — 其他專案裡想保留的內容先收進 Inbox，回 vault session 再決定是否內化

## 工具書籤

- [[Obsidian-Skills]] — 實際安裝使用的 Claude Code skills（obsidian-cli / obsidian-markdown / obsidian-bases / defuddle）
- [[Obsidian-CLI-整合指南]] — 讓 Claude Code 讀寫 vault 的 CLI（kepano 維護）
- [[bookmark-defuddle-網頁清洗CLI|defuddle]] — 網頁內容清洗 CLI，把網頁納入半自動卡片盒的第一步

## 發佈

- [[Quartz-部署筆記]] — Obsidian vault 透過 Quartz 4 發佈成靜態站的個人設定（發佈層與筆記本體分屬兩個 repo，GitHub Actions → bugloop.com）

## 踩坑紀錄

- [[daily-append-bug]] — `daily:append` 在特定環境失效的解法
