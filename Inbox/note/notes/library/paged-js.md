---
title: Paged.js
created: 2026-06-03
updated: 2026-06-04
tags:
  - library
  - css
  - frontend
---

# Paged.js

這份文件說明如何在前端專案中使用 Paged.js 進行分頁印刷版面設計，包含安裝、基本用法、常見設定與最佳實踐，適合需要生成 PDF 或印刷版面的前端開發參考。

## 安裝與基本設定

### 透過 CDN 引入

建議下載 polyfill，請造訪 [https://unpkg.com/pagedjs/dist/](https://unpkg.com/pagedjs/dist/)。
曾經遇過 cdn 引入失敗的情況，建議下載後放在本地。

```html
<script src="js/paged.polyfill.js"></script>
```

```html
<script src="https://unpkg.com/pagedjs/dist/paged.polyfill.js"></script>
```

## 基本用法

### 基礎分頁設定

```css
@page {
  size: A4;
  margin: 2cm;
}
```

### 頁首與頁尾

```css
@page {
  @top-center {
    content: '文件標題';
  }

  @bottom-center {
    content: '第 ' counter(page) ' 頁，共 ' counter(pages) ' 頁';
  }
}
```

## 固定文字在頁面位置

本節說明如何在每頁的頁首/頁尾（margin box）或固定位置重複顯示 DOM 中的內容，例如 Logo、訂單編號或文件標題。

- `position: running(name)`：將頁面中某個元素標記為可供頁首/頁尾引用的來源。
- `element(name)`：在 margin box 中取回由 `position: running(name)` 標記的元素（整個元素內容會被複製到欄位）。
- `string-set` + `string(name)`：擷取元素的文字內容（常用於標題或章節名）到 margin box 中的文字插入點。

```css
@page {
  @top-left {
    width: 100px;
    content: element(logo);
  }

  @top-right {
    font-size: 14px;
    content: element(order-id);
  }

  @top-center {
    font-size: 18px;
    content: string(title);
  }
}

/* 將來源元素標記為 running，並在畫面上隱藏原始位置（印刷/分頁輸出時會使用 margin box 的內容） */
.order-logo {
  position: running(logo);
  display: none;
}

.order-id {
  position: running(order-id);
  display: none;
}

.order-title {
  string-set: title content(text);
  display: none;
}
```

```html
<img class="order-logo" src="/assets/images/logo/logo.svg" alt="公司 Logo" />
<div class="order-id">訂單編號<br />A123456</div>
<div class="order-title">文件標題</div>
```

## 分頁控制

### 避免元素被分頁切斷

`break-inside: avoid;` 是分頁排版最常用的屬性之一，可以防止元素在分頁時被切斷，確保內容完整，常用於表格、圖片、段落等。

範例：

```css
.break-inside-avoid {
  break-inside: avoid;
}
```

### 分頁斷點控制

分頁時可用以下 CSS 屬性控制元素的分頁行為：

- `break-before: always;` 強制元素前方分頁，常用於章節或標題。
- `break-after: always;` 強制元素後方分頁，常用於段落或圖片。

範例：

```css
.break-before-always {
  break-before: always;
}

.break-after-always {
  break-after: always;
}
```

## 參考資料

- [Paged.js 官方網站](https://pagedjs.org/)
- [Paged.js GitHub](https://github.com/pagedjs/pagedjs)
