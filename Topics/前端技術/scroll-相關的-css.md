---
title: scroll 相關的 css
created: 2026-06-03
updated: 2026-06-08
tags:
  - css
  - frontend
---

# scroll 相關的 css

這份文件介紹 CSS 中與 scrollbar 相關的常用技巧與客製化方法，包含隱藏、樣式調整等，適用於前端專案美化與體驗優化。

## 隱藏 scrollbar

有時需要隱藏滾動條但保留滾動功能，可使用以下樣式：

```scss
.no-scroll {
    -ms-overflow-style: none;
    scrollbar-width: none;

    &::-webkit-scrollbar {
        display: none;
    }
}
```

適用於需要隱藏原生 scrollbar 的區塊，例如橫向捲動圖片列表。

## 穩定 scrollbar 佔位

使用 `scrollbar-gutter: stable;` 可確保滾動條出現時不會導致內容寬度跳動。

```scss
.scroller {
  scrollbar-gutter: stable;
}
```

適合用於內容可能出現滾動條的容器，提升版面穩定性。

> 註：`scrollbar-gutter` 目前僅部分瀏覽器支援，建議搭配瀏覽器相容性測試。

## 客製化 scrollbar 樣式

可透過 CSS 變數與對應屬性自訂 scrollbar 外觀：

```scss
.scroller {
    --scrollbar-color-thumb: rgba(0, 0, 0, 0.2);
    --scrollbar-color-track: rgba(0, 0, 0, 0.2);
    --scrollbar-width: thin;
    --scrollbar-width-legacy: 10px;
    --scrollbar-border-radius: 7px;

    scrollbar-color: var(--scrollbar-color-thumb) var(--scrollbar-color-track);
    scrollbar-width: var(--scrollbar-width);

    &::-webkit-scrollbar-thumb {
        background: var(--scrollbar-color-thumb);
        border-radius: var(--scrollbar-border-radius);
    }
    &::-webkit-scrollbar-track {
        background: var(--scrollbar-color-track);
    }
    &::-webkit-scrollbar {
        max-width: var(--scrollbar-width-legacy);
        max-height: var(--scrollbar-width-legacy);
    }
}
```

可用於自訂捲軸顏色、寬度與圓角，提升 UI 一致性與美觀。

## 參考

- [Chrome 開發者官方文件：CSS 滾動條樣式](https://developer.chrome.com/docs/css-ui/scrollbar-styling?hl=zh-tw)
