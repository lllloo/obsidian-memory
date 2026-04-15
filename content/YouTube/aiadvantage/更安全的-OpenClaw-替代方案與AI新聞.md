---
title: 更安全的 OpenClaw 替代方案與 AI 新聞
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-20
source: https://www.youtube.com/watch?v=ILMQu9NGQEI
---

## 本週主題：誰在打造消費者版 OpenClaw

各大公司與新創都在嘗試建造自己的 OpenClaw 版本，本集整理各方進展與比較。

### 什麼是 OpenClaw（複習）

OpenClaw 不只是工作助手，而是真正幫你「做事」的個人 agent，能存取整個作業系統、排程任務、自動執行工作。缺點：需要專屬機器（許多人用 Mac Mini）長期開機運行。

## Claude Cowork 的兩大更新

Cowork 之前缺少的兩個關鍵功能已補齊：

**1. 排程任務**（數週前加入）
- Schedule 標籤頁可設定重複任務
- 完成一件事後即可自動化，不需再次手動執行

**2. Dispatch — 手機遠端控制**（本週新增）
- Anthropic 稱之為 "Dispatch"
- 手機像對講機一樣控制電腦上的 Cowork
- 掃描 QR code 配對手機 app，更新桌面版與手機版後即可使用
- 需開啟「保持電腦不休眠」選項並授予資料夾存取權

### Dispatch 實測

- 從手機送出指令「Organize my desktop」
- Cowork 制定計畫並執行，在電腦上自動整理了桌面
- 介面美觀，有進度條與任務狀態顯示

### 安全建議

- 授予檔案存取前先備份
- 可限縮 Cowork 只能存取指定資料夾
- 使用久了容易對 AI 動作失去警覺，需保持習慣性確認

## 競爭產品比較

| 產品 | 運行方式 | 特點 |
|------|----------|------|
| Claude Cowork | 需桌面 app | Anthropic 官方，較安全，完整功能 |
| Genspark Claw | 網頁版 | 不需安裝，但定位不明確 |
| Manus (My Computer) | 網頁版 | Perplexity 版的 OpenClaw |
| Perplexity 版 | 需桌面 app | 介面最精緻，視覺接近 Cowork |

作者觀點：連這些產品的開發者自己也搞不清楚真正的使用場景，Genspark 的示範影片顯示「排一個家庭電話、訂零食、撒彩帶、印博物館票」——過於零散。

## 後製補充（剪輯時加入）

- Claude Code 也新增了類似 Dispatch 的功能：可透過 Telegram 遠端控制
- **Google Stitch** 發布：整合多個設計工具的網站設計器，被稱為 "AI Figma"，Figma 股價在發布當天下跌

## Photoshop 新功能：3D 物件旋轉

- 可在三維軸上旋轉圖片中的物件，AI 即時生成被遮擋的那一面
- 流程：移除背景 → Transform Image → Rotate Object
- 目前僅限 **Photoshop Beta**，需要 Creative Cloud 訂閱
- 實測用貓咪圖片測試，效果驚艷但不完美，搭配 Harmonize 功能可調整色彩協調

## Sora 新功能：Reference 場景合成

- 可帶入多個物件生成新影片場景（競品如 VO3.1 早已有此功能）
- 與 VO3.1 直接比較：Sora 常遺漏物件，VO3.1 更可靠且整體品質更高
- 結論：如果要創作影片內容，VO 仍是首選

## Google Maps AI 整合

- 手機限定功能，目前僅限美國與印度
- 新增 AI 導航說明，解決複雜路口判斷問題
- 根據歷史搜尋記錄提供個人化餐廳與地點推薦
- 仍未正式推送給所有用戶

## AI Igor 替代主持實驗

- 作者因手術無法錄製，由 AI 替代主持上週節目
- 工具：ElevenLabs（聲音）+ HeyGen（頭像）
- 加入作者慣用詞彙清單大幅提升寫作風格相似度
- 有觀眾表示只聽音頻無法分辨差異，但看影片明顯看得出來
