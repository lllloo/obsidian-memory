---
title: JavaScript 日期處理
created: 2026-06-03
updated: 2026-06-22
tags:
  - javascript
  - frontend
  - library
---

# JavaScript 日期處理

這份文件說明 JavaScript 原生 Date、Moment.js、Day.js 的常用日期操作方法，包含初始化、格式化、驗證等，適用於前端開發常見情境。

> **💡 資料儲存建議**
>
> 建議所有日期時間資料（無論是 API 傳輸、資料庫儲存、JSON 欄位等）都統一使用 `toISOString()` 格式（如：`2025-08-15T12:34:56.789Z`）。
>
> - 標準化：符合 ISO 8601 標準，易於跨系統交換。
> - 時區明確：預設為 UTC，避免本地時區混淆。
> - JSON 友好：Date 物件可以直接轉換為 JSON 字串會變成 ISO 格式。
>
> 範例：
>
> ```js
> const now = new Date()
> const isoString = now.toISOString() // "2025-08-15T12:34:56.789Z"
> ```

## 基本操作

### 設定日期

使用不同的日期處理庫建立特定日期時間的物件。

```js
const dateObj = new Date('2023/01/01 08:01:02')
const momentObj = moment('2023/01/01 08:01:02', 'YYYY-MM-DD HH:mm:ss')
const dayjsObj = dayjs('2023/01/01 08:01:02', 'YYYY-MM-DD HH:mm:ss')
```

> **ℹ️ Day.js 自訂格式需外掛**
>
> Day.js 以第二參數傳入自訂格式字串解析（`dayjs(str, format)`）需先載入 `customParseFormat` 外掛，否則格式參數會被忽略、退回原生解析：
>
> ```js
> import customParseFormat from 'dayjs/plugin/customParseFormat'
> dayjs.extend(customParseFormat)
> ```

### 取得年分

從日期物件中擷取年份資訊的方法：

```js
dateObj.getFullYear()
// 2023
momentObj.format('YYYY')
// '2023'
dayjsObj.format('YYYY')
// '2023'
```

### 取得月份

從日期物件中擷取月份資訊，注意原生 Date 與庫的差異：

```js
dateObj.getMonth()
// 0
// 回傳 0-11
momentObj.format('MM')
// '01'
dayjsObj.format('MM')
// '01'
```

> **⚠️ Date 物件提醒**
>
> 原生 Date 物件的月份是從 **0** 開始計算（0-11），而 Moment.js 與 Day.js 則回傳正常月份（01-12）。

### 取得日期

擷取月份中的日期（1-31）：

```js
dateObj.getDate()
// 1
momentObj.format('DD')
// '01'
dayjsObj.format('DD')
// '01'
```

### 取得星期幾

取得星期資訊，所有庫皆使用 0-6 表示（星期日為 0）：

```js
dateObj.getDay()
// 0
// 回傳 0-6，星期天是 0
momentObj.format('d')
// '0'
// 回傳 0-6，星期天是 0
dayjsObj.format('d')
// '0'
// 回傳 0-6，星期天是 0

// 轉換為中文星期
;['日', '一', '二', '三', '四', '五', '六'][dateObj.getDay()]
// '日'
```

Day.js：載入台灣中文語系，以 `dd` 取得星期的最短名稱（min name），如「日」「一」「二」

```js
import dayjs from 'dayjs';
import 'dayjs/locale/zh-tw'; // 載入台灣中文語系
dayjs.locale('zh-tw');       // 設定為台灣中文語系

const weekDayText = dayjs().format('dd')
// 取得當前星期的最短名稱（如「日」）
```

> **ℹ️ dd / ddd / dddd 的差異**
>
> Day.js（與 moment）的星期 token：`dd` 是最短名（min name，zh-tw 為「日」「一」）、`ddd` 才是一般所稱的縮寫（short name，如「週日」）、`dddd` 是完整名（「星期日」）。別把 `dd` 籠統稱作「縮寫」，以免與 `ddd` 混淆。

### 取得時

擷取時間的小時部分（24 小時制）：

```js
dateObj.getHours()
// 8
momentObj.format('HH')
// '08'
dayjsObj.format('HH')
// '08'
```

### 取得分

擷取時間的分鐘部分：

```js
dateObj.getMinutes()
// 1
momentObj.format('mm')
// '01'
dayjsObj.format('mm')
// '01'
```

### 取得秒

擷取時間的秒數部分：

```js
dateObj.getSeconds()
// 2
momentObj.format('ss')
// '02'
dayjsObj.format('ss')
// '02'
```

### 取得年月日

將日期格式化為常用的「年-月-日」格式：

```js
// 原生 Date 物件（注意需手動處理月份 +1）
;`${dateObj.getFullYear()}-${dateObj.getMonth() + 1}-${dateObj.getDate()}`
// '2023-1-1'

// Moment.js
momentObj.format('YYYY-MM-DD')
// '2023-01-01'

// Day.js
dayjsObj.format('YYYY-MM-DD')
// '2023-01-01'
```

> **ℹ️ 格式化比較**
>
> 使用 Moment.js 或 Day.js 可以更方便地獲得標準格式的日期字串，不必手動處理月份的 +1 問題，且自動補零保持格式一致性。

### 年月取得天數

獲取指定年月共有多少天（處理月底日期時非常有用）：

```js
// 原生 Date 物件
new Date(year, month, 0).getDate()
// 31

// Moment.js
moment(`${year}/${month}`).daysInMonth()
// '31'

// Day.js
dayjs(`${year}/${month}`).daysInMonth()
// 31
```

### moment/dayjs 轉 Date Object

將 Moment 或 Day.js 物件轉換為原生 JavaScript Date 物件：

```js
moment().toDate()
dayjs().toDate()
```

## 複雜操作範例

### 檢查昨天的日期是否在給定日期之前

用於驗證日期順序或檢查時間流程的有效性：

```js
// 使用 moment
// 檢查昨天是否在指定日期之前
moment().subtract(1, 'day').isBefore(moment(date), 'day')
// 回傳 true 表示「昨天」早於「指定日期」

// 使用 dayjs
// 兩種等效寫法
dayjs().subtract(1, 'day').isBefore(dayjs(date), 'day')
dayjs().add(-1, 'day').isBefore(dayjs(date), 'day')
```

### 檢查當前時間是否晚於特定時間點

以下程式碼檢查當前時間是否晚於早上 9 點，如為 **true** 表示已過早上 9 點，為 **false** 表示尚未到 9 點。常用於排程或時間控制邏輯。

```js
// 使用 moment
import moment from 'moment'
// 檢查現在時間是否晚於上午 9 點
moment().isAfter(moment('09:00', 'HH:mm'), 'minute')

// 使用 dayjs
import dayjs from 'dayjs'
import customParseFormat from 'dayjs/plugin/customParseFormat'
dayjs.extend(customParseFormat)
// 檢查現在時間是否晚於上午 9 點
dayjs().isAfter(dayjs('09:00', 'HH:mm'), 'minute')
```

> **ℹ️ 外掛使用說明**
>
> Day.js 需要先載入 `customParseFormat` 外掛才能使用自訂格式解析時間。

### 日期轉 ISO 字串

將日期轉換為符合 ISO 8601 標準的字串格式，常用於 API 通訊或資料存儲。

```js
const dateObj = new Date('2023/01/01 08:01:02')
dateObj.toISOString()
// '2023-01-01T00:01:02.000Z'

// 使用 moment
momentObj.toISOString()
// '2023-01-01T00:01:02.000Z'

// 使用 dayjs
dayjs('2023/01/01 08:01:02').toISOString()
// '2023-01-01T00:01:02.000Z'
```

> ISO 8601 是國際標準的日期時間表示法，格式為 `YYYY-MM-DDTHH:mm:ss.sssZ`，其中 Z 表示 UTC 時區。

### 日期有效性驗證

檢查日期字串是否為有效的日期格式，用於表單驗證或資料處理前的檢查。

```js
// 使用 moment（moment 有 overflow 檢查，預設即可擋無效日期）
moment('2023-02-30').isValid() // false (2月沒有30日)
moment('2023-01-15').isValid() // true

// 使用 dayjs：核心預設為「非嚴格」，會把溢位日期滾到合法日，不擋無效日期
dayjs('2023-02-30').isValid() // true（溢位被接受，解析成 3 月初）
dayjs('2023-01-15').isValid() // true

// 要讓 dayjs 嚴格檢查無效日期，需載入 customParseFormat 外掛並用嚴格模式（第三參數 true）
import customParseFormat from 'dayjs/plugin/customParseFormat'
dayjs.extend(customParseFormat)
dayjs('2023-02-30', 'YYYY-MM-DD', true).isValid() // false
```

> **⚠️ 注意**
>
> 原生 Date 與 Day.js 核心（非嚴格模式）對無效日期都很寬鬆，會把溢位日期滾到下一個合法日。moment 預設即偵測 overflow 回傳 false；Day.js 則需搭配 `customParseFormat` 外掛的嚴格模式才能擋。

### 獲取當月第一天和最後一天

取得當月第一天和最後一天的日期，常用於報表生成、月曆視圖或日期範圍選擇。

```js
// 使用 moment
moment().startOf('month').format('YYYY-MM-DD') // 當月第一天
moment().endOf('month').format('YYYY-MM-DD') // 當月最後一天

// 使用 dayjs
dayjs().startOf('month').format('YYYY-MM-DD') // 當月第一天
dayjs().endOf('month').format('YYYY-MM-DD') // 當月最後一天
```

> **💡 應用場景**
>
> 這個功能在開發月報表、財務統計或行事曆應用時特別有用。

## 參考資料

- [Date - JavaScript | MDN](https://developer.mozilla.org/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Date) - JavaScript 原生 Date 物件官方文件
- [Moment.js](https://momentjs.com/) - 功能豐富的日期處理庫，不過現在推薦使用 Day.js
- [Day.js](https://day.js.org/) - 輕量級日期處理庫，API 與 Moment.js 相容，體積更小
