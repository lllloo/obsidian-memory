---
title: DESIGN.md - Google Stitch 設計系統文件格式
created: 2026-04-14
updated: 2026-04-21
tags:
  - design-system
  - design
  - ai-tools
  - frontend
  - claude-code
---

DESIGN.md 是 Google Stitch 提出的設計系統文件格式，概念類似 README.md，但專為 AI coding agent 設計，讓 LLM 能讀取並產生一致的 UI。

## 是什麼

一個純 Markdown 檔案，記錄專案的設計系統規則：色彩、字體、間距、元件樣式等。無需專有格式或工具，直接放進專案根目錄即可。

命名慣例：`DESIGN.md`（放在專案根目錄）

## 用途

- AI coding agent（Claude Code、Cursor、Gemini CLI）讀取後，能依規格產生與設計稿一致的 UI
- 取代傳統 Figma handoff 流程
- 納入 Git 版控，追蹤設計系統的變更歷程

## 標準 9 大區段（註：1-8 為官方 alpha spec，9 為社群擴展）

1. **Visual Theme & Atmosphere** — 風格調性、設計哲學、密度感
2. **Color Palette & Roles** — 語義化色彩命名、hex 值與功能說明
3. **Typography Rules** — 字體家族與完整字級階層
4. **Component Stylings** — 按鈕、卡片、輸入框、導覽列，含互動狀態
5. **Layout Principles** — 間距比例、網格系統、留白策略
6. **Depth & Elevation** — 陰影系統與介面層次
7. **Do's and Don'ts** — 設計護欄與反模式
8. **Responsive Behavior** — 斷點、觸控目標、收合策略
9. **Agent Prompt Guide（社群擴展）** — 快速色彩參考與預設 prompt 範例

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
- Input border: 1px solid #E0E0E0, focus: 2px solid Primary
```

## 撰寫原則

- 使用具體數值（「8px」而非「圓角」）
- 語義化命名（primary、surface、accent）
- 精簡為 token 層級，不塞完整 CSS
- 納入版控，合併前審查變更

## 配套檔案

| 檔案 | 說明 |
|------|------|
| `DESIGN.md` | 設計系統文件（本格式） |
| `preview.html` | 視覺目錄，呈現色彩、字級、元件 |
| `preview-dark.html` | 深色模式視覺目錄 |

## 與 Claude Code 整合

1. 在 Stitch 完成設計後，匯出 `DESIGN.md` 放專案根目錄
2. 在 `CLAUDE.md` 加入指示：「生成或修改任何 UI 元件時，請參照 DESIGN.md」
3. 每次 prompt 明確引用：「依照 DESIGN.md 的設計系統建立 primary button」
4. 可將 DESIGN.md 的 token 轉換為 Tailwind config（`tailwind.config.js`）

常見錯誤：
- DESIGN.md 只放本機，未納入版控
- Stitch 設計未完成就匯出
- CLAUDE.md 未隨 tech stack 更新

## Google Stitch design-md Skill

社群有 `design-md` skill 可自動分析 Stitch 專案並產生 DESIGN.md，安裝方式以實際 repo 說明為準（過去常見路徑：`google-labs-code/stitch-skills`，請先確認 repo 是否仍存在）。

五階段分析流程：

1. **Retrieval** — 抓取專案畫面、HTML、設計 metadata
2. **Extraction** — 識別 design token（色彩、字體、間距、元件）
3. **Translation** — 將 CSS/Tailwind 值轉為語義化設計語言
4. **Synthesis** — 產生完整 DESIGN.md 文件
5. **Alignment** — 確保輸出符合 Stitch Effective Prompting Guide

## 參考資源

- [Google Stitch](https://stitch.withgoogle.com/) — 官方入口
- [Stitch 介紹（Google Developers Blog）](https://developers.googleblog.com/stitch-a-new-way-to-design-uis/)
- [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — 各大品牌設計系統的 DESIGN.md 範例集
