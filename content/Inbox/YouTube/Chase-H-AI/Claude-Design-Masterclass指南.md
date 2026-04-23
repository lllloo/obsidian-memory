---
title: Claude Design Masterclass 深度指南
created: 2026-04-20
updated: 2026-04-20
source: https://www.youtube.com/watch?v=iJRq1kLLRmY
published: 2026-04-19
parent: "[[01.index]]"
tags:
  - youtube
---

## 核心定位

- Claude Design 是 Anthropic 對 Google Stitch 的回應，提供視覺化介面生成 web app、mobile app、slide deck 的 mock-up
- 只能在 web app（`claude.ai/design`）使用，Claude Code 與 desktop app 皆不支援
- 使用 Opus 4.7 時 screenshot fidelity 為 Opus 4.6 的 3 倍，處理圖片類輸入更精準
- Pro、Max 5、Max 20x 用戶共用同一個 weekly usage 額度，與原本 Claude 訂閱額度分開但上限一致

## 兩大核心價值：variants 與 tweaks

與 Claude Code 相比，Claude Design 一次成形（one-shot）的結果差異不大，真正拉開差距的是**快速迭代**：

- **Variants（宏觀）**：要求產出數種完全不同風格的設計（terminal、editorial、hypermaximal、brutalist、synth wave、soft pastel、print newspaper 等），在 macro 層級挑方向
- **Tweaks（微觀）**：對單一版本調整色盤、accent、corner radius、background grid、font、emphasis、headline、layout，全部即時預覽
- 建議工作流：先跑 variants 選定大方向 → 再對該版本 aggressively 增加 tweaks → 最後 export 到 Claude Code 做工程化整合

## 設定與使用流程

### Design System（品牌風格模板）

- 可上傳 GitHub repo、本地資料夾、字型、logo、assets，讓 Claude Design 擷取品牌風格形成可複用模板
- **資源消耗巨大**：單次建立需 5–15 分鐘處理，直接吃掉 weekly usage 的 20–25%
- 建議：僅在確定要大量沿用某一品牌時建立一個，不要一次建立多個

### 起新專案的三個設定

1. **Design system**：選既有的或 none
2. **Fidelity**：wireframe 或 high-fidelity（可隨時切換）
3. **Context 輸入**：design system、screenshot、codebase、Figma 檔；也可以在畫布上用 sketch / pen / text / sticky note 示意排版

### 建議使用 plan mode 強化輸入

- 在 prompt 結尾加「ask me questions before you build anything」可觸發類 plan mode
- 實測 Claude Design 會問 10–15 題（vs Claude Code plan mode 通常僅 3–8 題），能顯著降低後續 iteration 次數與 usage 消耗

## 三類專案的實作重點

### Web app landing page

- 零 context 的裸 prompt 成本約 4% weekly usage 一版
- 加入 aggressive tweaks 再 +7%、加兩個 variants 再 +5%，完整 landing page 流程總計約 17%
- 可針對任一區塊在 edit mode 下調整 opacity、width、color 等細節

### Slide deck

- 本影片以 Agentic OS design system 產出「Claude Design vs Google Stitch」五頁簡報，約 5% usage（每頁約 1%）
- 有 design system 時輸出品牌一致性明顯優於 Claude Code 拿同一 prompt 產生的結果
- 同樣可用 variants + tweaks 流程精修

### Mobile app

- 直接起 mobile 專案：prompt 內指明「for a mobile app」即可
- Web app → mobile：在原專案右上 share → **duplicate project**，產生 `<原名>-remix`，再 prompt「show me the same design in mobile format」
- 會自動為所有現有 web variants 生成對應 mobile 版本，本次示例 9 個 mock-up 共 5% usage

## 協作與輸出

- **Comment**：點選任一元素留言，可立即送 Claude 或加入佇列供團隊成員批註
- **Draw / pen / sticky note**：直接在畫布上標示想調整的位置
- **Share**：與團隊成員共同編輯同一份設計
- **Export**：下載 zip、PDF、PowerPoint、送 Canva、送 HTML，或直接複製一行指令丟進 Claude Code

## 與 Claude Code 的定位切分

- Claude Code：工程化、跑完整 dev loop、最終整合
- Claude Design：純視覺迭代階段，加速「看到選項 → 挑一個 → 微調」的前端設計循環
- 最佳流程是 Claude Design 先達到 80–90% 的視覺完成度（variants + tweaks），再 export 到 Claude Code 實作後續工程細節

## 注意事項

- Design system、variants、tweaks、mobile 轉換都會咬 weekly usage，務必先做 macro variants 再做 micro tweaks，避免為每個 variant 都跑 tweaks
- Context 越少，輸出越容易 regression to the mean；建議至少給一張 dribble / Awwwards 等參考圖或 sketch
