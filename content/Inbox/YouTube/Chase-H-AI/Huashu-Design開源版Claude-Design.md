---
title: Huashu Design — 開源版 Claude Design 實測
created: 2026-04-27
updated: 2026-04-27
source: https://www.youtube.com/watch?v=Nmk1wxoi6ys
published: 2026-04-26
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - claude-design
---

## 核心定位

- Huashu Design 是一個剛釋出的開源 GitHub repo，將 Claude Design 的 system prompts 與設計哲學重新打包成一個 skill，可載入 Claude Code、Codex 或任意 coding agent 使用
- 解決 Claude Design 的最大痛點：即便訂閱 20x 方案，weekly usage 不到一小時就會用完；改用 skill 後吃的是 Claude Code 的 context / 訂閱額度，不再被 Claude Design 的獨立配額綁住
- 雖然表面是「一個 skill」，底下其實掛了 20 份 markdown 深度指南（slide deck、設計風格、動畫最佳實務等）、components 與 assets 庫，以及一條完整的 executable toolchain（HTML → MP4、Playwright 驗證實際渲染）

## 三回合對比測試

作者用同樣的 prompt 同時餵 Claude Design 與 Huashu Design 做頭對頭比對。

### Test 1：從零生成 SaaS 落地頁

- Prompt：用 design skill 為虛構 SaaS 產品 Lighthouse 做落地頁，先問需求再開工
- Huashu 反問 6 個問題（產品定位、目標族群、vibe、需要區塊、變體數、文案來源），Claude Design 問題類似但提供視覺方向選項
- 雙邊都要求三個 variant：Huashu 給出 ledger / terminal / paper 三種風格，並排呈現；Claude Design 給出 terminal / editorial / spatial，作者吐槽 spatial 那版「典型 AI slop」漸層感
- 作者強調這個比對不是看誰絕對好看，而是 Huashu skill 的成果與 Claude Design 「非常接近」就是大勝
- Tweaks 對比：
  - Claude Design 的 tweaks 已內建在介面，可即時切換明暗、accent、headline，且分 spatial / global 兩層
  - Huashu 的 tweaks 同樣可換 preset、display family、dark mode、accent、layout density、trust strip 顯示等，項目較少但「再 prompt 一次就能補」
- 用量結算：Claude Design 此測就吃掉 15% 週用量；Huashu skill 此測吃 170K tokens，幾乎用不到 20x 方案週用量的 1%

### Test 2：套既有 design system 重做落地頁

- 把作者既有的 Agentic OS dashboard 拆成 design system，要求兩邊用同一套設計風重做 Lighthouse 落地頁
- Claude Design 約 3 分鐘完成、吃掉 10% 週用量，並順手把 dashboard 也重建一份塞進落地頁
- Huashu skill 約 11 分鐘、70K tokens，整體配色字體與設計系統一致，但細節（terminal 區塊未置中、sprite logo 略有差異）稍弱
- 結論：Claude Design 整體略勝（因為它本來就有預載的 design system 概念），但 Huashu skill 是「現場自己拼出 design system」，差距相對於成本完全可接受

### Test 3：簡報 Slide Deck

- 兩邊都要求沿用同一套 design system 為 Lighthouse 生簡報
- Claude Design 幾分鐘完成，吃掉 6% 週用量；封面 sprite 略被拉伸
- Huashu skill 結果與 Claude Design 風格高度一致：封面、頁二、頁三都到位，僅頁四裁切、末頁文字略重疊，皆屬一個 prompt 可修
- 結論：第三項測試 Huashu skill 再次與 Claude Design 打成接近平手

## 結論

- 真空中比較 Claude Design 仍勝出：原生 GUI 的 draw / edit / comment / 團隊協作是 skill 永遠做不到的
- 但對「不需要 GUI 互動、只要拿到設計成品」的多數使用者，Huashu skill 已經足夠取代 Claude Design，且不再被 weekly usage 卡住
- 比起 Claude Code 內建的 front-end design skill，Huashu skill 是明顯升級
- Skill 不只能做網頁與簡報，還涵蓋 motion design、infographic 等項目，建議直接試用
