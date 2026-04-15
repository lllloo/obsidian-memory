---
title: 用 Claude Code 43 個行銷 Skills 打造 SaaS 產品行銷系統
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-21
source: https://www.youtube.com/watch?v=qt4xzTLY1BQ
---

## 系統概覽

43 個行銷 Skills，作者用此系統讓 BookZero.ai 從 0 成長到前 1000 個用戶。核心流程分為 8 個必要步驟 + 5 條進階路徑。

## Step 1：Product Marketing Context 設定

所有後續 skills 的資料來源，相當於行銷系統的 CLAUDE.md。

**執行方式**：`/marketing-context-setup`（掃描整個 codebase：landing page、README、文件）

**輸出**：包含 12 個章節的 MD 檔案——產品概覽、目標受眾、競爭環境等。

建立後，Claude 會提問確認準確性（如：testimonial 是真實還是示範用？anti-persona 是誰？）並透過 Supabase MCP 查詢實際數據補充。

## Step 2：Analytics & GA4 追蹤

**目的**：在優化前建立衡量基準，避免盲目優化。

**技能執行**：`/marketing-analytics-tracking`，讀取 marketing context，分析現有 GA4 缺口。

**實際實作**：
- UTM 追蹤（Google、Facebook、YouTube 等廣告來源）
- GA4 purchase/conversion events
- Admin 行銷儀表板（Supabase 用戶數據 + GA4 流量來源、轉換漏斗、頁面瀏覽、內容表現）
- 時間範圍切換：7 天 / 30 天 / 90 天

## Step 3：SEO 稽核與競品分析

**技能執行**：`/marketing-seo-audit [domain] [semrush-data-folder]`

**輸出重點**：
- 整體評分（7/10）
- 優先修正：H1 標籤、meta tags、untapped keywords（2100 個未開發關鍵字）
- 競品關鍵字差距分析
- 行動計劃：技術修正 → 效能優化 → 外部連結（Product Hunt、Hacker News）→ 訪客投稿 → 內容創作

**PageSpeed 結果**：搭配 web vitals skill 後，SEO 達 100 分。

## Step 4：Landing Page CRO

**技能執行**：指定流量來源和轉換目標

**優化原則**：前三個 section 最關鍵——減少文字、縮短訊息、清楚 CTA。

BookZero 案例：三步驟流程（Upload → Import → Match）整合為單一 section，hero section 去除冗餘說明，突顯時間節省價值（每年省 126 小時 → 每月只需 5 分鐘）。

## Step 5：Web Vitals & LCP 優化

**技能執行**：`/marketing-web-vitals [url]`

**流程**：Lighthouse 稽核（同時跑 mobile + desktop）→ 識別 LCP bottleneck → 確認修正計劃 → 實作 → 重新測試（迴圈直到達標）。

**實際結果**：
- Mobile: 73 → 97
- Desktop: 64 → 99

修正後的最佳實踐寫入 CLAUDE.md performance 章節，之後新開發的 component 會自動遵循。

## Step 6：Signup-to-Activation CRO

**目的**：減少從註冊到真正使用產品的摩擦。

**稽核發現的問題**：
- 空白 table 沒有引導（→ 改為有 CTA 的教學空狀態）
- 缺乏「Aha Moment」慶祝回饋
- 信件 nurture 不夠個人化
- 缺乏 onboarding nudge 引導下一步

**實際改動**：
- 登入頁：左邊加 testimonial，右邊簡化表單
- dashboard：三步驟進度引導（Capture Receipts → Import Statements → Match）
- 追蹤：onboarding nudge 點擊率、activation 完成率（簽名 → 完成設定 → 第一筆對帳）

## Step 7：AI SEO（GEO - Generative Engine Optimization）

**目的**：讓 ChatGPT、Gemini、Perplexity 在用戶詢問相關問題時引用你的產品。

**執行**：提供競品資料（SEMrush/Ahrefs）→ 分析 AI 可見度缺口

**發現缺口**：AI 無法從頁面提取定價、功能、評分 → 需要 Schema markup。

**三階段修正**：
1. Schema 技術修正（讓 AI 能提取結構化資料）
2. FAQ 章節 + 新部落格（針對缺少的關鍵字）
3. 圖片 SEO 優化

**評估方式**：手動查詢「best bookkeeping software in Canada」檢查是否被 ChatGPT/Perplexity/Google 引用（需 2-3 週後追蹤）。

## Step 8：內容策略與 Blog 生成

利用競品資料識別內容缺口 → 用 SEO content writer skill + Nano Banana 2（圖片生成）自動產出包含標題、SEO 關鍵字、重點摘要、配圖的部落格文章。

## 5 條進階路徑

| 問題情境 | 對應路徑 | 包含 Skills 數 |
|---------|---------|--------------|
| 沒人找到你 | 內容 & SEO（關鍵字研究、技術 SEO、Schema） | 11 |
| 訪客沒轉換 | 轉換優化（理解→優化→捕獲 phases） | — |
| 想拓展規模 | 成長（付費廣告、病毒傳播、有機社群） | — |
| 用戶流失 | 留存率提升 | — |
| 想募資 | YC checklist + 募資 recipe | — |

全部 43 個 skills 和完整 playbook 在 School community 提供下載。
