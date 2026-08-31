---
title: ChatGPT Chrome 擴充功能到底有多強
description: 借用現有 Chrome Profile 的瀏覽器 Agent，與 Plugin、內建 Browser 的分工判準，加上發票報表與跨網站接力兩個實測
created: 2026-08-31
updated: 2026-08-31
source: https://www.youtube.com/watch?v=Mhq6IS2vSQM
published: 2026-08-26
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - workflow
  - automation
---

## 它是什麼、解決了什麼痛點

ChatGPT Chrome Extension 等於把 ChatGPT 搬進瀏覽器，讓它直接接手你在瀏覽器裡的工作。

過去讓 AI 操作瀏覽器的痛點：

- 每次開的是全新視窗，沒有登入資訊與 cookies，查後台或看文件就卡在登入畫面。
- 操作不穩定、權限動不動失效、畫面卡死。
- 一邊操作一邊搶走你的分頁與焦點，無法在背景做事。

擴充功能的解法是**直接借用現有的 Chrome Profile**：你平常已登入的公司管理後台、Gmail、Google Drive 都能直接進去讀取與操作，瀏覽器裡裝的其他擴充功能也能無縫共用。它會自己開新分頁、用 Tab Group 把同一任務的相關頁面整理起來，在背景跨分頁做事而不搶走眼前畫面。

作者的對比體感：先前用 Claude in Chrome 的體驗破碎（權限失效需重新登入、執行到一半卡住），改用 ChatGPT Chrome Extension 後速度與流暢度不在同一級別，是第一次覺得瀏覽器 Agent 穩定到可以處理真實工作。

## 三種入口怎麼選

| 入口 | 適用時機 | 特性 |
|---|---|---|
| 專屬 Plugin（如 GitHub、Slack） | 該 App 有官方 Plugin 時優先用 | 走官方 API、結構化資料，最快最穩、token 最省、最精準安全 |
| Chrome Extension | 沒有 Plugin 但有網頁版；需沿用現有登入身分、cookies、已開分頁 | 公司內部系統、小眾 Web SaaS 都適用 |
| ChatGPT App 內建 Browser | 本機開發測試、查公開網頁、想把任務隔離 | 雖可在設定裡匯入憑證與 Cookies，本質仍是獨立沙盒，不動到平常用的 Chrome |

適合交給 Chrome Extension 的兩大類工作：

1. **根本不會有 Plugin 的網頁 App**——預約系統、記帳網站、公司內部管理後台。作者提到一位客戶的內部後台工具很慢，過去要拜託內部工程師開發 API 才能串自動化，現在擴充功能可直接繞過這段溝通自行自動化。
2. **需要跨網頁、跨 Web App 接力的繁複工作**——例如收到訊息要查訂單進度，得同時開內部 CRM 查資料、開 Google Calendar 確認排程、再把整理好的回覆貼回通訊軟體。

## 安裝與啟動

1. 打開 ChatGPT 桌面版，左側選單進 Plugins，找到 Chrome 並安裝（讓 ChatGPT 具備與 Chrome 溝通的能力）。
2. 點設定流程裡的連結跳轉到 Chrome Web Store，點「加到 Chrome」安裝官方 Extension 並同意權限。
3. 確認瀏覽器右上角出現擴充功能圖示，點開確認側邊欄能正常載入。

**多 Profile 注意事項**：如果 Chrome 裡有個人用、公司用、測試用等多個 Profile，務必確認 Extension 裝在要執行任務的那個 Profile 底下——它只看得到該 Profile 底下的瀏覽器視窗。

兩個下指令的入口：

- 在 ChatGPT 開新對話，用白話文叫它啟用 Chrome 插件，或在指令前加 `@Chrome` 強制呼叫。
- 直接在瀏覽器側邊欄打開插件，把需求與檔案丟進去。

## 實測一：八張發票變 Google Sheets 報表

Prompt 只給了一句話等級的需求：附檔是本月的 8 張發票，把發票資訊整理到 Google Sheets 上，讓它變成排版專業、好閱讀好理解的報表，方便後續分析與請會計處理。刻意不給詳細規格，是為了測模型對「一份好報表」的定義。

結果：它逐一讀取八張發票 PDF 匯入資料，並自動建了三張 Sheet——發票明細（日期、廠商、金額、品項）、品項明細、分析摘要（各類別支出佔比與加總），連該有的計算公式都自己寫好，排版與配色也堪用。

作者強調的重點不是「AI 會建報表」（用 Claude Code 或 Google Sheets Plugin 也做得到），而是**網頁介面操作能力**：選取範圍、設定格式、調整欄寬的滑鼠操作速度快到不是人類手動可及，且該段影片未加速。相較一年前類似 Perplexity 的 Browser 或 OpenAI 先前的 AI 原生 Browser Atlas，已不是同一級別。

## 實測二：跨網站接力規劃 Team Building

任務：規劃一場位於台北大安站附近、十人的室內 Team Building 活動，需跨越多個網站與 Web App 連續接力。

它的實際動作：

- 在瀏覽器建了名為「規劃台北團隊活動」的 Tab Group，開啟不同店家網頁與 Google Maps 分頁。
- 比對十人包場費用，同時在 Google Maps 實測從大安站走過去的步行時間。
- 切換到 Google Docs 開新文件，整理活動類型、費用、步行時間與優缺點分析。
- 接力切到 Google Calendar，點進指定日期下午時段建立暫定活動，把推薦店家地址與詳細時間表放進說明欄。
- 打開 WhatsApp Web，把活動時間、地點與流程通知打進對話框，停在等待審核送出的狀態。

整套流程約 20 分鐘。作者的觀察是：任務步驟再多它仍能遵從指令不偏掉，即使中間經過上下文壓縮，一開始輸入的指令與資訊也不會被弄丟。

## 兩個安全使用原則

因為它直接連進你日常在用的 Chrome，安全邊界要顧好：

1. **不可逆的操作一律停在最後一步**。任務涉及寄信、發布社群貼文、刪除資料、付款時，在 Prompt 明確寫上「停在確認畫面、不要送出」，把核准權留在自己手上，不要把決策完全交給自動化。
2. **處理敏感任務時使用獨立的 Chrome Profile**。切到乾淨的工作 Profile，避免私人分頁、瀏覽紀錄、通訊軟體的聊天名稱或敏感通知被 AI 當成背景 context 讀取，甚至意外出現在任務畫面裡。

## 結論

從操作速度、穩定度到跨分頁協調能力，OpenAI 的方向已經明確：把 ChatGPT 從幫工程師寫 code 的工具或一般問答 AI，升級成能幫所有人操作數位工作環境的通用 Agent，而 Chrome Extension 是這塊拼圖的重要一環。工作中若有大量開新分頁查資料、複製貼上、填寫網頁表單的雜事，適合裝來試。
