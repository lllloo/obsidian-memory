---
title: Img 相關 css
created: 2026-06-03
updated: 2026-06-08
tags:
  - css
  - frontend
---

# Img 相關 css

這份文件說明常見圖片相關 CSS 實作方式，包含背景圖與 `<img>` 標籤的等比例縮放、填滿、置中等技巧，適用於網頁前端開發。

## 圖片同比例稱到最大

### cover：縮放背景圖片以完全覆蓋背景區

```css
.background-img {
    background-image: url('');
    background-position: center;
    background-size: cover;
}
```

上述範例將背景圖片等比例縮放，確保覆蓋整個容器，可能會裁切部分圖片。

```css
img {
    object-fit: cover;
    object-position: center;
    width: 100%;
    height: 100%;
}
```

此寫法讓 `<img>` 元素內容等比例填滿容器，超出部分會被裁切。

### contain：縮放背景圖片以完全裝入背景區

```css
.background-img {
    background-image: url('');
    background-position: center;
    background-size: contain;
    background-repeat: no-repeat;
}
```

此設定讓背景圖片完整顯示於容器內，可能會留白。

```css
img {
    object-fit: contain;
    object-position: center;
    width: 100%;
    height: 100%;
}
```

讓 `<img>` 內容完整顯示於容器內，維持比例，可能會留白。

## 圖片依照比例

```css
img {
    width: 100%;
    aspect-ratio: 1920 / 850;
}
```

設定圖片寬度 100%，並以 aspect-ratio 維持比例，適合響應式設計。
