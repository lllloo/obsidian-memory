---
title: Claude Code 搭配 Nano Banana 製作動態網站
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-16
source: https://www.youtube.com/watch?v=jQxHo9PC19Q
parent: "[[01.index]]"
---

## 核心概念

在網頁 hero section 加入動態影片背景，是對抗 AI slop 外觀的高效武器。實作簡單但視覺效果遠超 99% 的 AI 生成網站。

## 完整工作流程

**步驟一：圖片生成（Nano Banana Pro）**

- 使用提示模板（可從 Chase AI 社群取得）
- 模板格式含：camera type、light description、atmosphere 等欄位
- 靈感來源：Pinterest、Dribbble、MidJourney（可作為風格參考圖）
- 先構思 landing page 整體構圖再生成圖片（避免圖片與頁面不協調）
- 通常需多次迭代

**步驟二：影片生成（Kling 或 VO）**

提示原則：
- 保持靜態，極慢且細膩的動態
- 範例：「keep it static and have extremely slow and subtle motion」

**影片長度選擇**：

| 方案 | 優點 | 缺點 |
|------|------|------|
| 15 秒長影片 | 創作空間大、實作簡單 | 結尾重置有輕微抖動 |
| 5 秒 + 循環 | 無縫循環 | 需用 ffmpeg 拼接，動態選擇受限 |

推薦：15 秒長影片。用戶通常不會在 hero 停留超過 5-10 秒就開始滾動，且實作更簡單。

設定注意：Always turn off **enhance**（保持對 prompt 的控制）。

**步驟三：Claude Code 實作**

1. 建立新目錄，把圖片和影片放入
2. 在該目錄開啟 Claude Code
3. 最基本提示：

```
Create a landing page for [用途].
Use the MP4 file in the folder to create an animated hero section.
Use the still image to replace the video for mobile users.
Use the front-end design tool.
Spin up a dev server when finished.
```

靜態圖給手機版：避免在手機載入完整影片。

**額外工具**：
- 前端設計 skill（front-end design tool）
- UIUX Pro Max skill（業界特定設計風格）
- 21st.dev：預建元件 + 對應 prompt，可直接複製貼入 Claude Code

**步驟四：部署**

1. 在 Claude Code 輸入：「Commit and push our code to this new repo」並貼入 GitHub repo URL
2. 前往 Vercel → Add New Project → Import GitHub repo → Deploy
3. 部署完成即可公開訪問（免費）

## 重點提醒

- 圖片和影片的生成都需要多次迭代，不要期望一次成功
- 設計目標是「wow factor」，不是壓倒觀看者——less is more
- 靜態圖片必須提供給手機用戶，不要讓手機載入影片
