---
title: Claude Code + Nano Banana = Beautiful Animated Websites
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/jQxHo9PC19Q
---

利用 AI 圖片生成 + 影片生成 + Claude Code 建立帶有動態背景 Hero Section 的網站，對抗千篇一律的 AI 生成設計。

## 完整工作流程

### Step 1：生成靜態圖片（Nano Banana Pro）
- 使用提示詞模板（分解為：相機類型、光線描述、氛圍等）
- 提供參考圖片（從 Pinterest / MidJourney 找靈感）
- 需多次迭代直到滿意
- 同時考慮網頁構圖（例如左側留空用於文字）

### Step 2：生成動態影片（Cling 3.0 / VO 3.1）
- 提示詞重點：**保持靜態，極慢的細微動作**
- 關閉 Enhance（保持對提示的控制）
- **影片長度選擇**：
  - 長版（15 秒）：創意空間大，簡單實作，主流做法
  - 短版（5 秒）+ 循環：需用 FFmpeg 複製反轉拼接，但受動作方向限制

### Step 3：Claude Code 生成網頁
最低限度的 Prompt：
```
建立 [用途] 的 landing page
使用資料夾中的 MP4 做動態 Hero Section
使用靜態圖片作為手機版替代（不載入影片）
使用 front-end design tool
```
- 可額外加入 UIUX Pro Max Skill 提升設計品質
- 提供喜歡的網站截圖作為參考，減少後續迭代
- 21st.dev：pre-built 元件 + prompt，可直接複製到 Claude Code

### Step 4：部署（GitHub + Vercel）
1. 在 GitHub 建立新 repo（可設 private）
2. Claude Code 內：commit 並 push 到 repo（首次需認證）
3. 前往 Vercel，Import repo → Deploy
4. 部署完成即獲得公開 URL

## 關鍵技巧

- 動畫目的是「wow factor」，應克制：幾秒吸引注意後用戶就會滾動
- 動作過多反而顯得廉價，**less is more**
- 手機版用靜態圖片替代影片，避免效能問題
- FFmpeg 可讓 Claude Code 自動處理影片的複製、反轉、拼接
