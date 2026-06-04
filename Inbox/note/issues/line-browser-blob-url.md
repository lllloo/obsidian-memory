---
title: LINE 付款頁面 redirect 處理
created: 2026-06-03
updated: 2026-06-04
tags:
  - bug
  - frontend
  - javascript
---
# LINE 付款頁面 redirect 處理

本文件說明在 LINE 內建瀏覽器（WebView）中，付款頁面使用跳頁的方式處理。

## 問題描述

原本的程式碼：

```js
const formHtml = `<html>...</html>`
const blob = new Blob([formHtml], { type: 'text/html' })
const url = URL.createObjectURL(blob)
window.location.assign(url)
```

在 LINE 內無法正確作用。

### 原因解析

LINE 內建瀏覽器（WebView）對於 `window.location.assign(url)` 跳轉到 Blob URL 的行為，常常會因安全性或瀏覽器限制而無法正確載入內容，導致 formHtml 頁面無法顯示。
此外，Blob URL 可能會被 LINE 的 WebView 阻擋或無法正確解析，造成畫面空白或無反應。

而且沒有跳任何錯誤訊息，讓開發者難以追蹤問題。

## 解決方式（一）：解析並送出 form

如果 formHtml 內容主要是表單（form），可用 DOMParser 解析並自動送出：

```js
const formHtml = `<html>...</html>`
// 解析 formHtml 並擷取 form
const parser = new DOMParser()
const doc = parser.parseFromString(formHtml, 'text/html')
const form = doc.querySelector('form')
if (form) {
  document.body.appendChild(form)
  form.submit()
}
```

### 原理說明

此方法會將 formHtml 內容中的 form 元素直接插入目前頁面並自動送出。
適合 formHtml 內容為單一 form，且目的是直接送出資料。

#### 注意事項

- formHtml 必須包含 form 標籤。
- 只會送出第一個找到的 form。

## 解決方式（二）：覆蓋整頁內容

改成以下寫法：

```js
const formHtml = `<html>...</html>`
document.open()
document.write(formHtml)
document.close()
```

這樣可在 LINE 內正確顯示付款頁面。

### 原理說明

`document.open()`、`document.write()`、`document.close()` 會直接覆蓋目前頁面的內容，將 formHtml HTML 寫入，無需跳轉或產生新的 URL。

這種方式能避開 LINE WebView 對於 Blob URL 的限制，確保 formHtml 頁面能正確顯示。

#### 注意事項

- formHtml 內容必須是完整的 HTML 字串（含 `<html>...</html>` 標籤）。
- 使用 `document.write` 會清空原本頁面，請確認不會影響其他流程。
