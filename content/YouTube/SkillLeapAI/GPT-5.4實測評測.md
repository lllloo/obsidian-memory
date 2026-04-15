---
title: GPT-5.4 實測評測
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-05
source: https://www.youtube.com/watch?v=rwaC1i-p8do
---

## 模型概況

- **GPT-5.4 Thinking**：發布當天同時推出 GPT-5.4 Pro
- **GPT-5.3 Instant**（幾天前已發布）：即時回答，無思考過程
- GPT-5.3 沒有 Thinking 版，版號命名因此不連續
- GPT-5.4 Thinking 在部分基準測試略勝 Claude Opus 4.6 與 Gemini 3.1 Pro，但差距接近

## 五大升級重點

1. **知識工作**：Excel 試算表（含公式）與 PowerPoint 簡報建立能力大幅提升，勝過 5.2
2. **Computer Use（原生）**：首個原生支援電腦操作的通用模型，可處理資料輸入、Email / 行事曆
3. **Coding 能力**：Thinking 版媲美專為程式設計的 GPT-5.3 Codex
4. **Token 效率**：tool calling token 用量下降；整體使用成本可能比 5.2 更低
5. **Hallucination 減少 33%**：相較 5.2，持續逼近 1% 目標

## 實測：深度網路研究

- Prompt：分析 AI 消費者產品的幻覺問題是否隨版本改善，要求三段式輸出
- 可在執行中追加指示（如「增加到 15 個來源」）不需重啟對話
- 約 57 秒完成；結果附引用來源，架構清晰

## 實測：文件輸出

- **PowerPoint**：從研究結果轉成 15 頁投影片，約 5 分鐘，附來源參考；可要求重新設計保留內容
- **Excel**：一次 prompt 產生含公式的多頁試算表，約 10 分鐘；建議事後 spot check 數字
- Thinking Effort 可調整：Standard（預設）→ Heavy（複雜任務）

## 實測：Coding

- **測試 1**：AI 工具比較儀表板（圓角卡片、深淺模式切換）—— 篩選功能正常，但比較功能和外部連結有 bug
- **測試 2**：24 小時城市光線模擬 —— 從清晨到夜晚動畫運作正確，首次 prompt 即完成
- 作者評估：Coding 最佳仍是 Claude Opus 4.6，儘管基準測試 5.4 略勝

## 實測：寫作（主觀評估）

- 測試：YouTube 影片開場 hooks，5 個選項
- 問題：出現 M dash（即使系統指令明確禁止），tone 不符個人風格
- 比較：Gemini 與 Claude 在零設定下寫出自然對話語氣的表現更佳

## 使用注意

- 上市初期帳號可能延遲數小時才能使用
- Plus 方案有限量，Pro 方案無限量
- Thinking Effort 設 Heavy 時等待時間顯著拉長
