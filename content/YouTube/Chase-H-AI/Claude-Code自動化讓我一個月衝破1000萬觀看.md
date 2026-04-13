---
title: 這些 Claude Code 自動化讓我一個月內衝破 1000 萬觀看
tags:
  - youtube
  - claude-code
  - content-creation
  - automation
  - obsidian
created: 2026-04-12
updated: 2026-04-12
published: 2026-03-30
source: https://youtu.be/7q_rbT1a9dE
---

一人團隊在 30 天內用 Claude Code 內容系統產出 90 支影片（30 部長片 + 60 部短片），累積 1,000 萬觀看，無編輯、無助理。

## 內容製作四階段

### 1. Research（研究）
**YouTube Pipeline Skill**：透過 Notebook LM API CLI 工具，將 YouTube URL 送至 Notebook LM（Gemini）分析，不消耗 Claude Code tokens。

**靈感來源（Knowledge Fountainhead）：**
- **Twitter 研究引擎**：每 30-45 分鐘抓取 40-90 則推文，依 velocity/authority/timing/opportunity/replyability 評分，透過 Softmax 隨機化，推送至 Telegram
- **GitHub 趨勢腳本**：每日晨間推送過去 7 天新建的 AI 類 Top 10 trending repos 至 Obsidian vault

### 2. Ideation（構思）
**Ideation Skill**：分析競爭格局、找出市場缺口、提供影片構想（含角度、desire mapping、排名）。關鍵：AI 輔助分析，人類做最終決策。

### 3. Scripting（腳本）
三個 skills：
- **Hook Skill**：產生 5 種 hook 變體（含 spoken/visual/text overlay）
- **Outline Skill**：大綱、章節重點、視覺輔助建議、參考資料
- **YouTube Title Skill**：參考既有表現佳的標題，分 Tier 1（穩健）/ Tier 2（計算性冒險）

所有輸出儲存至 Obsidian vault，方便交叉參照。

### 4. Distribution（發佈）
**Content Cascade Skill**：YouTube 影片 → 自動產生 Blog（SEO 優化）+ Twitter 串 + LinkedIn post

**Short Form Skill**：將長片濃縮為 30/60/90 秒短片腳本

一部 YouTube 影片 → 6 個平台內容（YouTube、Blog、Twitter、LinkedIn、Shorts/Reels/TikTok）

## 關鍵原則

- Claude Code 是**協作者**，不是自動輸出機器
- 每個階段都要人工確認，才能維持個人聲音
- 所有分析結果存於 Obsidian vault，方便人類追蹤
- 縮圖純手工製作（AI 在純視覺創意上仍不夠好）
