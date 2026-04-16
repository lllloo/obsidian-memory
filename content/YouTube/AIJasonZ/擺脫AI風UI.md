---
title: 如何擺脫千篇一律的 AI 風 UI
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-07-08
source: https://www.youtube.com/watch?v=Nocg_8ECs6w
parent: "[[01.index]]"
---

## 核心思路：Flow Engineering

不追求「完美 prompt」，而是把資深設計師的思考過程拆解為步驟流，讓模型逐步產出。

## 四步驟 UI 設計流

### 第一步：Layout（版面對齊）

- 在實作前用 ASCII wireframe 快速對齊版面
- 提示：「先輸出 ASCII wireframe，不要直接實作」
- 好處：生成極快（約 1 秒），可快速迭代確認資訊層級
- 支援互動表示：如「點擊漢堡選單後，sidebar 從左滑出推移主內容」

### 第二步：Theme（風格設定）

- 確定版面後才確定風格（顏色、字型、陰影、圓角）
- 工具推薦：**Tweakcn**（專注 Shadcn 主題設計的平台）
  - 調整顏色、字型、陰影直到滿意
  - 點擊「Code」複製 CSS stylesheet 貼給 agent
- 有了正確風格，UI 品質可從 60% 提升到接近 90%+

### 第三步：Animation（互動設計）

提示模型思考關鍵互動動畫：
```
請列出需要動畫的元素、關鍵 keyframe 和觸發時機
```
- 即使是簡單的 keyframe 描述，也能讓模型在實作時納入 hover、transition、slide 等互動
- 進階：用 Mermaid 圖描述用戶互動流程

### 第四步：實作

- 有了 layout + theme + animation 的上下文，一次生成品質大幅提升
- 先完成一個滿意的元件，再擴展到其他頁面（保持風格一致）

## 擴展應用

- 完成第一個元件後，用同樣的 layout/theme/animation 規格生成其他元件
- 範例：property listing card → 日曆預約 view → 地圖 view → 價格歷史圖表

## SuperDesign Extension

作者開發的開源工具（superdesign.dev）：
- 在 IDE 中直接生成並預覽 UI
- 支援在 infinite canvas 上並排顯示多個 UI 變體
- 內建上述四步驟流程
