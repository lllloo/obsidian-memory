---
title: Claude Code 行銷與內容創作的七個層級
created: 2026-05-04
updated: 2026-05-04
source: https://www.youtube.com/watch?v=S6YwrVql83U
published: 2026-04-30
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
---

## 核心觀點

- 不是工具不夠，是 **taste 不夠**——堆工具會讓影片 6 小時就過時
- 影片分兩半：前半談 taste（如何讓內容聽起來像你而非 AI slop）、後半談系統與規模化
- 從第 1 到第 7 層逐步從「praying」升級到「autonomous agent」

## Level 1：AI Slop

- 最常見：直接對 ChatGPT 說「幫我寫 tweet / LinkedIn / blog」
- 頂多再叮嚀「不要 m-dash、不要像 AI」
- 全網 90% 內容停在這一層，是 AI 給人壞印象的主因
- 該掌握的技能：辨識 AI default 措辭、寫清楚的 prompt、願意 iterate（不是直接交 first output）
- 升級條件：別讓 AI 「猜」你的 voice，要明確注入

## Level 2：Voice Injector

- 用 `claude.md` 或專屬 voice doc 把自己的聲音、語氣寫成文件
- 作者範例 doc 結構：core mission / voice & tone guidelines / words & phrases to never use / on-brand phrases / 平台特定要點
- 真正用法：餵 3-10 篇好作品（自己的或他人的）→ 請 Claude Code 用模板把語氣抽出來
- 反 trap：
  - 不要餵 30,000 字 dissertation——context rot
  - 不要建 RAG 塞 40,000 篇——蠢
  - 也不要以為一次寫完就定案：要持續用真實 post 表現回填 doc

> 90% 的人連這層都到不了。第二層做好就贏一大半人。

## Level 3：Strategy & Ideation

- 解決「要寫什麼」的問題
- 作者每日流程：Claude Code 跑 morning report 自動掃 AI / coding agent / Anthropic 相關內容（Twitter、GitHub、web），輸出到 Obsidian vault
- 篩出有興趣的話題 → 觸發 deep research workflow（YouTube pipeline skill → Notebook LM CLI → 摘要與內容構想 brief）
- 通用模板：
  1. 搞清楚**自己的資訊源**（科技業：Twitter > GitHub > YouTube > IG/TikTok/LinkedIn）
  2. 定義想從中擷取什麼（重點摘要、so-what、可寫的 content idea）
  3. 把流程描述給 Claude Code → 用 skill creator skill 自動轉成 skills
- trap：把 ideation 過度產品化（建一堆 dashboard）。它只是 step 1，不是成品

## Level 4：Creative Director（多模態）

- 從文字進到 image / video，**底層原理一樣**：reference + prompt + voice doc
- 工具會週週換（VO3 → Cling → Seed Dance；Nano Banana → GPT Image 2），但 prompt 結構通用
- 關鍵技巧：**JSON prompt 模板**
  - 給 Claude Code 一張 reference image → 用 JSON prompt generator skill 拆成 JSON
  - 用自然語言改 JSON 中的 text / background / 主角等
  - 再把 JSON 餵給 Nano Banana Pro / GPT Image 2 → 出風格一致的圖
- 應用：找 IG 上 44k 讚的 carousel → 截圖 → 拆 JSON → 改成自己的版本
- 真正解鎖：累積一整套 reusable JSON prompt templates（例：30 個 carousel 模板）

## Level 5：Scale & Repurpose

- 做一份內容、轉成多個平台
- 作者範例 skill：`content cascade`——一支 YouTube 影片自動產 LinkedIn post / Twitter thread / blog post / short-form 大綱，最後存進 Supabase，一道指令 push live
- 注意每個平台的 voice variant：基礎 voice doc 不變，但要為 LinkedIn / Twitter 各做專屬子 skill
- trap：以為每個平台講同一句話就好——會稀釋 voice

## Level 6：Automation

- 用 loop / schedule / cron 把 skill 串成自動流程
- Claude Code 內可用 `/schedule` 或桌面 app 的 Routines（local 或 remote）
- 不需要全自動，可選擇只自動化 ideation 或內容生成
- **絕對不要自動化 posting**——AI 要產的是草稿，你要當把關者
- 必備 taste checkpoints：例如 carousel 生成只先看第 1 張，確認後再產第 2-6 張
- trap：完全放手讓 AI 跑，沒有任何人類檢查點 → 品牌會被反噬
- 作者觀點：這是「應該停在這」的層級

## Level 7：Autonomous Agent

- AI avatar 完全自動的 loop（HeyGen 級的擬真度）
- 已有人在跑：每天 6-8 支 YouTube 長片，全自動 scrape → 寫腳本 → AI 配音與配圖 → 自動上片 → 重複
- 邏輯：純粹靠數量，1% 命中也能賺錢
- 作者觀點：**不建議**
  - 對個人品牌長期有害
  - 影片技術還沒到位
  - 文字（書籍、blog）唯一已可規模化的形式（Amazon 已限制每日上架書數）
- 建議：理解架構，不必照做

## 作者最高槓桿建議

- Level 2 + Level 3 是真正的金礦：voice 鎖定 + ideation 自動化 = 90% 完成度
- 要起步只需做一件事：**對 Claude Code 開麥克風做 stream of consciousness**——把現有行銷流程口述出來 → 請它拆成離散任務 → 用 skill creator skill 轉成可執行的 skills
- 高槓桿排序：
  1. 建立 voice doc 並持續 iterate
  2. 把日常 marketing workflow 拆成 skills
- 工具會換，但這兩件事不會過時
