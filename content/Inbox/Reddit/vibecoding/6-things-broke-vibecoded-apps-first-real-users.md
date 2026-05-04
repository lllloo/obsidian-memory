---
title: "6 things that broke when my vibe coded apps got their first real users"
created: 2026-05-04
updated: 2026-05-04
source: https://www.reddit.com/r/vibecoding/comments/1t23dqw/6_things_that_broke_when_my_vibe_coded_apps_got/
published: 2026-05-02
tags:
  - reddit
  - vibecoding
  - best-practices
  - bug
---

> **繁中摘要**：9 年資歷後端工程師審計 50+ vibe-coded apps（最高 1000+ 使用者）後整理的 6 大 production 翻車模式，每條都附 paste-ready 修法，涵蓋 auth email、Supabase RLS、Stripe webhook、context rot、rate limiting。

---

## 原文重點

### 1. Auth Email 寄不到（Supabase 預設 SMTP）

- **症狀**：Supabase Auth 預設 SMTP deliverability 很差，驗證信進垃圾郵件 / 促銷分頁，看似 1000 註冊實際 400 驗證。
- **修法**：上線前換掉預設 SMTP，配 `Resend` / `Postmark` + 驗證網域，設好 SPF / DKIM / DMARC（DMARC 至少 `p=quarantine`）。上線前用 `mail-tester.com` 測試。

### 2. Supabase RLS 名存實亡

- **症狀**：AI 說 RLS「已啟用」，但 default policy 常常等於對所有人開放。據稱 200+ vibe-coded app 審計中 89% 中招。
- **修法**：每張 table policy 都要 reference `auth.uid()` vs owner column。檢查 query：

```sql
SELECT tablename, policyname, qual
FROM pg_policies
WHERE schemaname = 'public';
```

逐 row 人工 review。

### 3. Stripe Webhook 沒驗簽

- **症狀**：webhook endpoint 沒驗證 Stripe signature → 任何人 POST 假 webhook 即可升級自己訂閱、或降級別人。Agent 不會主動加這一步。
- **修法**：在 edge function / webhook handler 用：

```js
stripe.webhooks.constructEvent(rawBody, signature, webhookSecret);
```

webhook secret 從 Stripe Dashboard → Developers → Webhooks → Signing secret 取。**不要 log，存 Supabase secret，不寫進 code。**

### 4. Context Rot Cascade

- **症狀**：跟 agent 配對工作 4 個月後，agent 失去對 app 整體理解，「修一個小東西」會改寫 auth flow、弄壞 3 個無關功能。
- **三個習慣**：
  1. 每次 agent run 前 commit 到 GitHub
  2. 用 Chat Mode 規劃，再切 Agent Mode 執行（Chat Mode 不寫 code，只 1 credit）
  3. App 約 80 個 component 後，prompt 要 scope 到特定檔案：「only modify components/Pricing.tsx, dont touch anything else」

### 5. Free Tier Abuse 把錢燒光

- **症狀**：前端「Generate」按鈕直接打 OpenAI / Anthropic edge function，沒 rate limit。一條 Twitter 提及或 Reddit 貼文就可能讓帳單在數小時內爆 `$400`。
- **隱含修法**：加 rate limit、把 AI 呼叫放在後端、加 user-level 配額（原文後續因 4000 字截斷未完整顯示，但要點明確）。

### 6. （原文截斷）

剩餘第 6 點被 4000 字 truncate 切掉，**閱讀時請回原文 permalink**。

## 社群討論亮點

- 「vibe coding 壓縮 build time，但不會幫你免掉 architecture / security / product ops / scale 的責任，只是讓人更快撞牆」——把這篇歸納成「不是 exotic engineering 問題，是無聊的 production 基本功」。
- 另一條補充建議：寫 RLS policy 時用 Supabase 的 「simulate as user」測；寄信驗證率從 40% 拉到 80%+ 的關鍵是 SPF/DKIM 加 dedicated provider。
