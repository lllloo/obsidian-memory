---
title: ChatGPT 新功能全解析與本週 AI 新聞
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-04-03
source: https://www.youtube.com/watch?v=GIPlnfHQcz0
---

## OpenAI 本週背景

- 完成 $122B 融資，估值達 $852B（史上最大 VC 單輪融資）
- 明確宣示目標：打造**統一 AI 超級 App**
- 收入結構：約 2/3 來自 ChatGPT 訂閱；Anthropic 則相反，主要來自 API 與開發者

## ChatGPT 新功能

### 位置分享
- 路徑：Settings → Data Controls → Location
- 啟用後可詢問「附近推薦咖啡廳」等地點相關問題
- 結果呈現：地圖 + 圖片 + 連結，視覺化程度提升
- 手機端可設定「僅 App 使用中允許存取位置」
- Gemini 早已有此功能，ChatGPT 本週跟進

### 長文本自動轉附件
- 超過 **5,000 字元**的貼上內容自動轉為 `.txt` 附件
- **關鍵差異**：附件 ≠ 直接文字
  - 直接文字：完整進入 context window，細節保留率 100%
  - 附件：中間有摘要步驟，可能遺失細節
- 若需完整細節：按「Show in text field」將附件內容轉回文字
- OpenAI 內部文件說明：附件設計是為了避免單筆輸入消耗整個 context window（降低公司 token 成本）

### Google Drive 整合簡化
- 原本 Google Docs、Sheets、Drive 各自獨立連接器，現整合為單一 **Google Drive** 連接器
- 若已連接舊版，建議重新進入 Settings → Apps 確認連線正常
- 作者提醒：這類連接器仍有資料摘要失真問題，可靠性有限

### 其他 ChatGPT 更新
- Apps 更新：Box、Notion、Linear、Dropbox 可升級至新版
- 行動端介面：全螢幕選單、滑動切換，歷史紀錄、GPTs、圖像生成入口更清晰
- **CarPlay 語音模式**：需 iOS 26.4+，可在車內與 ChatGPT 對話
- 購物介面大改版，視覺更佳，商品資料更新頻率提升
- Codex 新增 plugins（使用 Claude Code / OpenClaw 的人幾乎不會用到）

## Google 新發布

### Gemini 3.1 Flash Live
- 升級語音對話模式：比前代更快，支援 screen share 與相機輸入
- context window 更大，可記憶更長對話
- 實測：打斷回應靈敏，多模態辨識（辨識錄影環境）表現良好

### Gemma 4 開源模型系列
- 31B 模型 benchmark 接近 DeepSeek 3.2，幾乎達到 Qwen 水準
- 最大亮點：可在高規格 MacBook（M5 Max 128GB）本地執行
- 開源可用，適合 OpenClaw Mac mini 用戶

## 其他快報

- **Suno 5.5**：聚焦個人化與用戶控制，品質進步空間有限（前版本已達高水準）
- **Google Lyria**：可生成最長 3 分鐘音樂，整合進 Gemini 直接生成
- **Claude Code 電腦操控功能**：可點擊電腦按鈕，作者評估目前仍不穩定
- **Claude Mythos 洩漏**：當時（影片錄製時）尚不確定真假
- **Claude Tools 手機版**：實測可靠性差，40% 機率遺漏或做錯，不推薦
- **Microsoft Copilot** 新增 Council & Critique 機制：兩個 AI agent 分別負責深度探索與驗證，形成反饋迴圈
