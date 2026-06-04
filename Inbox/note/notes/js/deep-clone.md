---
title: 深拷貝（Deep clone）快速參考
created: 2026-06-03
updated: 2026-06-04
tags:
  - javascript
  - frontend
---

# 深拷貝（Deep clone）快速參考

將一個物件或陣列完整複製（含巢狀結構），以免修改原始資料。

## 推薦做法

- 優先：`structuredClone(value)`（現代瀏覽器與支援的 Node.js）。
- fallback：若只含 JSON 資料可用 `JSON.parse(JSON.stringify(obj))`。
- 需處理各種型別與 edge case 時，使用成熟函式庫（例如 `_.cloneDeep`）。

```js
// 簡短範例（瀏覽器 / Node.js 支援）
const src = { n: 1, d: new Date(), m: new Map([[1, 'a']]) }
const copy = structuredClone(src)
```

## 注意事項與支援（簡要）

- `structuredClone` 支援多數內建型別並能處理循環參考，但不會複製函式或閉包。遇到無法序列化的 host objects 可能會拋錯，實務上請在不確定時使用 try/catch 做容錯處理。
- JSON 方法（`JSON.parse(JSON.stringify(...))`）只適用於 JSON 資料，會丟失 Date、RegExp、Map/Set、undefined、Symbol、函式等，且無法處理循環參考。
- `_.cloneDeep` 功能最全面，但需額外依賴並會增加封包大小。
- 支援情況：`structuredClone` 已在現代桌面與行動瀏覽器支援；Node.js 17+ 也包含原生支援。

## 參考

- MDN: <https://developer.mozilla.org/en-US/docs/Web/API/structuredClone>
