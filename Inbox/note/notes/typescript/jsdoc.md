---
title: JSDoc 型別註解
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/notes/typescript/jsdoc
tags:
  - javascript
  - typescript
---

# JSDoc 型別註解

JSDoc 可用於 JavaScript/TypeScript 進行型別註解，提升編輯器提示與型別安全。適用於不想寫 `.ts` 但仍需要型別檢查的 JS 專案，或在 `.ts` 中補充額外型別說明。

> Vue 專案的 JSDoc 用法請參閱 [Vue 的 JSDoc 型別註解](https://bugloop.com/notes/typescript/vue-jsdoc)。

## @type

為變數標註型別，支援原始型別、DOM 型別與泛型。

```js
/** @type {string} */
var s

/** @type {Window} */
var win

/** @type {PromiseLike<string>} */
var promisedString

/** @type {HTMLElement} */
var myElement = document.querySelector(selector)
```

### 型別轉換（Casts）

在任何括號運算式前加上 `@type` 標籤來進行型別轉換：

```js
var numberOrString = Math.random() < 0.5 ? 'hello' : 100
var typeAssertedNumber = /** @type {number} */ (numberOrString)
```

轉型為 const：

```js
let one = /** @type {const} */ (1)
```

## @param 與 @returns

為函式參數和回傳值加上型別說明。

```js
/**
 * 加總兩個數字
 * @param {number} a 第一個數字
 * @param {number} b 第二個數字
 * @returns {number} 相加結果
 */
function add(a, b) {
  return a + b
}
```

### 可選參數與預設值

```js
/**
 * @param {string} name
 * @param {number} [age] 可選參數
 * @param {string} [role='user'] 帶預設值的可選參數
 */
function createUser(name, age, role = 'user') {}
```

### 解構參數

```js
/**
 * @param {{ name: string, age: number }} options
 */
function greet({ name, age }) {
  console.log(`${name}, ${age}`)
}
```

## @typedef

定義可重複使用的物件型別。

```js
/**
 * @typedef {Object} User
 * @property {string} name 使用者名稱
 * @property {number} age 年齡
 * @property {string} [email] 可選屬性
 */

/** @type {User} */
const user = { name: 'Alice', age: 30 }
```

## @template

定義泛型參數，適用於通用函式。

```js
/**
 * 回傳陣列的第一個元素
 * @template T
 * @param {T[]} arr
 * @returns {T | undefined}
 */
function first(arr) {
  return arr[0]
}
```

## @callback

定義函式型別，適合描述 callback 簽名。

```js
/**
 * @callback Comparator
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */

/** @type {Comparator} */
const ascending = (a, b) => a - b
```

## @enum

定義列舉值。

```js
/** @enum {number} */
const Direction = {
  Up: 0,
  Down: 1,
  Left: 2,
  Right: 3,
}
```

## import 型別

在 JSDoc 中直接引入其他模組的型別，不需要實際 import。

```js
/** @type {import('./types').User} */
const user = getUser()

/** @param {import('express').Request} req */
function handler(req) {}
```

## 參考資料

- [TypeScript 官方 JSDoc 型別文件](https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html)
- [TypeScript without TypeScript — JSDoc superpowers](https://fettblog.eu/typescript-jsdoc-superpowers/)
- [Boost Your JavaScript with JSDoc Typing](https://dev.to/samuel-braun/boost-your-javascript-with-jsdoc-typing-3hb3)
