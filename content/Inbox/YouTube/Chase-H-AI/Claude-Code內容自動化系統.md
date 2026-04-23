---
title: Claude Code 內容自動化系統：一人團隊創造千萬次觀看
created: 2026-04-15
updated: 2026-04-15
source: https://www.youtube.com/watch?v=7q_rbT1a9dE
published: 2026-03-30
parent: "[[01.index]]"
tags:
  - youtube
---

## 內容創作四大階段

整個系統圍繞四個階段：**研究 → 構思 → 腳本 → 分發**，每個階段都有對應的 Claude Code 技能。

30 天內 90 部影片（30 長片 + 60 短片）全由一人完成，未出現單篇超過 40 萬觀看的爆款，靠的是持續穩定的小贏。

## 知識源頭（步驟零）

在進入技能流程前，需要先確定「創意從哪裡來」：

- **Twitter 抓取 Web App**：每 30~45 分鐘從特定作者與關鍵字抓取 40~90 則推文，根據 velocity、authority、timing、opportunity、replyability 評分，透過 Softmax 概率挑選，推送至 Telegram，所有歷史記錄存 Supabase 去重
- **GitHub 趨勢腳本**：每天早上自動抓取 AI 類過去七天新建的 Top 10 trending repos，包含星數、語言、連結、說明，存入 Obsidian vault；附上當月 Top 5 與每日建議

## 研究技能：YouTube Pipeline

確定主題後，使用 YT pipeline 技能，它會：
- 取得相關 YouTube URLs
- 調用 NotebookLM-PY CLI 工具將內容送至 Notebook LM（跑在 Google 伺服器，不消耗自己的 tokens）
- 自動取回 Notebook LM 分析結果與各類輸出物（podcast、slide、影片等）

Pipeline 技能是「高階技能」，會呼叫其他技能。所有輸出存在 Obsidian vault 中，方便查閱關聯文章。

## 構思技能：Ideation

接收已完成的研究後，Ideation 技能會輸出：
- 競爭格局（飽和角度、開放缺口、表現異常的影片）
- 9 個以上的影片方向（標題、角度、目標慾望、格式、競爭缺口）
- 以排名呈現建議

**核心原則**：Claude Code 是協作者，不是自動執行者。每個階段都要人工介入確認，否則輸出會很通用且糟糕。

## 腳本技能

三個技能組合：

- **Hook 技能**：每個 Hook 拆分為口語 Hook、視覺 Hook、文字覆蓋（短影片用），提供 5 個變體
- **Outline 技能**：輸出目標長度、相關 Obsidian 文件、各章節重點與視覺輔助建議
- **YouTube Title 技能**：對比歷史表現最佳標題，分 Tier 1（穩健）和 Tier 2（冒險性），附上縮圖文字選項

## 分發技能

- **Content Cascade**：YouTube 影片 → 自動抓取 transcript → Blog（自動發布到網站）→ Twitter thread（7 個回覆）→ LinkedIn 草稿；Blog 附嵌入影片，具 SEO 優化，採用作者本人寫作風格訓練
- **Short Form 技能**：從長片濃縮 Hook、腳本、字幕，輸出 30/60/90 秒格式

一部 YouTube 影片可覆蓋 6 個平台（YouTube、Blog、Twitter、LinkedIn、Shorts/Reels/TikTok）。
