---
title: 前端 Cookie 操作
created: 2026-06-03
updated: 2026-06-22
tags:
  - javascript
  - frontend
  - library
  - security
---

# 前端 Cookie 操作

這份文件說明如何在前端專案中使用 [js-cookie](https://github.com/js-cookie/js-cookie) 套件進行 Cookie 操作，包含安裝、基本用法、常見情境與注意事項，適合日常前端開發參考。

## 為什麼要用 js-cookie？

雖然可以用原生 JavaScript 操作 Cookie，但 js-cookie 有以下優點：

- **語法簡潔易懂**：提供 set/get/remove 等直觀 API，減少繁瑣字串處理，程式碼更易讀。
- **自動處理編碼**：自動處理 Cookie 的編碼與解碼，避免資料錯誤。
- **支援多屬性設定**：可輕鬆設定 expires、path、domain、secure、sameSite 等屬性，原生需自行組合字串，容易出錯。
- **取得所有 Cookie**：可直接取得所有 Cookie（物件），原生只能解析字串。
- **跨瀏覽器相容性**：自動處理不同瀏覽器的細節與相容性問題。

總結：js-cookie 讓 Cookie 操作更安全、簡單、可維護，適合日常前端開發使用。

## 基本用法

### import

```js
import Cookies from 'js-cookie'
```

### 設定 Cookie

```js
Cookies.set('name', 'value')
// 設定過期時間（天數）
Cookies.set('name', 'value', { expires: 7 })
// 設定路徑（path 預設為 '/'，站台全域可見）
Cookies.set('name', 'value', { path: '/' })
```

> **ℹ️ `path` 的預設與 `''` 的特殊語意**
>
> `path` 預設為 `'/'`（整個站台可見）。設成 `''` 並非「設定某個路徑」的一般寫法，其語意是讓 cookie 僅在目前頁面路徑可見，且移除時必須帶相同的 `{ path: '' }`，否則 `Cookies.remove('name')` 會失敗。

### 讀取 Cookie

```js
Cookies.get('name') // 取得指定 Cookie 值
Cookies.get() // 取得所有 Cookie（物件）
```

### 刪除 Cookie

```js
Cookies.remove('name')
// 若設定時指定了 path，刪除時也需指定相同的 path
Cookies.remove('name', { path: '/' })
```

### withAttributes 用法

`withAttributes` 可用於預設多個屬性，產生一個新的 Cookies 實例，後續 set/remove 皆自動帶入這些屬性，適合多次操作同一組屬性時簡化程式碼。

```js
const myCookies = Cookies.withAttributes({ expires: 7 })
myCookies.set('token', 'abc')
myCookies.remove('token')
```

## 最佳預設屬性（SameSite & Secure）

建議設定 Cookie 時，預設加上 `SameSite` 和 `Secure` 屬性，提升安全性：

```js
Cookies.set('name', 'value', {
  sameSite: 'Lax', // 防止 CSRF，推薦預設 Lax
  secure: true, // 僅 HTTPS 傳送 Cookie
})
```

可用 `withAttributes` 建立帶有安全預設的新實例：

```js
const safeCookies = Cookies.withAttributes({
  sameSite: 'Lax',
  secure: true,
})
safeCookies.set('token', 'abc')
```

**建議**：除非有特殊需求，Cookie 預設都加上 `SameSite: 'Lax'` 與 `Secure: true`，確保安全性。

## 如果有 node.js 需求可以考慮 universal-cookie

雖然 js-cookie 已能滿足大多數前端需求，但若你的專案有以下情境，建議改用 [universal-cookie](https://www.npmjs.com/package/universal-cookie) ：

- 需要同時在伺服器端（Node.js）與瀏覽器端操作 Cookie，例如 Next.js、Nuxt.js、SSR 等同構應用。
- 需於 React 等框架的伺服器端取得或設定 Cookie。
- 希望前後端共用一致的 Cookie 操作 API，簡化跨平台開發。

universal-cookie 提供更彈性的 API，適合現代全端應用場景。

## 參考資料

- [js-cookie 官方文件](https://github.com/js-cookie/js-cookie)
- [universal-cookie（npm）](https://www.npmjs.com/package/universal-cookie)
- [MDN Cookie](https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie)
