---
title: SPA 內部跳轉為何要用 router 而非原生 a href
created: 2026-04-23
updated: 2026-04-24
tags:
  - frontend
  - vue
  - spa
  - best-practices
  - bug
---

## 一句話結論

SPA 內用 `<a href>` 跳頁會觸發**整頁導航**，之後的 `router.back()` 已經不是 Vue Router 在動，而是退化成瀏覽器原生 `history.back()`——掉進 bfcache 雙命運，資料「該刷沒刷、該留沒留」同時發生。

## 技術鏈

1. `<a href="/B">` → 瀏覽器原生導航，整個 app 被炸掉重建
2. B 頁**新的 Router 實例**從 `window.history.state` 反推脈絡，常對不上
3. `router.back()` 內部就是 `window.history.back()` → 又是整頁導航回 A → app 第三次重建
4. bfcache 命中與否決定下一步

## bfcache 雙命運

| 命中 bfcache                       | 沒命中 bfcache                             |
| ---------------------------------- | ------------------------------------------ |
| A 從記憶體抓出來                   | A 整頁重新載入                             |
| `onMounted` **不跑**、API **不打** | Pinia、表單、ref 全**歸零**                |
| 看到**完全舊**畫面                 | API 從**預設參數**重打（使用者篩選不見了） |

兩種命運在不同次測試間切換，跨瀏覽器與分頁狀態行為都不同——不是邏輯亂，是根本不可控。

## 什麼時候才該用 `<a href>`

外部網站、下載檔案（`download`）、非 SPA 後端頁、`target="_blank"`。

## 修法

改成 `<router-link>` / `router.push` → 上面所有症狀一次解決。

```html
<router-link to="/performance-main">
  <img src="..." />
</router-link>
```
