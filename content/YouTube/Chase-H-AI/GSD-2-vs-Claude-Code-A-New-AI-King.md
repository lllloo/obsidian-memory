---
title: "GSD 2 vs Claude Code: A New AI King?"
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/ZgfybHGxzJU
---

GSD 2（Get Shit Done 2）從 Claude Code 的 orchestration 外掛，升級為基於 Anthropic PI SDK 的獨立 CLI 工具，與 Claude Code 正面競爭。本影片進行實測比較。

## GSD 2 核心特性

- **架構改變**：不再是 Claude Code add-on，而是獨立 CLI，基於 PI SDK
- **鐵則**：一個任務必須在一個 context window 內完成，太大就拆成兩個任務
- **Auto 模式**：給一個 prompt，自動規劃、執行完整專案
- **Step 模式**：更手動控制，可在執行中介入
- **雙終端架構**：一個執行終端（auto），一個討論終端（可即時溝通）
- **Token 預算控制**：可設定最高花費上限，防止意外超支

## 實測：個人支出追蹤 Web App

任務：含 expense form、expense list、dashboard、monthly summary，深色模式設計。

| 指標 | Claude Code | GSD 2 |
|------|------------|-------|
| 完成時間 | 4 分 38 秒 | ~90 分鐘（卡死重跑兩次） |
| 費用 | <1% 五小時用量 | ~$27.20 API 費用 |
| 視覺設計 | 較佳 | 普通 |
| 穩定性 | 穩定 | 中途卡住多次 |

## 重要警告

- GSD 2 宣稱支援 OAuth（Max 方案），但 **使用 Max 帳號在 Claude Code 外部可能被封鎖**
- Max 方案實際價值遠超訂閱費（$200/月 ≈ $2500–$5000 API 幣值），Anthropic 不允許濫用
- 必須使用 API key（OpenRouter 或 Anthropic 直接），費用昂貴

## 結論

對 Claude Code 用戶而言，GSD 2 目前**沒有使用理由**：
- 更貴（API 費用 vs 訂閱制）
- 更慢
- 結果並不更好

GSD 2 的上下文管理理念很好，但只有在「完全不用 Claude Code、純 API 模式」下才有其定位。
