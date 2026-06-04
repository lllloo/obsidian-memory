---
title: Tailwind sr-only 造成多餘 scrollbar
created: 2026-06-03
updated: 2026-06-04
tags:
  - bug
  - frontend
  - css
  - tailwind
---
# Tailwind sr-only 造成多餘 scrollbar

## 問題背景

Tailwind CSS 的 `sr-only` 是提供給螢幕閱讀器使用的無障礙 class，會把元素視覺上隱藏但仍保留在 DOM 讓輔助科技讀取。在某些情境下，使用 `sr-only` 後頁面會出現非預期的水平或垂直 scrollbar，或是 `body` 高度比預期多出 1px。

## sr-only 的實際樣式

Tailwind 官方的 `sr-only` 定義如下：

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

重點在 `position: absolute` 加上 `margin: -1px`，元素會被定位到 containing block 之外 1px 的位置。

## 發生原因

`position: absolute` 的元素會依**最近的 positioned 祖先**（`position` 為 `relative`、`absolute`、`fixed`、`sticky` 的元素）作為 containing block 來定位。

當 `sr-only` 元素的祖先全部都沒有 positioned 設定時，containing block 會退回到 `<html>` （initial containing block）。此時 `margin: -1px` 會讓元素跑到 viewport 左上角外 1px，觸發 `<html>` 的 scrollbar。

典型症狀：

- 頁面右側出現不該有的垂直 scrollbar
- 行動裝置 Chrome 出現水平 scrollbar
- `body` 高度比 viewport 多出 1px
- 把 `sr-only` 元素放進 `overflow-scroll` 容器後，document 本身也跟著可以捲動

## 解決方法

### 方法 1：父層加 `position: relative`（推薦）

在 `sr-only` 的祖先節點建立 containing block，讓絕對定位侷限在該區塊內：

```html
<div class="relative">
  <span class="sr-only">Loading</span>
  <!-- 其他內容 -->
</div>
```

這是最乾淨、副作用最少的做法，也符合 Tailwind 官方在 issue 討論中的建議。

### 方法 2：父層加 `overflow: hidden`

`overflow` 非 `visible` 的元素本身也會成為 containing block（對 `position: absolute` 的子孫元素而言），因此也能解決：

```html
<div class="overflow-hidden">
  <span class="sr-only">Loading</span>
</div>
```

注意此方法會裁切其他溢出內容，需視版面需求採用。

### 方法 3：在 sr-only 上補 `top-0 left-0`

直接把位置鎖定在 containing block 左上角，消掉 `margin: -1px` 造成的偏移：

```html
<span class="sr-only top-0 left-0">Loading</span>
```

屬於局部修補，適合無法動父層的情境，但治標不治本。

## 建議

專案中廣泛使用 `sr-only` 時，習慣在版面容器（layout wrapper、section、card 等）預先加上 `relative`，可避免重複踩到同一個坑。

## 參考資料

- [Tailwind Discussion #12429 — sr-only inside a div with overflow produces unwanted scroll](https://github.com/tailwindlabs/tailwindcss/discussions/12429)
- [Tailwind Issue #8571 — Using sr-only in scrollable div influences body height](https://github.com/tailwindlabs/tailwindcss/issues/8571)
- [Tailwind Issue #1648 — sr-only adds a horizontal scrollbar on Chrome (mobile)](https://github.com/tailwindlabs/tailwindcss/issues/1648)
- [Tailwind Discussion #13355 — Does sr-only need to be position absolute?](https://github.com/tailwindlabs/tailwindcss/discussions/13355)
