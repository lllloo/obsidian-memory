---
title: If you're about to launch a "vibe coded" app… read this first
created: 2026-04-27
updated: 2026-04-27
source: https://www.reddit.com/r/vibecoding/comments/1sthzcj/if_youre_about_to_launch_a_vibe_coded_app_read/
published: 2026-04-23
tags:
  - reddit
  - vibecoding
  - best-practices
  - ai-tools
---

> **繁中摘要**：20 年資歷工程師整理 vibe coding 上線前 5 項基本檢查（隱私政策、安全 headers、OWASP、env/credential 洩漏、API key 不放前端），每項附可直接餵給 AI 工具的 prompt。

---

## 原文重點

上線前 5 項自我檢查（任何 AI coding 工具皆適用）：

**1. 法規層（保護自己，不只 app）**

- 收集任何使用者資料即進入法規範圍（GDPR 等）
- 至少要有：privacy policy、清楚知道資料怎麼存／怎麼處理、不亂用使用者資訊

**2. 基礎安全 posture（兩分鐘可做）**

```
Review my app as a security specialist and make sure I have strong security headers and a solid baseline security posture
```

**3. 對齊 OWASP（headers 不夠）**

```
Review my app against OWASP standards and highlight vulnerabilities
```

涵蓋 SQL injection、XSS、auth 問題等。

**4. 防止洩漏（AI 生成程式碼最常犯）**

常見坑：`.env` 值跑進前端、API response 回太多、secrets 進 logs。

```
Check my app for any credential or sensitive data leaks in frontend or API routes
```

**5. API key 絕不放前端**

key 一旦進瀏覽器就視同外洩。對策：移到 server-side、走 proxy、加權限鎖。

```
Ensure no API keys are exposed in frontend code or network calls
```

## 社群討論亮點

- **EU 無障礙法（accessibility）**：每個 button、image、text 都要符合可讀性、screen reader、鍵盤導航、高對比支援；除合規外也是品質訊號
- **rate limiting on API routes**：補充項，不少 vibe coded app 因無 rate limit 被打到帳單爆炸（呼應另一篇 GCP $25K 慘案）
- **env leak 應排第一**：AI 常把東西放錯位置，新手不知道該找什麼；OWASP prompt 也常被低估，多數人以為 AI 已自動 review 安全（其實不會，除非明確問）
