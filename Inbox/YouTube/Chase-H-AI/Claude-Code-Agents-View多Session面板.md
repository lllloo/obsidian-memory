---
title: Claude Code Agents View 多 Session 面板
created: 2026-05-15
updated: 2026-05-15
source: https://www.youtube.com/watch?v=7zxIeRWasbc
published: 2026-05-11
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - dashboard
---

## Agents View 是什麼

Claude Code 新推出的 **Agents View**：把多個 terminal 視窗中的 Claude Code session 整合到單一面板，可同時看所有 session 狀態並從一個地方回應。對於常同時開三到六個視窗跑不同專案的人來說極有用。

## 啟動方式

terminal 輸入：

```
claude agents
```

帶出 Agents View 視窗，把所有 session 列在一起。

## 三段狀態分區

面板把 session 分成三類：

- **Needs Input**：等待使用者回應
- **Working**：正在執行
- **Completed**：已完成

## 操作流程

- **進入 session**：點該 session → 完整 terminal 視圖呈現，跟原本獨立開的 terminal 一樣
- **返回 Agents View**：左方向鍵
- **快速回應（不離開面板）**：游標移到 session 上 → 空白鍵，會顯示經過時間、目前進度，並可直接回覆，等於探頭進房間問「進度如何？做 X、Y、Z」
- **刪除 session**：游標移到 session 上 → Ctrl+X → 確認刪除

## 把現有 Terminal Session 加入 Agents View

在某個獨立 terminal 跑的 Claude Code session 想丟進 Agents View：在該 session 內輸入 `/bg`（background），該 session 停在當前 terminal、自動出現在 Agents View 的 Working 區。

## 在 Agents View 直接開新 Session

不用回 terminal，直接在 Agents View 內描述任務就會建立新 session 並進入 Working 狀態。可以做到完全不離開這個面板。

## 退出行為（不會中斷 session）

關掉 Agents View 視窗 **不會** 中斷裡面的 session。下次再 `claude agents` 啟動，所有 session 完整還在。避免不小心關掉就誤殺一堆背景任務。

## 為什麼有用：解決「視覺記憶」問題

平行跑多個 session 的常見痛點：

- 派一個任務後跳去做別的，過一小時才想起「對齁，那個還在跑」
- 不管多少 hook 通知，只要視覺上看不到，就會忘記

Agents View 把所有 session 變成 always-visible 狀態，可在單一頁面看完所有正在跑的東西、處理需要回應的 session。
