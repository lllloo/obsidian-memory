---
title: AI Agent 用 Rork 在幾分鐘內建立 20 萬美元手機 App
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-22
source: https://www.youtube.com/watch?v=ds1k2cmtqdI
---

## 概覽

- Rork Max 是 AI 驅動的手機 App 開發工具，由 **Claude Code + Opus 4.6** 提供動力。
- 一個 18 歲不懂寫程式的用戶，用 Rork 建立了兩款 App，收到 $200,000-$300,000 的收購報價。
- 目標：讓任何人都能用自然語言建立手機 App，不需要學習程式語言。

## 支援平台

- iPhone、iPad、Apple Watch、Apple TV、Apple Vision Pro
- 全部使用 **Swift**（Apple 官方程式語言）原生開發

## 舊工作流 vs 新工作流

| 面向 | 舊方式 | Rork Max |
|------|-------|---------|
| 設備需求 | 需要 Mac | 任何電腦、瀏覽器即可 |
| 工具 | Xcode + Swift 學習曲線 | 單一網頁介面 |
| 語言 | 需要學 Swift | 純自然語言描述 |
| 測試 | 實體裝置插線 | 一鍵安裝到手機 |
| 發布 | 幾週到幾個月 | 兩步驟上架 App Store |

## 實測：天氣 App（含 AI 助理）

**Prompt 範例：**
「Build a beautiful weather app with real-time location based weather, animated backgrounds (rain particles, falling snow, sunrays, clouds), hourly and 7-day forecast, clean minimal Apple style UI. Include a built-in AI chat assistant that answers weather related questions.」

**執行過程：**
1. Rork 自動拆分為 8 個步驟，逐一執行
2. 使用 Opus 4.6（200K context window）完成開發
3. 在網頁模擬器中即時顯示預覽

**結果（幾分鐘完成）：**
- 雲朵動畫、雨滴粒子效果
- 7 天天氣預報與每小時溫度
- 內建 AI 問答助理（「這週會下雨嗎？」→ 即時回答）
- 一個 Prompt，零次人工介入

## 部署到手機

1. 在 Rork 右上角點擊「Publish」→ 取得預製網址（可分享）。
2. 取得 QR Code，用手機相機掃描。
3. 在 App Store 安裝 **Expo Go**（免費）。
4. 掃描 QR Code → 在 Expo Go 中開啟 → App 立即在手機上運行。

## AI Agent 執行時間的進化

- 2025 年初：Agent 執行約 30 秒到 1 分鐘就需要使用者介入。
- 2026 年：Opus 4.6 可自主運行 **14.5 小時**不中斷。
- 未來：Agent 將能運行數天甚至數週，完成複雜的業務工作流程。

## Rork 的技術突破

- 真正的突破不只是讓 AI 寫 Swift 程式碼——而是：
  1. **讓 AI Agent 能寫正確的 Swift 程式碼**（Claude Code + Opus 4.6）
  2. **在瀏覽器中即時編譯並展示結果**（無需安裝任何工具）
- 這兩件事合在一起，讓完全不懂程式的人也能在幾分鐘內看到 App 運行在手機上。

## 建立 App 的成本

- 可切換目標平台：iOS、Android、iPad（點擊右上角切換）。
- Rork 透明顯示使用的 AI 模型（Opus 4.6）。
- 使用 Rork Max 開始前，確保左上角已切換 **Rork Max 模式**。

## 結語

- 使用成本遠低於傳統開發，但創造的商業價值可能達數十萬美元。
- 最關鍵的是：有想法 + 執行力 > 程式技能。
- 建議：直接前往 rork.com，描述你想建立的 App，在手機上試試看。
