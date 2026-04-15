---
title: 停止把一切都叫做 Mock
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-07
source: https://www.youtube.com/watch?v=RvKPOjlQKyM
---

## 術語混亂的歷史

- 「mock object」一詞首次出現於 2000 年的論文，幾乎立刻就被誤解
- 2003 XP 大會：NUnit 主要作者 Charlie P 把 stub 稱為 mock，原始論文作者 Tim McKinnon 在台下舉手糾正，當場上台畫白板說明
- 2007 年 Gerard Meszaros 出版 *xUnit Test Patterns*，引入「test double」統一術語，但仍未有效解決混亂
- 此後各種 mocking framework 繼續使用不一致的術語，情況愈演愈烈

## Meszaros 的定義（值得了解，即使沒人嚴格遵守）

**Stub**
- 實作 SUT（system under test）使用的介面
- 透過回傳固定值或拋出特定例外來控制 **indirect inputs**
- 不驗證任何參數，不主動讓測試失敗
- 最簡單的 test double

**Fake**
- 類似 stub，但有更完整的輕量級實作
- 行為像真實物件，但缺乏完整的效能、穩定性或持久性
- 典型例子：in-memory database

**Spy**
- 可以做 stub 能做的一切（控制 indirect inputs）
- 額外功能：記錄所有方法呼叫，讓你在 assert 階段驗證呼叫了哪些方法、傳入哪些參數

**Mock**
- 與 spy 類似，都可用來驗證互動
- 關鍵差異：mock 在 **act 階段**就可以主動讓測試失敗（expectations 不滿足時立即觸發）
- spy 是事後查帳；mock 是設了期望、現場爆炸
- 「trigger-happy spy」

**判斷依據是執行時行為，不是建立方式**
- 手寫的實作不自動是 fake；用 framework 產生的不自動是 mock
- 決定類型的是它在 runtime 怎麼運作

## 實際建議：用動詞描述用途

作者的結論：與其糾正術語，不如說清楚這個物件**幫你做了什麼**。

- 「我用這個 mock 來 **stub** 這些值」
- 「我用這個 mock 來 **spy on** 這個重要互動」
- 「這個 mock 幫我 **design** 與 collaborator 的互動」

## Mock 被遺忘的原始目的：設計工具

- 原始 mock objects 論文的目標是**更好的物件導向設計**，不是更容易的測試設計
- 核心原則：tell don't ask——物件應封裝資料與操作，不暴露 getter 讓測試直接驗狀態
- Mock 讓你驗證 indirect outputs（與 collaborator 的互動），而不需要加 getter
- 這個設計面向的意義在語義擴散中幾乎完全消失
