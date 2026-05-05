---
title: Impeccable — 前端設計 Skill
created: 2026-05-05
updated: 2026-05-05
source: https://impeccable.style
tags:
  - claude-code
  - skill
  - design
  - frontend
---

> 1 個 Claude Code skill（含 23 commands + 7 references + 27 條 deterministic anti-pattern 規則）灌入「設計師術語、判準與美感」，解 AI 預設前端輸出的 slop 問題。同時支援 Cursor、Gemini CLI、Codex、VS Code Copilot，跨 harness 可用。詳見 [[Claude-Code-前端設計工作流]] 的 Layer 1 脈絡。

## 解什麼問題

Coding agent 預設前端輸出高度雷同：紫色漸層、Inter、bento box、過度 card nesting、灰底灰字、鈍化的 easing。Impeccable 的論點是「**根本不是工具不夠、是 taste 不夠**」，所以把設計師的術語（七大面向）與反模式直接灌進 skill，agent 讀完才寫 code。

## Skill 結構

- 演進邏輯：作者把原本 **18 個獨立 design skills 合併為 1 skill + 23 commands**——少觸發碰撞、共享資料層
- **27 條 deterministic anti-pattern 規則** + **12 條 LLM critique 規則**

七大設計面向（reference 對應）：

1. Typography
2. Color & Contrast
3. Spatial Design
4. Motion Design
5. Interaction Design
6. Responsive Design
7. UX Writing

## 23 commands 分類

| 類別 | 命令 |
|------|------|
| 啟動／脈絡 | `teach`（建專案設計脈絡）、`document`（產 DESIGN.md）、`extract`、`onboard` |
| 從零打造 | `craft`（從 approved mock 出 code）、`shape`、`layout` |
| 領域微調 | `typeset`、`colorize`、`animate`、`delight`、`adapt`、`optimize`、`clarify` |
| 風格強度調整 | `bolder`、`quieter`、`distill`、`harden`、`polish`、`overdrive` |
| 體檢／批判 | `audit`（找 anti-pattern）、`critique`（design heuristics 評分） |
| 互動模式 | `live`（瀏覽器內微調，目前 alpha） |

## 兩種工作流

### A. Greenfield：從零打造

1. `teach` 或 `craft`：訪談式建立 product / design 兩份脈絡（DESIGN.md 化已成行業趨勢）
2. **Macro 階段**：要求 3 種**差異明顯**的 layout 並排比較。這個技巧**不限 Impeccable**——任何前端設計 skill 都建議套用，理由：視覺方向必須親眼看到三種以上才好決定
3. **Micro 階段**：`live` 進瀏覽器，點元件後下文字 prompt 或預設指令（`bolder` / `quieter` / `distill` / `polish` / `adapt` / `delight`），指定 variant 數量（×2/3/4），對單一 variant 做 tune
4. 收尾：`polish` 對齊 design system、`harden` 處理 edge case

### B. 編輯既有網站

1. `document`：把現有 codebase 逆向工程成 DESIGN.md
2. `critique`：評分式批判（design health 指標、是否 AI slop、給 3 條改善方向 A/B/C 讓使用者選）
3. `audit`：找具體 anti-pattern

## Live 模式（目前 alpha）

對指定頁面執行 `impeccable live` 啟動本地 server。瀏覽器內：

- 點任一元件 → 跳右側 sidebar
- 對該元件下文字 prompt 或預設指令（同上 bolder/quieter/...）
- 指定 variant 數量（×2 / ×3 / ×4）
- 對單一 variant 做 tune（offset 強度、配色微調）
- accept 套用

差異化：micro 調整不必回 CLI 來回，比純 prompt 工作流更貼近設計師實際操作。

## 限制與注意

- **Mood Board 單圖輸入效果差**：訪談式輸入比給單張參考圖更有效；走 mood board 流程需準備多張資產
- **alpha 階段的 Live**：偶有 reload 卡頓
- **`document` 產的 DESIGN.md** 與專案實際 design tokens 對齊偶爾要手動修

## 跟既有 Topics 的關係

- [[Claude-Code-Skills]] 介紹 skill 通用機制（progressive disclosure、metadata）；本 Card 是「複雜 skill 結構（多 commands + 多 references + anti-pattern 規則）」的具體案例
- [[Claude-Code-前端設計工作流]] 的 Layer 1（Skill 注入）已將 Impeccable 列為入口工具；本 Card 是該段的細節展開

## 來源

- 官網：<https://impeccable.style>
- Repo：<https://github.com/pbakaus/impeccable>
- 影片：Chase H AI《Impeccable 修補 Claude Code 前端設計痛點》— <https://www.youtube.com/watch?v=0-AosS67IGU>
