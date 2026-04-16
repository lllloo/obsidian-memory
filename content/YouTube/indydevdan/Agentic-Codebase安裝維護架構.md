---
title: 每個 Agentic Codebase 都應該有的一個 Prompt（工程團隊篇）
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-26
source: https://www.youtube.com/watch?v=3_mwKbYvbUg
parent: "[[01.index]]"
---

## 核心概念

衡量一個工程團隊品質的指標：新工程師在本地跑起專案所需的時間。結合「確定性腳本 + Claude Code hooks + Agentic prompt」，可以標準化 codebase 的安裝與維護流程。

## 工具：Justfile 指令啟動器

- `just` 是一個輕量 command runner，作為工程工作的啟動平台
- 將所有常用指令、agent 執行方式集中在一個 `justfile`
- 團隊成員與 agent 不需要記憶 CLI flags，直接 `just <command>` 執行
- 範例指令：`just cli`、`just clmm`（codebase maintenance）

## Claude Code Setup Hook

```
# settings.json 中新增 setup hook
{
  "setupHook": {
    "init": "bash scripts/setup-init.sh",
    "maintenance": "bash scripts/setup-maintenance.sh"
  }
}
```

- `--init` flag：在 session 啟動前執行安裝腳本（`uv sync`、`npm install`、DB 初始化）
- 只在需要時執行，不是每次 session 都跑
- 適用場景：安裝依賴、跑 migration、週期性維護

## 安裝 Prompt（`/install`）

結構：確定性腳本 + Agentic prompt 組合

```
workflow:
  1. /prime — 載入 codebase 文件，讓 agent 理解架構
  2. 讀取 setup hook 產生的 log 檔案
  3. 驗證安裝結果並回報
  4. 若有問題，根據 prompt 內嵌的 common issues 引導解決
```

- 加入「human-in-the-loop 模式」：agent 提問 → 工程師回答 → 繼續執行
- 互動問題範例：如何處理 database？安裝模式（full/minimal）？是否檢查環境變數？
- Claude Code 一次最多支援 4 個問題

## 維護 Prompt（`/maintain`）

- 同樣結合確定性腳本 + agentic prompt
- 用途：更新依賴（`npm update`）、DB migration、清理 dead code、安全檢查
- 在 prompt 中加入 common issues 區段：

```
## Common Issues
- Problem: Database corruption
  Solution: Clear the database and rerun migration
```

## 模式總結

三個核心元素：
1. **Justfile**：標準化所有指令入口
2. **Setup Hook**：確定性腳本，在 session 啟動時執行
3. **Agentic Prompt**：在腳本執行後接手，處理第二、三層問題

優勢：
- 新工程師跑一個指令，有 agent 引導整個安裝流程
- 每個人用相同方式設定，消除設定差異
- 可安排定期健康檢查，自動更新有漏洞的套件
- Prompt 成為「會執行的活文件（living document that executes）」
