---
title: 5 Open Source Repos That Make Claude Code UNSTOPPABLE (March 2026)
tags:
  - youtube
  - claude-code
  - open-source
  - github
  - ai
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/6SnFH43qPAw
---

2026 年 3 月最值得關注的五個 GitHub 開源專案，讓 Claude Code 更強大。

## 1. AutoResearch（by Karpathy）⭐ ~60K

機器學習演算法自動化實驗框架。

**運作方式：**
- 三個核心檔案：`program.md`（定義任務）、`train.py`（被 LLM 修改的「權重」）、`prepare.py`（基礎程式碼）
- 自動執行實驗 → 評分 → 若改善則 commit，若退步則 git reset → 循環

**適合場景（需要可量化評分）：**
- 程式執行速度優化
- Prompt 優化
- Claude Code skill 的 pass/fail 測試
- 系統提示格式驗證

**不適合：**創意寫作、主觀評估等無法二元評分的任務

實際案例：Shopify 用 0.8B 參數內部模型跑 37 次實驗後提升 19% 效率

## 2. OpenSpace（by HKU Data Intelligence Lab）⭐ ~1.7K

MCP-based 自動優化 Claude Code skills 的系統。

**三個自動化等級：**
- **autofix**：修復完全壞掉的 skill
- **autoimprove**：讓可用的 skill 更好
- **autolearn**：標記已達最優，停止修改

宣稱效果：真實任務中減少 46% token 用量、4.2 倍更高品質輸出（HKU 內部 benchmark）

## 3. CLI-Anything（by HKU）⭐ ~24K

將任何開源專案自動轉為 Claude Code 可用的 CLI 工具。

**流程：**兩行安裝 → 指向開源 repo → 自動分析/測試/文件化/發佈為 CLI tool

已支援：Blender、Audacity、OBS、Zoom、draw.io 等
意義：縮短「AI agent 與軟體操作」之間的落差

## 4. Claude Peers⭐ ~1K

讓多個 Claude Code terminal session 互相溝通。

**運作：** MCP server + SQLite，session 啟動時自動同步對話摘要給其他 session

**應用場景（搭配 Anthropic 工程部落格建議的三角架構）：**
- Session 1：規劃者（Planner）
- Session 2：執行者（Executor）
- Session 3：評估者（Evaluator）

解決 Claude Code 自我評估能力弱的問題

## 5. Google Workspace CLI

Google 開發者製作（非官方 Google 產品），讓 Claude Code 存取 Google 全套服務（Gmail、Drive、Docs、Calendar 等）。

**安全考量：**
- 建議沙箱化：只開放特定 Drive 資料夾或獨立 email
- 內建 Google Model Armor：掃描 prompt injection 風險

**建議：** clone repo 後讓 Claude Code 協助選擇需要哪些 skills，不需全部開放
