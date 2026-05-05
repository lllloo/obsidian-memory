---
title: Vibe-Coded App 上線工程實踐
created: 2026-05-05
updated: 2026-05-05
tags:
  - vibecoding
  - best-practices
  - workflow
  - moc
---

> Vibe-coded app 從 demo 走到 production，不是突然遇到新工程問題，而是用更快速度撞上舊工程基本功：auth email、RLS、webhook 驗簽、SEO / crawler visibility、rate limit、成本控管。AI 能壓縮 build time，但不會替人免掉 architecture、security、product ops、scale 的責任。

## 核心判斷

社群審計 50+ vibe-coded apps（最高 1000+ 使用者）後的共識：

- **AI 寫得快，但預設只補 happy path**：邊角案例、安全驗簽、配額限制不會自動出現
- **「AI 已 review」不是安全審計**：除非明確要求 OWASP / security review，agent 通常不會主動掃
- **Production bug 多半很無聊**：SMTP deliverability、auth policy、SEO、rate limit 都是過去十年就存在的基本功
- **AI 生成程式碼有常見 anti-pattern**：env 跑進前端、API key 寫死、API response 回太多、secrets 進 logs

一句話：vibe coding 不是新工程問題，是把舊工程缺口用新速度暴露出來。

## 開發階段：人要守住工程方向

一個 20 年資歷遊戲開發者用 30 天 + Claude 上線多人 .io 遊戲的實戰，重點不是「AI 全自動完成」，而是人類把流程工程化：

- 先寫 PRD / DESIGN 文件，鎖住 gameplay、network protocol、視覺語言，但接受實作中會偏離
- 拆成編號階段，逐步完成 rendering、movement、玩法、多人、bots、UI、mobile、audio、deploy、analytics、polish
- 用 persistent memory file 跨 session 記錄規則、專案狀態、code 位置索引
- 每個階段都由人類 review diff、實際跑、做小幅 polish

人類最重要的價值不在打字，而在判斷：

- **偏離計畫的時機**：AI 太死守原文件會走錯路，完全忽略文件又會每次重來
- **手感與真實體驗**：production 與 localhost 的操作差異、長時間使用的疲勞感，必須實際試
- **Debug 打破鎖死**：AI 會在錯誤假設上越鑽越深，需要人要求先驗證假設
- **擋 scope creep**：AI 永遠願意加功能，人要決定何時停

規則文件也要節制。把整套軟工書塞進 `AGENTS.md` 會碰到遵循上限；實務上更適合選 1-2 個當前最相關的治理原則，再用 path-scoped rules 讓規則只在需要時載入。細節見 [[Claude-Code-規則系統設計]]。

## 上線前：最小 Checklist

每個 vibe-coded app 上線前，至少要跑一次這些檢查：

- [ ] **法規與資料處理**：有 privacy policy，知道收了哪些資料、存在哪裡、如何刪除與處理
- [ ] **Security baseline**：要求 agent 檢查 security headers、auth flow、OWASP 常見漏洞
- [ ] **Credential leak**：確認 API key、token、secret 沒進前端 bundle、network call、API response、logs
- [ ] **Crawler visibility**：右鍵檢視原始碼，確認內容文字在 HTML 裡；若只有 `<div id="root"></div>` + `<script>`，GPTBot / ClaudeBot / PerplexityBot 基本看不到內容
- [ ] **SEO / discoverability**：提交 `sitemap.xml`，不要期待 Google 自動發現新站
- [ ] **Accessibility baseline**：鍵盤導航、button / image label、screen reader、高對比至少過一輪

可直接丟給 agent 的兩個 prompt：

```text
Review my app against OWASP standards and highlight vulnerabilities.
```

```text
Check my app for any credential or sensitive data leaks in frontend or API routes.
```

## 上線後：5 個常見翻車點

### 1. Auth email 寄不到

Supabase 預設 SMTP 是 best-effort、非 production 用途。驗證信進垃圾郵件或促銷分頁時，看似 1000 註冊，實際可能只有 400 驗證。

修法：上線前換成 Resend、AWS SES、Postmark、Twilio SendGrid、ZeptoMail、Brevo 等正式 SMTP provider；設定 SPF / DKIM / DMARC，並用 [mail-tester.com](https://www.mail-tester.com/) 測。

### 2. Supabase RLS 名存實亡

RLS 真正危險的模式不是「沒開」，而是 AI 開了 RLS 後又加了過寬 policy，例如 `USING (true)` 或對 `anon` role 開放。

修法：每張 table 的 policy 必須 reference `(select auth.uid())` 與 owner column，並人工檢查 `pg_policies`，特別找無條件 policy。

### 3. Stripe webhook 沒驗簽

Webhook endpoint 若沒驗證 Stripe signature，任何人都能 POST 假 event 升級自己訂閱或降級別人。

修法：webhook route 必須拿 raw body，使用 `stripe.webhooks.constructEvent()` 驗 `stripe-signature` header；`whsec_` secret 放 secret store，不寫進 code、不進 logs。

### 4. Context rot cascade

App 長大後，agent 會失去整體理解。「修一個小東西」可能改寫 auth flow、弄壞無關功能。

修法：每次 agent run 前先 commit；先用 Chat / Plan Mode 規劃，再切 Agent Mode 實作；大型 app 要 scope 到特定檔案。通用機制與對策見 [[Context-Engineering]]。

### 5. Free tier abuse

前端按鈕直接打 OpenAI / Anthropic edge function，又沒有 rate limit，一次社群曝光就可能讓帳單在數小時內暴增。

修法：LLM 呼叫移到後端；加 per IP + per user rate limit；設定 user-level 配額與 daily / monthly cap；監控成本曲線，超過閾值自動降級。

## 速查表

開發階段：

- 鎖 PRD / DESIGN 文件，但接受實作中會修；偏離時機由人判
- 編號階段切分 + persistent memory file 維持方向
- 規則文件精選，不把整套書塞進 `AGENTS.md`
- 每階段 review diff、實跑、判斷

上線前：

- [ ] 隱私政策、資料處理說明
- [ ] Security headers + OWASP review
- [ ] Credential / API key 不在前端
- [ ] View source 看得到內容文字
- [ ] `sitemap.xml`
- [ ] 基本 accessibility 檢查

上線後：

- [ ] SMTP 換掉預設 + SPF / DKIM / DMARC
- [ ] 每張 table 的 RLS policy 個別 review
- [ ] Stripe webhook 驗簽
- [ ] Agent 工作先 commit + 規劃 + scope 到檔案
- [ ] LLM 呼叫走後端 + rate limit + user 配額

## 外部來源

來自 Inbox/Reddit/vibecoding/ 的五篇貼文摘要：

- [I've been in game dev for over 20 years and just tried vibecoding a production-quality competitive multiplayer .io game in 30 days](https://www.reddit.com/r/vibecoding/comments/1t10tmu/ive_been_in_game_dev_for_over_20_years_and_just/) — 30 天 solo + Claude 上線實戰
- [6 things that broke when my vibe coded apps got their first real users](https://www.reddit.com/r/vibecoding/comments/1t23dqw/6_things_that_broke_when_my_vibe_coded_apps_got/) — 50+ apps 審計
- [If you're about to launch a "vibe coded" app… read this first](https://www.reddit.com/r/vibecoding/comments/1sthzcj/if_youre_about_to_launch_a_vibe_coded_app_read/) — 上線前 checklist
- [Vibe-coded CSR sites are invisible to Google and AI crawlers](https://www.reddit.com/r/vibecoding/comments/1sysz4m/so_apparently_all_our_vibe_coded_sites_are/) — CSR vs AI bot
- [I rewrote 13 software engineering books into AGENTS.md rules](https://www.reddit.com/r/vibecoding/comments/1suo2vy/i_rewrote_13_software_engineering_books_into/) — agent rule ceiling

相關主題（vault 內）：

- [[Claude-Code-規則系統設計]] — CLAUDE.md / AGENTS.md / Rules 機制與規則寫法
- [[Context-Engineering]] — Context rot 機制與對策
- [[Claude-Code-多-Agent-協作]] — Agent 協作架構
