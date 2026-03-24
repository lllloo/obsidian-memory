---
title: CSS Border 容器的 Padding 規則
tags:
  - css
  - frontend
  - 切版
created: 2026-03-24
updated: 2026-03-24
---

**當外層容器有 `border`（邊框）時，內部的 padding 不能加在外層容器上，必須分配到各子區塊。**

## 原因

如果 `padding` 加在外層，內部子元件的 `border-b`（分隔線）會因為有內距而無法貼齊外框的左右邊緣，視覺上會出現兩側缺角的斷線。

## 規則

> **有 border 的容器 → padding 放到子元件，不放外層。**

## 範例

```html
<!-- 錯誤：padding 加在有 border 的外層 -->
<div class="border px-4">
  <div class="border-b py-2">第一列</div>
  <div class="py-2">第二列</div>
</div>

<!-- 正確：padding 分配到子元件 -->
<div class="border">
  <div class="border-b px-4 py-2">第一列</div>
  <div class="px-4 py-2">第二列</div>
</div>
```
