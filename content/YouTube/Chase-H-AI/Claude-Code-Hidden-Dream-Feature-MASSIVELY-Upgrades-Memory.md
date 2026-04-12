---
title: Claude Code's Hidden /dream Feature MASSIVELY Upgrades Memory
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/E-1Lmyv6Cjo
---

介紹 Claude Code 的 `/dream` 功能（記憶體整合），說明 auto memory 系統的運作原理，以及如何在尚未獲得官方存取的情況下自製等效 skill。

## Auto Memory 運作機制

- Claude Code 會自動根據對話內容建立 markdown 記憶檔案，無需手動干預
- 記憶檔案存放於 `~/.claude/projects/<project>/memory/` 資料夾
- 包含一個主索引 `memory.md`（類似 skills 的 manifest），以及各主題獨立的 markdown 檔案
- 主索引在每次 session 開始時載入，告訴 Claude Code 有哪些記憶可用

## Auto Memory 的問題

| 問題 | 說明 |
|------|------|
| 重複檔案 | 多個記憶檔說同一件事 |
| 矛盾資訊 | 前後對話產生衝突指示 |
| 過時資料 | 不再適用的資訊殘留 |
| 相對日期 | 「下週五」隨時間失去意義 |
| 索引膨脹 | 主索引越來越大，形成 context bloat |

## Dream 的四步驟修正流程

1. **讀取現有記憶**：分析 memory.md 主索引
2. **對比 session 記錄**：讀取最近 5 次 session 的 JSONL transcript，確認實際使用情況
3. **合併整理**：消除重複、解決矛盾、更新過時資料、將相對日期改為絕對日期
4. **精簡索引**：裁剪 memory.md（上限 200 行，越短越好）

## 自製 Dream Skill

- dream 的 prompt 已公開（由已獲存取用戶分享）
- 作法：複製 prompt → 告訴 Claude Code 建立名為 `dream` 的 skill
- 建議加入 flag 選項：
  - `/dream` → 專案層級
  - `/dream user` → 使用者層級（跨所有專案的 memory）
  - `/dream all` → 兩者都執行

## 實測結果

執行 `/dream` 後識別 7 個問題：近重複、矛盾、過時資料（×2）、相對日期、錯誤分類、過於冗長。最終合併數個檔案、更新 4 個、裁剪 3 個、保留 5 個不變。
