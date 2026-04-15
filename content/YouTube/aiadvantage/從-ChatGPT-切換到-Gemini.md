---
title: 從 ChatGPT 切換到 Gemini
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-17
source: https://www.youtube.com/watch?v=aK3lAZ5hhm0
---

## 前提說明

無法做到完美一鍵遷移，但可以系統性地把核心 context 帶過去。以下分三個層級處理。

## 第一層：帳戶級 Context

### Custom Instructions 遷移

ChatGPT 有四個欄位（What would you like ChatGPT to know / How would you like ChatGPT to respond）。逐一複製貼到 Gemini：

1. 開啟 Gemini → Settings → **Instructions for Gemini**
2. 點 Add，貼入對應內容
3. 重複四次欄位的搬移

### Memories 遷移

1. 在 ChatGPT 點擊 Manage → 查看所有 memories
2. 先刪除不準確或過時的記憶
3. 遷移方式（二選一）：
   - **逐一貼入（推薦）**：每條獨立加入 Gemini Instructions，Gemini 會視為獨立資訊，而非一整塊
   - **全選複製一次貼入**：快但資訊會被當成一整塊處理，相關性較低

## 第二層：Projects 與 GPTs

Gemini 沒有等同於 ChatGPT Projects 的功能。替代方案是使用 **Gems**（Gemini 等同於 GPTs 的功能）。

### GPTs → Gems（直接對應）

介面幾乎相同，直接複製貼上：

| ChatGPT GPT | Gemini Gem |
|-------------|------------|
| Name | Name |
| Instructions | Instructions |
| Conversation starters | 在 Instructions 末尾加說明（效果近似） |
| Capabilities | Tools（可選：Music、Deep Research 等） |
| Knowledge files | Upload files 或連結 Google Doc |

Gems 的優勢：
- 可連結 **動態 Google Doc**（多人協作、自動更新）
- 可啟用 Music 生成、Deep Research 等 ChatGPT 沒有的工具

### Projects → Gems（有限度對應）

- 可行部分：將 project 的檔案下載後重新上傳至 gem 的 Knowledge tab；複製 project instructions 貼入 gem instructions
- **無法複製的部分**：對話群組功能，Gemini 沒有等同的 project folder 結構

## 第三層：既有對話記錄

完全自動匯入不可行，有以下選項：

**備份 ChatGPT 資料**
- 支援方案：Plus、Pro、Academic、Enterprise（Teams 不支援匯出）
- 操作：個人頭像 → Settings → Data Controls → **Export Data**
- 24 小時內收到所有資料的壓縮檔

**搬移特定對話**
- 找到重要對話，全選 → 複製
- 在 Gemini 貼入並加上提示：「This is context from a previous conversation」

## 長期建議：可攜式 Context 策略

與其依賴各平台的 memory 與 projects，作者建議：

- 把所有個人 context 存成 **Markdown 文件**
- 需要時直接上傳到任何平台（gem、project、chat）
- 不受平台遷移影響，任何時候都能快速載入 context
