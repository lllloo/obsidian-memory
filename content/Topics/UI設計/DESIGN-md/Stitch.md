---
title: Google Stitch
created: 2026-04-20
updated: 2026-04-25
tags:
  - design
  - design-system
  - claude-code
  - mcp
---

> Google Labs 的 AI-native 軟體設計畫布。對 Claude Code 使用者來說，Stitch 最有價值的地方是：把設計發想、設計系統、變體探索，以及交給 coding agent 落地的流程串在一起。

## Stitch 的官方定位

Google 在 2026-03-18 的官方文章把 Stitch 描述為 **AI-native software design canvas**。官方目前強調的是：

- 用文字、圖片、程式碼等多種上下文生成高保真 UI
- 在 infinite canvas 上探索多個方向與變體
- 透過 design agent、Agent manager、voice 與 interactive prototypes 快速迭代
- 用 `DESIGN.md`、MCP、skills、SDK 與 export 串接後續開發流程

截至 2026-04，Stitch 仍以 **Beta** 形式對外提供；若要描述費用或長期可用性，建議以當下官方頁面為準，不要寫成永久免費承諾。

## 為什麼跟 Claude Code 有關

如果你是用 Claude Code 做前端，Stitch 的角色通常不是取代 coding agent，而是補足它不擅長的部分：

- **視覺發想**：先在畫布上探索方向，而不是一開始就用 code 逼設計定型
- **設計系統**：把 design rules 透過 `DESIGN.md` 在設計與開發之間流動
- **交接**：把 screen、variants、HTML、design system 再交給 Claude Code 做 component 化、重構與整合

## 官方目前強調的能力

### 1. AI-native canvas

Stitch 的新介面主打 infinite canvas，可把文字、圖片或既有程式碼作為上下文直接丟進畫布，從早期 ideation 一路走到 prototype。

### 2. Design agent 與 Agent manager

官方把 Stitch 內的設計代理流程描述成能沿著整個專案脈絡推進，並透過 Agent manager 幫你平行探索多個方向。

### 3. `DESIGN.md` 設計系統流

官方已把 `DESIGN.md` 納入 Stitch 的設計系統工具箱，重點是 **匯入 / 匯出 design rules**，讓設計規則能在不同專案與不同工具之間重用。

### 4. Voice 與 prototype 預覽

官方 blog 明確提到 voice capabilities，以及把靜態設計快速串成 interactive prototype 的能力，這兩者都屬於「加速迭代」的工具，而不是保證某種固定產出品質。

## 模型與命名：不要寫死成單一清單

Stitch 目前的模型命名會依 surface 而異：

- 官方前台 / 宣傳文案會出現像 **3 Flash**、**Thinking with 3.1 Pro**、**Redesign (Nano Banana Pro)**、**Ideate** 這種使用者介面名稱
- `@google/stitch-sdk` 目前公開的 `modelId` 則是 **`GEMINI_3_PRO`** 與 **`GEMINI_3_FLASH`**

所以在筆記裡最好避免寫成「官方固定只有哪四個模型」。較穩妥的寫法是：**模型名稱會隨 UI 與 SDK surface 不同而變動，實作時以當下官方 UI / SDK docs 為準。**

## 基本工作流（保守版）

1. **找靈感**：用 Dribbble、Godly.website、Awwwards、Pinterest 等來源先定方向
2. **在 Stitch 做第一輪設計探索**：可帶文字、截圖、網站 URL 或既有 code 作為上下文
3. **用 variants / voice / prototype 預覽迭代**：快速比較不同 layout、color scheme、content 與 flow
4. **匯出設計成果**：可依情境使用 HTML export、`DESIGN.md`、MCP / SDK
5. **交給 Claude Code 實作**：把 export 結果整理成元件、頁面與實際專案結構

這條流程的重點是「先把視覺方向定清楚，再交給 coding agent」，而不是期待單一 prompt 一次到位。

## Stitch Skills：以目前官方 repo 為準

`google-labs-code/stitch-skills` 目前公開的 skill 主要包括：

- `stitch-design`
- `design-md`
- `enhance-prompt`
- `stitch-loop`
- `react-components`（安裝旗標為 `--skill react:components`）
- `shadcn-ui`

安裝方式目前以 `skills` CLI 為主：

```bash
npx skills add google-labs-code/stitch-skills --list
npx skills add google-labs-code/stitch-skills --skill stitch-design --global
npx skills add google-labs-code/stitch-skills --skill design-md --global
npx skills add google-labs-code/stitch-skills --skill enhance-prompt --global
npx skills add google-labs-code/stitch-skills --skill react:components --global
npx skills add google-labs-code/stitch-skills --skill shadcn-ui --global
```

如果筆記裡要提 skill 名稱或安裝指令，務必以 repo README 當下版本為準，因為這些名稱會比文章或影片更新得更快。

## Stitch MCP 與 SDK

官方生態目前可分成兩層：

### MCP / Tool access

- `@google/stitch-sdk` 目前支援直接呼叫 Stitch 的 tool / MCP 能力
- SDK 文件中示例的 server base URL 為 `https://stitch.googleapis.com/mcp`
- 驗證方式可用 `STITCH_API_KEY`，或用 OAuth + `GOOGLE_CLOUD_PROJECT`

### SDK 能做的事

`@google/stitch-sdk` 目前公開支援的能力包括：

- 建立 / 讀取 project
- 從文字 prompt 生成 screen
- 編輯 screen
- 生成 variants
- 取得 HTML 與 screenshot
- 建立 / 更新 design system

這讓 Stitch 比單純「複製匯出程式碼」更像是一個可編排的設計工具層。

## 實務上最容易寫錯的地方

- **把 `DESIGN.md` 寫成「每次建構前自動產出」**：官方目前明確支撐的是 import / export design rules，不是保證每次都自動生成
- **把舊影片裡的模型名當成現在的官方清單**：模型與 UI 命名會漂移
- **把社群工具當成官方主流程**：像 `davideast/stitch-mcp` 這類社群工具可提，但要明確標成替代方案，而不是官方 baseline
- **把主觀體感寫成性能結論**：像「兩個 prompt 就像素級還原」「4 分鐘完成整個驗證」這種句子，都應改成經驗分享口吻或直接刪掉

## 市場反應（若要提數字）

如果要引用 Figma 股價反應，較穩的寫法是：

- Google 於 2026-03-18 發布 Stitch 的「vibe design」更新
- CNBC 於 2026-03-19 報導：Figma 股價 **週三下跌 8%，週四再跌逾 4%，兩日累計約 12%**

這比把「12%」寫成單日最高跌幅要精確得多。

## 相關主題

- [[DESIGN.md-官方規格]] — 官方 base spec 與 canonical 區段
- [[DESIGN.md-使用指南]] — 撰寫原則、品牌範例庫與 extended format
- [[Awesome-Design-MD]] — 各大品牌的 DESIGN.md 範例庫
- [[Claude-Code-前端設計工作流]] — 把 Stitch 放進整體前端設計流程裡看

## 外部來源

### 官方資源

- Stitch 官方頁：<https://stitch.withgoogle.com>
- Stitch「vibe design」官方文章：<https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/>
- DESIGN.md 開源公告：<https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/>
- `@google/stitch-sdk`：<https://github.com/google-labs-code/stitch-sdk>
- `google-labs-code/stitch-skills`：<https://github.com/google-labs-code/stitch-skills>

### 市場反應

- CNBC：<https://www.cnbc.com/2026/03/19/figma-stock-drops-11percent-after-google-releases-vibe-design-product-stitch.html>

### 影片摘要（延伸參考）

- Chase H AI《Claude Code 搭配 Stitch 進行網頁設計》— <https://www.youtube.com/watch?v=qqcpiDXPCvY>
- AILABS-393《現在我這樣用 Google Stitch 設計》— <https://www.youtube.com/watch?v=VNx9Gy5pHZI>
- AILABS-393《Google Stitch 與 Claude Code 的整合方式》— <https://www.youtube.com/watch?v=b0lwCDNOFUY>