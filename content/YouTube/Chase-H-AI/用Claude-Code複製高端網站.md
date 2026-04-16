---
title: 用 Claude Code 15 分鐘複製十萬美元網站
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-27
source: https://www.youtube.com/watch?v=i-jawzwnjSA
parent: "[[01.index]]"
---

## 這個練習的真實目的

不是真的「偷」網站，而是透過模仿高水準前端設計來學習：
1. 接觸更多創意可能（而非重複看到同樣的 SaaS 模板）
2. 逆向理解專業網站的實作方式（scroll animation、parallax、shading 等）

示範網站：Moon（羅馬屋頂酒吧），有視差動效、陰影跟隨滑鼠、滾動展開雞尾酒杯動畫。

## 五步流程

### 步驟一：找靈感

推薦 **Awwwards**（awwwards.com），可看到業界最高水準的前端設計，而非無聊的 AI 模板。

### 步驟二：網站解析（Site Teardown）

Claude Code 需要三樣資料：
- **HTML**：按 `Ctrl+U` 取得原始碼，全選複製貼入 Claude Code
- **截圖**：主頁、動畫關鍵幀、特效細節
- **CSS 與 JavaScript**：在 HTML 末尾找到各 `.js`、`.css` 檔案的引用 URL，使用 **Site Teardown 技能**（含強化 prompt，確保 web fetch 抓完整而非截斷）讓 Claude Code 自行取回

Site Teardown 技能輸出範例：技術棧（GSAP、ScrollTrigger、Lenis）、13 個頁面區塊、19 種效果、完整設計系統。

### 步驟三：素材製作

以 Moon 的月亮素材為例：
- 用 AI 圖像工具（Nano Banana Pro）生成「完全照亮」和「完全陰影」兩張綠幕月亮圖
- 用 AI 影片工具（Google Veo 3.1）生成 4 秒過渡影片，注意 prompt 強調「不移動鏡頭、不縮放、不漂移」
- 讓 Claude Code 從影片抽取 54 幀，每幀對應一個滑鼠位置

綠幕的原因：月亮是獨立素材，不能有背景跟著動；綠幕讓 AI 去背更容易。

### 步驟四：建構

把 MP4 和其他素材交給 Claude Code，指定「按照 Site Teardown 的結果建構」。
- 輸出不會是 100% 複製，預期 90% 相似度
- 差異處：截圖比對 → 貼回 Claude Code → 請它對照原版修正

### 步驟五：迭代與個人化

模仿到位後，替換成自己的主題：
- 換掉月亮素材
- 修改 headline 與 copy
- 應用相同的 scroll animation 概念

學習的核心價值：每次複製一個網站，就對「這種效果怎麼做的」有更清晰的認識，逐漸建立前端設計直覺。
