---
title: Pencil 讀取規則
tags:
  - 切版
  - frontend
  - css
created: 2026-03-26
updated: 2026-03-26
---

**讀取任何 Node，必須遞迴到所有葉節點。不能只確認容器層的屬性就停止。**

## 遞迴讀取原則

只確認容器的 gap，沒有往下讀子元件的內部結構，會漏掉：

- 子元件欄位之間的 gap
- 子元件的 padding

正確做法：

1. 確認容器層屬性（gap、padding、fill…）
2. 對每個子元件（ref）用 `batch_get` 讀取原始 component
3. 繼續往下，直到葉節點

## ref 節點的 descendants override

`ref` 節點可以透過 `descendants` 覆寫子節點屬性。讀取 ref 時必須同時確認：

- `descendants` 裡有沒有 override 子節點的 fill、text、padding 等屬性
- 子節點可能被完全替換（有 `type` 欄位）或只替換 `children`
- 巢狀 override 用 `/` 分隔，例如 `"ok-button/label"`

> ref 元件的預設屬性定義在 component 層，instance 的 `descendants` 才是最終值。
