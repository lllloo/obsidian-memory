---
title: iOS image 高度錯誤問題
created: 2026-06-03
updated: 2026-06-04
tags:
  - bug
  - frontend
  - css
  - flexbox
---
# iOS image 高度錯誤問題

在 iOS 系統中，如果高度不確定，可能會遇到圖片高度顯示異常，與其他瀏覽器（如 Chrome、Firefox）顯示結果不一致。

## 問題描述

當 `<img>` 元素放在 `<table>` 內，當圖片上層的 height 不確定時，Safari 可能無法正確計算 `<img>` 的高度，導致圖片顯示不正常，例如使用 `aspect-ratio` 屬性去撐開高度。

### 會錯誤的程式碼

```html
<div style="width: 300px; height: 300px; border: 2px solid red">
  <table style="height: 100%; width: 100%">
    <tr>
      <td>
        <div style="width: 100%; aspect-ratio: 1; border: 2px solid blue">
          <img
            src="https://picsum.photos/1000"
            style="width: 100%; height: 100%; object-fit: cover;"
          />
        </div>
      </td>
    </tr>
  </table>
</div>
```

### 修改的程式碼

```html
<div style="width: 300px; height: 300px; border: 2px solid red">
  <table style="height: 100%; width: 100%">
    <tr>
      <td>
        <div
          style="width: 100%; aspect-ratio: 1; border: 2px solid blue; display: flex; flex-direction: column;"
        >
          <img
            src="https://picsum.photos/1000"
            style="flex: 1; width: 100%; object-fit: cover;"
          />
        </div>
      </td>
    </tr>
  </table>
</div>
```

## 修正原理說明

將外層 `div` 設為 flex 容器，並讓 `<img>` 使用 `flex: 1`，可確保圖片自動填滿父容器的高度與寬度。這樣能避免 Safari 在 table 結構下無法正確計算圖片高度的問題，讓圖片能完整填滿且維持正確比例。其他瀏覽器（如 Chrome、Firefox）也能正常顯示。

## 參考資料

- [MDN - object-fit](https://developer.mozilla.org/zh-CN/docs/Web/CSS/object-fit)
