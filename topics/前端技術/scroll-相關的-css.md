---
title: scroll 相關的 css
created: 2026-06-03
updated: 2026-06-12
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

> 註：`scrollbar-gutter` 自 2024 年底起已是 Baseline（廣泛可用）——Chrome / Edge、Firefox、Safari 新版皆支援。一般情境可直接使用，僅在需相容舊版 Safari 時才需 fallback。確切起始版本回查 [caniuse](https://caniuse.com/mdn-css_properties_scrollbar-gutter)。

## 客製化 scrollbar 樣式

可透過 CSS 變數與對應屬性自訂 scrollbar 外觀：

```scss
.scroller {
    --scrollbar-color-thumb: rgba(0, 0, 0, 0.2);
    --scrollbar-color-track: rgba(0, 0, 0, 0.2);
    --scrollbar-width-legacy: 10px;
    --scrollbar-border-radius: 7px;

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

> 注意：標準屬性（`scrollbar-color` / `scrollbar-width`）與 `::-webkit-scrollbar-*` 偽元素**並非平行疊加**。新版 Chromium（Chrome/Edge 121+）起，頁面只要出現標準屬性就會**覆蓋**偽元素樣式，導致原本雙寫的客製外觀失效。要兩套並存應用 `@supports` 隔離：讓 WebKit 引擎走偽元素（可精確控寬如 `max-width: 10px`），其餘瀏覽器才套標準屬性。
>
> ```scss
> @supports not selector(::-webkit-scrollbar) {
>   .scroller {
>     scrollbar-width: thin;
>     scrollbar-color: var(--scrollbar-color-thumb) var(--scrollbar-color-track);
>   }
> }
> ```

## 參考

- [Chrome 開發者官方文件：CSS 滾動條樣式](https://developer.chrome.com/docs/css-ui/scrollbar-styling?hl=zh-tw)
