---
title: Vibe Coding 入門：用 AI 建立應用程式
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-19
source: https://www.youtube.com/watch?v=7HErPVFNO0Q
---

## 什麼是 Vibe Coding

- 使用自然語言建立真實 app，不需傳統程式碼知識
- 目前是 AI 領域最熱門的趨勢之一，作者有近一半的 AI 使用時間在 vibe coding

## 使用平台：Base 44

- 目前最易用且功能完整的 vibe coding 平台之一
- 定價從 $16/月起，進階功能（身分驗證、後端函式、自訂 domain）需升級方案

## 建立流程

### 1. 撰寫初始 Prompt

- 可開啟「Planning 模式」讓 AI 先生成詳細計畫再執行
- 可上傳截圖作為 UI 參考（模仿顏色、版面、風格）
- 若不確定如何描述，用 ChatGPT 或 Gemini 幫你生成 vibe coding prompt

**示範 Prompt：**
「建立一個內部創作者管理系統，用來管理整個 YouTube 內容流程。使用者可以登入，可以建立影片想法、腳本，並透過完整工作流程從構想到發布。」

### 2. 查看 AI 計畫

- AI 會根據 prompt 擴充功能細節：儀表板設計、使用者流程、各模組元件
- 全程不需看程式碼

### 3. 疊代修改（Refinement）

**技巧：每次只修改一件事，避免多個大改動同時發送**

範例修改 prompt：
- 「把選單移到左側，變成傳統 dashboard 版面」
- 「切換為深色模式」
- 「把 Pipeline 頁面改成可拖動的卡片」

### 4. 以使用者身份測試

- 點擊「Act as a User」模式進行測試
- 發現功能問題後，用 prompt 修正

## Base 44 進階功能

- **Visual Editor**：點擊頁面上任何元素即可直接修改文字或顏色，不需輸入 prompt
- **Discuss 模式**：純聊天詢問 AI，不執行任何修改
- **Suggestions（建議）**：AI 自動提出功能改進建議（如「加入 AI 功能讓使用者輸入大綱主題後自動生成」）
- **模型選擇**：預設自動選最佳模型；付費方案可手動選 Claude Opus、Gemini、GPT-5 等

## Dashboard 管理功能

- **Users**：查看所有使用者、管理角色（admin / 一般使用者）、傳送邀請
- **Security Check**：發布前執行安全檢查，確保 API 金鑰等敏感資料不外洩
- **Analytics**：發布後查看流量、使用者來源國家、各頁面瀏覽量、銷售概覽
- **Code 頁面**：所有程式碼均可查看，可交給開發者進一步修改

## 發布流程

1. 確認功能完整後按「Publish」
2. 自動生成公開連結（非自訂網址）
3. 想要自訂網址：購買 domain 並連接

## 積分制度

- 每次與 AI 對話（初次生成、後續修改）均消耗積分
- 各方案有每日補充積分；需要更多積分可升級或購買

## 為何值得使用 Vibe Coding

- 可完全按自己需求訂製工具，不受限於現成 SaaS 產品
- 不需要等待外部廠商加入你需要的功能
- 適合解決特定業務問題的內部工具
