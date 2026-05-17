---
title: 訂機票、找飯店、查評價不用開 3 個網站：Claude 一次跑完旅行規劃
created: 2026-05-04
updated: 2026-05-04
source: https://www.youtube.com/watch?v=RxdY3RSRtM0
published: 2026-05-01
parent: "[[01.index]]"
tags:
  - youtube
  - claude
  - mcp
  - travel-planning
---

## 場景設計

- 規劃聖誕節澳洲 17 天旅行（雪梨 / 墨爾本）
- 一個對話視窗內同時調度多個 MCP，避免在 Skyscanner、Booking、Google Maps 之間來回切
- 三個 MCP 協作：Google Flights MCP、Trivago MCP、Google Maps MCP

## Google Flights MCP：機票查詢

- 指令範例：「幫我查台北直飛雪梨或墨爾本的機票，要經濟艙與商務艙價格，旅行 17 天左右」
- Claude 自動把自然語言轉成 MCP 可溝通的查詢參數
- 結果含直飛航班、票價區間、商務艙加價幅度
- 比 Skyscanner 多了主動分析：避開跨年回程、越早出發越便宜、雪梨比墨爾本便宜
- 並建議適合的出發時段與行程方向

## Trivago MCP：飯店篩選

- 預算設定：每晚 NT$4,000–4,500
- 條件：不要青年旅館、位置自然、基本整潔
- 補充指令：找不到評價時改去 Google Maps 查
- 多 MCP 協作流程：
  - 先用 Google Flights 取得旅行時間區間
  - 把區間傳給 Trivago MCP 篩飯店
  - 拿飯店名稱再給 Google Maps MCP 比對

## 城市 ID 解歧義

- Trivago 查城市時發現「墨爾本」有多個結果（澳洲、佛羅里達州都有）
- Claude 自動判斷澳洲墨爾本，鎖定正確 ID 後才繼續查飯店

## 資料格式整理

- MCP 回傳 JSON 結構化資料（含三星四星標籤、評分、樣本數）
- Claude 主動整理重點：因樣本足夠、可信度高，本輪先不額外查 Google Maps

## 重要安全提醒：不要綁信用卡 / 券商

- 講者明確不給 Claude 信用卡資訊，也不把美股 MCP 連到券商帳號
- 風險考量：直接綁自動交易資格風險過大
- 推薦做法：MCP 做查詢與規劃，最後一步「實際下訂」由人手動完成

## 二次驗證：交叉比對發現雷點

- 對前兩名飯店做第二輪 Google Maps 查證
- 流程：找地點 ID → 用 ID 抓評價 → 比對 TripAdvisor 與其他平台
- 發現具體雷點：
  - 某間隔音不好、走廊有說話聲、陽台噪音、房間偏小
  - 某間有發霉、衛生問題嚴重
- 平台單一資料源看不到的資訊，靠交叉比對才浮現

## 最終建議（四間飯店分級）

- 一間雙平台都好評 → 必選
- 一間隔音不佳但仍可接受
- 一間衛生視狀況
- 一間明顯不衛生 → 排除

## 此工作流的核心優勢

- 平台 vs Claude 的差異：單一平台只能在自己資料庫內篩選，無法跨平台交叉比對
- Claude 做的事其實是「人會做的交叉比對」，差別在於速度快得多
- 一個對話視窗內完成飛機、住宿、評價驗證三件事，不需切多個 app
