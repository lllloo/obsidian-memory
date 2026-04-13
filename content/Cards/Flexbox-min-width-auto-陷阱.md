---
title: Flexbox min-width auto 陷阱
created: 2026-04-13
updated: 2026-04-13
tags:
  - css
  - flexbox
  - tailwind
---

## 問題

在 flexbox 中，子元素的 `min-width` 預設是 `auto`，意思是**不會縮小到比自己內容還窄**。

當左側有固定寬度子元素（例如 `w-[366px]` × 2 + `w-[60px]` + gaps ≈ 900px），即使設了 `flex-1` 也**不會縮到 900px 以下**。右側 `w-[500px] shrink-0` 又不能縮，兩者加起來超過可用寬度時，右側就被擠出去。

## 解法

加上 `min-w-0`（`min-width: 0`），告訴瀏覽器左側可以縮到比內容還窄。`flex-1` 才能真正分配剩餘空間。

```
沒有 min-w-0：  [左側 min 900px 不讓步][右側 500px 被擠出]
有 min-w-0：    [左側 flex-1 可收縮    ][右側 500px 完整顯示]
```

## 適用情境

- flex 子元素內部有固定寬度的子孫元素時
- flex 子元素需要真正收縮到小於內容寬度時
- 搭配 `overflow-hidden` 或 `overflow-auto` 使用
