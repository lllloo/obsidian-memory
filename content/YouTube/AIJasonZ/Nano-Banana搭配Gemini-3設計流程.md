---
title: Nano Banana 搭配 Gemini 3 設計流程
tags:
  - youtube
  - gemini
  - ui-design
  - frontend
created: 2026-04-14
updated: 2026-04-14
published: 2025-12-12
source: https://www.youtube.com/watch?v=RYnxU_MTVvU
---

## 核心思路

Nano Banana 是圖像生成模型，不受技術實作限制，因此能輸出 coding agent 不敢嘗試的創意設計（傾斜 UI、3D 物件、特殊材質）。用它生成 mockup 作為 source of truth，再交 coding agent 實作，可大幅提升最終設計品質。

## 四步驟流程

### 步驟一：規劃（Plan）

用 Google AI Studio + Gemini 3 Pro 做設計規劃（文字輸出，成本最低）：
- 提供產品截圖與品牌資訊
- 附上 2-3 張風格參考圖（太多會混淆模型）
- 輸出：content hierarchy、layout spacing、animation 規劃、線框圖（ASCII art）

建議參考圖來源：Dribbble、web-interaction.gallery、relive.design（按色系找靈感）

### 步驟二：Mockup 生成（Mock Gen）

把規劃結果給 Nano Banana，輸出高創意 UI mockup：
- 指定「UI mode」輸出
- 快速（約 30 秒），可快速生成多版本比較
- 可持續調整（Nano Banana 迭代修改能力強，不要刪掉重來）

### 步驟三：資產萃取（Asset Extraction）

對 mockup 中難以用程式碼實現的視覺元素（3D 物件、特殊背景）：
1. 請 Nano Banana 萃取特定元素為高解析度圖片（4K）
2. 需移除 UI element，只留背景資產（`remove the UI elements, keep only the 3D background`）
3. 去除背景透明化：上傳到 Replicate 的 background-remover 模型（$1 可處理近 2,000 張）
4. 可進一步用 Replicate 生成帶視差效果的影片，供捲動動畫使用

### 步驟四：Coding（Code）

把 mockup 和資產交給 coding agent 實作：
- 直接複製 mockup 圖
- 複雜部分可先讓 agent 分析困難點、規劃做法，再進入 build mode
- 遇到 logo 比例問題：提醒「keep the UR ratio of the mockup the same」

## 注意事項

- 傳多張圖給 Gemini 時，它較關注最新的圖，logo 等元素可能被忽略，需明確指定
- 用 `useRef` + bounding box 取元素位置，避免 hard-code cursor 座標
- 設計完可用 Nano Banana 做設計審查，輸出帶標記的改善建議
