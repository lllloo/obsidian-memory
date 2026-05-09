---
title: 三分鐘完成 Claude Code 安裝：2026 最新安裝指南（Windows CLI）
created: 2026-05-09
updated: 2026-05-09
source: https://www.youtube.com/watch?v=vGwAJURmZd0
published: 2026-05-08
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
---

## 前置需求

在 Windows 上安裝 Claude Code CLI，需要先以**系統管理員權限**開啟 PowerShell：

- 按 Windows 鍵，搜尋 PowerShell
- 在 PowerShell 上按右鍵，選擇「以系統管理員身分執行」
- 這步驟非常關鍵，不可直接點開

## 安裝流程

一鍵安裝指令會依序完成以下步驟：

1. **安裝 Git** — Chocolatey 依賴 Git 才能執行，因此先裝 Git
2. **安裝 Chocolatey** — Git 安裝完成後自動接著跑 Chocolatey 官方安裝腳本
3. 整個過程約 5～10 分鐘內可完成

## 重新開啟 PowerShell（關鍵步驟）

安裝完成後，**必須先關閉目前的 PowerShell**，再重新以系統管理員身分開啟一個新的 PowerShell 視窗，才能讓路徑設定生效。

## 驗證安裝成功

在新的 PowerShell 中輸入 `claude` 指令，Claude Code 若成功啟動並能回應問題，即代表安裝完成。
