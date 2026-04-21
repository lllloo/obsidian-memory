---
title: Claude Code 前端設計工作流
created: 2026-04-20
updated: 2026-04-21
tags:
  - claude-code
  - design
  - frontend
  - moc
---

涵蓋 AI slop 的本質、工作流策略分層、工具速查、與核心原則。

## 核心問題：AI Slop

Claude Code 在 agentic coding 表現卓越，但前端設計是普遍弱項。預設生成物高度雷同：紫色漸層、Inter 字體、bento box 卡片、通用 SaaS 模板。

根本原因有兩層：

- **模型面**：訓練資料相近，AI 在沒有設計方向時會收斂到「平均值」審美
- **使用者面**：品味瓶頸——不知道好的設計長什麼樣子，就無法用文字告訴模型要什麼

所有解法都在處理這兩層之一。

## 工作流策略分層

按**介入深度**由淺到深排列。每一層都在解決上一層的瓶頸。

### Layer 1：Prompt 注入（用 Skill 灌觀念）

最低成本的介入，安裝 Skill 讓 Claude Code 拿到「設計觀念」。

- **[Impeccable](https://impeccable.style)**（[repo](https://github.com/pbakaus/impeccable)）：18 個子指令，用**反模式**（anti-patterns）直接列舉 AI slop
- **[UI/UX Pro Max](https://ui-ux-pro-max-skill.nextlevelbuilder.io/)**（[repo](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)）：官方 frontend-design skill 進化版，涵蓋 161 種產品類別的推理規則，生成前會問答確認方向
- **[Taste Skill](https://www.tasteskill.dev)**（[repo](https://github.com/Leonxlnx/taste-skill)）：用 `DESIGN_VARIANCE`（1–10，從乾淨置中到非對稱現代）與 `MOTION_INTENSITY` 兩個參數調節風格強度，適合差異化
- **[awesome-design-md](https://github.com/VoltAgent/awesome-design-md)**：概念源自 Google Stitch 的 DESIGN.md，內建 ElevenLabs / Bugatti 等知名網站的設計系統拆解

**局限**：還是 AI 模板感，核心問題沒解——使用者仍無法描述真正想要的視覺。

### Layer 2：視覺參考（從描述改為展示）

轉策略：不描述、直接給截圖。

靈感來源：

- **Awwwards**（[[Awwwards-找前端設計靈感]]）、Godly.website、Pinterest、Dribbble
- 操作：截圖 → 拖入 Claude Code → 「風格接近這個」

**瓶頸**：截圖 → 程式碼有天然轉換損失，近似但不精準，反覆截圖迭代效率低。

### Layer 3：逆向工程（拿到原始碼）

突破截圖瓶頸：不只看外觀，拿 HTML/CSS/JS。

- **手動 teardown**：`Ctrl+U` 複製 HTML 貼給 Claude Code，讓它分析並抓出 CSS/JS 結構。門檻低但要自己整理
- **[Skill UI](https://skillui.vercel.app/)**：把任意網站逆向工程成 Claude Code 可用的 skill，自動化上一條的流程
  - 標準模式靜態分析 HTML/CSS，Ultra 模式用 Playwright 抓滾動截圖、hover/focus 狀態、動畫 keyframe
- 第一次嘗試可達 80–90% 相似度（影片作者示範估值）
- **額外收穫**：讓 Claude Code 解釋「這個效果是怎麼做到的」，每複製一個網站就多一個技術認知

### Layer 4：Flow Engineering（拆解設計思考）

不追求完美 prompt，把資深設計師的思考過程拆成步驟流。

**四步驟**：

1. **Layout**：先用 ASCII wireframe 對齊版面（生成 ~1 秒，可快速迭代）
2. **Theme**：用 [Tweakcn](https://tweakcn.com) 調 Shadcn 主題，複製 CSS 變數貼給 agent
3. **Animation**：讓模型列出需要動畫的元素 + keyframe + 觸發時機
4. **實作**：有 layout + theme + animation 三層 context，一次生成品質大幅提升

**[SuperDesign](https://superdesign.dev)**（[repo](https://github.com/superdesigndev/superdesign)）：IDE 內 infinite canvas 並排多變體，內建此流程，支援 Cursor / Windsurf / Claude Code / VS Code。

### Layer 5：設計工具整合（視覺化 + MCP）

文字不夠高效時，引入視覺工具。

- **Figma MCP + Shadcn MCP**（Vibe Design）：Figma 選 frame 複製 link → Claude Code「implement 100% pixel perfect」→ 兩個 prompt 內達像素級還原
  - 若 Figma 稿用 Shadcn 元件且 layer 名對應，Shadcn MCP 自動從 registry 抓元件
  - 第三方 Shadcn registry：Fancy Components、Animate UI、Magic UI、Plate UI
- **Stitch**（[[Stitch]]）：視覺畫布生成 variants，可匯出程式碼或轉入 Claude Code
- **[Pencil](https://www.pencil.dev/)**：VS Code / Cursor 側邊的 infinite vector canvas，邊畫邊生成 React/Tailwind，透過 MCP 與 Claude 溝通
- **[Figma](https://www.figma.com/)** / **[paper.design](https://paper.design/)**：傳統與新興向量設計工具，截圖或匯出後給 Claude Code 實作

流程：工具生成設計稿 → 截圖或匯出 → Claude Code 實作。

### Layer 6：個人化（加入原創元素）

從複製轉向創作：

- **元件**：[21st.dev](https://21st.dev/)、[CodePen](https://codepen.io/) 找高品質元件，直接複製 prompt
- **自製素材**：Midjourney / Nano Banana Pro 生成品牌藝術圖，配 Kling 3.0 / Veo 3.1 做細微動態背景影片（見 [[Nano-Banana-動態-Hero-Section]]）
- **視覺說故事**：素材與應用主題連結（例：Argus 情報 App → 千眼神意象 → 「See what's next」）
- **排版**：主動指定 Google Fonts（Claude Code 預設偏 Inter，不會主動換字體）
- **質感細節**：頁面載入動畫、計數器跳升、高光掃過、捲動進度條、GSAP + Lenis 捲動動畫（見 [[GSAP-與-Lenis-捲動動畫分工]]）

### Layer 7：前端建築師（超出 AI 輔助範圍）

客製 WebGL、shader、3D 互動，電玩等級視覺。目前 AI 還無法有效輔助這層，**[WebGPU Skill](https://github.com/dgreenheck/webgpu-claude-skill)**（給 Three.js + TSL 用的 Claude skill）是少數能嘗試的工具。

## 工具速查

| 情境 | 推薦工具 | 所屬層級 |
|------|---------|----------|
| 直接複製參考網站風格 | Skill UI / 手動 teardown | 3 |
| 用知名網站設計系統 | awesome-design-md（[[Awesome-Design-MD]]） | 1 |
| 從零比較多方案 | Stitch / SuperDesign | 4, 5 |
| 從零問答式確認方向 | UI/UX Pro Max | 1 |
| 需要精緻小元件 | 21st.dev | 6 |
| 整體品質提升 | Impeccable | 1 |
| 差異化視覺 | Taste Skill | 1 |
| 像素級還原 Figma | Figma MCP + Shadcn MCP | 5 |
| 主題（色彩/字型/陰影） | Tweakcn | 4 |
| 字體選擇 | Google Fonts | 6 |
| Hero 動態背景 | Nano Banana Pro + Kling 3.0 | 6 |
| 進階動態效果 | WebGPU Skill | 7 |
| 前端互動測試 | Playwright CLI | 通用 |

「通用」表示不屬於 Layer 1–7 的設計層級分類，屬跨層級的測試輔助工具。

## 核心原則

- **反模式 > 正模式**：明確說「這是 AI slop，不要做」比「做出好設計」更有效
- **版面優先**：先對齊 layout 再談 theme，避免在錯版面上調風格
- **展示 > 描述**：截圖、原始碼、參考元件，都比純文字 prompt 有效
- **持續暴露**：瓶頸在使用者品味，解法是複製 + 拆解 + 重建，累積設計語彙

## 常見陷阱

**徵兆：生成物仍像 AI 模板**
- 原因：只停在 Layer 1，沒給視覺參考或原始碼
- 解法：往 Layer 2–3 推進，給截圖或 HTML

**徵兆：截圖迭代無限輪**
- 原因：純視覺還原有損失，反覆對齊成本高
- 解法：往 Layer 3 拿原始碼，或用 Layer 5 的 Figma MCP 做像素級整合

**徵兆：生成品質在 60% 天花板**
- 原因：沒做 theme，色彩/字型/陰影靠模型隨機
- 解法：Layer 4 用 Tweakcn 產 CSS，主題品質可拉到 90%+

**徵兆：用 Inter 字體、版面對但不耐看**
- 原因：沒有質感細節
- 解法：Layer 6 補 Google Fonts + 動畫/素材

## 相關主題

- [[Stitch]] — Google Stitch 主題 MOC（Layer 5 工具的深度細節）
- [[DESIGN.md-Google-Stitch-設計系統文件格式]] — 設計系統文件格式規範
- Claude Design（MOC 待建立）— Claude 官方視覺設計介面，留作後續獨立整理

## 來源

**影片**

- [Claude Code 前端設計七層級（Chase H AI）](https://www.youtube.com/watch?v=1PXFAFMgdns)
- [Claude Code 前端設計技巧、Plugins 與 CLIs Top 10（Chase H AI）](https://www.youtube.com/watch?v=Q9ty3eopOPs)
- [如何擺脫千篇一律的 AI 風 UI（AIJasonZ）](https://www.youtube.com/watch?v=Nocg_8ECs6w)
- [Vibe Design 工作流：Figma MCP + Shadcn MCP（AIJasonZ）](https://www.youtube.com/watch?v=4j51FMU-SUQ)
