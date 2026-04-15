---
title: 請相信我（對不起 Anthropic）
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-23
source: https://www.youtube.com/watch?v=RIkSlHgQYog
---

## T3 Code 新增 Claude Code 訂閱整合

T3 Code 宣布支援直接使用 Claude Code 訂閱，只需在本機安裝並登入 Claude Code CLI，即可在 T3 Code 中使用 Claude 的補貼推論額度，完全免費、開源。

## 為什麼 T3 Code 能做到但 Open Code 不行

**Open Code 的做法**：自建 OAuth 流程，直接管理使用者的 Claude Code token，相當於繞過 Anthropic 的 harness，使用第三方 harness 存取訂閱。Anthropic 認為這違反服務條款並發送律師函，強制下架。

**T3 Code 的做法**：不自建 harness，不處理 OAuth，不接觸 API key。T3 Code 是呼叫本機已安裝的 Claude Code CLI，等於在官方 harness 上加一層 UI，並非取代 harness。

Claude Code 本身在評估後也認為 T3 Code 的實作符合服務條款。

## Anthropic 政策的模糊性

Matt Pocock（TypeScript 教學者）花了超過一週嘗試向 Anthropic 確認：用 Agent SDK 的 OAuth token 在 local dev loop 中並行多個 Claude Code 執行緒，是否合規？未獲明確答覆。

Theo 認為這種模糊是刻意為之——讓 Anthropic 保有在任何時候改變規則、封禁任何工具的彈性。

## Claude Code 補貼的商業邏輯

- $200/月方案可使用約 $5,000 的推論資源（25 倍補貼）
- Anthropic 用補貼吸引重度用戶和意見領袖，鎖定在自家 harness
- T3 Code 無法靠自己的 API 提供同等補貼，因此選擇「讓用戶帶自己的訂閱進來」

## 免責聲明

Theo 明確表示：

- T3 Code 目前的整合方式在他的理解中是合規的
- 但他無法保證 Anthropic 未來不會改變政策或封禁帳號
- 如果有用戶因使用 T3 Code 被封禁，他願意協助調查並公開報導

## 對 Anthropic 的呼籲

> Anthropic，請直接告訴我們答案。我做的關於你們政策的報導，比你們公司任何員工加起來都多。給我們一個清楚的說法，這不難。
