---
title: URLSearchParams 查詢字串處理
created: 2026-06-03
updated: 2026-06-23
tags:
  - javascript
  - frontend
---

# URLSearchParams 查詢字串處理

這份文件以 JavaScript 原生 `URLSearchParams` 為主，說明其用法、限制與常見情境。若遇到 `URLSearchParams` 無法處理的需求，才推薦使用 `qs`、`query-string` 等第三方套件。

## URLSearchParams 基本用法

`URLSearchParams` 用於處理網址查詢字串（query string），可解析、組裝、修改參數，瀏覽器與 Node.js 皆支援。

### 建立與解析

```js
const params = new URLSearchParams('?foo=1&bar=2')
params.get('foo') // '1'
params.has('bar') // true
```

### 新增、修改、刪除參數

```js
params.set('foo', '100')
params.append('baz', '3')
params.delete('bar')
params.toString() // 'foo=100&baz=3'
```

### 轉物件

```js
Object.fromEntries(params) // { foo: '100', baz: '3' }
```

> **⚠️ 限制**
>
> - 只支援一層 key-value 結構，不支援巢狀物件與陣列。
> - 參數值一律為字串。
> - 陣列參數需重複 key，例如 `a=1&a=2`，無法自訂格式。

---

## URLSearchParams 做不到的情境

### 1. 巢狀物件/陣列

- `URLSearchParams` 僅支援單層 key-value，無法正確處理巢狀物件或陣列（如 `a[0]=1&a[1]=2`、`foo[bar]=1`）。
- 若需處理巢狀結構，建議使用 `qs`（`query-string` 刻意不支援巢狀物件，巢狀需自行 `JSON.stringify`）。

### 2. 陣列格式自訂

- `URLSearchParams` 只支援重複 key，不支援 brackets、indices、comma 等格式。
  - brackets 格式：以中括號標示陣列元素，例如 `a[]=1&a[]=2`，解析後為 `{ a: ['1', '2'] }`。常見於 PHP、Ruby 等後端框架。
  - indices 格式：以中括號加索引標示，例如 `a[0]=1&a[1]=2`，解析後為 `{ a: ['1', '2'] }`，可保留順序。
  - comma 格式：以逗號分隔多個值，例如 `a=1,2`，解析後為 `{ a: ['1', '2'] }`。部分 API 或前端框架會採用。
- 若需自訂陣列格式，建議用 `qs` 或 `query-string`。

這些格式皆非 `URLSearchParams` 標準支援，需用 `qs`、`query-string` 等第三方套件處理。選擇哪種格式，需依後端或 API 規範決定。

### 3. 特殊編碼需求

- `URLSearchParams.toString()` 採 `application/x-www-form-urlencoded` 序列化（空白編成 `+` 而非 `%20`），編碼規則固定、無法自訂。
- 若需 RFC 3986 風格（空白為 `%20`）或自訂編碼行為，需自行處理或改用第三方套件。

---

## 推薦第三方套件

### qs

- [qs](https://github.com/ljharb/qs) 支援巢狀物件、陣列、自訂格式與進階選項。
- 適合複雜資料結構、API 參數序列化。

### query-string

- [query-string](https://github.com/sindresorhus/query-string) 語法簡潔，支援陣列與多種 `arrayFormat`（bracket / index / comma / separator）、格式自訂；**刻意不支援巢狀物件**（巢狀需自行 `JSON.stringify` 後放入），巢狀結構請改用 `qs`。
- 適合前端專案、簡單易用。

---

## 注意：`+` 與空白的編碼

查詢字串中 `+` 的語意取決於採用哪套規則：

- **`application/x-www-form-urlencoded`**（HTML 表單編碼，也是 WHATWG URL 標準的 urlencoded parser）：解析時把 `+` 還原為空白，序列化時把空白寫成 `+`、把字面 `+` 編成 `%2B`。
- **RFC 3986** 通用 URI 語法：`+` 只是普通合法字元，空白應編成 `%20`。

`URLSearchParams` 走的是前者，**解析時會自動把 `+` 轉成空白**——與 `qs`、`query-string` 行為一致，三者並無差異。這是標準行為（主流瀏覽器與 Node.js 皆然），並非舊系統或瀏覽器的偏差。

### 範例

```js
// 三者解析時都會把 + 解成空白
new URLSearchParams('a=1+2').get('a') // '1 2'
qs.parse('a=1+2') // { a: '1 2' }
queryString.parse('a=1+2') // { a: '1 2' }
```

### 真正的陷阱：保留字面的 `+`

問題不在「三者解析行為不同」，而在「想保留字面的 `+`」（例如傳遞含 `+` 的 base64 字串）時會被誤轉成空白。解法是組裝時用 `append()` / `set()`，它們會把 `+` 編成 `%2B`：

```js
const params = new URLSearchParams()
params.append('a', '1+2')
params.toString() // 'a=1%2B2'
params.get('a') // '1+2'
```

### 跨系統不一致的來源

不一致來自「序列化端與解析端採用不同標準」，而非 `URLSearchParams` 本身：

- 後端依 RFC 3986 把 `+` 當字面加號時，前端用 `URLSearchParams` 把空白序列化成的 `+` 會被後端解成字面 `+`。
- 前端改用 `encodeURIComponent`（空白編成 `%20`、`+` 編成 `%2B`）時，與預期 `+` 代表空白的後端對不上。

> **⚠️ 注意**
>
> 整合時務必在兩端統一約定 `+` 的處理方式，避免資料解析錯誤。

---

## 參考資料

- [MDN - URLSearchParams](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams)
- [qs 官方文件](https://github.com/ljharb/qs)
- [query-string 官方文件](https://github.com/sindresorhus/query-string)
