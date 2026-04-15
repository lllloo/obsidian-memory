---
title: Google AI 霸主佈局與本週 AI 新聞
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-04-10
source: https://www.youtube.com/watch?v=NOqh_Jk7ZQQ
---

## Anthropic 相關動態

- **Claude Mythos**：Anthropic 旗艦模型，尚未發布但 benchmark 極為亮眼，作者認為會延續 Claude 一貫高水準
- Anthropic 取消讓 Claude 訂閱者透過 OAuth 使用 OpenClaw 的能力，原本 $200/月方案現在需要 $1,000–$3,000/月 API 費用
- **Claude Code 原始碼洩漏**（非 April Fool's joke）：
  - 洩漏後社群發現 Claude Code 內建「dreaming function」，每天將當天經驗存入文字檔，下次喚起時讀取，實現跨 session 記憶
  - OpenClaw 數天內跟進，推出相同的 dreaming 記憶機制

## Google 新發布

- **Gmail AI Inbox**：僅限 $250 Ultra 方案美國用戶，自動達到 inbox zero，重點在郵件優先排序與每日個人化摘要（非自動回覆）
- **Google Vids 更新**：整合 AI 影片生成、音樂生成、AI Avatar；支援自訂 avatar、投影片加旁白與背景音樂，流程最低摩擦
- **Runway Characters**：互動式 AI avatar，免費方案可體驗，目前仍在 beta
- **Sea Dance 2.0**：視覻生成模型，現已上線主流平台，鏡頭運動表現優異，位居 AI 影片排行榜前段

## LLM Wiki 概念（Andre Karpathy）

- Karpathy 分享用 LLM 建立個人研究知識庫的方式：把各主題存成純文字檔，讓 agent 搜尋
- 部分測試顯示比 RAG 流程效率高 70 倍（尚未完全驗證）
- 區別：RAG 將資料存入向量資料庫再檢索；LLM Wiki 直接讓 agent 存取全部文字檔
- 作者本人用 Obsidian + OpenClaw 建立個人工作 wiki，讓 agent 以此為 context 協作

## 開源模型動態

- **GLM 5.1**（中國）：754B 參數，coding benchmark 接近 Opus 4.6，支援長達 8 小時 agentic 任務，Apache 2.0 授權完全開源
- **Gamma 4**（Google 開源）：體積小到可在部分手機執行，與 GLM 5.1 形成大小兩極

## 其他快報

- **Suno 5.5**：音樂品質更佳，頻道已開始使用 AI 生成片尾 jingle
- **Microsoft MAI**：首次推出自家模型（轉錄、語音、圖像），直接與 OpenAI 競爭；Claude 雲端連接器新增 Microsoft 365 支援
