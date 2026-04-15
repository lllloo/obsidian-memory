---
title: Clean Code 是迷思還是真理
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-23
source: https://www.youtube.com/watch?v=OjW_0ZRdN5E
---

Kevlin Henney 與 Daniel Terhorst-North 探討「Clean Code」這個概念的起源、演化與局限。

## Clean Code 的三個脈絡

1. **Robert C. Martin 的《Clean Code》（2008）**：最廣為人知的版本，有具體規則（函數長度、命名等），但部分建議被視為教條
2. **Kent Beck 的 Tidy First**：更近期的詮釋，刻意用「tidy」而非「clean」區別
3. **Richard Gabriel 的「Habitability」（宜居性）**：更早的概念，Kevlin Henney 認為最能描述程式碼品質的本質

**Habitability 的兩個特質：**
- **Comfortable**（舒適）：在程式碼中移動時不感到恐懼或不安
- **Confident**（有信心）：有信心做出改變

Daniel Terhorst-North 把這個再延伸到 **CUPID**——「joyful code」（讓你快樂的程式碼）。

## 教條式 Clean Code 的問題

《Clean Code》中「把程式碼拆成小函數」的建議，放在 1990 年代有其脈絡：
- 當時大型組織把一個需求拆給多個不同的團隊（UI 團隊、DB 團隊、服務層團隊），各自在不同地方工作
- 分離程式碼是為了讓不同人不互相衝突

現在全棧工程師獨立完成整個功能，過度分散程式碼反而造成「碎片化」（fragmentation），需要四處搜尋才能理解一個功能。

## Goldilocks 原則：不是越小越好

Kevlin Henney 的核心觀點：程式碼的「大小」不是線性關係，而是 Goldilocks zone：

- **太大**：思維不得不在閱讀中拆解和重組，認知負擔過重
- **太小**：所有碎片散落各處，需要在腦中重新拼湊，同樣消耗認知資源
- **剛好**：程式碼對應你的思維方式，讀起來舒適

「小」的目標不是行數，而是**需要多少思考量**（cognitive load）。

## Locality of Behavior（行為局部性）

HTMX 作者提出的概念：把完成一個**目標**所需的所有程式碼放在一起，而不是按技術層（DB 層、服務層、UI 層）分散。

Daniel Terhorst-North 稱之為 **Single Goal Principle**：
> 若我想達成某個目標，完成該目標所需的所有元件是否就在手邊？

這是對「Separation of Concerns」教條的反思——按技術層分離常導致碎片化，按業務目標組織才真正有意義。

## 限制理論（Theory of Constraints）的應用

Eliyahu Goldratt 的《The Goal》（1984）給出框架：任何系統中，真正要最佳化的只有**瓶頸（constraint）**。

應用到 Clean Code：
- 程式碼的「清潔度」應完全服務於「能否快速有效地修改」
- 比這更清潔 = 過度設計，是機會成本
- 若程式碼的混亂正在拖慢你，那就是當前的瓶頸，需要提升

## 最終答案

Clean Code 不是迷思，但**不是固定點**——它是一個相對的、與人有關的概念：

> 這段程式碼是否讓我移動起來舒適、有信心做出改變？它是否正在拖慢我們？

這是脈絡判斷，不是一組固定規則。具體的 coding 實踐（命名、邊界等）是工具箱，判斷依據是「現在這個讓我們慢下來了嗎？」
