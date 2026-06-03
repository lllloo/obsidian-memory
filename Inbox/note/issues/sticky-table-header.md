---
title: Sticky Table Header 的邊框穿透問題
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/issues/sticky-table-header
tags:
  - bug
  - frontend
  - css
  - tailwind
---
# Sticky Table Header 的邊框穿透問題

製作可捲動表格時，將捲動容器套在 table 外層並對 `<th>` 加上 `position: sticky` 後，捲動時表頭底部邊框會消失，內容從下方穿透出來。

## 基本寫法

捲動容器套在整個 table 外層，`sticky` 加在 `<th>` 上：

```html
<div class="overflow-y-auto max-h-[500px]">
  <table>
    <thead>
      <tr>
        <th class="sticky top-0 z-10 bg-white">欄位名稱</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>資料</td>
      </tr>
    </tbody>
  </table>
</div>
```

注意 `sticky` 要加在 `<th>` 上，而不是 `<thead>` 或 `<tr>`。CSS 2.1 規範明確指出 `position: relative` 不適用於 `<thead>`、`<tr>` 等 table 結構元素，而 `sticky` 的運作依賴 relative 定位，因此在這些元素上無效。

## 問題：捲動時邊框穿透

這樣做之後，捲動時表頭的底部邊框會消失。

### 原因

`border-collapse: collapse`（CSS table 的預設行為）會讓相鄰儲存格共用邊框。當 `<th>` 加上 `position: sticky` 後，sticky 元素本身會移動，但共用的邊框屬於相鄰的 `<td>`，並不會跟著動，導致捲動時邊框留在原地而表頭已經移走。

這是跨瀏覽器都存在的已知問題，在 [W3C CSS Working Group](https://github.com/w3c/csswg-drafts/issues/3136)、[Chromium](https://bugs.chromium.org/p/chromium/issues/detail?id=702927)、[Firefox](https://bugzilla.mozilla.org/show_bug.cgi?id=1658119) 的 bug tracker 都有記錄。

有兩種解法，各有適用情境。

### 解法一：`box-shadow` 模擬邊框（較輕量）

直接在 `<th>` 上用 `box-shadow` 模擬底部邊框，完全不需要動 `border-collapse`：

```css
th {
  position: sticky;
  top: 0;
  box-shadow: inset 0 -1px 0 #e5e7eb; /* 模擬 border-bottom */
}
```

```html
<!-- Tailwind（用 [box-shadow] 任意值） -->
<th class="sticky top-0 [box-shadow:inset_0_-1px_0_#e5e7eb]">
```

`box-shadow` 屬於元素本身的繪製層，不受 `border-collapse` 影響，sticky 移動時跟著走。適合只需要表頭底線、不想動整張表格樣式的情況。

### 解法二：改用 `border-collapse: separate`（較完整）

如果整張表格需要保留完整邊框（上下左右都有），改用 `border-collapse: separate` 加上 `border-spacing: 0`：

```css
/* 純 CSS */
table {
  border-collapse: separate;
  border-spacing: 0;
}
```

```html
<!-- Tailwind -->
<table class="border-separate border-spacing-0">
```

`border-spacing: 0` 是為了讓儲存格之間不產生間距，視覺上與 `collapse` 相同，但邊框現在完全屬於各自的儲存格，sticky 元素移動時邊框也會跟著走。

> **如何選擇：** 只需要表頭底線 → 用解法一；整張表格有四周邊框需求 → 用解法二。

## 附帶問題：`border-collapse: separate` 下 `<tr>` 的邊框失效

改成解法二後，若原本是在 `<tr>` 上設定 `border-b` 作為行分隔線，會發現分隔線消失。

CSS table model 在 `border-collapse: separate` 模式下不支援 `<tr>` 的邊框屬性，只有 `<td>` 和 `<th>` 的邊框會生效。

```css
/* 把行分隔線改設在 td */
tbody td {
  border-bottom: 1px solid #e5e7eb;
}
```

```html
<!-- Tailwind：在 td 加上 border-b -->
<td class="border-b border-gray-200">...</td>
```

## 完整範例

### 解法一（box-shadow）

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
</head>
<body class="p-8">
  <div id="app">
    <div class="overflow-y-auto max-h-48 border border-gray-200">
      <table class="w-full">
        <thead>
          <tr>
            <th class="sticky top-0 z-10 bg-white text-left px-4 py-2 [box-shadow:inset_0_-1px_0_#9ca3af]">名稱</th>
            <th class="sticky top-0 z-10 bg-white text-left px-4 py-2 [box-shadow:inset_0_-1px_0_#9ca3af]">狀態</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row.name">
            <td class="border-b border-gray-200 px-4 py-2">{{ row.name }}</td>
            <td class="border-b border-gray-200 px-4 py-2">{{ row.status }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <script>
    Vue.createApp({
      data() {
        return {
          rows: [
            { name: '項目 A', status: '啟用' },
            { name: '項目 B', status: '停用' },
            { name: '項目 C', status: '啟用' },
            { name: '項目 D', status: '啟用' },
            { name: '項目 E', status: '停用' },
            { name: '項目 F', status: '啟用' },
            { name: '項目 G', status: '啟用' },
            { name: '項目 H', status: '停用' },
          ]
        }
      }
    }).mount('#app')
  </script>
</body>
</html>
```

### 解法二（border-collapse: separate）

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
</head>
<body class="p-8">
  <div id="app">
    <div class="overflow-y-auto max-h-48 border border-gray-200">
      <table class="w-full border-separate border-spacing-0">
        <thead>
          <tr>
            <th class="sticky top-0 z-10 bg-white text-left px-4 py-2 border-b border-gray-400">名稱</th>
            <th class="sticky top-0 z-10 bg-white text-left px-4 py-2 border-b border-gray-400">狀態</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row.name">
            <td class="border-b border-gray-200 px-4 py-2">{{ row.name }}</td>
            <td class="border-b border-gray-200 px-4 py-2">{{ row.status }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <script>
    Vue.createApp({
      data() {
        return {
          rows: [
            { name: '項目 A', status: '啟用' },
            { name: '項目 B', status: '停用' },
            { name: '項目 C', status: '啟用' },
            { name: '項目 D', status: '啟用' },
            { name: '項目 E', status: '停用' },
            { name: '項目 F', status: '啟用' },
            { name: '項目 G', status: '啟用' },
            { name: '項目 H', status: '停用' },
          ]
        }
      }
    }).mount('#app')
  </script>
</body>
</html>
```

## 參考資料

- [Position Sticky and Table Headers — CSS-Tricks](https://css-tricks.com/position-sticky-and-table-headers/)
- [HTML table sticky header with borders — DEV Community](https://dev.to/kzuraw/html-table-sticky-header-with-borders-51n4)
- [W3C CSSWG Issue #3136 — Collapsed table borders don't follow sticky rows/cells](https://github.com/w3c/csswg-drafts/issues/3136)
- [Chromium Bug #702927 — position: sticky does not work on thead or tr](https://bugs.chromium.org/p/chromium/issues/detail?id=702927)
- [Firefox Bug #1658119 — sticky table cells lose their border](https://bugzilla.mozilla.org/show_bug.cgi?id=1658119)
