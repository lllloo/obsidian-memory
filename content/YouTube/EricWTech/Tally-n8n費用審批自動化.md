---
title: 用 Tally + n8n 建立非同步費用審批自動化系統
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-28
source: https://www.youtube.com/watch?v=7SviuycyCb0
---

## 系統架構概覽

員工用 Tally 表單提交費用 → n8n 檢查重複 → 傳送 Slack 審批請求 → 等待主管決定 → 處理逾時 → 自動記錄或拒絕

這是一個真正**有狀態（stateful）**的非同步工作流，而非直線型自動化。

## 為什麼選 Tally

- 免費方案：無限表單、無限提交
- 內建處理：檔案上傳、條件邏輯、表單驗證——不需額外設定
- 檔案上傳後 URL 直接出現在 n8n 提交資料中，無需額外儲存步驟

## 建立 Tally 表單

必要欄位：
- 短文字：員工姓名
- 數字：費用金額
- 下拉選單：類別（Travel、Software、Meals）
- 上傳欄位：收據圖片

進階功能：條件邏輯——選擇 "Other" 類別時顯示額外文字欄位（全部視覺化設定，無需程式碼）。

取得 API key：Workspace Settings → API → Generate key。

## n8n 工作流設定

### Step 1：Tally Trigger

搜尋 Tally 節點 → 填入 API key → 選擇表單 → 執行 step 後測試提交，提交資料以結構化 JSON 出現。

### Step 2：防止重複提交

每筆 Tally 提交都有唯一 `submission ID`，利用此 ID 做冪等性（idempotency）檢查：

1. 加入 Google Sheets 節點（Get Rows），查詢 `expense_requests` 表是否存在此 ID
2. 加入 IF 節點：
   - **True（重複）**：靜默終止或通知管理員
   - **False（新提交）**：將完整資料 + submission ID 寫入 Google Sheets

### Step 3：Slack 審批（非同步等待）

使用「傳送訊息並等待回應」模式（**不是**一般傳送訊息）：

訊息內容：員工姓名、金額、類別、收據連結（Tally 直接提供 file URL）。

加入兩個按鈕：
- `approve` → 回傳 "approved"
- `deny` → 回傳 "rejected"

機制：n8n 生成 resume URL，主管點擊按鈕後 Slack 呼叫此 URL，工作流從暫停處繼續。

**逾時設定**：在 Slack 節點加入 wait limit（例如 48 小時），超時後進入 timeout 分支。

### Step 4：Switch 節點處理決策

三個路由：
- `approved` → 更新 Google Sheets 狀態欄為 "approved"，加入時間戳記
- `rejected` → 更新狀態為 "rejected"，可加入拒絕原因欄位
- fallback（逾時）→ 另外處理

決策後：傳送 Slack 或 email 通知員工結果。

## 完整流程

```
Tally Trigger
→ 檢查重複提交
→ 記錄到 Google Sheets
→ Slack 傳送並等待審批
→ Switch（approved / rejected / timeout）
→ 更新 Google Sheets 狀態
→ 通知員工
```

## 可維護性建議

- 節點命名要清楚：`if` → `Check Duplicate Submission`；Slack 節點 → `Send Slack Approval and Wait`
- 在重要節點（重複檢查、逾時分支）加上說明備註
- 可將 Google Sheets 換成 Airtable，Slack 換成 email，或加入多層審批

官方 n8n workflow template 可直接 clone 並替換自己的 credentials。
