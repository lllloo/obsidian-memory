---
title: Vault 運作模式
created: 2026-05-25
updated: 2026-10-13
tags:
  - vault
  - meta
---

# 運作模式 — Karpathy LLM Wiki

本檔只留設計取捨；可執行流程以 [AGENTS.md](../AGENTS.md) 為準，檔案職責與導航以 [vault-map.md](vault-map.md) 為準。

## 核心構想

採 Karpathy LLM Wiki：AI 讀原始來源，將知識整合成持續維護的互聯 wiki。價值在可累積的摘要、關聯與矛盾處理；概念與實作比較分別見 [[LLM-Wiki-知識管理模式]]、[[LLM-Wiki-生態實作比較]]。

本 vault 聚焦 coding agent／LLM 工具生態與跨專案方法論。專案特定的實作、bug 與狀態留在各自 repo；私人筆記在 Notion，不參與核心流程。

## 三層與三個動作

- raw 是 write-once 的事實來源；wiki 是 AI 全權維護的活知識庫；schema 約束流程並保存操作狀態。
- Ingest 整合來源與既有主張；單一來源典型牽動 10–15 頁。Query 先讀索引再讀頁，附引用；有價值的答案可回存 wiki。Lint 檢查結構與近期矛盾／明確事實錯誤，由 AI 自主修補。
- 使用者提供來源、問題與方向，並事後 review GitHub diff；AI 負責維護與 commit／push。超過 15 頁的 ingest 與 skill 變更依 AGENTS.md 的確認流程。

## Skill 升級訊號

不預先建立 skill；手動流程重複至少 3 次並形成固定套路時，才提議 codify。候選記在 [MEMORY.md](MEMORY.md)；達到門檻時主動提議，使用者同意後才寫 skill。既有流程已涵蓋的事情不另建平行入口。

## 為何有效

把摘要、交叉引用、歸檔與一致性維護交給 AI，讓每次 ingest 與 Query 回存累積成可再次使用的知識。局部維護優先於全庫重整，避免維護成本隨規模無界成長。

Knowledge Compounding 框架把持久知識層視為可改變後續任務成本的資產（[arXiv 2604.11243](https://arxiv.org/abs/2604.11243)）。**限制：preprint、未確認同儕審查，僅 n=4 查詢、單一系統，30 天數字為推估；框架可用於表述，數字勿引**。跨系統橫評（[arXiv 2606.24775](https://arxiv.org/abs/2606.24775)，12 個記憶系統／5 workload／11 資料集）支持局部維護成本較低，但不是 markdown wiki 的直接實測。失效模式與證據限制見 [[Agent-維護知識庫的已知失效模式]]。

## 刻意不做

- 不建立真人閱讀入口、架構讀本、公開發佈層或 PR 合併通知；本 repo 只供 AI 執行核心流程（2026-10-13 使用者拍板）。Obsidian 設定、Web Clipper 與 Git bundle 保留作既有工具支援。
- 不自動讀寫 Notion，也不將私人筆記納入 raw／wiki 來源。
- 不建立跨專案查詢入口或自動同步；他 repo 的實作回該 repo 做。
- 不做無界的全庫語意整理：ingest 只自檢當輪頁，lint 機械層掃結構，語意層受近期窗口與頁數上限約束；可改可不改的措辭、單純過時與交叉引用缺口不報。
- 不另建 log.md、執行心跳或結案報告；操作歷史用 git，BACKLOG 只留未決項與去重約束。
- 不預先加入搜尋引擎、圖片下載或簡報產物；目前以索引與 Grep 查詢，實際需求出現時再評估。

## 時間抗性

wiki 描述行為與限制，易變版本細節指向官方 changelog；raw 保留來源快照。證據翻案在 wiki 就地留痕，引用時保留強度與限制。
