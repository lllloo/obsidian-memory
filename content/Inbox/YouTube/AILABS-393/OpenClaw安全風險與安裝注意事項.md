---
title: 安裝 OpenClaw 前必須了解的安全風險
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-04
source: https://www.youtube.com/watch?v=M3P0hQMQtq0
parent: "[[01.index]]"
---

## OpenClaw 是什麼

OpenClaw（原名 Clawdbot，後改為 MoltBot，最終在 3 天內完成重新命名成為 OpenClaw）是一個自架的 AI 助理，成為史上成長最快的開源專案之一。

重要澄清：**開源不等於免費，自架不等於安全。**

安裝過程：依照官方文件的步驟操作可以完成安裝，但 channel 整合有問題——WhatsApp 因 408 錯誤頻繁斷線，透過 Discord 連接則穩定許多。

## 費用問題

OpenClaw 支援眾多模型（包括 OpenRouter），應用程式本身免費，但真正的費用是 **token 消耗**：

- OpenClaw 不只依賴 system prompt，還有內建記憶、推理以及 skills、channels 等整合
- 每次查詢都會傳送大量資訊
- 一個每天執行的簡單 cron job 可能一個月花費約 **128 美元**
- 即使切換到較小的模型，費用也不會大幅降低——問題在於架構設計，而非模型本身

**造成費用攀升的主因：**
- Heartbeat 定期檢查伺服器狀態並執行任務
- 所有對話歷史隨每次查詢一起傳送（用於保持 context），這自然燒掉大量 token
- 對話越長，回應時間越慢（從 session 初始的 2-12 秒增加到 context 累積後的 119 秒）

**建議：**
- 設定 API 費用監控和警報，建立適當的用量預算
- 將 heartbeat 間隔增加到 2 小時以上
- 睡眠前清除 session
- 若本地執行，可用 Ollama 本地模型降低費用，但需要足夠的運算能力

## 安全性問題

Cisco 公開稱 OpenClaw 為「安全夢魘」，其安全政策本身也有嚴重缺陷：

**憑證儲存問題：**
- 所有憑證和 session 以**明文 JSON 檔案**儲存，包含裝置資訊和身份資料
- 任何有系統存取權的人都能讀取
- OpenClaw 能執行 shell 指令、存取磁碟檔案、在機器上執行 scripts——給 AI 這種權限風險極高

**Skills 安全問題：**
- ClawHub 上的社群 skills 公開提供，Cisco 用開源掃描工具掃描後發現：
  - 僅一個 skill 就有 9 個安全問題（2 個嚴重、5 個高危）
  - 該 skill 功能上等同惡意程式，明確指示 bot 執行 curl 指令，將資料傳送給 skill 作者控制的外部伺服器

**Prompt Injection：**
- OpenClaw 的安全政策明確將注入攻擊列為「超出範圍」，不負責因此造成的資訊洩露

## 降低風險的建議

**選用有內建護欄的模型：**
- OpenAI 和 Anthropic 的模型有內建安全護欄，對明顯攻擊有一定防護
- 即便如此，仍可能被精心設計的注入攻擊繞過

**Skills 管理：**
- 只安裝絕對必要的 skills
- 涉及密碼或敏感系統且非必要的 skills 應阻止安裝
- 從社群安裝前先執行（現已開源的）掃描工具，或只安裝社群已驗證的 skills

**系統存取最小化：**
- 在不含敏感資料的獨立帳號中使用
- **最佳做法：用 Docker 沙箱化**——Docker 容器互相隔離，限制跨容器的系統資源存取
- 或建立只含 OpenClaw 設置的虛擬機
- 不再使用的整合（如 Discord）應重置 token 撤銷 OpenClaw 的存取
