---
title: Claude Code 10 個進階技巧
created: 2026-04-15
updated: 2026-04-15
source: https://www.youtube.com/watch?v=TmsH-RIHvas
published: 2026-02-11
parent: "[[01.index]]"
tags:
  - youtube
---

## 1. Insights 指令分析工作習慣

`/insights` 分析過去所有 sessions，產生報告：

- 找出最常出問題的地方
- 建議可改善的 workflow 功能
- 把報告中的 tips 複製進 `CLAUDE.md` 供未來使用

## 2. 專案文件四件組

開發前先讓 Claude 產生文件，而非手寫：

- `PRD.md`：需求與範圍
- `architecture.md`：資料格式、檔案結構、API 設計
- `decision.md`：所有決策記錄（作為後續參考）
- `feature.json`：所有功能的 token-efficient JSON，含完成標準與 `passes` 追蹤欄位

## 3. Context7 MCP 取得最新文件

```bash
# 安裝後 Claude 自動取得指定 library 的最新文件
```

防止依賴版本不符造成的程式錯誤，彌補模型知識截止日的落差。

## 4. Hooks 控制 Agent 行為

Hooks 在 Claude Code lifecycle 特定時間點執行 shell 指令：

- Exit code 0：成功，繼續執行
- Exit code 2：阻止（blocking error），Claude 收到錯誤訊息並修正
- 其他 exit code：non-blocking，顯示於 verbose mode

**TDD 保護 hook（pre-tool-use）：**

```bash
# 若路徑包含 test 目錄或 test 關鍵字 → exit 2
# 阻止 Claude 修改測試檔案
```

## 5. MCP CLI 模式（實驗性）

設定 `experimental MCP CLI flag = true`，MCP tools 不再佔用 context window：

- Claude 改用 `mcp-cli-info` 和 `mcp-cli-call` 透過 bash 呼叫
- 只有用到的工具才按需載入
- 大幅減少多 MCP 場景的 context bloat

## 6. Git Work Trees 平行 Agent

Branches 共用 working directory 會造成衝突，改用 work trees：

```bash
# 每個 agent 有獨立的 work tree
# 完成後 merge 合併
```

## 7. TypeScript Strict Mode

`tsconfig.json` 設定 `strict: true`，讓 compiler 在 build 時抓到：

- null value 問題
- 隱式型別
- Runtime 前的潛在錯誤

Agent 能依賴 terminal 錯誤訊息自動修正，不需等到 runtime 才發現問題。

## 8. User Stories 驅動測試

開發前撰寫 user stories（放在專屬資料夾）：

- 描述用戶如何與系統互動
- 包含 priority 與 acceptance criteria
- 涵蓋最佳路徑與所有 edge cases

Agent 逐一實作 stories，確保實作符合用戶預期。

## 9. Adversarial 平行 Agent

兩個 agent 對抗式協作：

- Research agent：執行研究任務
- Fact checker：驗證 research agent 的每個發現

兩者持續溝通，fact checker 阻止 research agent 輸出錯誤資訊。同樣模式可用於開發：一個 agent 實作，另一個 review 是否符合計畫。

## 10. 賦予 Agent 「眼睛」

解決 terminal-based agent 無法看到 client-side runtime 問題：

- **Claude Chrome extension**：DOM capture、console log
- **Puppeteer MCP**：隔離瀏覽器（不含現有 sessions）
- **Versel Agent Browser（推薦）**：
  - 使用 accessibility tree（唯一 element reference）
  - DOM 從數千 token 壓縮至 200-400 token
  - 比 Chrome extension 更 context-efficient

在 `CLAUDE.md` 設定：優先使用 agent browser，fallback 才用 MCP。

## 額外：預測性錯誤偵測

讓 Claude 主動識別「可能但尚未發生」的問題：要求 Claude 檢視實作並列出可能失敗的地方。Claude 透過 pattern matching 已知失敗模式，可找到多層測試未能發現的問題（曾找到 18 個潛在 production 問題）。
