---
title: Claude Code 前端設計工作流
created: 2026-04-20
updated: 2026-05-27
tags:
  - claude-code
  - design
  - frontend
---

涵蓋 AI slop（AI 生成 UI 千篇一律）的本質、七層工作流分層、核心原則。

## 核心問題：AI Slop

Claude Code 在 agentic coding（自主代理寫程式）表現卓越，但前端設計是普遍弱項。預設生成物高度雷同：紫色漸層、Inter 字體、bento box（便當盒式格狀排版）卡片、通用 SaaS 模板。

根本原因兩層：

- **模型面**：訓練資料相近，AI 在沒有設計方向時收斂到「平均值」審美
- **使用者面**：品味瓶頸——不知道好的設計長什麼樣，就無法用文字告訴模型要什麼

所有解法都在處理這兩層之一。

## 七層工作流

按**介入深度**由淺到深排列，每層解上一層的瓶頸。

### Layer 1：Skill 注入

最低成本介入，用 Skill 把設計觀念灌進 agent。四種互補方向：

- **[Impeccable](https://impeccable.style)**（[repo](https://github.com/pbakaus/impeccable)）：1 個 skill + 23 個設計命令，用**反模式**（anti-patterns）直接列舉 AI slop。詳見 [[bookmark-Impeccable-前端設計Skill|Impeccable]]
- **[UI UX Pro Max](https://www.uupm.cc/)**（[repo](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)）：提供 style / color / typography / landing pattern 的設計資料庫與 design-system generation
- **[Taste Skill](https://www.tasteskill.dev)**（[repo](https://github.com/Leonxlnx/taste-skill)）：用 `DESIGN_VARIANCE`、`MOTION_INTENSITY`、`VISUAL_DENSITY` 三個參數調節風格強度，適合差異化
- **[awesome-design-md](https://github.com/VoltAgent/awesome-design-md)**：DESIGN.md 範例庫（ElevenLabs / Bugatti 等知名網站設計系統拆解），詳見 [[bookmark-Awesome-Design-MD-設計範例庫|Awesome-Design-MD]]

**局限**：只解了模型面（給設計觀念），沒解使用者面（品味瓶頸）。

### Layer 2：視覺參考

轉策略：不描述，直接給截圖。

- **[Awwwards](https://www.awwwards.com)**（[[bookmark-Awwwards-前端設計靈感站|Awwwards]]）、Godly.website、Pinterest、Dribbble
- 操作：截圖 → 拖入 Claude Code → 「風格接近這個」

**瓶頸**：截圖 → 程式碼有天然轉換損失，近似但不精準，反覆截圖迭代效率低。

### Layer 3：逆向工程

突破截圖瓶頸：拿 HTML/CSS/JS。

- **手動 teardown**：`Ctrl+U` 複製 HTML 貼給 Claude Code，門檻低但要自己整理
- **[Skill UI](https://skillui.vercel.app/)**：自動化前者；Ultra 模式用 Playwright 抓滾動截圖、hover/focus、動畫 keyframe

**額外收穫**：讓 Claude Code 解釋「這個效果是怎麼做到的」，每複製一個網站就多一個技術認知。

### Layer 4：Flow Engineering

不追求完美 prompt，把資深設計師的思考過程拆成步驟流。

四步驟：

1. **Layout**：先用 ASCII wireframe 對齊版面（生成 ~1 秒，可快速迭代）
2. **Theme**：用 [Tweakcn](https://tweakcn.com) 調 Shadcn 主題，複製 CSS 變數貼給 agent
3. **Animation**：讓模型列出需要動畫的元素 + keyframe + 觸發時機
4. **實作**：有 layout + theme + animation 三層 context，一次生成品質大幅提升

**[SuperDesign](https://superdesign.dev)**：IDE 內 infinite canvas（無限延展畫布）並排多變體，內建此流程。

### Layer 5：設計工具整合

文字不夠高效時，引入視覺工具。

- **Figma MCP + Shadcn MCP**（Vibe Design）：把 Figma frame、元件資訊與 registry 線索交給 agent 落地；若設計稿命名乾淨、元件選型一致，還原會更穩，但不應寫成保證式的像素級還原
  - 若 Figma 稿用 Shadcn 元件且 layer 名對應，Shadcn MCP 自動從 registry 抓元件
  - 第三方 Shadcn registry：Fancy Components、Animate UI、Magic UI、Plate UI
- **[Stitch](https://stitch.withgoogle.com/)**（[[bookmark-Stitch-AI設計畫布|Stitch]]）：視覺畫布生成 variants，可匯出程式碼或轉入 Claude Code
- **[Pencil](https://www.pencil.dev/)**：VS Code / Cursor 側邊的 infinite vector canvas（無限延展向量畫布），邊畫邊生成 React/Tailwind，透過 MCP 與 Claude Code 溝通（[[Pencil-讀取規則]]）
- **[Figma](https://www.figma.com/)** / **[paper.design](https://paper.design/)**：傳統與新興向量設計工具，截圖或匯出後給 Claude Code 實作

流程：工具生成設計稿 → 截圖或匯出 → Claude Code 實作。

### Layer 6：個人化

從複製轉向創作。

- **元件**：[21st.dev](https://21st.dev/)、[CodePen](https://codepen.io/) 找高品質元件，直接複製 prompt
- **自製素材**：Midjourney / Nano Banana Pro 生成品牌藝術圖，配 Kling / Veo 做細微動態 Hero（首屏主視覺）背景影片（[[Nano-Banana-動態-Hero-Section]]）
- **視覺說故事**：素材與應用主題連結（例：Argus 情報 App → 千眼神意象 → 「See what's next」）
- **排版**：主動指定 Google Fonts（Claude Code 預設偏 Inter，不會主動換字體）
- **質感細節**：頁面載入動畫、計數器跳升、高光掃過、捲動進度條、GSAP + Lenis 捲動動畫（[[GSAP-與-Lenis-捲動動畫分工]]）

### Layer 7：前端建築師（超出 AI 輔助範圍）

客製 WebGL、shader、3D 互動，電玩等級視覺。目前 AI 還無法有效輔助這層，**[WebGPU Skill](https://github.com/dgreenheck/webgpu-claude-skill)**（給 Three.js + TSL（Three.js Shading Language，著色器語言）用的 Claude Code skill）是少數能嘗試的工具。

## 核心原則

- **反模式 > 正模式**：明確說「這是 AI slop，不要做」比「做出好設計」更有效
- **版面優先**：先對齊 layout 再談 theme，避免在錯版面上調風格
- **展示 > 描述**：截圖、原始碼、參考元件，都比純文字 prompt 有效
- **持續暴露**：瓶頸在使用者品味，解法是複製 + 拆解 + 重建，累積設計語彙

## 常見陷阱

| 徵兆 | 原因 | 解法 |
|---|---|---|
| 生成物仍像 AI 模板 | 只停在 Layer 1，沒給視覺參考或原始碼 | 往 Layer 2-3 推進，給截圖或 HTML |
| 截圖迭代無限輪 | 純視覺還原有損失 | 往 Layer 3 拿原始碼，或 Layer 5 Figma MCP |
| 版面有了但主題質感停在範本感 | 沒做 theme，色彩 / 字型 / 陰影靠模型亂猜 | Layer 4 用 Tweakcn 把主題變數定下來 |
| 用 Inter 字體、版面對但不耐看 | 沒有質感細節 | Layer 6 補 Google Fonts + 動畫/素材 |

## 相關

- [[bookmark-Impeccable-前端設計Skill|Impeccable]] — Layer 1 工具細節
- [[bookmark-Awesome-Design-MD-設計範例庫|Awesome-Design-MD]] — Layer 1 範例庫
- [[Pencil-讀取規則]] — Layer 5 工具的使用規則
- [[bookmark-Stitch-AI設計畫布|Stitch]] — Layer 5 工具的深度細節
- [[bookmark-DESIGN.md-設計系統規格|DESIGN.md]] — 設計系統文件格式規範
- [[動效與互動]] — Layer 6 動效深度

## 來源

- [Claude Code 前端設計七層級（Chase H AI）](https://www.youtube.com/watch?v=1PXFAFMgdns)
- [前端設計技巧、Plugins 與 CLIs Top 10（Chase H AI）](https://www.youtube.com/watch?v=Q9ty3eopOPs)
- [如何擺脫千篇一律的 AI 風 UI（AIJasonZ）](https://www.youtube.com/watch?v=Nocg_8ECs6w)
- [Vibe Design 工作流：Figma MCP + Shadcn MCP（AIJasonZ）](https://www.youtube.com/watch?v=4j51FMU-SUQ)
