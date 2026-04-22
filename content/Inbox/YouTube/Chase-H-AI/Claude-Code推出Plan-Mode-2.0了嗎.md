---
title: Claude Code 推出 Plan Mode 2.0 了嗎
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-06
source: https://www.youtube.com/watch?v=eEYbwJWVQtQ
parent: "[[01.index]]"
---

## Ultra Plan 是什麼

Claude Code 洩漏資料中出現、隨後正式發布的新功能。運作方式：

1. 在本地 terminal 啟動 plan mode session
2. 該 session 被推送至雲端 Claude Code（瀏覽器介面）進行處理
3. 在網頁介面審閱並修改計畫
4. 點擊「Approve Plan」將計畫帶回 terminal 執行

啟用指令：

```
ultraplan
# 或
/ultraplan
```

**前置需求**：必須有已建立且至少含一個 commit 的 GitHub repo。

## Ultra Plan vs 本地 Plan Mode 頭對頭測試

測試任務：從零建立一個 Kanban board web app（greenfield project），要求使用 frontend-design skill。

| 項目 | 本地 Plan Mode | Ultra Plan |
|---|---|---|
| 規劃時間 | 5 分鐘以上（需重啟一次）| 約 30 秒 |
| 是否遵循 skill 指令 | 是（用了 Google Fonts、frontend-design 排版）| 否（完全忽略 skill）|
| 架構輸出 | 含技術選型、排版細節 | 含 Mermaid 圖、依賴清單，程式碼量多幾百行 |
| 介面操作 | terminal 純文字 | 可 highlight 特定段落留言或 emoji |
| 計畫品質（AI 評審）| Gary Tan 認為 Ultra Plan 略優 | 同左 |

## 前端產出比較

- 本地 Plan Mode（有 frontend-design skill）：卡片有陰影層次、橙色小裝飾、優先度顏色標示
- Ultra Plan：功能相同，視覺較平，缺少 skill 帶來的設計細節

兩者後端程式碼品質差異不大，主要差在框架選擇與程式碼行數。

## 使用建議

**適合用 Ultra Plan 的情境：**
- 需要快速規劃且 skills 不重要的場景
- 專案夠複雜，能讓 Ultra Plan 發揮額外運算資源的優勢（簡單 Kanban 可能不夠複雜）

**不適合的情境：**
- 需要在計畫階段調用特定 skill（Ultra Plan 穩定忽略 skill 指令）
- 已有精心設計的 skill workflow 的用戶

**核心問題**：Ultra Plan 無法可靠地呼叫 skills，這是重大缺陷。作者在影片外部測試也重現了同樣問題。

## 結論

Ultra Plan **不是** 本地 Plan Mode 的直接替代品，是速度與 skill 支援的取捨。目前感覺是倉促發布的功能（文件薄弱，從洩漏到上線僅 2 天），預期未來會有大量更新與改進。建議自行測試複雜專案，結果因專案而異。
