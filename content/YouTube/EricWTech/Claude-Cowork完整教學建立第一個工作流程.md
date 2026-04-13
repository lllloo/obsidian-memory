---
title: "Claude Cowork 完整教學：如何建立你的第一個工作流程"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-27
source: https://youtu.be/3FCYpGz7ptM
---

**影片描述**：完整示範如何使用 Claude Cowork 自動化日常工作，涵蓋三種 Claude 工具的差異比較、專案設定、工作流程建立、Skill 轉換，以及 Connectors、排程任務和記憶功能的探索。

**重點摘要：**
- **三種 Claude 工具差異**：Claude Chat 是即時對話研究工具（可安裝瀏覽器擴充控制瀏覽器）；Claude Code 是 CLI 開發工具，專注建立應用程式；Claude Cowork 則整合了檔案修改、深度研究、瀏覽器操作、SMTP 連接、Skills 等所有功能，在 Claude 桌面應用程式的 UI 中運行，不需終端機。
- **專案設定**：點選 Cowork 頁籤後建立 Project，可從零開始、匯入現有 Claude Chat 專案，或選擇本機資料夾；可設定系統層級的 Instructions（類似 system prompt）。
- **Connectors**：透過 Plus 按鈕安裝連接器（如 Gmail、Google Calendar、PDF Viewer），可依熱門度排序篩選；已連接的服務讓 Claude 可直接操作對應資料。
- **實際示範：642 張收據轉 CSV**：作者用語音輸入描述需求（擷取 vendor、幣別、金額、稅額、類別、日期、付款方式），Claude 先提問確認（批次大小、輸出格式、業務類別標準、OCR 失敗處理策略）再執行，進行中右側顯示 to-do 進度，最終輸出含所有欄位的 CSV，包括 needs_review 標記與原因。
- **Skill 封裝**：示範將「收據轉 CSV」工作流程儲存為可重複呼叫的 Skill，方便日後一鍵觸發，不需重新描述流程；Skill 可跨 project 引用。
- **Plugins**：Cowork 提供擴充 plugin 生態系，作者示範安裝與確認已安裝 plugin 的方式。
- **排程任務與記憶**：支援定時自動執行工作流程（Scheduled Tasks）及跨 session 儲存使用者偏好或背景資訊（Memories）。
- **OCR 準確率限制**：示範中部分收據日期未被正確識別，作者趁機介紹自家產品 BookZero.ai，該平台使用專門針對收據微調的 OCR 模型，準確率更高。
