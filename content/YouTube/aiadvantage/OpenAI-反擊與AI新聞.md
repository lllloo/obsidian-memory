---
title: OpenAI 反擊與本週 AI 新聞精選
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-06
source: https://www.youtube.com/watch?v=9FruIqE0OEw
---

## GPT-5.3

OpenAI 發布 GPT-5.3 Instant，定位為「更有人性」的版本。與前代 5.2 的差異不在於輸出「什麼」，而在於「怎麼回應」。

**實測對比**（問：我的 YouTube 直播間要不要養一隻戴帽子的貓？）：
- **5.2**：認真看待問題，列出戴帽注意事項，語氣嚴肅說教
- **5.3**：接住玩笑語氣，回應中夾帶幽默，說「貓會革命推翻你」——跟著問題的語調走

這是 OpenAI 有意識轉向「更易相處、少說教」模型的產品策略。5.3 Instant 已向所有方案開放，包含免費帳號。

## GPT-5.4

5.3 發布後不久，5.4 隨即跟上：
- Thinking 模型與 $200 Pro 方案升級至 5.4
- 多項 benchmark 達到 state-of-the-art，尤其在 Agentic 工具使用方面
- 最大亮點：**使用電腦的能力（Computer Use）**，且在此項上超過 Opus 4.6
- API context window 擴展至 **100 萬 token**，與 Opus 4.6 對齊

**注意**：Computer Use 類型的提升需要實際使用才能判斷，benchmark 參考性有限，需幾天後才能有完整評價。

## ChatGPT Projects 新增 Google Drive 資料夾支援

這是比模型更新更實用的功能。原本 Projects 只能逐一上傳檔案；現在可以：

1. 在 Google Drive 建立一個資料夾
2. 將資料夾連結貼入 Projects 的 Sources
3. ChatGPT 自動取用資料夾內的所有內容，並動態同步

**建議用法**：建立一個 Markdown 檔案放入此資料夾，寫入所有關於自己與工作的深度脈絡。Markdown 格式是 AI 讀取效率最高的格式。多人團隊也可在同一個 Google Drive 資料夾協作更新，讓 ChatGPT 的 Project 持續獲得最新資訊。

## Claude Cowork 排程任務

Claude Cowork 新增**任務排程功能**，終於補上這個關鍵缺口。

**運作方式**：設定好一個工作流（如：每天爬取生成式 AI 最新消息）後，可以排定執行頻率（每天一次、兩次等），之後自動執行，無需手動觸發。

**對比 ChatGPT 的排程功能**：ChatGPT 有類似功能但執行品質差；Claude 的版本可靠度明顯更高。這是朝向真正「個人 Agentic 助理」的關鍵功能，目前需要 Pro / Max / 企業方案。

## Google 工具整合更新

Google 將多個獨立實驗性工具整合升級：

**Google Stitch**（網頁設計工具）：新增直接點擊介面進行編輯的功能，操作更直覺。

**Google Opal**（no-code 自動化）：新增 Agent 步驟，允許在工作流中加入 LLM 判斷節點，決定走哪條分支——在保持消費者友善的同時，大幅提升功能深度，接近 n8n 等技術工具的能力。

**Google Flow**（設計師創作工具）：整合更多功能至單一平台，包含：精確影片編輯、套索選取局部修改、物件增刪、鏡頭運動控制。圖片生成免費，其餘功能付費。

## Gemini 3.1 Flash-Lite

針對開發者的輕量高速模型。與前代 2.5 Flash-Lite 相比：成本更低（每百萬 output token 僅 0.25 美元）但能力更強，整體效能超越原本定價更高的舊版本。AI 成本持續下降。

## 快報

**Qwen 3.5 小型模型**：首個能在手機或舊筆電運行、且達到 Llama 70B 水準的模型。雖然仍遠不及頂端模型，但「能在舊硬體上跑出可用品質」這件事本身就是突破。

**Anthropic vs. 美國國防部**：Anthropic 拒絕美國政府要求其模型支援國防部的請求，OpenAI 隨後填補此缺口。此事引發大量關於 AI 安全與地緣政治的討論。

**Adobe Firefly Quick Cut**：號稱 AI 影片剪輯工具，實測多次效果不佳，目前不建議使用。

**Perplexity Computer**：同時向多達 19 個模型查詢並整合最佳答案的服務，理念有趣但尚未看到明確使用價值。

**Notion 自訂 Agent**：可在 Notion 中設定 Agent，整合 Slack 問答、自動路由開發者回饋等，本質上是將現有自動化功能更緊密整合進 Notion。

**青少年使用 AI 研究**：研究顯示幾乎所有青少年都用 AI 完成作業，引發爭議。觀點：這不是學生的問題，而是教育系統需要重新設計符合現有工具的作業型態。
