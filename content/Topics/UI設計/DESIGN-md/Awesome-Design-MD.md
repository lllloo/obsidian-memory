---
title: Awesome Design MD
created: 2026-04-12
updated: 2026-04-29
tags:
  - design
  - design-system
  - ai-coding
  - resources
---

[AWESOMEDESIGN.md](https://getdesign.md/) 是 [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 的瀏覽前端，收集熱門網站設計系統靈感。它提供的是**從公開網站抽出的 DESIGN.md 參考文件**，適合拿來做風格研究與 prompt / agent context 起點。

## 關於 DESIGN.md

`DESIGN.md` 是 Google Stitch 提出的 agent-friendly 設計系統文件格式；`awesome-design-md` 則是把許多公開網站的視覺語彙整理成可重用的 DESIGN.md 範例集合。

> 注意：這些不是官方設計系統，而是從公開可見設計模式整理的靈感來源，與各品牌無關聯也未獲授權。

GitHub 來源：[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)

每個品牌的 DESIGN.md 文件格式為：`https://getdesign.md/<brand>/design-md`

## DESIGN.md 結構

這個 collection 採用的是 **extended 9-section format**，不是 Google 官方 base spec 的唯一寫法：

| # | 節名 | 內容 |
|---|------|------|
| 1 | Visual Theme & Atmosphere | 氛圍、密度、設計哲學 |
| 2 | Color Palette & Roles | 語義色名 + hex + 功能角色 |
| 3 | Typography Rules | 字型家族、完整層級表 |
| 4 | Component Stylings | 按鈕、卡片、輸入框、導覽與狀態 |
| 5 | Layout Principles | 間距比例、網格、留白哲學 |
| 6 | Depth & Elevation | 陰影系統、表面層級 |
| 7 | Do's and Don'ts | 設計護欄與反模式 |
| 8 | Responsive Behavior | 斷點、觸控目標、收合策略 |
| 9 | Agent Prompt Guide | 快速色彩參考、即用提示詞 |

每個品牌另外附有 `preview.html`（淺色）與 `preview-dark.html`（深色）視覺預覽；這是 collection 的附加產物，不是官方 spec requirement。

## 品牌涵蓋範圍

按產業分 9 類，每類舉幾個代表品牌——repo 仍在增加，完整清單以 GitHub README 為準：

- **AI & LLM 平台**：Claude、Mistral、xAI、ElevenLabs、Cohere、RunwayML…
- **開發工具 & IDE**：Cursor、Vercel、Warp、Raycast、Superhuman…
- **後端、資料庫 & DevOps**：Supabase、Sentry、ClickHouse、PostHog…
- **生產力 & SaaS**：Linear、Notion、Cal.com、Resend、Zapier…
- **設計 & 創意工具**：Figma、Framer、Webflow、Miro、Airtable…
- **金融科技 & 加密**：Stripe、Coinbase、Wise、Revolut…
- **電商 & 零售**：Airbnb、Nike、Shopify、Meta…
- **媒體 & 消費科技**：Apple、Spotify、NVIDIA、WIRED、Pinterest、SpaceX…
- **汽車**：Tesla、Bugatti、Ferrari、BMW、Lamborghini…

選用情境例：做 AI 工具站 → 看 Claude / Mistral / xAI；做開發者文件 → 看 Vercel / Supabase / Linear；做極簡編輯介面 → 看 Notion / Linear / Resend。

完整品牌風格描述：[awesome-design-md README](https://github.com/VoltAgent/awesome-design-md)；瀏覽預覽：[getdesign.md](https://getdesign.md/)。

## 相關主題

- [[DESIGN.md-官方規格]] — 官方 8 大 canonical 區段、alpha spec 狀態、官方 CLI
- [[DESIGN.md-使用指南]] — 撰寫原則、Claude Code 整合工作流、design-md skill 五階段
- [[Stitch]] — Google Stitch（DESIGN.md 提出者，生成範例的主要工具）