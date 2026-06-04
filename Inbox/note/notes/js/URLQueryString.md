---
title: URLSearchParams 為主的查詢字串處理
created: 2026-06-03
updated: 2026-06-04
tags:
  - javascript
  - frontend
---

# URLSearchParams 為主的查詢字串處理

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
- 若需處理巢狀結構，建議使用 `qs` 或 `query-string`。

### 2. 陣列格式自訂

- `URLSearchParams` 只支援重複 key，不支援 brackets、indices、comma 等格式。
  - brackets 格式：以中括號標示陣列元素，例如 `a[]=1&a[]=2`，解析後為 `{ a: ['1', '2'] }`。常見於 PHP、Ruby 等後端框架。
  - indices 格式：以中括號加索引標示，例如 `a[0]=1&a[1]=2`，解析後為 `{ a: ['1', '2'] }`，可保留順序。
  - comma 格式：以逗號分隔多個值，例如 `a=1,2`，解析後為 `{ a: ['1', '2'] }`。部分 API 或前端框架會採用。
- 若需自訂陣列格式，建議用 `qs` 或 `query-string`。

這些格式皆非 `URLSearchParams` 標準支援，需用 `qs`、`query-string` 等第三方套件處理。選擇哪種格式，需依後端或 API 規範決定。

### 3. 特殊編碼需求

- `URLSearchParams` 會自動進行 URI 編碼，無法自訂。
- 若需自訂編碼行為，可考慮第三方套件。

---

## 推薦第三方套件

### qs

- [qs](https://github.com/ljharb/qs) 支援巢狀物件、陣列、自訂格式與進階選項。
- 適合複雜資料結構、API 參數序列化。

### query-string

- [query-string](https://github.com/sindresorhus/query-string) 語法簡潔，支援巢狀物件、陣列、格式自訂。
- 適合前端專案、簡單易用。

---

## 注意：遇到 + 可能有的問題

在查詢字串中，`+` 依 RFC 3986 標準應視為字元加號（`+`），但部分舊系統或瀏覽器會將 `+` 解讀為空白（space）。這會導致以下問題：

- `URLSearchParams` 會將 `+` 當作字元加號，不會自動轉為空白。
- `qs` 與 `query-string` 會自動將 `+` 解析為空白（預設行為，模仿傳統表單編碼）。
- 若後端或第三方 API 將 `+` 當作空白，前端用 `URLSearchParams` 組裝的查詢字串可能出現資料不一致。

### 範例

```js
// 解析 a=1+2
new URLSearchParams('a=1+2').get('a') // '1+2'
qs.parse('a=1+2') // { a: '1 2' }
queryString.parse('a=1+2') // { a: '1 2' }
```

### 解法建議

- 若需與後端或第三方 API 相容，建議統一使用 `qs` 或 `query-string` 處理。
- 若必須用 `URLSearchParams`，遇到 `+` 需手動轉換：

  ```js
  const val = params.get('a').replace(/\+/g, ' ')
  ```

- 組裝查詢字串時，若要將空白轉為 `+`，可用 `encodeURIComponent(str).replace(/%20/g, '+')`。

> **⚠️ 注意**
>
> 跨系統整合時，請務必確認查詢字串的 `+` 處理方式，避免資料解析錯誤。

---

## 參考資料

- [MDN - URLSearchParams](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams)
- [qs 官方文件](https://github.com/ljharb/qs)
- [query-string 官方文件](https://github.com/sindresorhus/query-string)
