---
title: Gemini 3 GSAP 動畫與 Motion.dev 技巧
tags:
  - youtube
  - gemini
  - animation
  - frontend
created: 2026-04-14
updated: 2026-04-14
published: 2025-12-24
source: https://www.youtube.com/watch?v=oL6bLQOXwAY
---

## 兩個核心動畫函式庫

### GSAP — 複雜捲動動畫

適合 landing page 的 scroll-driven animation：
- 以 ScrollTrigger 將動畫進度直接綁定到用戶捲動量
- `scrub` 選項：動畫隨捲動前進/後退，產生「活的」互動感
- 可按字符、行、段落分別驅動文字動畫

### Motion.dev（前身 Framer Motion）

適合 React 應用內的 UI 狀態動畫與 micro interaction：
- 模型訓練資料最多，準確率最高
- 可模擬 cursor 動作（需用 `useRef` 取 bounding box 而非 hard-code 座標）
- 支援 self-playing 展示動畫（用於 landing page product showcase）

## 為什麼預設結果很普通

Distributional convergence 問題：模型根據訓練資料的統計分佈預測 token，通用且安全的設計佔多數，導致預設輸出千篇一律。

解法：分離創意思考與實作。

## 正確流程

1. **先規劃**：給模型具體的動畫時序描述（不要給「酷炫動畫」這種模糊指令）
2. **具體化**：說明 layout 結構、元素如何移動、持續時間
3. **再實作**：讓模型專注把規劃轉成程式碼

### 規劃用 Prompt 範例（GSAP）

```
Create a horizontal scroll animation using GSAP ScrollTrigger.
Layout: a continuous horizontal text flow (not full-screen slides).
Use a single container so items flow naturally next to each other.
Embed visual elements like SVG curves inline with text.
Should feel like reading a long sentence, not flipping slides.
```

## 利用模型幫規劃動畫

在 Google AI Studio 設置系統指令：
```
You are a world-class GSAP motion designer.
Think deeply about the epicenter of design and the one core interaction that makes users say "wow".
Tie back to scroll scrub so the interaction feels live.
Think through all animated elements, timeline, transformations one by one.
Constraints: No 3D models, complex SVG, or video assets—only HTML/CSS/JS.
```

## Motion.dev MCP 工具

加入 motion.dev 的 MCP server 可給 agent 載入 Framer Motion 官方文件，提高動畫程式碼正確率（只有兩個工具：list docs / read doc，token 消耗低）。
