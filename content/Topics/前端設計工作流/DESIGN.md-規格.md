---
title: DESIGN.md 設計系統規格
created: 2026-04-21
updated: 2026-04-25
tags:
  - design
  - design-system
  - ai-coding
  - frontend
  - moc
---

涵蓋 DESIGN.md 是什麼、官方 canonical 區段、常見 extended sections、品牌範例庫，以及與 Claude Code 整合的常見工作流。

## 是什麼

**DESIGN.md** 是 Google Stitch 提出的設計系統文件格式——一個純 Markdown 檔案，放在專案根目錄，記錄色彩、字型、間距、元件樣式等規則，讓 AI coding agent（Claude Code、Cursor、Gemini CLI）讀取後產出一致的 UI。

**何時用**：

- 開始新專案要為 AI agent 建立設計規範
- 想讓設計系統納入 Git 版控、取代 Figma handoff
- 團隊要確保多個 agent（或多人）產出視覺一致

## 官方 canonical 8 大區段（alpha spec）

| # | 區段 | 內容 |
|---|------|------|
| 1 | Overview | 品牌與整體風格說明 |
| 2 | Colors | 色彩 token 與語義用途 |
| 3 | Typography | 字型 token 與階層 |
| 4 | Layout | 版面與間距原則 |
| 5 | Elevation & Depth | 表面層級與陰影 |
| 6 | Shapes | 圓角 / shape 規則 |
| 7 | Components | 元件 token 與狀態 |
| 8 | Do's and Don'ts | 設計護欄與反模式 |

> 官方 spec 目前是 `alpha`，而且 sections 可以省略；重點是**有寫的區段要遵守 canonical order**。

## 常見 extended sections（不是官方必填）

像 `awesome-design-md` 這類 collection，常會在官方 8 段之外，再額外加入：

- `Responsive Behavior`
- `Agent Prompt Guide`

這些延伸段落對實務很有幫助，但應明確標成 **extended format**，不要誤寫成官方 base spec 的必填要求。

## 撰寫原則

- **具體數值**：寫「8px」而非「圓角」
- **語義命名**：primary / surface / accent，不用 blue-500
- **token 層級**：只寫 token，不塞完整 CSS
- **納入版控**：與程式碼同步，合併前審查變更

## 品牌範例庫：awesome-design-md

[getdesign.md](https://getdesign.md/)（GitHub: [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)）收集數十個知名品牌的 DESIGN.md，按產業分類；它採用的是 **Stitch format + extended sections** 的整理版本，而不是 Google 官方 spec 本身：

- **AI 平台**：Claude、Cohere、ElevenLabs、Mistral、xAI 等
- **開發工具**：Cursor、Vercel、Raycast、Warp、Superhuman
- **後端/DevOps**：MongoDB、Supabase、Sentry、PostHog
- **生產力 SaaS**：Linear、Notion、Intercom、Cal.com
- **設計創意**：Figma、Framer、Webflow、Miro
- **媒體消費**：Apple、Nike、Spotify、The Verge
- **金融/電商**：Stripe、Coinbase、Airbnb、Shopify

**使用方式**：每個品牌的 DESIGN.md 格式為 `https://getdesign.md/<brand>/design-md`，直接下載貼入專案。

> **注意**：這些不是官方設計系統，而是從公開可見設計模式整理的靈感來源，未獲授權，僅適合用於學習或風格參考。

## 與 Claude Code 整合（常見工作流）

這一段屬於實務工作流建議，不是 DESIGN.md spec 本身。

1. 完成設計後把 `DESIGN.md` 放專案根目錄
2. 在 `CLAUDE.md` 加指示：「生成或修改任何 UI 元件時，請參照 DESIGN.md」
3. 每次 prompt 明確引用：「依照 DESIGN.md 建立 primary button」
4. 可把 token 轉為 Tailwind config（`tailwind.config.js`）

## 格式範例

```markdown
## Colors
- Primary: #1A73E8
- Error: #EA4335
- Surface: #FFFFFF

## Typography
- Font Family: Inter, sans-serif
- Heading 1: 32px, 700 weight
- Body: 16px, 400 weight, 1.5 line-height

## Spacing
- Base unit: 8px
- Small: 8px | Medium: 16px | Large: 24px | XL: 32px

## Components
- Button border radius: 8px
- Card border radius: 12px, shadow: 0 2px 8px rgba(0,0,0,0.1)
```

## 官方工具與相關 skill

- 官方現在有 `@google/design.md` CLI，可用來 `lint`、`diff`、`export`、`spec`
- 若要驗證檔案是否符合目前 spec，可直接跑：`npx @google/design.md lint DESIGN.md`
- `google-labs-code/stitch-skills` 裡也有 `design-md` skill，可把 Stitch 專案分析為較自然語言、偏 agent-friendly 的 DESIGN.md 說明

這三者的角色不同：

- **spec / CLI**：定義格式與驗證規則
- **Stitch**：產生 / 套用設計系統
- **skills**：把設計流程串進 agent 工作流

## 常見陷阱

**徵兆：Agent 產出 UI 與設計稿不一致**
- 原因：DESIGN.md 只放本機，agent 讀不到或未納入版控
- 解法：commit 進 git，`CLAUDE.md` 明確指示 agent 讀取

**徵兆：DESIGN.md 內容變來變去**
- 原因：Stitch 設計未完成就匯出
- 解法：在 Stitch 階段先定稿視覺方向再產 DESIGN.md

**徵兆：token 轉 Tailwind 時衝突**
- 原因：語義命名（primary）與 Tailwind 預設（blue-500）未對齊
- 解法：在 `tailwind.config.js` 覆寫 theme，保持單一命名來源

## 相關主題

- [[Stitch]] — Google Stitch MOC（生成 DESIGN.md 的主要工具）
- [[Claude-Code-前端設計工作流]] — Layer 1 Prompt 注入層引用此 MOC
- [[動效與互動]] — 動效類別的設計規格

## 來源卡片

- [[Awesome-Design-MD]] — 品牌範例庫總覽
- [[DESIGN.md-Google-Stitch-設計系統文件格式]] — 格式與 9 區段定義

## 外部資源

- [getdesign.md](https://getdesign.md/) — 品牌範例瀏覽入口
- [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — GitHub 源
- [Google Stitch](https://stitch.withgoogle.com/) — 官方入口
- [google-labs-code/design.md](https://github.com/google-labs-code/design.md) — 官方 spec 與 CLI
- [Stitch’s DESIGN.md format is now open-source](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/) — 開源公告