---
title: DeepSec AI 安全掃描架構
created: 2026-05-09
updated: 2026-05-09
source: https://www.youtube.com/watch?v=qkc1j3_k8gs
published: 2026-05-08
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - security
---

## 背景：AI 生成程式碼的安全危機

近期 AI coding agent 引發多起嚴重事故（整個 project 被刪除、production 資料庫遭清空、Apple 內部 CLAUDE.md 外洩），促使工具層需要更系統化的安全審查機制。Vercel 因此發布了 DeepSec。

## DeepSec 核心架構

DeepSec 不是讓 Claude Code 直接掃全庫，而是分層設計：

### 1. Regex 過濾（第一層，快速）

對全部檔案進行 regex-only 掃描，比對已知安全敏感模式（如常見漏洞類型的程式碼特徵），從大量檔案中篩出需要深度審查的子集。這一層純程式碼邏輯，速度快、無 token 消耗。

### 2. Agent 調查（第二層，並行）

過濾後的檔案依約每批 5 個分組，為每批組裝含框架資訊的 fresh prompt，送交 Claude Agent SDK 或 Codex Agent SDK（只讀工具存取，防止誤改）同步並行調查。結果合併去重後正規化。

使用的模型：Claude Opus 4.7（max effort）+ GPT 5.5（x-high reasoning），成本極高，適合大型 codebase 而非日常使用。

### 3. 再驗證（可選）

對調查結果二次確認，過濾誤報（false positive 率約 10–20%）。

### 4. 報告與 Export

輸出 Markdown/JSON 報告，依嚴重度分類。Export 後每個問題獨立一檔，包含：
- 問題來源（檔案 + 行號）
- 嚴重度與模型信心度
- 引入問題的 commit 與負責的 committer
- 建議修正方式與重現步驟

## 執行流程

```bash
# 1. 初始化（安裝依賴，在 .deepsec/ 資料夾執行）
deepsec init

# 2. 建立 info.md（讓 Claude 填寫專案概述、認證流程、威脅模型、已知 false positive）
# 在 .deepsec/ 資料夾執行，agent 會往上一層讀 codebase

# 3. 執行 regex 掃描
deepsec scan

# 4. 執行 agent 調查（可指定 API key，預設用 Claude Code 訂閱）
deepsec process

# 5. 生成報告
deepsec report

# 6. （可選）再驗證
# 執行 revalidation step

# 7. 匯出結果
deepsec export
```

## DeepSec 的侷限

- 僅關注程式碼中**明確存在**的問題，不涵蓋執行期動態漏洞（如 CORS 問題）
- 不擅長邏輯層與架構決策類的安全問題
- `info.md` 若列出「已知漏洞」，DeepSec 會刻意跳過它們，只尋找未記錄的新問題——此設計為刻意行為，非 bug

## DeepSec vs 直接用 Claude Code 審查

| 面向             | DeepSec                        | Claude Code 直接審查              |
| ---------------- | ------------------------------ | --------------------------------- |
| 大型 codebase    | 適合（並行、分批）             | 慢且耗 token                      |
| 問題範疇         | 聚焦 regex 命中的明確漏洞      | 涵蓋更廣（含架構、邏輯問題）      |
| 修正建議         | 詳細（每問題獨立報告）         | 詳細但分散                        |
| 容錯             | 中斷後可從斷點續跑             | 取決於 prompt 設計                |
| 成本             | 高（使用最強模型並行）         | 中等                              |

實測案例：同一 codebase，DeepSec 找出 9 個問題、Claude 找出 39 個（聚焦範疇後降至 13 個）。DeepSec 遺漏的幾個問題屬於執行期動態漏洞，是其設計邊界外的項目。

## AILABS DeepSec Skill

影片作者將 DeepSec 完整流程封裝成 skill，含：
- 端對端流程指令（從 scan 到 export）
- 錯誤補償邏輯（填補 DeepSec 遺漏的執行期漏洞）
- eval 評估集、參考資料、輔助腳本
