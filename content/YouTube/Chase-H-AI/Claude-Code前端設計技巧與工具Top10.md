---
title: Claude Code 前端設計技巧、Plugins 與 CLIs Top 10
tags:
  - youtube
  - claude-code
  - frontend
  - design
created: 2026-04-16
updated: 2026-04-16
published: 2026-04-15
source: https://www.youtube.com/watch?v=Q9ty3eopOPs
---

這部影片介紹 10 種工具與技巧，幫助使用者在 Claude Code 中產出高品質前端設計，對抗千篇一律的「AI slop」美學（紫色漸層、Inter 字體、大量 bento box 卡片）。

## 核心問題：AI Slop

Claude Code 在前端設計上的最大弱點是「taste（品味）」。預設生成物高度雷同：紫色漸層、Inter 字體、相同的卡片排版。以下工具的共同目標都是解決這個問題。

## 工具總覽

### 1. Impeccable（技能 Skill）

- 單一 skill，包含 18 個子指令，涵蓋 UX、排版、元件、跨平台等設計領域
- 網站：impeccable.style，可直觀看到各指令的 before/after 效果
- 核心方法：用「反模式（anti-patterns）」直接告訴 LLM 什麼是 AI slop（例：border accent、glassmorphism、sparklines）——明確說「這是 AI slop，不要做」比說「做出好設計」更有效
- 附 Chrome extension，可在真實網頁上標示 AI slop 元素
- 安裝後約一個月，仍屬新工具

### 2. Skill UI（技能 Skill）

- 可將任意現有網站逆向工程為 Claude Code 可用的 skill
- 使用方式：指向目標網站（如 Stripe、Notion），生成對應設計風格的 skill
- 兩種模式：
  - 標準模式：分析 HTML 結構
  - Ultra 模式：使用 Playwright 抓取滾動截圖與滑鼠互動狀態，更精準
- 適合場景：開始新專案但不確定視覺方向時，以現有網站為起點

### 3. WebGPU Skill（技能 Skill）

- 教 Claude Code 撰寫 WebGPU 相關程式碼，實現網頁與顯示卡直接互動的動畫效果
- 支援：renderer 設定、shader、node-based material
- 適合對進階視覺效果（類似 WebGL、custom shaders）有興趣的使用者
- 學習門檻較高，屬進階工具

### 4. awesome-design.md（技能 Skill）

- GitHub 超過 50,000 stars 的熱門 repo
- 概念來源於 Google Stitch 的「design markdown」（設計系統 prompt）
- 內建多個知名網站的設計系統分解（11labs、Bugatti 等），包含：色彩、排版、按鈕、表單元件、卡片等具體規格
- 與 Skill UI 的差異：提供現成的設計系統 prompt，供使用者選用後自行建構，而非直接複製整個網站

### 5. Stitch（Google 工具）

- awesome-design.md 的靈感來源，由 Google 提供
- 工作流程：
  1. 輸入專案描述 prompt（可附截圖作為靈感）
  2. 自動生成 design markdown（包含色彩、字體、按鈕、標籤等設計系統）
  3. 產出多個版面變體（hero、全站）
  4. 可視覺化調整後，複製程式碼或一鍵轉入 Claude Code
- 優點：在進入 Claude Code 前就能視覺化比較多個方案，節省反覆修改的時間
- 免費；支援 MCP 整合，但作者認為視覺操作更直覺
- 相關延伸影片：作者有發布 Stitch + Claude Code 完整教學

### 6. UI/UX Pro Max（技能 Skill）

- 定位為 Anthropic 官方 frontend design skill 的進化版
- 特點：
  - 在生成前主動詢問問題，了解網站類型與目標用途
  - 161 條產業別設計規則
  - 支援多種前端框架（不限 React）
- 適合場景：沒有特定參考網站、對設計方向還不確定時的起點

### 7. 21st.dev（元件庫）

- 提供大量現成前端元件，可直接複製 prompt 後貼入 Claude Code
- 典型用法：在 21st.dev 找到喜歡的元件（例如帶有燈光跟隨效果的按鈕、滑鼠跟隨的卡片光暈），點「Copy Prompt」，在 Claude Code 貼上即可
- 最大價值：小型精緻細節（按鈕發光、卡片互動、陰影效果）——這些細節讓網站看起來有用心
- 也可作為設計靈感來源：即使不直接使用，也能擴展自己對設計可能性的認知
- 大多數元件免費

### 8. Taste Skill（技能 Skill）

- 嘗試讓 Claude Code 具備「品味」的 skill 集合
- 包含多個子技能，並提供「抽象程度」調節設定
- 效果：生成結果不再千篇一律，有更多滾動動畫、避免重複的 bento box 版型
- 定位：邊際效益型工具，適合想在現有生成結果上再做差異化的使用者

### 9. Google Fonts（字體資源）

- 免費字體庫，包含大量可直接在專案中使用的字體
- Claude Code 預設傾向使用 Inter，不主動選擇多樣字體
- 建議做法：告訴 Claude Code 網站類型與目標感受，讓它推薦 5 個 Google Fonts 字體選項，再從中挑選
- 字體是設計觀感的核心要素，不應交由 Claude Code 隨機決定

### 10. Playwright CLI（測試工具）

- 非純設計工具，但在前端設計流程中不可或缺
- 用途：自動化測試網頁所有互動（表單、按鈕、邊緣情況）
- 優於 Playwright MCP：CLI 模式更高效
- 使用方式：安裝後告訴 Claude Code「用 Playwright CLI 測試這個頁面的所有互動」
  - 支援 headed（可見）或 headless（背景）模式
- 大幅加速前端設計迭代，避免手動測試每個邊緣情況

## 工具選用建議

| 情境 | 推薦工具 |
|------|---------|
| 有參考網站，想直接複製風格 | Skill UI |
| 想選用知名網站設計系統 | awesome-design.md |
| 從零開始，需要視覺化比較多方案 | Stitch |
| 從零開始，想問答式確認方向 | UI/UX Pro Max |
| 需要精緻小元件 | 21st.dev |
| 提升整體生成品質 | Impeccable |
| 差異化視覺風格 | Taste Skill |
| 進階動態效果 | WebGPU Skill |
| 字體選擇 | Google Fonts |
| 前端互動測試 | Playwright CLI |
