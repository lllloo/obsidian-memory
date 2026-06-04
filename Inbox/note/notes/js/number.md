---
title: 數字計算與格式化
created: 2026-06-03
updated: 2026-06-04
source: https://bugloop.com/notes/js/number
tags:
  - javascript
  - frontend
  - library
---

# 數字計算與格式化

JavaScript 的浮點數運算存在精度問題，本文介紹如何使用 `big.js` 進行精確的四則運算與四捨五入，以及常用的數字格式化方法。

## 浮點數精度問題

JavaScript 使用 IEEE 754 雙精度浮點數，直接運算可能產生誤差：

```js
0.1 + 0.2
// 0.30000000000000004

(1.005).toFixed(2)
// '1.00'（預期 '1.01'）
```

建議使用 [big.js](https://mikemcl.github.io/big.js/) 處理需要精確計算的場景，例如金額、數量等。

## 四則運算

使用 `big.js` 封裝後，加減乘除都能避免浮點數誤差。

使用前先安裝：

```sh
npm i big.js
```

> **⚠️ 關於 toNumber 的注意事項**
>
> `big.js` 的計算結果若最後轉回 JavaScript 的 `number`，仍會受到浮點數與安全整數範圍的限制（例如超過 $2^{53}-1$，或需要保留很多小數位）。
>
> 如果你希望「精度從頭到尾都不要回到浮點數」，可以改回傳字串，例如使用 `.toString()` 或 `.toFixed(dp)`；只有在確定結果落在安全範圍且允許以 `number` 表示時，才使用 `.toNumber()`。

```js
import Big from 'big.js'

const add = (a, b) => Big(a).plus(b).toNumber()
const sub = (a, b) => Big(a).minus(b).toNumber()
const mul = (a, b) => Big(a).times(b).toNumber()
const div = (a, b) => Big(a).div(b).toNumber()
```

```js
add(0.1, 0.2)  // 0.3
sub(1, 0.3)    // 0.7
mul(0.1, 0.2)  // 0.02
div(0.3, 0.1)  // 3
```

## 四捨五入

```js
// 需先引入 Big：import Big from 'big.js'
const round = (num, dp = 2) => {
  return Big(num).round(dp).toNumber()
}

round(1.005)     // 1.01
round(1.255, 1)  // 1.3
round(1.005, 0)  // 1
```

| 參數 | 說明 | 預設值 |
| --- | --- | --- |
| `num` | 要四捨五入的數字 | — |
| `dp` | 保留小數位數 | `2` |

> **💡 與原生 toFixed 的差異**
>
> 原生 `(1.005).toFixed(2)` 因浮點數精度問題會回傳 `'1.00'`，而 `round(1.005)` 使用 big.js 計算，能正確回傳 `1.01`。

> **ℹ️ 其他捨入模式**
>
> `big.js` 預設使用四捨五入（`ROUND_HALF_UP`，`Big.RM = 1`）。若有其他需求，可在使用前修改全域設定：
>
> | `Big.RM` | 模式 | 說明 |
> | --- | --- | --- |
> | `0` | `ROUND_DOWN` | 無條件捨去 |
> | `1` | `ROUND_HALF_UP` | 四捨五入（預設） |
> | `2` | `ROUND_HALF_EVEN` | 銀行家捨入（四捨六入五取偶） |
> | `3` | `ROUND_UP` | 無條件進位 |
>
> ```js
> Big.RM = 2 // 改為銀行家捨入
> ```

## 數字格式化

### 千分位逗號

使用 `Intl.NumberFormat` 將數字加上千分位逗號，常用於金額顯示。

以下範例使用 `en` locale，讓千分位分隔符固定為逗號（`,`）；若你希望依使用者語系顯示，可改用 `undefined` 或指定 `zh-TW`。

```js
const toThousands = (value) => {
  if (value === null || value === undefined) return ''
  if (typeof value === 'string' && value.trim() === '') return ''

  const n = Number(value)
  if (Number.isNaN(n)) return typeof value === 'string' ? value : '' // 無法轉換的字串（如 'abc'）原樣回傳，保留使用者輸入；非字串則回傳 ''
  if (!Number.isFinite(n)) return '' // Infinity / -Infinity 無法格式化，回傳 ''

  // 使用 'en' 固定千分位為逗號（,），避免不同語系出現不同分隔符號
  return new Intl.NumberFormat('en').format(n)
}

toThousands(1000000)   // '1,000,000'
toThousands(1234.56)   // '1,234.56'
toThousands('')        // ''
toThousands(null)      // ''
```

### 數字補零

使用 `String.padStart()` 將數字補足指定位數，常用於編號、日期格式化。

```js
const numberPad = (value, length, padString = '0') => {
  return String(value).padStart(length, padString)
}

numberPad(5, 2)      // '05'
numberPad(5, 3)      // '005'
numberPad(12, 4)     // '0012'
numberPad(5, 3, ' ') // '  5'
```

## 參考資料

- [big.js](https://mikemcl.github.io/big.js/) - 任意精度十進制算術庫
- [Intl.NumberFormat - MDN](https://developer.mozilla.org/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat) - 數字格式化國際化 API
- [String.prototype.padStart() - MDN](https://developer.mozilla.org/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/String/padStart)
