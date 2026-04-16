---
title: Claude Code 前端設計七層級
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-26
source: https://www.youtube.com/watch?v=1PXFAFMgdns
parent: "[[01.index]]"
---

## 層級一：只有 Prompt

基礎起點。直接用文字描述讓 Claude Code 建立頁面。

問題：沒有設計方向，AI 填補創意空缺的結果是紫色漸層、通用 SaaS 模板。根本原因是「你不知道好的設計長什麼樣子，就無法用文字告訴 Claude Code」。

Plan Mode 會問些表層問題（顏色風格、框架選擇），但仍不夠。

## 層級二：引入設計技能

加入外部設計 Prompt 技能，例如：
- **UIUX Pro Max Skill**（GitHub，52,000 星）：注入配色、排版、間距觀念，並列出 AI 常見設計陋習要避免
- 安裝指令：`/plugin marketplace` 搜尋後安裝，或用 URL 讓 Claude Code 自動安裝
- 呼叫方式：`/frontend-design <prompt>` 或自然語言「用前端設計技能修改」

效果明顯但仍是 AI 模板感，因為核心問題未解：無法描述你真正想要的視覺。

## 層級三：視覺導演（給參考截圖）

轉變策略：從「描述」改為「展示」。

靈感來源：
- **Awwwards**（awwwards.com）：業界頂尖前端設計
- **Godly.website**：無限捲動設計展示
- **Pinterest**：搜尋「SaaS landing page」
- **Dribbble**：搜尋各類 UI 設計

操作：截圖喜歡的頁面，直接拖入 Claude Code，說「我希望風格接近這個」。

天花板：截圖 → 程式碼有天然的轉換損失，近似但不精準，反覆截圖迭代效率低。

## 層級四：複製者（取得原始程式碼）

突破層三瓶頸：不只看外觀，要拿到 HTML、CSS、JavaScript。

方法：
1. `Ctrl+U` 取得 HTML，複製全部貼入 Claude Code
2. HTML 底部有 CSS / JS 檔案連結，讓 Claude Code 用 **Site Teardown 技能**（增強版 web fetch）完整抓取
3. 提供截圖作為視覺補充

結果：Claude Code 能輸出完整技術分析（使用的框架如 GSAP、ScrollTrigger、Lenis，各種動效實作方式），並以此為基礎重建頁面，第一次嘗試就能達到 80~90% 相似度。

副產品：讓 Claude Code 解釋「這個效果是怎麼做到的」，每次複製一個網站就增加一個技術認知。

## 層級五：個人化（加入原創元素）

從複製轉向創作：

- **元件**：從 21st.dev、CodePen、Monaé 找高品質元件，直接複製 prompt 整合
- **自製素材**：用 MidJourney / Nano Banana Pro 生成品牌藝術圖，配合 Kling 3.0 / Veo 3.1 加入微動態背景影片（15 秒、動作細微）
- **視覺說故事**：讓頁面素材與應用主題有連結（範例：Argus 社群情報 App → 千眼神 Argus 意象 → 標語「See what's next」）
- **排版**：使用 Google Fonts，字型影響質感很大

進階細節提升質感：頁面載入動畫、計數器動態跳升、高光掃過效果、捲動進度條。

## 層級六：外部視覺工具輔助

當在 terminal 裡用文字調整視覺細節已不夠高效，引入：
- **Stitch**（Google，免費）：視覺畫布，可生成重設計、調整 variants
- **Pencil.dev**：在 VS Code / Cursor 側邊即時編輯
- **Figma / paper.design**

流程：在工具中生成設計稿 → 截圖 → 貼回 Claude Code 說「照這個做」

## 層級七：前端建築師（自訂 WebGL / 3D）

目前超出一般使用者能力範圍。需要客製 WebGL、shader、3D 互動體驗，類似電玩等級視覺。2026 年 3 月 AI 還無法有效輔助這個層級。

---

**核心論點**：前端設計瓶頸不是 AI 沒品味，而是使用者無法用文字表達品味。解決路徑是持續暴露在高水準設計中，再透過複製、拆解、重建逐漸建立設計語彙。
