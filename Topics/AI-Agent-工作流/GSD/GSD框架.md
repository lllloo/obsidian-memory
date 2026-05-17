---
title: GSD 框架（Get Shit Done）
created: 2026-04-20
updated: 2026-05-08
source: https://github.com/gsd-build/gsd-2
tags:
  - claude-code
  - agent-framework
---

GSD 是以 fresh session、state machine、狀態外部化為核心的 agent orchestration 工具，把長任務切成可由新 session 接力的單位、進度落到檔案系統，避免單一對話 context 拖到爛掉。分兩條線：v1 `get-shit-done` 為注入到 agent host 的 workflow pack（資料夾 `.planning/`），v2 `gsd-2` 為基於 Pi SDK 的 standalone CLI（資料夾 `.gsd/`），兩線並行維護。

## 連結

- v2 repo：<https://github.com/gsd-build/gsd-2>
- v1 repo：<https://github.com/gsd-build/get-shit-done>

## 相關

- [[Harness-Engineering]] — orchestration / context 控制取徑
