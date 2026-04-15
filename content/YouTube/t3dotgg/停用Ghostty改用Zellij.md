---
title: 停用 Ghostty 改用 Zellij（Zedmux）
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-12
source: https://www.youtube.com/watch?v=EUE8N6mqtGg
---

## 為何離開 Ghostty

- 使用 Ghostty 近一年，整體仍很好：快速、穩定、開源、高度客製
- 離開原因：AI agentic 工作模式讓「同時處理多個專案」需求大增，Ghostty + tmux 的層級結構無法對應新的工作形態
- 工作分支越來越多、越來越複雜，tab/panel/window 的管理方式逐漸崩潰

## 新工具：Zellij（Zedmux）

- 基於 `libghosty`（Ghostty 底層函式庫）開發，由 Maniflow 團隊打造
- 核心設計：**側欄管理專案，每個專案內可開多個分割 pane，每個 pane 內可再開 tab**
- 與 Ghostty 熱鍵相容（如 `Cmd+D` 分割）
- 內建 Claude Code 整合：跑 claude 指令後，離開視窗會收到完成通知

## 日常使用場景

- 每個專案一個側欄條目，可重新命名、釘選
- 一個條目內：左半 claude code、右半 git terminal，bun dev server 放在同一 pane 的後台 tab
- 同時開多個專案不再混亂，hot key 快速跳專案：`Cmd+1`、`Cmd+2`...
- 可在 T3 Code（codeex）與 Claude Code（terminal）間靈活切換

## 現存問題

- zsh 狀態列有 bug：clear 後會重複出現多行狀態
- 內建瀏覽器是 Safari WebView，無擴充套件、無 cookies，預設會攔截終端連結——需手動關閉 `open terminal links in Zedmux browser`

## 未來想像：Niri 式的 paper window manager 概念

- Niri：視窗不互相搶佔空間，而是「無限橫向捲動畫布」
- 每個視窗保持自己的大小，透過移動視角來切換
- Theo 的願景：Zellij 內每個 pane 能像 Niri 一樣無限橫向滑動，巢狀管理任意深度
- 進一步：整合真正的 Chrome（帶 profile、擴充套件、cookies），讓一個 app 成為開發全流程入口

## Mitchell Hashimoto 的觀點

> Ghostty app 一直是 libghosty 的「技術 demo」，真正的目標是讓社群基於這個函式庫打造各種專注特定用途的終端工具。Zellij 的出現正是他最期待看到的事。

## macOS Spaces 為何不夠用

- 切換 app 時常跳到錯誤的 workspace
- 視窗分組不靈活，無法像 Niri 那樣精確控制
- 切換動畫最長達 0.5 秒，無法關掉，改 fade 也很難看
