---
title: GSD 2 對決 Claude Code
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-17
source: https://www.youtube.com/watch?v=ZgfybHGxzJU
parent: "[[01.index]]"
---

## GSD 2 的重大變化

GSD 原本是跑在 Claude Code 內部的 orchestration layer。GSD 2 改為**獨立 CLI 工具**，基於 Python SDK 構建，不再是 Claude Code 的附加元件，而是競爭對手。

核心理念不變：
- 把大計劃拆分為 phases → tasks
- 每個 task 由 sub-agent 在獨立 context window 執行
- 鐵律：一個 task 必須在一個 context window 內完成

新功能：
- **Auto mode**：給計劃後走開，完全自動執行直到完成
- **Step mode**：更手動、更有掌控感
- Token 預算上限設定（避免意外燒錢）

## 費用警告

GSD 2 雖然可以用 Max plan 的 OAuth 認證，但**強烈不建議**。Anthropic 明確表示 Max plan 不可在 Claude Code 外使用，違者可能被封帳號。

實際費用：
- 必須使用 API key（Anthropic 直接或 OpenRouter）
- $200 Max plan ≈ $2,500-5,000 API credits 的等值
- 因此在 GSD 2 裡用 API 非常昂貴

## 安裝與設定

```bash
# 安裝
pip install gsd  # （複製 GitHub 指令）

# 登入設定
gsd  # 走 setup wizard，建議用 API key

# 設定 preferences
/gsdres  # → models → 設研究/計劃模型（Opus）、執行模型（Sonnet）
/gsdres  # → 設 budget ceiling（如 $20）

# 切換模型
/model
```

使用時建議開兩個 terminal：
- Terminal 1：GSD auto（實際執行工作）
- Terminal 2：討論 terminal（隨時補充指令，GSD 從磁碟讀取）

## 頭對頭測試：個人記帳 Web App

測試任務：個人費用追蹤 app，含費用表單、費用清單、dashboard、月度摘要。

**結果對比：**

| 指標 | Claude Code | GSD 2 |
|------|-------------|-------|
| 時間 | 4 分 38 秒 | 約 1.5 小時（多次卡住） |
| 費用 | <1% 5小時用量 | ~$27.20 API 費用 |
| 視覺效果 | 較佳 | 較差 |
| 功能完整性 | 達標 | 達標 |

GSD 2 期間卡住數次，分別停頓 17 分鐘、40 分鐘，需完全重啟才完成。

## 最終評估

GSD 2 目前不推薦給 Claude Code Max plan 用戶，原因：
- 更慢、更貴
- 產出結果不更好
- 只有在純 API 使用者、或需要處理「巨大複雜專案」時才可能值得

架構思想很好（context window 管理、任務分解），但成本效益目前不划算。
