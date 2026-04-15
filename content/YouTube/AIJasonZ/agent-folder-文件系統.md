---
title: .agent 資料夾讓 Claude Code 效能提升 10 倍
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-10-06
source: https://www.youtube.com/watch?v=MW3t6jP9AOs
---

## 核心概念：Context Engineering

- Claude Code 有 200,000 token 上限，context 越大效能越差
- `/context` 指令可查看 token 消耗分佈
- 目標：讓 conversation history 只包含相關、必要的資訊

## 優化 Context 的基本手段

- 移除不常用的 MCP（可釋放 2%+ context）
- 使用 sub-agent 將研究步驟隔離到獨立 thread，只回傳摘要
- 實作完特定功能後主動執行 `/compact`，清理對話歷史

## .agent 文件系統架構

```
.agent/
  readme.md          # 所有文件的索引，說明各文件用途
  task/              # 每個功能的 PRD / 實作計畫
  system/            # 專案架構、DB schema、API 文件
  sops/              # 標準操作程序（SOP）
```

### task 資料夾

- 每次實作功能前，先用 plan mode 產生實作計畫
- 計畫完成後存入 `task/` 資料夾
- 之後實作類似功能時可引用作為參考

### system 資料夾

- 跨功能的全域架構文件：專案結構、DB schema、API endpoint
- 隨 codebase 成長持續更新

### sops 資料夾

- 記錄標準流程（如「新增 DB table 的步驟」、「整合 Replicate 模型的流程」）
- agent 犯錯後，要求生成 SOP，避免重複犯錯

### readme.md

- 所有文件的導覽索引
- agent 初始化時先讀 readme，快速找到相關文件

## `/update-doc` 指令設計

- 初始化：`/update-doc initialize` → 掃描 codebase，建立初始 .agent 架構
- 實作功能後：`/update-doc` → 更新相關文件、SOP
- 當 agent 犯錯並修正後：要求生成 SOP，記錄正確做法

## 實際操作流程

1. `CLAUDE.md` 加入 docs 規則：「實作功能後更新 .agent 文件」、「計畫前先讀 readme」
2. 實作新功能時：plan mode → 存 task → 實作
3. 失敗修正後：生成 SOP → 更新 readme
4. 下次開新 conversation：agent 自動讀 readme，掌握全局上下文

## 效益

- agent 無需每次重新掃描整個 codebase
- 減少 context 噪音，提升實作準確率
- 跨 conversation 保持一致性
