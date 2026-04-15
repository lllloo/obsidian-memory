---
title: Claude Cowork 完整介紹與測試
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-14
source: https://www.youtube.com/watch?v=BWAr7gTkll8
---

## 什麼是 Claude Cowork

Anthropic（Claude 的製造商）發布了一個研究預覽版產品，名為 Claude Co-work，可能是目前最接近消費者級 AGI 體驗的產品。這是一個 agentic AI 系統，設計目標是替你「做事」——移動檔案、連接服務——盡量減少你的介入。

它可以視為 Claude Code 的非開發者版本：
- Claude Code：為開發者設計，可寫程式、建立檔案、推送 GitHub、部署網站
- Claude Co-work：為一般用戶設計的 agentic 助手

背景：Claude Code 推出後，用戶開始將其用於非開發用途（行銷計畫、產品構思、Instagram 活動等），Manus、GenSpark 等新創也以此為靈感推出類似工具。Co-work 是 Anthropic 自己建造的消費者版答案。

**當前限制**：僅限 Max 方案（$100/月）、僅 Mac desktop app，研究預覽版。

## 可用的 Connectors

以下三種效果最好：
- **本地檔案系統**：直接處理電腦上的本地檔案
- **Brave Search**：網路搜尋
- **Claude for Chrome 擴充功能**：遠端控制瀏覽器

外部 connectors（Gmail、Google Calendar 等）在此版本仍不穩定，與之前相同。

## 實測：整理桌面

**流程**：
1. 輸入「幫我整理桌面上的所有檔案」
2. 選擇桌面資料夾並允許存取
3. 系統先詢問偏好（依專案主題、截圖不刪除移到截圖資料夾、合併舊存檔資料夾）
4. 不需再次提示，自動建立新資料夾結構並執行整理

**結果**：截圖資料夾、壁紙、書籍相關資料、大型存檔資料夾，全部整齊分類。後續追加「也整理存檔資料夾」同樣成功。

## 實測：Gmail 重點摘要

同步啟動第二項任務：「開啟我的 Gmail 並告訴我過去 24 小時最重要的 3 封郵件」

結果：成功開啟 Gmail、讀取收件匣並回報重點。比使用獨立瀏覽器擴充更直觀——所有任務集中在 Co-work 一個介面內。

## 最後一步：視覺化檔案結構

將整理完的桌面結構生成樹狀圖 Web App（Artifact），清楚呈現整個資料夾架構。

## 意義與展望

這個研究預覽版在 10 天內建成，仍有明顯缺陷，但代表 AI 的發展方向：
- 大型公司都會朝這個方向推進
- 小型公司最終必須在特定利基深化
- ChatGPT 版本的類似產品只是時間問題

連接器目前尚不穩定，但這不會是永久狀態。
