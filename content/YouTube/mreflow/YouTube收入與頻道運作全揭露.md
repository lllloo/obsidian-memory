---
title: YouTube 收入與頻道運作全揭露
tags:
  - youtube
created: 2026-04-16
updated: 2026-04-16
published: 2026-04-15
source: https://www.youtube.com/watch?v=ncVQneK7FlE
---

## 片頭製作流程

Matt Wolfe 的標誌性 AI 動態片頭是這樣製作的：

- 在 Da Vinci Resolve 中從影片擷取兩張靜態畫面：一張「人物不在鏡頭內」、一張「人物就座後」
- 上傳至 **Leonardo**（他是顧問並持有少量股權），利用其整合多款影片生成模型的優勢
- 常用模型：**VO 3.1 Fast**、**Cling Video 3.0**、**Seed Dance 2.0**（透過 Runway ML）
- 提示詞範例：「一隻爪子從天花板降下，抓起角落的人，移動到椅子上放下」
- Cling 3.0 與 VO 3.1 會同時生成音效，通常直接沿用
- 若 Leonardo 跑不出滿意效果，備用方案是 **Runway ML**（使用 Seed Dance 2.0）

## 影片錄製與剪輯工作流程

**Live Editing（即時剪輯）**是 Matt 的核心方式，目標是錄製時就做好大部分編輯工作：

- 使用 **Stream Deck XL** 在錄製時即時切換鏡頭、場景、畫面布局、燈光
- 使用 **OBS** 錄製，多機位含主攝影機、螢幕分享、TopDown 鏡頭
- 原始錄影通常長達 1.5～2 小時

**後製剪輯流程：**

1. 用 **Recut** 自動偵測並移除靜默片段（1 小時 5 分鐘 → 約 26 分鐘）
2. 在 Recut 中以 2x 速度瀏覽，手動刪除口誤片段
3. 從 Recut 匯出 XML 檔，匯入 Da Vinci Resolve
4. 套用 **Greg's Presets**（付費 preset 包），使用自製縮放效果 highlight 螢幕文字

**AMA 問題展示系統**是用 Cursor vibe coding 出來的：

- 一個叫「Local AMA Control Room」的本地 app
- 截圖 YouTube 留言後拖入，可重新排序，搭配動畫 overlay 在錄製時逐題顯示

## 辦公室與硬體設備

- **主機**：Mac Studio（M3 Ultra）+ 自組 PC（Nvidia RTX 5090）+ **DGX Spark**（128GB VRAM，用來跑本地模型）
- **筆電**：MacBook M4 Pro（旅行用）
- **相機**：主攝影機 + 附 teleprompter 的第二機 + TopDown 攝影機
- **音訊**：Roadcaster Pro（多麥克風輸入）
- **控制**：Stream Deck XL 控制鏡頭切換、OBS 場景、燈光
- **其他收藏**：各世代電玩主機、Apple Vision Pro / Meta Quest Pro/3、3D 印表機、去役 Google TPU、原版 Gemma 模型權重（隨身碟）

## 自動化工作流程

**FutureTools 網站更新自動化（N8N）：**

1. 在 Google Spreadsheet 新增工具列
2. N8N 偵測到新列後啟動
3. 爬取工具官網內容 + 查詢 **Perplexity** 彙整資訊
4. 送入 AI 模型（主要：**GPT-4o mini**；fallback：**Gemini**，因 context window 較大）
5. 自動產生名稱、描述、分類、付費/免費標記、短網址
6. 同步更新 Spreadsheet、Webflow（舊站）、Supabase + Vercel（新站）

**AI 新聞資料庫自動化（make.com）：**

- 使用 **Raindrop** 收藏新聞，依存入的集合類別觸發不同 make.com 流程
- 流程：擷取文章 → ChatGPT 寫摘要 → 更新 Obsidian dashboard → 儲存至 Supabase
- 支援 tag 路由：不同 tag 會觸發額外資訊補充步驟

**其他常用工具：**

- **Cursor**：日常開發主力，用來 vibe code 各種內部小工具
- 用 Cursor 建了「Comment Grabber」Python 腳本，掃描過去 6 週 YouTube 留言，篩出問題並匯出 CSV

## YouTube 收入與頻道策略

**AdSense 收入（近 100 萬訂閱）：**

- 近 28 天：約 **$6,000～7,000 美元**
- 2024 年是最佳年份，AdSense 表現明顯高於其他年份
- 2023 年約 $170,000（全年）
- 品牌合作收入高於 AdSense，但具體數字未公開

**頻道策略：**

- 定位為「每週五一支影片」——整理一週 AI 重點，讓觀眾只看一支就掌握全局
- 刻意減少發影片頻率，接受觀看次數下降，換取品質與可持續性
- 曾考慮多語言配音（接觸 Ditto 與 ElevenLabs），正在推進

## AI 產業觀點

**AI 會殺死創作者嗎？**

- Matt 認為不會，人們仍然想看真實人類的觀點與評論
- AI 生成的「無臉頻道」雖然存在，但背後仍需大量測試與故事敘事的投入
- Gen Alpha 目前可能接受低品質 AI 內容，但隨年紀增長偏好會改變

**ChatGPT vs Anthropic：**

- ChatGPT 仍是消費端主導品牌（如 Kleenex 之於面紙），一般用戶不太會離開
- Anthropic 的策略優勢：深度聚焦寫程式能力，程式能力提升後帶動其他所有能力
- OpenAI 近期也意識到這一點，開始同樣押注在程式/工具使用能力上

**如何追蹤 AI 資訊：**

- 每天早上用 **Feedly** 瀏覽 200～400 則訂閱（Google、Meta、Nvidia、Anthropic、11 Labs 等官方 Blog + The Verge、TechCrunch 等媒體 + 多份 AI Newsletter）
- 在 X 上維護公開清單「AI is awesome」，每日瀏覽
- 值得分享的內容手動存入 Raindrop → 自動化儲存至 futuretools.io/news
