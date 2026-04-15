---
title: 如何從 ChatGPT 切換到 Claude（完整保留記憶）
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-02
source: https://www.youtube.com/watch?v=7R3ZIVF-c1I
---

## 遷移方式

Claude 官方提供了從 ChatGPT 匯入記憶的功能，入口在 Claude.ai 的 **設定 → 功能 → 從其他 AI 服務匯入記憶**。

## 操作步驟

**第一步：最大化 ChatGPT 記憶讀取範圍**

在 ChatGPT 中，進入 設定 → 個人化，確保以下三項全部開啟：
- 參考已儲存的記憶
- 參考瀏覽器記憶
- 參考對話紀錄

**第二步：使用 Thinking 模型執行擷取 prompt**

切換到 Thinking 模型（非 Auto），貼入 Claude 提供的擷取 prompt 並執行。Thinking 模型會進行更多推理循環，從帳號中找出更多資訊。

**第三步：複製並匯入至 Claude**

複製 ChatGPT 輸出的記憶區塊（通常是 code block 格式），回到 Claude，右鍵貼上後點選「加入記憶」。Claude 會自動將這些資訊格式化成分類清晰的記憶條目，且每晚根據新對話自動更新。

## 遷移後整理

完成後可以逐條瀏覽新建立的記憶，若有誤差可點擊編輯修正。此步驟非必要，但有助於確保品質。

## Projects 用戶的遷移方式

若在 ChatGPT 中有使用 Projects（附有上下文檔案的對話集合），處理方式稍有不同：

1. 在對應 Project 中以 Thinking 模型執行擷取 prompt（可獲得更多 Project 內的資訊）
2. 在 Claude 中建立新 Project（如：工作脈絡）
3. 在 Project 的 instructions 中手動貼入擷取到的資訊
4. 約 12 小時後，Claude 的 Project 記憶會整合更新，完成完整遷移
