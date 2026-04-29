---
title: Impeccable 修補 Claude Code 前端設計痛點
created: 2026-04-29
updated: 2026-04-29
source: https://www.youtube.com/watch?v=0-AosS67IGU
published: 2026-04-27
parent: "[[01.index]]"
tags:
  - youtube
---

## Impeccable 是什麼

- 開源 GitHub repo，本質是**單一 Claude Code skill**，把「設計師才會用的術語、語言與美感判準」灌進 Claude Code，解決 AI 出圖 taste 不足、prompt 太籠統的根本問題
- 雖然只是一個 skill，內含 **23 個 commands** 與 **7 個 domain-specific reference files**，並列出 anti-pattern 清單
- 同時提供 Chrome extension 與 CLI，但作者實測 99% 的價值都在 skill 上，本片只示範 skill 流程
- 安裝只要一行指令貼進 terminal
- 官方網站 `impeccable.style` 對每個 command 都有 before/after 對照，可即時看出 plain Claude Code vs. Impeccable 的差異

## 七大設計支柱

Impeccable 涵蓋的不只是配色，而是橫跨七個面向的完整設計系統：

1. Typography（字體）
2. Color（色彩）
3. Spatial design（空間設計）
4. Responsiveness（響應式）
5. Interactions（互動）
6. Motion（動態）
7. UX writing（介面文案）

## 兩種使用路徑

### A. Greenfield：從零打造網站

入口指令：`impeccable craft`

- 進入類似 plan mode 的訪談流程，產出兩份檔案：
  - `product.md`：產品定位
  - `design.md`：設計系統規範（與 Google Stitch 的 design system 概念一致，作者觀察「design.md 化」正成為產業標準）
- 訪談題量比 Huashu Design 深，接近 Claude Design 的水準（約 13 題：客戶、產品定位、訪客心境、主要 CTA、聲音／視覺、scope 是否只 hero / full scroll、是否有真實截圖等）
- 範例 prompt：

  ```text
  let's build a landing page for my fake SAAS product, Lighthouse.
  It's an analytics platform for solo founders / small teams.
  Ask me any questions you want.
  ```

### B. 編輯既有網站

入口指令：`impeccable document`

- 反向把現有 codebase 逆向工程出一份 `design.md`，再以此為基礎做後續修改
- 配合 `impeccable critique` 取得評分式批判（見下節）

## Macro Layout：一次產三種變體（作者個人技巧）

不要讓 Claude Code 只生一個版面就交差。在 prompt 加上：

- 給我三種**差異明顯**的 layout 變體
- 三個都能點開全螢幕單看
- 同時並排顯示在同一頁，便於比對

範例產出三種風格：

- **Editorial**（經典米白＋襯線字）
- **Drenched**（飽和色塊、大膽配色）
- **Brutalist**（灰階、刻意 offset 的方塊與線條）

作者強調這個技巧不是 Impeccable 獨有，而是從 Google Stitch 學來的工作流，無論用哪個設計 skill 都建議套用，理由是「視覺東西必須親眼看到三種以上才知道自己要哪個方向」。

## Impeccable Live（alpha 階段最大亮點）

進入指令：對指定頁面執行 `impeccable live`，Claude Code 會起本地 server 並回傳 localhost 連結。

進到瀏覽器後可直接點選任一元件，跳出右側 sidebar 操作：

- **Free form**：純文字 prompt 改該元件
- **預設指令**：bolder / quieter / distill / polish / adapt / delight ...（即 23 個 commands 的子集）
- **Variant 數量**：可指定一次出 ×2 / ×3 / ×4 個變體
- **Tune**：對單一變體做 micro 微調（offset 強度、配色、是否顯示 key 等）
- **Detect**：掃描頁面是否有 AI slop 或 anti-pattern；Impeccable 自家產出的頁面通常掃不到問題，自己原本的網站才看得出差異

互動式範例：

```text
bolder + add color × 3
```

意義：用 `bolder` 預設 prompt（推安全設計往「有衝擊力但不混亂」的方向）疊加自訂 prompt `add color`，產出三個 variant，再用 tune 微調，滿意後按 accept 套用。

作者觀點：Live 才是 Impeccable 真正的差異化，micro 調整不必再用 CLI 來回，alpha 階段雖偶有 reload 卡頓，但已經比其他 frontend design skill 領先一截。

## `impeccable critique`：AI Slop 體檢

對既有網站執行 `impeccable critique`，會給出：

- **是否 AI slop 的判決**（borderline / yes / no）
- **10 項 design health 指標**，每項滿分 4，例如「cognitive load」拿 5/8 失敗
- **具體扣分原因**（背景動態與內容互搶、兩個等權重 CTA 優先級不明、service section 用了 4 種視覺語言等）
- **總分等級**（25/40 = acceptable）
- **三條改善方向**讓使用者選 A/B/C 切入

作者本人網站被點出的問題：
- Service card 像「clip art 大雜燴」
- 用了 glass morphism（Impeccable 不喜歡）
- 載入了某字體卻從未使用
- 個人品牌 Chase 本人在站上露出太少（策略缺口）

## 從 Mood Board 啟動的限制

實測把單一 reference image 當 mood board 給 Impeccable craft：

- 風格 vibe 與配色能抓到
- 但因為只有「一張圖」，Impeccable 沒辦法像官方 case study 那樣切片利用，整體輸出比純訪談版還弱
- 可能是 prompting 問題；建議要走這條路就準備多張資產

## 完整工作流總結

1. `impeccable craft`（greenfield）或 `impeccable document`（既有 codebase）建立基線
2. **Macro 階段**：要求三組差異明顯 layout 並排比較，挑一個方向
3. `impeccable live` 進瀏覽器做 micro 變體疊代（bolder / delight / quieter ＋ free form）
4. 滿意後跑 `impeccable polish` 做 design system 最終檢查、`impeccable harden` 處理 edge case 與錯誤
5. 既有網站可加跑 `impeccable critique` 與 `impeccable detect` 做 AI slop 體檢

## 作者結論

- 100% 值得加進設計工具棧，無論是 greenfield 或既有網站
- Live 是上週才加上的功能，是 Impeccable 與其他 frontend design skill 拉開距離的關鍵
- Macro 三變體並排（自己 prompt 出來）＋ micro 變體（Impeccable Live）的組合，是目前最強的 AI 前端設計工作流
