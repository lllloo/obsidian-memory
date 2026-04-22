---
title: 這個重大更新改變了我使用 Claude Code 的方式
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-04-14
source: https://www.youtube.com/watch?v=sncxStbRSwI
parent: "[[01.index]]"
---

## Adviser 策略概念

Anthropic 推出的 **Adviser 策略**改變了 Claude Code 的模型協作方式：

- **執行者（Executive）**：Claude Sonnet，負責所有工具呼叫、程式碼修改、對外輸出
- **顧問（Adviser）**：Claude Opus，只在 Executive 遇到困難時才被諮詢，不直接寫程式碼
- 啟用指令：在 Claude Code 設定 `--advisor` 並指定 Opus 為顧問模型

**為何需要此策略：**
- Anthropic 持續調降使用限制，Opus 消耗 token 快
- 純 Sonnet 在複雜邏輯上有能力上限
- Adviser 策略讓 Opus 只在必要時介入，兼顧品質與 token 效率
- Anthropic 實驗結果：此組合在 SU-Bench 上優於單獨使用 Sonnet，成本也低於全程使用 Opus

## 實測案例

### 案例一：Real-time 同步 bug 修復

- 問題：多裝置同步時，移動與縮放元素正常，但刪除不同步
- 單獨使用 Sonnet 多次嘗試均無法修復
- 開啟 Adviser 後，Sonnet 判斷問題困難，主動諮詢 Opus
- Opus 指出同步邏輯斷點的確切位置與需要重構的部分
- Sonnet 直接套用建議，無額外來回
- 結果：多裝置測試通過，刪除同步正常運作

### 案例二：大規模 UI 改版

- 任務：將現有應用換用新 UI 元件庫並同時進行多處 UI 變更
- Sonnet 用 Playwright MCP 先了解現有 UI 佈局
- 判斷這是重大變更，主動諮詢 Adviser
- Opus 發現新舊元件庫有版本衝突問題，需先解決依賴
- Sonnet 依序解決依賴 → 確認應用正常運行 → 逐一改寫元件
- **限制**：整個過程花了 31 分鐘，因為 Sonnet 循序執行而非平行處理
- Opus 作為主要 agent 會更快，它能識別可平行執行的任務

### 案例三：新功能實作失誤後修正

- 任務：在既有 codebase 新增一個頁面與新功能
- 預期 Sonnet 會諮詢 Adviser，但它自行完成實作，判斷是常規任務
- 測試發現問題：修改某元件，變更外溢到預覽區域外的元件；需要手動按 Run 才能同步
- 手動要求使用 Adviser 後：
  - Opus 識別根本原因——錯誤的元件選擇
  - Sonnet 套用修正，串流立即生效，元件邊界問題解決

## 策略的邊界與限制

**適合使用的情境：**
- 在 token 限制內工作，且任務不需要全程 Opus 級別推理
- 需要偶爾深度推理但大多為直接實作的中小型應用

**不適合的情境：**
- 複雜應用、多個相互依賴的元件、多個潛在失敗點 → 直接使用 Opus
- Sonnet 即使遵循 Adviser 建議，仍可能選錯實作路徑，因為它無法同時評估多種方案的下游影響

**已知問題：**
- Executive 不總是能正確判斷任務複雜度，可能跳過諮詢
- 需要手動提示「使用 Adviser」才能觸發正確行為
- 複雜 app 的來回修正可能比一開始就用 Opus 花更多時間
