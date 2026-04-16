---
title: GSD vs Superpowers vs Claude Code：新 AI 之王？
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-12
source: https://www.youtube.com/watch?v=celLbDMGy8w
parent: "[[01.index]]"
---

## 三者是什麼

GSD 和 Superpowers 都是架設在 Claude Code 之上的 **orchestration 層**，提供更完善的規劃系統、測試系統，以及用 sub-agent 驅動開發來對抗 context rot。

**核心差異：**
- **Superpowers**：強調 TDD（鐵律：沒有失敗測試就不寫生產程式碼，red-green-refactor 循環）；另有 Visual Companion 功能可在 dev server 直接比對多款設計
- **GSD**：強調狀態與上下文管理，自動建立 requirements.md、roadmap.md、state.md 等文件作為子 agent 的北極星，流程更為明確與剛性（使用 `/gsd new project` 等指令逐步推進）

**安裝方式：**
- Superpowers：Claude Code 內執行 `/plugin` 搜尋安裝
- GSD：執行單行安裝指令

## 測試任務

為 AI 代理公司建立完整網站，包含三個部分：
1. 落地頁（hero、about、services、lead capture form）
2. 部落格列表頁
3. 隱藏版部落格生成器（輸入 YouTube URL 或文章 URL，用 Anthropic SDK 生成文章，抓取縮圖）

刻意留下詮釋空間（抓取 transcript 的方式、縮圖策略、語氣設定），觀察三者的自主判斷能力。

## 規劃階段比較

| 指標 | Claude Code | Superpowers | GSD |
|------|------------|------------|-----|
| 規劃時間 | ~10 分鐘 | ~40 分鐘 | ~40 分鐘 |
| 規劃 token 用量 | ~50K | ~200K | ~600K |

GSD 在規劃時啟動 4 個平行 researcher sub-agent（stack research、features research、architecture、pitfalls），各自消耗 33K–75K tokens 後再合成，因此 token 消耗遠高於 Superpowers。

## 執行階段比較

| 指標 | Claude Code | Superpowers | GSD |
|------|------------|------------|-----|
| 執行時間 | ~10 分鐘 | ~15 分鐘 | ~60 分鐘 |
| 執行 token 用量 | ~150K | ~50K | ~600K |
| **總時間** | **~20 分鐘** | **~1 小時** | **~1 小時 45 分** |
| **總 token** | **~200K** | **~250K** | **~1.2M** |

GSD 每個 phase 都需要人工介入確認，執行者無法完全自動跑完。

## 輸出品質

三者最終產出的前端設計幾乎無法區分差異（因為沒有給定詳細設計指令，都是 AI 風格）。功能面：
- **Superpowers**：部落格生成器第一次就能正常運作
- **GSD**：部落格生成器初次失敗，修復後可用；內聯編輯器設計較好
- **Claude Code**：部落格生成器初次失敗，修復後可用

## 結論

**贏家：原生 Claude Code**，原因不在 token，在**時間**。

- 1.2M tokens vs 200K 是很大差距，但更關鍵的是 105 分鐘 vs 20 分鐘
- 用 Claude Code 省下的 40–80 分鐘繼續迭代，最終輸出一定優於等待 GSD 或 Superpowers
- Claude Code 本身已大幅改善 context rot 問題，GSD 和 Superpowers 當初填補的空缺已縮小

**推薦策略：**
- 99% 的情況用原生 Claude Code
- 任務真的複雜到不確定時，用 Superpowers（相對輕量，fluid 使用體驗，token 可控）
- 很難找到值得用 GSD 的情境（手動介入多、token 燃燒重、GSD 2.0 不支援 Max 方案）
