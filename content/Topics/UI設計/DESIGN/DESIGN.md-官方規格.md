---
title: DESIGN.md 官方規格
created: 2026-04-29
updated: 2026-04-29
tags:
  - design
  - design-system
  - frontend
---

DESIGN.md 是 Google Labs（Stitch 團隊）提出的設計系統文件格式——一個以純文字表示、由 optional YAML frontmatter 與 Markdown 正文組成的格式檔案，放在專案根目錄，以人機雙讀的方式記錄 design token 與規則，讓 AI coding agent 產出視覺一致的 UI。

## Spec 狀態

目前版本為 **`alpha`**，格式仍在演進中。核心規則：

- 所有 sections 均為選填（可省略不寫）
- **有寫的 sections 必須遵守 canonical order**（不可亂序）
- 未知 sections：工具應保留而非報錯
- 重複 section headings：視為格式錯誤（reject with error）

查證日期：2026-04-29，來源：[google-labs-code/design.md README](https://github.com/google-labs-code/design.md) 及 [docs/spec.md](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md)。

## 官方 Canonical 8 大區段

| # | 區段 | 別名 | 內容 |
|---|------|------|------|
| 1 | Overview | Brand & Style | 整體品牌風格、感受、個性描述 |
| 2 | Colors | — | 色彩 token 與語義用途（primary / surface / error…） |
| 3 | Typography | — | 字型 token 與層級慣例 |
| 4 | Layout | Layout & Spacing | 格線模型、間距策略、容器原則 |
| 5 | Elevation & Depth | Elevation | 陰影、色調層次、邊框等視覺層級方式 |
| 6 | Shapes | — | 圓角尺度與幾何語言 |
| 7 | Components | — | 按鈕、輸入框、卡片等元件 token 與狀態 |
| 8 | Do's and Don'ts | — | 設計護欄與常見反模式 |

社群有 extended format（如 `Responsive Behavior`、`Agent Prompt Guide`），非官方必填，詳見 [[DESIGN.md-使用指南]]。

## YAML Frontmatter Token Schema

DESIGN.md 本身可包含 YAML frontmatter，用來承載結構化 token（供 CLI 解析與 export 使用）：

```yaml
---
version: alpha
name: MyBrand
description: 品牌設計系統
colors:
  primary: "#1A73E8"
  surface: "#FFFFFF"
  error: "#EA4335"
typography:
  body-md:
    fontFamily: Inter, sans-serif
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
rounded:
  sm: 4px
  md: 8px
  lg: 12px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    rounded: "{rounded.md}"
---
```

Token 跨參照語法：`{path.to.token}`，例如 `{colors.primary}`。在 `components` 區塊內，也可參照複合 token，例如 `{typography.body-md}`。

### 推薦 Token 命名慣例

- **Colors**：primary、secondary、tertiary、neutral、surface、on-surface、error
- **Typography**：headline-display、headline-lg、body-md、label-sm
- **Rounded**：none、sm、md、lg、xl、full

> 官方 non-normative recommended tokens 目前只明列 Colors、Typography、Rounded 三類。`spacing` 常見範例會出現 `base`、`xs`、`sm`、`md`、`lg`、`xl`、`gutter`、`margin`，但不屬於官方明列推薦名單。

## Markdown 正文格式範例

YAML frontmatter 之後的 Markdown 本文承載人類可讀的設計說明，依 canonical order 排列：

```markdown
## Colors
- Primary: `#1A73E8` — 主要操作、連結
- Error: `#EA4335` — 錯誤狀態
- Surface: `#FFFFFF` — 頁面背景

## Typography
- Font Family: Inter, sans-serif
- Heading 1: 32px, 700 weight
- Body: 16px, 400 weight, 1.5 line-height

## Layout
- Base unit: 8px
- Small: 8px | Medium: 16px | Large: 24px | XL: 32px

## Components
- Button border-radius: 8px
- Card border-radius: 12px, shadow: 0 2px 8px rgba(0,0,0,0.1)
```

> 注意：Obsidian 中色碼 `#` 開頭若不加反引號會被解析為 tag，正文色碼一律用反引號包住。

## 官方 CLI：`@google/design.md`

安裝：

```bash
npm install @google/design.md
# 或免安裝直接執行
npx @google/design.md [command]
```

### 指令清單

| 指令 | 用途 | 範例 |
|------|------|------|
| `lint` | 驗證結構正確性（exit 1 = 有錯） | `npx @google/design.md lint DESIGN.md` |
| `lint --format json` | 輸出 JSON 格式報告 | `npx @google/design.md lint --format json DESIGN.md` |
| `diff` | 比對兩版差異，偵測 token regression（exit 1 = 有回退） | `npx @google/design.md diff DESIGN.md DESIGN-v2.md` |
| `export --format tailwind` | 輸出 Tailwind theme JSON | `npx @google/design.md export --format tailwind DESIGN.md > tailwind.theme.json` |
| `export --format dtcg` | 輸出 DTCG 格式 tokens | `npx @google/design.md export --format dtcg DESIGN.md > tokens.json` |
| `spec` | 輸出格式規格（供 agent prompt 使用） | `npx @google/design.md spec` |
| `spec --rules` | 附帶規則說明 | `npx @google/design.md spec --rules` |
| `spec --rules-only --format json` | 僅輸出規則的 JSON | `npx @google/design.md spec --rules-only --format json` |

`stdin` 支援（`lint`）：

```bash
cat DESIGN.md | npx @google/design.md lint -
```

## 配套資源（官方 repo）

官方 repo `google-labs-code/design.md` 內含：

- `docs/spec.md` — 完整格式規格文件
- `examples/` — 範例實作

## 來源背景

DESIGN.md 由 **Google Labs（Stitch 團隊）**提出，隨 Stitch 工具一同開源。定位是讓設計師能「將設計規則從專案帶到專案」，同時讓 AI agent 理解設計系統背後的語意（而非只看數值）。格式本身不綁定 Stitch，任何支援的 AI coding tool 皆可讀取。

## 相關主題

- [[DESIGN.md-使用指南]] — 撰寫原則、工作流建議、與 Claude Code 整合、五階段 skill
- [[Stitch]] — Google Stitch 工具 MOC
- [[Awesome-Design-MD]] — 品牌範例庫（awesome-design-md）

## 外部資源

- [google-labs-code/design.md](https://github.com/google-labs-code/design.md) — 官方 spec repo 與 CLI
- [docs/spec.md](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md) — 完整格式規格
- [Stitch's DESIGN.md format is now open-source](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/) — Google Labs 開源公告
- [stitch.withgoogle.com](https://stitch.withgoogle.com/) — Stitch 入口
